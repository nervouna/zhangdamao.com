# /// script
# requires-python = ">=3.10"
# dependencies = ["sherpa-onnx", "soundfile", "numpy"]
# ///
"""Transcribe a voice memo into timestamped lines.

Usage:
    uv run transcribe.py RECORDING [--model sensevoice|whisper] [--language zh]

Needs ffmpeg on PATH. Models are downloaded once from the sherpa-onnx
GitHub releases into ~/.cache/blog-transcribe (override with --cache).

sensevoice is fast and accurate for Chinese speech. whisper (large-v3
turbo) is slower but spells English names and titles better, so run both
when the recording mixes the two languages and compare the proper nouns.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import sherpa_onnx
import soundfile as sf

RELEASES = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models"
SENSEVOICE = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17"
WHISPER = "sherpa-onnx-whisper-turbo"
VAD = "silero_vad.onnx"


def fetch(cache, name, archive):
    """Return the cached model, downloading it first if it is missing.

    Work happens in a temporary directory inside the cache and is moved
    into place only after it succeeds, so an interrupted download never
    leaves a partial model behind.
    """
    target = cache / name
    if target.exists():
        return target
    cache.mkdir(parents=True, exist_ok=True)
    url = f"{RELEASES}/{name}{'.tar.bz2' if archive else ''}"
    print(f"Downloading {url}", file=sys.stderr)
    with tempfile.TemporaryDirectory(dir=cache) as tmp:
        download = Path(tmp) / "download"
        subprocess.run(["curl", "-fL", "--retry", "3", "-o", download, url], check=True)
        if archive:
            subprocess.run(["tar", "xjf", download, "-C", tmp], check=True)
            (Path(tmp) / name).rename(target)
        else:
            download.rename(target)
    return target


def recognizer(cache, model, language):
    if model == "sensevoice":
        folder = fetch(cache, SENSEVOICE, archive=True)
        return sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=str(folder / "model.onnx"),
            tokens=str(folder / "tokens.txt"),
            num_threads=4,
            use_itn=True,
            language=language,
        )
    folder = fetch(cache, WHISPER, archive=True)
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(folder / "turbo-encoder.int8.onnx"),
        decoder=str(folder / "turbo-decoder.int8.onnx"),
        tokens=str(folder / "turbo-tokens.txt"),
        language=language,
        task="transcribe",
        num_threads=4,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("recording", type=Path)
    parser.add_argument("--model", choices=["sensevoice", "whisper"], default="sensevoice")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--cache", type=Path, default=Path.home() / ".cache/blog-transcribe")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(args.recording),
             "-ar", "16000", "-ac", "1", str(wav)],
            check=True,
        )
        samples, rate = sf.read(wav, dtype="float32")

    rec = recognizer(args.cache, args.model, args.language)

    # Split on pauses so each segment is short enough for the recognizer.
    config = sherpa_onnx.VadModelConfig()
    config.silero_vad.model = str(fetch(args.cache, VAD, archive=False))
    config.silero_vad.min_silence_duration = 0.5
    config.silero_vad.max_speech_duration = 25
    config.sample_rate = rate
    vad = sherpa_onnx.VoiceActivityDetector(config, buffer_size_in_seconds=120)
    window = config.silero_vad.window_size

    def drain():
        while not vad.empty():
            segment = vad.front
            stream = rec.create_stream()
            stream.accept_waveform(rate, segment.samples)
            rec.decode_stream(stream)
            start = segment.start / rate
            print(f"[{int(start // 60):02d}:{start % 60:04.1f}] {stream.result.text}", flush=True)
            vad.pop()

    for i in range(0, len(samples) - window + 1, window):
        vad.accept_waveform(samples[i:i + window])
        drain()
    vad.flush()
    drain()


if __name__ == "__main__":
    main()
