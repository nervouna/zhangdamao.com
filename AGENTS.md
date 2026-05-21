# Repository Guidelines

## Project Structure & Module Organization

This is a Pelican-powered personal static site.

- `content/posts/`: blog posts in Markdown. Each post should include Pelican metadata such as `Title`, `Date`, `Slug`, `Category`, `Tags`, and `Summary`.
- `content/pages/`: standalone pages such as `about.md`.
- `content/images/` and `content/extra/`: static assets. Favicons and touch icons are mapped through `pelicanconf.py`.
- `themes/ignore-the-blueprint/`: active custom theme, including Jinja templates and CSS.
- `themes/pelican-alchemy/`: vendored/reference theme. Do not modify unless intentionally updating that theme.
- `output/`: generated site output. Treat as build artifact.
- Root scripts such as `create_post.py` and `generate_post_header.py` support local content workflows.

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
uv run python generate_post_header.py --help
```

Use `make publish` only when `publishconf.py` exists and is intentionally configured.

## Coding Style & Naming Conventions

Use concise, readable Python and explicit error handling for tooling scripts. Prefer `uv run` for Python entry points. Keep Markdown metadata consistent with existing posts. Use lowercase, hyphenated slugs and filenames, for example `content/posts/optimizing-zsh-config-on-mac.md`.

Theme edits should follow the existing warm editorial style in `themes/ignore-the-blueprint/static/css/style.css`. Keep templates simple and avoid unrelated formatting churn.

## Testing Guidelines

There is no dedicated test suite in this repository. For all content, template, or config changes, run:

```bash
make html
```

For visual or layout changes, also run a local server and inspect the affected pages:

```bash
make devserver PORT=8000
```

If changing metadata-generation scripts, test the relevant command with `uv run python ...` on a specific file before broad scans.

## Commit & Pull Request Guidelines

Use concise imperative commit messages with a type prefix, matching recent history:

```text
doc: update about projects
fix: unescape HTML entities in mail post code blocks
chore: switch to custom theme and fix Makefile pelican path
```

Allowed types include `feat`, `fix`, `doc`, `chore`, `refactor`, `test`, and `style`.

Pull requests should include a short summary, verification steps such as `make html`, and screenshots for visual theme changes.

## Security & Configuration Tips

Do not commit secrets, API keys, or local `.env` files. Ollama-backed metadata generation is local; make sure the required model is installed before running header-generation workflows.
