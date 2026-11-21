# Ignore the Blueprint

Personal website of GUAN Xiaoyu (a.k.a. ZHANG Damao).

This site is:

* Built with [Pelican][0]
* Managed with [mise][1] and [uv][2]
* Deployed on [CloudFlare][3]

The content is 100% hand written.

## Setup

Set up the local environment with `mise` and `uv`:

```bash
mise install
mise current
uv sync --locked
```

The repo pins Python in `mise.toml` and dependencies in `pyproject.toml` + `uv.lock`.

## Common Commands

Build the site:

```bash
make html
```

Cloudflare Pages uses the tracked production entry point:

```bash
bash scripts/build-pages.sh
```

The Pages dashboard must select Python 3.11.15, set
`SKIP_DEPENDENCY_INSTALL=1`, and use `output` as the build output directory.
The script pins uv, performs a locked sync, and builds with `publishconf.py`.

Serve the site locally with auto reload:

```bash
make devserver PORT=8000
```

* License: [WTFPL][4]

[0]: https://getpelican.com/
[1]: https://mise.jdx.dev/
[2]: https://docs.astral.sh/uv/
[3]: https://pages.cloudflare.com/
[4]: https://github.com/nervouna/zhangdamao.com/blob/main/LICENSE.txt
