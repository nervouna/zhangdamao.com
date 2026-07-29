#!/usr/bin/env bash

set -euo pipefail

readonly expected_python_version="3.11.15"
readonly expected_uv_version="0.11.2"
readonly python_bin="python3"

printf 'BLOGWRITER_PAGES_BUILD_V1\n'

actual_python_version="$($python_bin -c 'import platform; print(platform.python_version())')"
if [[ "$actual_python_version" != "$expected_python_version" ]]; then
  printf 'Expected Python %s, got %s.\n' "$expected_python_version" "$actual_python_version" >&2
  exit 1
fi

$python_bin -m pip install \
  --disable-pip-version-check \
  --no-cache-dir \
  "uv==$expected_uv_version"

actual_uv_version="$($python_bin -m uv --version | awk '{print $2}')"
if [[ "$actual_uv_version" != "$expected_uv_version" ]]; then
  printf 'Expected uv %s, got %s.\n' "$expected_uv_version" "$actual_uv_version" >&2
  exit 1
fi

$python_bin -m uv sync --locked

test -x .venv/bin/pelican
.venv/bin/pelican --version
.venv/bin/pelican content -s publishconf.py -o output
