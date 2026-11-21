# Repository Guidelines

## Project Structure & Module Organization

This is a Pelican-powered personal static site.

- `content/posts/`: blog posts in Markdown. Each post should include Pelican metadata such as `Title`, `Date`, `Slug`, `Category`, `Tags`, and `Summary`.
- `content/pages/`: standalone pages such as `about.md`.
- `content/images/` and `content/extra/`: static assets. Favicons and touch icons are mapped through `pelicanconf.py`.
- `themes/ignore-the-blueprint/`: active custom theme, including Jinja templates and CSS.
- `plugins/og_cards/`: Pelican plugin that renders a social preview card for every article into `output/og/<slug>.png` at build time, using the fonts bundled in `plugins/og_cards/fonts/`. Add an `Image:` metadata field (a site-relative path or a full URL) to a post to use its own picture instead. Pages and index pages share `og/default.png`.
- `output/`: generated site output. Treat as build artifact.
- `scripts/build-pages.sh`: Cloudflare Pages production build entry point.

## Build, Test, and Development Commands

Set up dependencies with:

```bash
mise install
uv sync --locked
```

Common commands:

```bash
make html                 # Build the static site into output/
make devserver PORT=8000  # Rebuild and serve locally with live reload
make serve PORT=8000      # Serve without regeneration
make clean                # Remove output/
```

Use `make publish` only when `publishconf.py` exists and is intentionally configured.

## Coding Style & Naming Conventions

Keep Markdown metadata consistent with existing posts. Use lowercase, hyphenated slugs and filenames, for example `content/posts/optimizing-zsh-config-on-mac.md`.

Bilingual posts are two files with the same `Date`: `<slug>.md` (English) and `<slug>-cn.md` (Chinese, slug also ends in `-cn`). Each opens with a link to the other, written as `[中文版]({filename}<slug>-cn.md)` and `[English version]({filename}<slug>.md)`.

Theme edits should follow the existing warm editorial style in `themes/ignore-the-blueprint/static/css/style.css`. Keep templates simple and avoid unrelated formatting churn.

## Writing Style

- Chinese text uses 「」 for quotes, with a space between Chinese and Latin words or numbers.
- State the post's own argument in the opening paragraph; keep background and summaries of other people's writing short and later.
- No parallelism or antithesis built for effect, and no filler transitions. Sharp is fine, ornamental is not.
- Read any cited article in full before paraphrasing it, and check its title, author and date against the source.
- The author edits drafts directly on the PR branch. Fetch and fast-forward before every edit, and keep their wording.
- To turn a voice memo into a post, use the `draft-post-from-recording` skill in `.claude/skills/`.

## Testing Guidelines

There is no dedicated test suite in this repository. For all content, template, or config changes, run:

```bash
make html
```

For visual or layout changes, also run a local server and inspect the affected pages:

```bash
make devserver PORT=8000
```

CI runs a stricter build; run it before pushing:

```bash
uv run pelican content -s publishconf.py -o output --fatal warnings
```

`publishconf.py` disables draft output, so a post with `Status: draft` is not rendered on Cloudflare previews or in production. To preview a post on a PR, leave the draft status off; nothing is published until the PR merges.

## Commit & Pull Request Guidelines

Use concise imperative commit messages with a type prefix, matching recent history:

```text
doc: update about projects
fix: unescape HTML entities in mail post code blocks
chore: switch to custom theme and fix Makefile pelican path
```

Allowed types include `feat`, `fix`, `doc`, `chore`, `refactor`, `test`, and `style`.

Pull requests should include a short summary, verification steps such as `make html`, and screenshots for visual theme changes.

Merging to `main` deploys to production through Cloudflare Pages within a few minutes. Every PR branch gets a preview at `https://<branch-with-slashes-as-dashes>.zhangdamao-com.pages.dev`. Articles live at `/blog/YYYY/MM/DD/<slug>`.

Squash-merge PRs with the title `<type>: <summary> (#N)`. Merge only when the author asks.

## Security & Configuration Tips

Do not commit secrets, API keys, or local `.env` files.
