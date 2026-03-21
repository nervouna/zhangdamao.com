from __future__ import annotations

from argparse import ArgumentParser, Namespace
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
import re
import sys
from git import Repo

import pelicanconf


PROJECT_ROOT = Path(__file__).resolve().parent
PROMPT_PATH = PROJECT_ROOT / 'prompt.txt'
POST_DIR = PROJECT_ROOT / pelicanconf.PATH / pelicanconf.ARTICLE_PATHS[0]
DEFAULT_MODEL = 'qwen3.5:0.8b'
DEFAULT_TIMEOUT = 120.0
REQUIRED_HEADERS = {'Title', 'Category', 'Tags', 'Summary', 'Date', 'Slug'}
HEADER_PATTERN = re.compile(r'^(?P<key>[A-Za-z][A-Za-z ]*):\s*(?P<value>.+)$')


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description='Generate Pelican headers for posts with Ollama.',
    )
    parser.add_argument(
        'paths',
        nargs='*',
        help='Markdown files to process. Defaults to untracked posts when omitted.',
    )
    parser.add_argument(
        '--model',
        default=DEFAULT_MODEL,
        help=f'Ollama model to use. Defaults to {DEFAULT_MODEL}.',
    )
    parser.add_argument(
        '--timeout',
        type=float,
        default=DEFAULT_TIMEOUT,
        help=(
            'Request timeout in seconds. Use 0 to wait indefinitely. '
            f'Defaults to {DEFAULT_TIMEOUT:g}.'
        ),
    )
    think_group = parser.add_mutually_exclusive_group()
    think_group.add_argument(
        '--think',
        action='store_true',
        dest='think',
        help='Enable thinking output for supported Ollama models.',
    )
    think_group.add_argument(
        '--no-think',
        action='store_false',
        dest='think',
        help='Disable thinking output for supported Ollama models.',
    )
    parser.set_defaults(think=False)
    return parser.parse_args()


def get_repo() -> Repo:
    return Repo(PROJECT_ROOT)


def get_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding='utf-8')


def resolve_candidate_paths(raw_paths: Sequence[str]) -> list[Path]:
    if raw_paths:
        return [Path(path).expanduser().resolve() for path in raw_paths]

    repo = get_repo()
    return [PROJECT_ROOT / Path(path) for path in repo.untracked_files]


def is_markdown_file(file_path: Path) -> bool:
    return file_path.suffix.lower() == '.md'


def is_post_file(file_path: Path) -> bool:
    return file_path.is_relative_to(POST_DIR)


def validate_post_path(file_path: Path) -> tuple[bool, str | None]:
    if not file_path.exists():
        return False, f'Skipping {file_path}: file does not exist.'
    if not file_path.is_file():
        return False, f'Skipping {file_path}: not a file.'
    if not is_markdown_file(file_path):
        return False, f'Skipping {file_path}: not a markdown file.'
    if not is_post_file(file_path):
        return False, f'Skipping {file_path}: not inside {POST_DIR}.'
    return True, None


def collect_posts(raw_paths: Sequence[str]) -> tuple[list[Path], list[str]]:
    valid_posts: list[Path] = []
    messages: list[str] = []
    seen: set[Path] = set()

    for file_path in resolve_candidate_paths(raw_paths):
        normalized_path = file_path.resolve()
        is_valid, message = validate_post_path(normalized_path)
        if not is_valid:
            if message:
                messages.append(message)
            continue
        if normalized_path in seen:
            continue
        seen.add(normalized_path)
        valid_posts.append(normalized_path)

    return valid_posts, messages


def get_post_content(file_path: Path) -> str:
    return file_path.read_text(encoding='utf-8')


def assemble_prompt(content: str) -> str:
    return get_prompt_template().format(content=content)


def get_ollama_completion(prompt: str, model: str, think: bool, timeout: float) -> str:
    try:
        import httpx
        import ollama
    except ImportError as exc:
        raise RuntimeError(
            'The ollama package is not available in the current Python environment.',
        ) from exc

    client_timeout = None if timeout <= 0 else timeout
    client = ollama.Client(timeout=client_timeout)

    try:
        response = client.generate(model=model, prompt=prompt, think=think)
    except httpx.TimeoutException as exc:
        timeout_text = 'the configured timeout' if timeout <= 0 else f'{timeout:g}s'
        raise RuntimeError(
            'Ollama did not respond within '
            f'{timeout_text}. If the model looks stuck, try `killall ollama` and rerun, '
            'or pass --timeout 0 to wait indefinitely.'
        ) from exc

    if isinstance(response, Mapping):
        return str(response['response']).strip()
    return response.response.strip()


def generate_slug_header(file_path: Path) -> str:
    return f'Slug: {file_path.stem}'


def generate_date_header() -> str:
    return datetime.now().strftime('Date: %Y-%m-%d %H:%M:%S')


def generate_headers(file_path: Path, model: str, think: bool, timeout: float) -> str:
    content = get_post_content(file_path)
    prompt = assemble_prompt(content)
    completion = get_ollama_completion(prompt, model=model, think=think, timeout=timeout)
    return f'{completion}\n{generate_date_header()}\n{generate_slug_header(file_path)}'


def parse_leading_headers(content: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    lines = content.lstrip('\ufeff').splitlines()
    saw_header = False

    for line in lines:
        if not line.strip():
            if saw_header:
                break
            continue

        match = HEADER_PATTERN.match(line)
        if not match:
            break

        saw_header = True
        headers[match.group('key')] = match.group('value')

    return headers


def has_existing_headers(file_path: Path) -> bool:
    headers = parse_leading_headers(get_post_content(file_path))
    return REQUIRED_HEADERS.issubset(headers)


def write_headers(file_path: Path, headers: str) -> None:
    content = get_post_content(file_path).lstrip('\ufeff')
    file_path.write_text(f'{headers}\n\n{content}', encoding='utf-8')


def format_runtime_options(model: str, think: bool, timeout: float) -> str:
    timeout_text = 'infinite' if timeout <= 0 else f'{timeout:g}s'
    return f'model={model}, think={think}, timeout={timeout_text}'


def process_post(file_path: Path, model: str, think: bool, timeout: float) -> str:
    if has_existing_headers(file_path):
        return f'↷ Skipped {file_path}: headers already exist.'

    write_headers(
        file_path,
        generate_headers(file_path, model=model, think=think, timeout=timeout),
    )
    return f'✓ Updated {file_path}'


def main() -> int:
    args = parse_args()
    posts, messages = collect_posts(args.paths)

    for message in messages:
        print(message)

    if not posts:
        print('No eligible posts found.')
        return 0

    has_failures = False
    for post in posts:
        try:
            print(
                process_post(
                    post,
                    model=args.model,
                    think=args.think,
                    timeout=args.timeout,
                )
            )
        except Exception as exc:  # pragma: no cover
            has_failures = True
            print(
                f'Unexpected error for {post} '
                f'({format_runtime_options(args.model, args.think, args.timeout)}): {exc}',
                file=sys.stderr,
            )

    return 1 if has_failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
