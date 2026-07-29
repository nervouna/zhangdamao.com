#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

fail() {
  printf 'readiness check failed: %s\n' "$1" >&2
  exit 1
}

require_literal() {
  local path="$1"
  local literal="$2"
  grep -Fq "$literal" "$path" || fail "$path is missing: $literal"
}

[[ "$(<.python-version)" == "3.11.15" ]] || fail '.python-version must pin 3.11.15'

git check-ignore -q scripts/build-pages.sh && fail 'scripts/build-pages.sh must be trackable'
git check-ignore -q scripts/check-publishing-readiness.sh && fail 'readiness check must be trackable'

bash -n scripts/build-pages.sh
require_literal scripts/build-pages.sh 'BLOGWRITER_PAGES_BUILD_V1'
require_literal scripts/build-pages.sh 'readonly expected_uv_version="0.11.2"'
require_literal scripts/build-pages.sh '"uv==$expected_uv_version"'
require_literal scripts/build-pages.sh 'uv sync --locked'
require_literal scripts/build-pages.sh '.venv/bin/pelican'

require_literal pyproject.toml 'package = false'

require_literal publishconf.py "DRAFT_SAVE_AS = ''"
require_literal publishconf.py "DRAFT_LANG_SAVE_AS = ''"
require_literal publishconf.py "DRAFT_PAGE_SAVE_AS = ''"
require_literal publishconf.py "DRAFT_PAGE_LANG_SAVE_AS = ''"
require_literal publishconf.py 'WITH_FUTURE_DATES = False'
require_literal publishconf.py "run_path(Path(__file__).with_name('pelicanconf.py'))"
require_literal tests/fixtures/future-post.md 'Date: 2099-01-01 00:00:00'
require_literal tests/fixtures/future-post.md 'Status: published'

require_literal pelicanconf.py "'extra/_redirects': {'path': '_redirects'}"
[[ "$(grep -c '^STATIC_PATHS = ' pelicanconf.py)" -eq 1 ]] || fail 'pelicanconf.py must define STATIC_PATHS exactly once'

require_literal content/pages/404.md 'Status: hidden'
require_literal content/pages/404.md 'Save_as: 404.html'
require_literal content/pages/404.md 'Template: 404'
require_literal themes/ignore-the-blueprint/templates/404.html '<meta name="robots" content="noindex,follow" />'
require_literal content/pages/pages-readiness-redirect.md 'Status: hidden'
require_literal content/pages/pages-readiness-redirect.md 'Url: __blogwriter-pages-readiness__/'
require_literal content/pages/pages-readiness-redirect.md 'Save_as: __blogwriter-pages-readiness__/index.html'
require_literal content/extra/_redirects '/__blogwriter-pages-readiness__/ /about-me/ 301'

jq -e '
  .schemaVersion == 1 and
  .remoteName == "origin" and
  .productionBranch == "main" and
  .githubOwner == "nervouna" and
  .githubRepository == "zhangdamao.com" and
  .pagesProjectName == "zhangdamao-com" and
  .checkAppSlug == "cloudflare-workers-and-pages" and
  .checkName == "Cloudflare Pages" and
  .productionOrigin == "https://zhangdamao.com" and
  .buildScript == "scripts/build-pages.sh" and
  .buildMarker == "BLOGWRITER_PAGES_BUILD_V1" and
  .selectedBuildImage == "v2" and
  .pythonVersion == "3.11.15" and
  .uvVersion == "0.11.2" and
  .automaticDependencyInstall == false and
  .publishSettings == "publishconf.py" and
  .outputDirectory == "output" and
  .redirectsSource == "content/extra/_redirects"
' .blogwriter/publish.json >/dev/null || fail 'publish contract does not match the frozen Gate 1 proposal'

printf 'Publishing readiness static checks passed.\n'
