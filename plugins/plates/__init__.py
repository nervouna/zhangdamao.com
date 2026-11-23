"""Give every article a "plate": three overlapping circles placed by its date.

The large circle never moves from the centre, so a column of plates keeps
one visual anchor. The medium circle sits on its rim at the month's clock
position (12 o'clock is December) and the small one at the day's position
(one turn is 31 days). Where circles overlap, the overlap is drawn in ink.

Sets two attributes on each article:

* ``plate``: inline SVG markup for templates, coloured by the theme's CSS.
* ``plate_circles``: ``[(cx, cy, r), ...]`` on a 100x100 square, which the
  ``og_cards`` plugin uses to draw the same plate on the social card.

``DEFAULT_PLATE_CIRCLES`` is the plate for things without a date of their own.
"""

import math

from markupsafe import Markup
from pelican import signals

SIZE = 100
RADII = (27, 17, 11)


def circles(month, day):
    centre = SIZE / 2
    orbit = RADII[0]

    def on_rim(turn):
        angle = turn * 2 * math.pi
        return centre + orbit * math.sin(angle), centre - orbit * math.cos(angle)

    return [
        (centre, centre, RADII[0]),
        (*on_rim((month % 12) / 12), RADII[1]),
        (*on_rim(day / 31), RADII[2]),
    ]


DEFAULT_PLATE_CIRCLES = circles(2, 21)


def _n(value):
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _overlap_path(a, b):
    """SVG path for the region shared by two circles, or '' if they are apart."""
    (x1, y1, r1), (x2, y2, r2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    if d >= r1 + r2:
        return ""
    if d <= abs(r1 - r2):
        # One circle lies inside the other: the overlap is the smaller circle.
        x, y, r = a if r1 < r2 else b
        return (
            f"M{_n(x - r)} {_n(y)}"
            f"a{_n(r)} {_n(r)} 0 1 0 {_n(2 * r)} 0"
            f"a{_n(r)} {_n(r)} 0 1 0 {_n(-2 * r)} 0Z"
        )
    along = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    half = math.sqrt(max(r1 * r1 - along * along, 0))
    theta = math.atan2(y2 - y1, x2 - x1)
    alpha = math.atan2(half, along)
    beta = math.atan2(half, d - along)
    start = (x1 + r1 * math.cos(theta - alpha), y1 + r1 * math.sin(theta - alpha))
    end = (x1 + r1 * math.cos(theta + alpha), y1 + r1 * math.sin(theta + alpha))
    return (
        f"M{_n(start[0])} {_n(start[1])}"
        f"A{_n(r1)} {_n(r1)} 0 {int(2 * alpha > math.pi)} 1 {_n(end[0])} {_n(end[1])}"
        f"A{_n(r2)} {_n(r2)} 0 {int(2 * beta > math.pi)} 1 {_n(start[0])} {_n(start[1])}Z"
    )


def svg(plate_circles):
    parts = [
        f'<svg class="plate" viewBox="0 0 {SIZE} {SIZE}" aria-hidden="true">'
    ]
    for index, (x, y, r) in enumerate(plate_circles, start=1):
        parts.append(f'<circle class="k{index}" cx="{_n(x)}" cy="{_n(y)}" r="{_n(r)}"/>')
    overlaps = "".join(
        _overlap_path(plate_circles[i], plate_circles[j])
        for i, j in ((0, 1), (0, 2), (1, 2))
    )
    if overlaps:
        parts.append(f'<path class="x" d="{overlaps}"/>')
    parts.append("</svg>")
    return Markup("".join(parts))


def assign_plates(generator):
    generator.context["DEFAULT_PLATE_CIRCLES"] = DEFAULT_PLATE_CIRCLES
    articles = (
        list(generator.articles)
        + list(generator.translations)
        + list(generator.drafts)
        + list(generator.drafts_translations)
    )
    for article in articles:
        article.plate_circles = circles(article.date.month, article.date.day)
        article.plate = svg(article.plate_circles)


def register():
    signals.article_generator_finalized.connect(assign_plates)
