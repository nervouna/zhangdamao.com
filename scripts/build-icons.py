"""Regenerate the favicon and touch icon from the site mark.

Run from the repository root after changing the mark or its colours:

    uv run python scripts/build-icons.py

The mark's geometry mirrors MARK_CIRCLES in plugins/plates and the colours
mirror the light-theme tokens in the theme's style.css.
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

OUT = Path("content/extra")

PAGE = "#f9fbfc"
INK = "#0c1014"
RED = "#e03106"
BLUE = "#093da1"

# The mark is 36x30 units; centre it on a 40-unit square.
UNITS = 40
CIRCLES = [((16, 21, 13), RED), ((28, 15, 9), BLUE)]


def draw_mark(size, background=None, inset=0.0):
    """Return the mark at ``size`` px, shrunk towards the centre by ``inset``."""
    scale = 8
    side = size * scale
    unit = side * (1 - 2 * inset) / UNITS
    offset = side * inset

    def box(circle):
        x, y, r = circle
        return [
            offset + (x - r) * unit,
            offset + (y - r) * unit,
            offset + (x + r) * unit,
            offset + (y + r) * unit,
        ]

    image = Image.new("RGBA", (side, side), background or (0, 0, 0, 0))
    masks = []
    for circle, colour in CIRCLES:
        mask = Image.new("L", (side, side), 0)
        ImageDraw.Draw(mask).ellipse(box(circle), fill=255)
        image.paste(colour, mask=mask)
        masks.append(mask)
    image.paste(INK, mask=ImageChops.multiply(*masks))
    return image.resize((size, size), Image.LANCZOS)


def svg():
    (x1, y1, r1), (x2, y2, r2) = (circle for circle, _ in CIRCLES)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {UNITS} {UNITS}">
<style>.x{{fill:{INK}}}@media (prefers-color-scheme:dark){{.x{{fill:#f0f2f4}}}}</style>
<clipPath id="a"><circle cx="{x1}" cy="{y1}" r="{r1}"/></clipPath>
<circle cx="{x1}" cy="{y1}" r="{r1}" fill="{RED}"/>
<circle cx="{x2}" cy="{y2}" r="{r2}" fill="{BLUE}"/>
<circle class="x" cx="{x2}" cy="{y2}" r="{r2}" clip-path="url(#a)"/>
</svg>
"""


if __name__ == "__main__":
    draw_mark(256).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    draw_mark(180, PAGE, inset=0.14).convert("RGB").save(
        OUT / "apple-touch-icon.png", optimize=True
    )
    (OUT / "favicon.svg").write_text(svg())
