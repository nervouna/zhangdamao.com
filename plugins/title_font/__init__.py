"""Ship the heading typeface as a small web font.

Glow Sans SC is about 9 MB per weight, far too large to serve. Headings only
use a few hundred distinct Chinese characters across the whole site, so this
plugin collects those characters at build time and writes a subset of the
font as WOFF2 (tens of kilobytes). Body text keeps using system fonts.

Sets ``TITLE_FONT`` in the template context to the site-relative path of the
subset, or to ``''`` when no heading contains a CJK character. The file name
carries a hash of its character set, so it can be cached forever.
"""

import hashlib
import re
from html import unescape
from io import BytesIO
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from pelican import signals

SOURCE_FONT = Path(__file__).parent.parent / "fonts" / "GlowSansSC-Normal-Heavy.otf"
CACHE_DIR = Path(".cache") / "title_font"
OUTPUT_DIR = "theme/fonts"

HEADING = re.compile(r"<h[1-4][^>]*>(.*?)</h[1-4]>", re.S)
TAG = re.compile(r"<[^>]+>")
# Latin text in headings is set in Archivo, so only CJK needs to be in the subset.
FIRST_CJK = 0x2E80


def _heading_text(item):
    text = [item.title]
    for match in HEADING.finditer(item.content or ""):
        text.append(unescape(TAG.sub("", match.group(1))))
    return "".join(text)


def _collect(generators, settings):
    text = [settings.get("SITENAME", ""), settings.get("SITESUBTITLE", "")]
    for generator in generators:
        for name in (
            "articles",
            "translations",
            "drafts",
            "drafts_translations",
            "pages",
            "hidden_pages",
            "draft_pages",
        ):
            for item in getattr(generator, name, []):
                text.append(_heading_text(item))
    return sorted({char for char in "".join(text) if ord(char) >= FIRST_CJK})


# Keys a CID-keyed font's per-range dictionaries may carry but cannot be saved
# with. fontTools drops them with a warning, and CI treats warnings as fatal.
UNSAVED_CFF_KEYS = (
    "FontBBox",
    "ItalicAngle",
    "StrokeWidth",
    "UnderlinePosition",
    "UnderlineThickness",
    "isFixedPitch",
)


def _slim_cff(font):
    """Remove what the subsetter leaves behind in the outline table.

    This font carries a font-wide private dictionary holding about seven
    thousand subroutines. In a CID-keyed font the glyphs use the dictionaries
    in the FDArray instead, so nothing reads it, but fontTools copies it into
    the subset, where it outweighs the glyphs several times over.
    """
    top = font["CFF "].cff.topDictIndex[0]
    if hasattr(top, "FDArray"):
        top.rawDict.pop("Private", None)
        top.__dict__.pop("Private", None)
    for font_dict in getattr(top, "FDArray", []):
        for key in UNSAVED_CFF_KEYS:
            font_dict.rawDict.pop(key, None)
            font_dict.__dict__.pop(key, None)


def _subset(chars):
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "locl", "ccmp"]
    options.name_IDs = [1, 2]
    options.notdef_outline = True
    options.hinting = False
    font = TTFont(SOURCE_FONT)
    subsetter = subset.Subsetter(options)
    subsetter.populate(text="".join(chars))
    subsetter.subset(font)
    _slim_cff(font)
    font.flavor = "woff2"
    buffer = BytesIO()
    font.save(buffer)
    return buffer.getvalue()


def build_title_font(generators):
    settings = generators[0].settings
    chars = _collect(generators, settings)

    relative = ""
    if chars:
        key = "".join(chars) + str(SOURCE_FONT.stat().st_size)
        digest = hashlib.sha1(key.encode()).hexdigest()[:10]
        cached = CACHE_DIR / f"{digest}.woff2"
        if not cached.exists():
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(_subset(chars))
        relative = f"{OUTPUT_DIR}/glow-sans-sc-titles.{digest}.woff2"
        target = Path(generators[0].output_path) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(cached.read_bytes())

    for generator in generators:
        generator.context["TITLE_FONT"] = relative


def register():
    signals.all_generators_finalized.connect(build_title_font)
