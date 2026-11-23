"""Generate a social preview card (Open Graph image) for every article.

Each article gets ``og/<slug>.png`` (1200x630) showing its title in the
theme's heading fonts next to its plate (see the ``plates`` plugin, which
must be listed before this one in ``PLUGINS``). Articles can opt out with an
``Image:`` metadata field pointing at their own picture. Pages and index
pages use ``og/default.png``, which shows the site name and subtitle.
"""

from pathlib import Path

from pelican import signals
from PIL import Image, ImageChops, ImageDraw, ImageFont

FONT_DIR = Path(__file__).parent.parent / "fonts"
LATIN_BOLD = FONT_DIR / "Archivo-ExtraBold.ttf"
LATIN_TEXT = FONT_DIR / "Archivo-SemiBold.ttf"
CJK_FONT = FONT_DIR / "GlowSansSC-Normal-Heavy.otf"

WIDTH, HEIGHT = 1200, 630
MARGIN = 80
DEFAULT_CARD = "og/default.png"

# sRGB equivalents of the light-theme tokens in the theme's style.css.
PAGE = "#f9fbfc"
INK = "#0c1014"
MUTED = "#565b61"
RED = "#e03106"
BLUE = "#093da1"
YELLOW = "#f6d32b"
PLATE_COLOURS = (RED, BLUE, YELLOW)

RULE_TOP = 138
RULE_WEIGHT = 6
FOOTER_TOP = HEIGHT - 110
PLATE_SIZE = 340
PLATE_UNITS = 100
TITLE_TOP = RULE_TOP + RULE_WEIGHT + 40
TITLE_WIDTH = WIDTH - 2 * MARGIN - PLATE_SIZE - 48
TITLE_AREA = FOOTER_TOP - TITLE_TOP - 16
TITLE_SIZES = (76, 66, 58, 50, 44)
MAX_TITLE_LINES = 4
LINE_SPACING = 1.25
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


def _runs(text, size, latin=LATIN_BOLD):
    """Split text into (run, font) pairs so each script uses its own face."""
    runs = []
    for char in text:
        path = CJK_FONT if _is_cjk(char) else latin
        if runs and runs[-1][1] == path:
            runs[-1][0] += char
        else:
            runs.append([char, path])
    return [(run, _font(path, size)) for run, path in runs]


def _width(text, size, latin=LATIN_BOLD):
    return sum(font.getlength(run) for run, font in _runs(text, size, latin))


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


def _draw_text(draw, x, baseline, text, size, fill, latin=LATIN_BOLD):
    for run, font in _runs(text, size, latin):
        draw.text((x, baseline), run, font=font, fill=fill, anchor="ls")
        x += font.getlength(run)
    return x


def _draw_circles(image, circles, left, top, width, height, units):
    """Draw circles given in ``units`` per ``width``, every overlap in ink."""
    scale = 3
    size = (width * scale, height * scale)
    unit = size[0] / units

    def box(circle):
        x, y, r = circle
        return [(x - r) * unit, (y - r) * unit, (x + r) * unit, (y + r) * unit]

    layer = Image.new("RGB", size, PAGE)
    draw = ImageDraw.Draw(layer)
    masks = []
    for circle, colour in zip(circles, PLATE_COLOURS):
        draw.ellipse(box(circle), fill=colour)
        mask = Image.new("L", size, 0)
        ImageDraw.Draw(mask).ellipse(box(circle), fill=255)
        masks.append(mask)
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            layer.paste(INK, mask=ImageChops.multiply(masks[i], masks[j]))
    image.paste(layer.resize((width, height), Image.LANCZOS), (left, top))


def render_card(path, title, site_name, footer_left, footer_right, circles, mark):
    image = Image.new("RGB", (WIDTH, HEIGHT), PAGE)
    draw = ImageDraw.Draw(image)

    # Header: the site mark and name over a heavy rule, as in the site header.
    mark_circles, (mark_units, mark_rows) = mark
    mark_height = 36
    mark_width = round(mark_height * mark_units / mark_rows)
    _draw_circles(image, mark_circles, MARGIN, 74, mark_width, mark_height, mark_units)
    if site_name:
        _draw_text(draw, MARGIN + mark_width + 14, 104, site_name, 32, INK)
    draw.rectangle(
        [MARGIN, RULE_TOP, WIDTH - MARGIN, RULE_TOP + RULE_WEIGHT - 1], fill=INK
    )

    # Plate on the right, centred between the rule and the footer.
    plate_top = RULE_TOP + RULE_WEIGHT + (FOOTER_TOP - RULE_TOP - RULE_WEIGHT - PLATE_SIZE) // 2
    _draw_circles(
        image, circles, WIDTH - MARGIN - PLATE_SIZE, plate_top, PLATE_SIZE, PLATE_SIZE, PLATE_UNITS
    )

    # Title, hanging from the rule on the left.
    size, lines = _fit_title(title, TITLE_WIDTH)
    baseline = TITLE_TOP + round(size * 0.86)
    for line in lines:
        _draw_text(draw, MARGIN, baseline, line, size, INK)
        baseline += round(size * LINE_SPACING)

    # Footer: date and category on the left, domain on the right.
    if footer_left:
        _draw_text(draw, MARGIN, HEIGHT - 62, footer_left, 26, MUTED, LATIN_TEXT)
    if footer_right:
        right = WIDTH - MARGIN - _width(footer_right, 26, LATIN_TEXT)
        _draw_text(draw, right, HEIGHT - 62, footer_right, 26, MUTED, LATIN_TEXT)

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
    mark = (generator.context["MARK_CIRCLES"], generator.context["MARK_BOX"])

    render_card(
        output / DEFAULT_CARD,
        site_name,
        "",
        settings.get("SITESUBTITLE", ""),
        domain,
        generator.context["DEFAULT_PLATE_CIRCLES"],
        mark,
    )
    for article in _all_articles(generator):
        if article.metadata.get("image"):
            continue
        footer = article.date.strftime("%Y.%m.%d")
        if getattr(article, "category", None):
            footer += f"   {article.category}"
        render_card(
            output / _card_path(article),
            article.title,
            site_name,
            footer,
            domain,
            article.plate_circles,
            mark,
        )


def register():
    signals.article_generator_finalized.connect(assign_cards)
    signals.article_writer_finalized.connect(write_cards)
