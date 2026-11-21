"""Generate a social preview card (Open Graph image) for every article.

Each article gets ``og/<slug>.png`` (1200x630) showing its title in the
theme's display fonts. Articles can opt out with an ``Image:`` metadata
field pointing at their own picture. Pages and index pages use
``og/default.png``, which shows the site name and subtitle.
"""

from pathlib import Path

from pelican import signals
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = Path(__file__).parent / "fonts"
LATIN_FONT = FONT_DIR / "Spectral-Medium.ttf"
CJK_FONT = FONT_DIR / "NotoSerifSC-Medium.otf"

WIDTH, HEIGHT = 1200, 630
MARGIN = 88
DEFAULT_CARD = "og/default.png"

# sRGB equivalents of the design tokens in the theme's style.css.
PAGE = "#f9f6f3"
INK = "#15110c"
MUTED = "#615d58"
RULE = "#d3d0cd"
ACCENT = "#9e4421"

TITLE_SIZES = (84, 72, 62, 54, 46)
MAX_TITLE_LINES = 3
LINE_SPACING = 1.32
HEADER_BOTTOM = 148
FOOTER_TOP = HEIGHT - 110
# Room the title block may use, leaving space for the accent bar above it.
TITLE_AREA = FOOTER_TOP - HEADER_BOTTOM - 96
NO_LINE_START = set("，。！？、；：」』）》〉】…—,.!?;:)]}")
NO_LINE_END = set("「『（《〈【([{")

_fonts = {}


def _font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(path), size)
    return _fonts[key]


def _is_cjk(char):
    return ord(char) >= 0x2E80


def _runs(text, size):
    """Split text into (run, font) pairs so each script uses its own face."""
    runs = []
    for char in text:
        path = CJK_FONT if _is_cjk(char) else LATIN_FONT
        if runs and runs[-1][1] == path:
            runs[-1][0] += char
        else:
            runs.append([char, path])
    return [(run, _font(path, size)) for run, path in runs]


def _width(text, size):
    return sum(font.getlength(run) for run, font in _runs(text, size))


def _tokens(text):
    """Break text into units that must stay on one line."""
    tokens = []
    word = ""
    for char in text:
        if _is_cjk(char) or char == " ":
            if word:
                tokens.append(word)
                word = ""
            tokens.append(char)
        else:
            word += char
    if word:
        tokens.append(word)

    merged = []
    for token in tokens:
        if merged and (token in NO_LINE_START or merged[-1][-1] in NO_LINE_END):
            merged[-1] += token
        else:
            merged.append(token)
    return merged


def _wrap(text, size, max_width):
    lines = []
    line = ""
    for token in _tokens(text):
        candidate = line + token
        if line.strip() and _width(candidate.strip(), size) > max_width:
            lines.append(line.strip())
            line = token.lstrip()
        else:
            line = candidate
    if line.strip():
        lines.append(line.strip())
    return lines


def _block_height(size, line_count):
    return round(size * LINE_SPACING) * (line_count - 1) + size


def _fit_title(title, max_width):
    for size in TITLE_SIZES:
        lines = _wrap(title, size, max_width)
        if (
            len(lines) <= MAX_TITLE_LINES
            and _block_height(size, len(lines)) <= TITLE_AREA
            and all(_width(line, size) <= max_width for line in lines)
        ):
            return size, lines
    size = TITLE_SIZES[-1]
    lines = _wrap(title, size, max_width)[:MAX_TITLE_LINES]
    while lines[-1] and _width(lines[-1] + "…", size) > max_width:
        lines[-1] = lines[-1][:-1]
    lines[-1] += "…"
    return size, lines


def _draw_text(draw, x, baseline, text, size, fill):
    for run, font in _runs(text, size):
        draw.text((x, baseline), run, font=font, fill=fill, anchor="ls")
        x += font.getlength(run)
    return x


def render_card(path, title, site_name, footer_left, footer_right):
    image = Image.new("RGB", (WIDTH, HEIGHT), PAGE)
    draw = ImageDraw.Draw(image)
    max_width = WIDTH - 2 * MARGIN

    # Header: site name over a hairline, as in the site header.
    if site_name:
        _draw_text(draw, MARGIN, HEADER_BOTTOM - 30, site_name, 34, INK)
        draw.line(
            [(MARGIN, HEADER_BOTTOM), (WIDTH - MARGIN, HEADER_BOTTOM)],
            fill=RULE,
            width=2,
        )

    # Title block, vertically centred between header and footer.
    size, lines = _fit_title(title, max_width)
    line_height = round(size * LINE_SPACING)
    block = _block_height(size, len(lines))
    top = HEADER_BOTTOM + 48 + (FOOTER_TOP - HEADER_BOTTOM - 48 - block) // 2
    draw.rectangle([MARGIN, top - 34, MARGIN + 56, top - 29], fill=ACCENT)
    baseline = top + round(size * 0.86)
    for line in lines:
        _draw_text(draw, MARGIN, baseline, line, size, INK)
        baseline += line_height

    # Footer: date and category on the left, domain on the right.
    if footer_left:
        _draw_text(draw, MARGIN, HEIGHT - 62, footer_left, 28, MUTED)
    if footer_right:
        right = WIDTH - MARGIN - _width(footer_right, 28)
        _draw_text(draw, right, HEIGHT - 62, footer_right, 28, MUTED)

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def _card_path(article):
    return f"og/{article.slug}.png"


def _all_articles(generator):
    return (
        list(generator.articles)
        + list(generator.translations)
        + list(generator.drafts)
        + list(generator.drafts_translations)
    )


def assign_cards(generator):
    """Tell templates which image each article should advertise."""
    generator.context["OG_DEFAULT_IMAGE"] = DEFAULT_CARD
    for article in _all_articles(generator):
        custom = article.metadata.get("image")
        article.og_image = custom.lstrip("/") if custom else _card_path(article)


def write_cards(generator, writer):
    settings = generator.settings
    output = Path(generator.output_path)
    site_name = settings.get("SITENAME", "")
    domain = settings.get("SITEURL", "").split("//")[-1].strip("/")

    render_card(
        output / DEFAULT_CARD,
        site_name,
        "",
        settings.get("SITESUBTITLE", ""),
        domain,
    )
    for article in _all_articles(generator):
        if article.metadata.get("image"):
            continue
        footer = article.date.strftime("%Y.%m.%d")
        if getattr(article, "category", None):
            footer += f"   {article.category}"
        render_card(
            output / _card_path(article), article.title, site_name, footer, domain
        )


def register():
    signals.article_generator_finalized.connect(assign_cards)
    signals.article_writer_finalized.connect(write_cards)
