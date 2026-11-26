"""Schedule 17 stand-in letters and numerals (no Transport file).

Forms are polygons and axis-aligned rects on a stroke-width grid:
  tile = 8 sw, cap height = 5.6 sw, stem = 1.0 sw (Part 2) or 1.2 sw (Part 1).
Lower case uses x-height 0.72 cap, with ascenders to cap and descenders 0.28 cap.
Part 5 (VMS) is the seven-bar set in render._digit_vms — do not use this module there.

Terminals are flat cuts (rx = 0, stroke-linecap = butt). Never a filled cell box.
"""
from __future__ import annotations

import math

CAP_SW = 5.6
X_RATIO = 0.72
DESC_RATIO = 0.28
ADVANCE = {
    "default": 5.0,
    "I": 2.4, "i": 2.2, "l": 2.2, "j": 2.6, "f": 3.2, "t": 3.4, "r": 3.6,
    "J": 4.2, "L": 4.4, "E": 4.6, "F": 4.6, "S": 4.8, "s": 4.4,
    "W": 7.2, "M": 7.0, "w": 6.4, "m": 7.0, "%": 7.2, " ": 3.0,
    "A": 5.6, "V": 5.6, "Y": 5.4, "O": 6.2, "Q": 6.2, "G": 5.6, "D": 5.6,
    "C": 5.6, "c": 4.6, "e": 5.0, "U": 5.6, "K": 5.6, "k": 4.8,
    "0": 4.6, "1": 3.4, "2": 5.0, "3": 5.0, "4": 5.2, "5": 5.0,
    "6": 5.2, "7": 4.8, "8": 5.2, "9": 5.2,
    "'": 2.0, '"': 3.4, ".": 2.2, "&": 5.6,
    "(": 3.0, ")": 3.0,
}

SHEET_CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789%.-&!'\"()"
)


def stem(cap_h: float, part: int = 2) -> float:
    sw = cap_h / CAP_SW
    return sw * (1.2 if part == 1 else 1.0)


# r3: advance scale for one word() call. 1.0 = the stand-in advances. Signs whose
# SI diagram sets the word tighter (601.1 STOP) pass a smaller value so the cap
# height can match the diagram; the stroke width is unchanged.
NARROW = 1.0


def advance_sw(ch: str) -> float:
    return ADVANCE.get(ch, ADVANCE["default"]) * NARROW


def measure(text: str, cap_h: float, tracking_sw: float = 1.1) -> float:
    sw = cap_h / CAP_SW
    if not text:
        return 0.0
    return (sum(advance_sw(ch) for ch in text) + tracking_sw * max(len(text) - 1, 0)) * sw


def fit_cap_h(text: str, max_width: float, tracking_sw: float = 1.1, max_h: float | None = None) -> float:
    """One x-height that keeps `text` inside max_width."""
    units = sum(advance_sw(ch) for ch in text) + tracking_sw * max(len(text) - 1, 0)
    if units <= 0 or max_width <= 0:
        return max_h or 0.0
    h = max_width / (units / CAP_SW)
    if max_h is not None:
        h = min(h, max_h)
    return h


# When GEOM is a list, primitives also append analytic geometry here so tests can
# rasterise glyphs without an SVG renderer (see glyph_mask()).
GEOM: list | None = None


def _bar(fill: str, x0: float, y0: float, x1: float, y1: float) -> str:
    if GEOM is not None:
        GEOM.append(("rect", x0, y0, x1, y1))
    return (
        f'<rect x="{x0:.4f}" y="{y0:.4f}" width="{x1 - x0:.4f}" height="{y1 - y0:.4f}" '
        f'fill="{fill}"/>'
    )


def _poly(fill: str, pts: list[tuple[float, float]]) -> str:
    if GEOM is not None:
        GEOM.append(("poly", list(pts)))
    s = " ".join(f"{x:.4f},{y:.4f}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}"/>'


def _slant(fill: str, xt: float, yt: float, xb: float, yb: float, t: float) -> str:
    """Diagonal stroke of uniform perpendicular width t between two horizontal cuts.

    Centreline runs (xt, yt) -> (xb, yb). Both ends are flat cuts on the
    horizontal lines y = yt and y = yb (Sch17 terminals meet the cap line or
    baseline square, never rounded).
    """
    dx, dy = xb - xt, yb - yt
    if abs(dy) < 1e-9:
        return _bar(fill, min(xt, xb), yt - t / 2, max(xt, xb), yt + t / 2)
    hw = t / 2 * math.hypot(dx, dy) / abs(dy)
    return _poly(fill, [(xt - hw, yt), (xt + hw, yt), (xb + hw, yb), (xb - hw, yb)])


def _half_w(t: float, dx: float, dy: float) -> float:
    """Horizontal half-width of a slant stroke of perpendicular width t."""
    return t / 2 * math.hypot(dx, dy) / abs(dy) if dy else t / 2


def _ring(fill: str, cx: float, cy: float, rx: float, ry: float, t: float) -> str:
    if GEOM is not None:
        GEOM.append(("arc", cx, cy, rx, ry, t, 0.0, 0.0))
    return (
        f'<ellipse cx="{cx:.4f}" cy="{cy:.4f}" rx="{rx:.4f}" ry="{ry:.4f}" '
        f'fill="none" stroke="{fill}" stroke-width="{t:.4f}" stroke-linecap="butt"/>'
    )


def _arc(fill: str, d: str, t: float) -> str:
    return (
        f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{t:.4f}" '
        f'stroke-linecap="butt" stroke-linejoin="miter"/>'
    )


def _open_c(
    fill: str,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    t: float,
    gap: float = 70.0,
    gap_center: float = 0.0,
) -> str:
    """C-shape: ellipse arc with a gap. gap_center=0 is east, 90 south, 180 west (SVG y-down)."""
    if GEOM is not None:
        GEOM.append(("arc", cx, cy, rx, ry, t, gap_center, gap))
        prev, globals()["GEOM"] = GEOM, None
        try:
            return _open_c(fill, cx, cy, rx, ry, t, gap, gap_center)
        finally:
            globals()["GEOM"] = prev
    a0 = math.radians(gap_center - gap / 2.0)
    a1 = math.radians(gap_center + gap / 2.0)
    x0 = cx + rx * math.cos(a0)
    y0 = cy + ry * math.sin(a0)
    x1 = cx + rx * math.cos(a1)
    y1 = cy + ry * math.sin(a1)
    return _arc(fill, f"M {x0:.3f} {y0:.3f} A {rx:.3f} {ry:.3f} 0 1 0 {x1:.3f} {y1:.3f}", t)


def char(ch: str, cx: float, cy: float, cap_h: float, fill: str, part: int = 2) -> str:
    """Draw one character. cy is the centre of the cap-height band."""
    if ch == " ":
        return ""
    t = stem(cap_h, part)
    h = cap_h
    w = advance_sw(ch) / CAP_SW * cap_h
    x0, y0 = cx - w / 2, cy - h / 2
    x1, y1 = cx + w / 2, cy + h / 2
    xm, ym = cx, cy
    xh = h * X_RATIO
    base = y1
    top_x = base - xh
    desc = base + h * DESC_RATIO

    def bar(a: float, b: float, c: float, d: float) -> str:
        return _bar(fill, a, b, c, d)

    def upoly(pts: list[tuple[float, float]]) -> str:
        return _poly(fill, [(x0 + px * w, y0 + py * h) for px, py in pts])

    if ch.isdigit() or ch == "%":
        return _numeral(ch, cx, cy, w, h, t, fill)

    if ch == ".":
        return bar(xm - t * 0.45, y1 - t, xm + t * 0.45, y1)
    if ch == "-":
        return bar(x0, ym - t * 0.5, x1, ym + t * 0.5)
    if ch in "'\"":
        # Foot / inch primes (imperial legends such as 14'-6"): tapered wedges
        # from cap height down to 0.36 H, leaning right at the top.
        def prime(px: float) -> str:
            return _poly(fill, [(px - t * 0.30, y0), (px + t * 0.55, y0),
                                (px + t * 0.05, y0 + h * 0.36), (px - t * 0.30, y0 + h * 0.36)])
        if ch == "'":
            return prime(xm - t * 0.12)
        return prime(xm - t * 0.95) + prime(xm + t * 0.70)
    if ch == "&":
        # r6: mixed-case stand-in ampersand for 827.1 "No A & E" (SI 2016 p213). Small upper
        # loop, open lower bowl and a leg falling to the baseline at the right; no counter shared
        # with '8' (the bowl is open) and no stem like 'E'.
        ou, ol, tu = h * 0.28, h * 0.30, t * 0.85
        return (
            _ring(fill, x0 + w * 0.40, y0 + ou, w * 0.26 - tu / 2, ou - tu / 2, tu)
            + _open_c(fill, x0 + w * 0.38, y1 - ol, w * 0.37 - t / 2, ol - t / 2, t, 70, -60)
            + _slant(fill, x0 + w * 0.27, y0 + h * 0.42, x1 - t * 0.55, y1, t)
            + bar(x0 + w * 0.66, y0 + h * 0.47, x1, y0 + h * 0.47 + t * 0.9)
        )

    # --- capitals ---
    if ch == "A":
        hw = _half_w(t, w / 2, h)
        return (
            _slant(fill, xm, y0, x0 + hw, y1, t)
            + _slant(fill, xm, y0, x1 - hw, y1, t)
            + bar(x0 + w * 0.24, y0 + h * 0.62, x1 - w * 0.24, y0 + h * 0.62 + t)
        )
    if ch == "B":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x0, y0, x1 - t * 0.35, y0 + t)
            + bar(x0, ym - t * 0.48, x1 - t * 0.35, ym + t * 0.48)
            + bar(x0, y1 - t, x1 - t * 0.35, y1)
            + bar(x1 - t, y0 + t * 0.05, x1, ym - t * 0.15)
            + bar(x1 - t, ym + t * 0.15, x1, y1 - t * 0.05)
        )
    if ch == "C":
        return _open_c(fill, xm, ym, (w - t) / 2, (h - t) / 2, t, 72)
    if ch == "D":
        # Stem plus a full-height rounded bowl that joins the stem. Short
        # top/bottom bars made a square inner counter that reads as P,
        # especially at small published sizes (818.1 "Dual").
        # Overlap the stem slightly so the joins stay solid.
        xa = x0 + t * 0.85
        ry = (h - t) / 2
        rx = min(x1 - t / 2 - xa, ry * 1.60)
        return (
            bar(x0, y0, x0 + t, y1)
            + (GEOM.append(("arc", xa, ym, rx, ry, t, 180.0, 180.0)) or "" if GEOM is not None else "")
            + _arc(fill, f"M {xa:.4f} {y0 + t / 2:.4f} A {rx:.4f} {ry:.4f} 0 0 1 {xa:.4f} {y1 - t / 2:.4f}", t)
        )
    if ch == "E":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x0, y0, x1, y0 + t)
            + bar(x0, ym - t * 0.48, x1 - t * 0.15, ym + t * 0.48)
            + bar(x0, y1 - t, x1, y1)
        )
    if ch == "F":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x0, y0, x1, y0 + t)
            + bar(x0, ym - t * 0.48, x1 - t * 0.2, ym + t * 0.48)
        )
    if ch == "G":
        return (
            _open_c(fill, xm, ym, (w - t) / 2, (h - t) / 2, t, 72)
            + bar(xm, ym - t * 0.48, x1 - t * 0.15, ym + t * 0.48)
            + bar(x1 - t, ym - t * 0.48, x1, y1 - t * 0.15)
        )
    if ch == "H":
        return bar(x0, y0, x0 + t, y1) + bar(x1 - t, y0, x1, y1) + bar(x0, ym - t * 0.48, x1, ym + t * 0.48)
    if ch == "I":
        return bar(xm - t * 0.52, y0, xm + t * 0.52, y1)
    if ch == "J":
        return bar(x1 - t, y0, x1, y1 - t * 0.4) + bar(x0 + t * 0.15, y1 - t, x1, y1) + bar(x0, ym + t, x0 + t, y1 - t * 0.2)
    if ch == "K":
        # Stem + arm and leg of full stroke weight meeting at the stem.
        jy = y0 + h * 0.58
        hw = _half_w(t, w, h * 0.58)
        return (
            bar(x0, y0, x0 + t, y1)
            + _slant(fill, x1 - hw, y0, x0 + t * 0.9, jy, t)
            + _slant(fill, x0 + w * 0.38, y0 + h * 0.42, x1 - hw, y1, t)
        )
    if ch == "L":
        return bar(x0, y0, x0 + t, y1) + bar(x0, y1 - t, x1, y1)
    if ch == "M":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x1 - t, y0, x1, y1)
            + _slant(fill, x0 + t * 0.5, y0, xm, y0 + h * 0.72, t)
            + _slant(fill, x1 - t * 0.5, y0, xm, y0 + h * 0.72, t)
        )
    if ch == "N":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x1 - t, y0, x1, y1)
            + _slant(fill, x0 + t * 0.5, y0, x1 - t * 0.5, y1, t)
        )
    if ch == "O":
        return _ring(fill, xm, ym, (w - t) / 2, (h - t) / 2, t)
    if ch == "P":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x0, y0, x1 - t * 0.15, y0 + t)
            + bar(x0, ym - t * 0.48, x1 - t * 0.15, ym + t * 0.48)
            + bar(x1 - t, y0 + t * 0.15, x1, ym + t * 0.48)
        )
    if ch == "Q":
        return (
            _ring(fill, xm, ym, (w - t) / 2, (h - t) / 2, t)
            + _slant(fill, xm + w * 0.08, y0 + h * 0.66, x1 - t * 0.4, y1, t)
        )
    if ch == "R":
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x0, y0, x1 - t * 0.15, y0 + t)
            + bar(x0, ym - t * 0.48, x1 - t * 0.15, ym + t * 0.48)
            + bar(x1 - t, y0 + t * 0.15, x1, ym + t * 0.48)
            + _slant(fill, x0 + w * 0.45, ym + t * 0.48, x1 - _half_w(t, w * 0.5, h / 2), y1, t)
        )
    if ch == "S":
        # Curved spine: upper bowl opens to the lower right, lower bowl to the upper
        # left; they meet tangentially at mid-height. Never the box form of "5".
        ry = (h - t) / 4
        return (
            _open_c(fill, xm, y0 + t / 2 + ry, (w - t) / 2 * 0.94, ry, t, gap=125, gap_center=28)
            + _open_c(fill, xm, ym + ry, (w - t) / 2, ry, t, gap=125, gap_center=208)
        )
    if ch == "T":
        return bar(x0, y0, x1, y0 + t) + bar(xm - t * 0.52, y0, xm + t * 0.52, y1)
    if ch == "U":
        # Overlapping stems + bottom bar: no notch at the corners.
        return (
            bar(x0, y0, x0 + t, y1)
            + bar(x1 - t, y0, x1, y1)
            + bar(x0, y1 - t, x1, y1)
        )
    if ch == "V":
        hw = _half_w(t, w / 2, h)
        return _slant(fill, x0 + hw, y0, xm, y1, t) + _slant(fill, x1 - hw, y0, xm, y1, t)
    if ch == "W":
        q = w / 4
        hw = _half_w(t, q, h)
        return (
            _slant(fill, x0 + hw, y0, x0 + q, y1, t)
            + _slant(fill, xm, y0, x0 + q, y1, t)
            + _slant(fill, xm, y0, x1 - q, y1, t)
            + _slant(fill, x1 - hw, y0, x1 - q, y1, t)
        )
    if ch == "X":
        hw = _half_w(t, w, h)
        return _slant(fill, x0 + hw, y0, x1 - hw, y1, t) + _slant(fill, x1 - hw, y0, x0 + hw, y1, t)
    if ch == "Y":
        jy = y0 + h * 0.50
        hw = _half_w(t, w / 2, h / 2)
        return (
            _slant(fill, x0 + hw, y0, xm, jy, t)
            + _slant(fill, x1 - hw, y0, xm, jy, t)
            + bar(xm - t * 0.5, jy - t * 0.3, xm + t * 0.5, y1)
        )
    if ch == "Z":
        return (
            bar(x0, y0, x1, y0 + t)
            + bar(x0, y1 - t, x1, y1)
            + _slant(fill, x1 - _half_w(t, w, h), y0 + t, x0 + _half_w(t, w, h), y1 - t, t)
        )
    if ch == "!":
        return bar(xm - t * 0.48, y0, xm + t * 0.48, ym + t * 0.35) + bar(
            xm - t * 0.48, y1 - t, xm + t * 0.48, y1
        )

    # --- lower case ---
    if ch == "a":
        return (
            _ring(fill, xm - t * 0.15, top_x + xh / 2, (w - t * 1.6) / 2, (xh - t) / 2, t)
            + bar(x1 - t, top_x, x1, base)
        )
    if ch == "b":
        return bar(x0, y0, x0 + t, base) + _ring(
            fill, xm + t * 0.1, top_x + xh / 2, (w - t * 1.8) / 2, (xh - t) / 2, t
        )
    if ch == "c":
        return _open_c(fill, xm, top_x + xh / 2, (w - t) / 2, (xh - t) / 2, t, 78)
    if ch == "d":
        return bar(x1 - t, y0, x1, base) + _ring(
            fill, xm - t * 0.1, top_x + xh / 2, (w - t * 1.8) / 2, (xh - t) / 2, t
        )
    if ch == "e":
        cy_x = top_x + xh / 2
        rr, rh = (w - t) / 2, (xh - t) / 2
        # Bowl open at the lower right (clear gap so it never reads "o"),
        # full-width crossbar through the middle.
        return (
            _open_c(fill, xm, cy_x, rr, rh, t, gap=95, gap_center=32)
            + bar(x0 + t * 0.2, cy_x - t * 0.5, x1 - t * 0.2, cy_x + t * 0.5)
        )
    if ch == "f":
        return (
            bar(xm - t * 0.4, y0 + t, xm + t * 0.4, base)
            + bar(xm - t * 0.4, y0, x1, y0 + t)
            + bar(x0, top_x, x1, top_x + t * 0.85)
        )
    if ch == "g":
        return (
            _ring(fill, xm, top_x + xh / 2, (w - t * 1.4) / 2, (xh - t) / 2, t)
            + bar(x1 - t, top_x, x1, desc - t)
            + bar(xm - w * 0.25, desc - t, x1, desc)
        )
    if ch == "h":
        return (
            bar(x0, y0, x0 + t, base)
            + bar(x0, top_x, x1 - t * 0.15, top_x + t)
            + bar(x1 - t, top_x + t * 0.4, x1, base)
        )
    if ch == "i":
        return bar(xm - t * 0.5, top_x, xm + t * 0.5, base) + bar(
            xm - t * 0.5, top_x - t * 1.55, xm + t * 0.5, top_x - t * 0.55
        )
    if ch == "j":
        return (
            bar(xm - t * 0.55, top_x - t * 1.7, xm + t * 0.55, top_x - t * 0.6)
            + bar(xm - t * 0.45, top_x, xm + t * 0.45, desc - t * 0.2)
            + bar(x0, desc - t, xm + t * 0.45, desc)
        )
    if ch == "k":
        jy = top_x + xh * 0.62
        hw = _half_w(t, w, xh * 0.62)
        return (
            bar(x0, y0, x0 + t, base)
            + _slant(fill, x1 - hw, top_x, x0 + t * 0.9, jy, t)
            + _slant(fill, x0 + w * 0.40, top_x + xh * 0.40, x1 - hw, base, t)
        )
    if ch == "l":
        return bar(xm - t * 0.5, y0, xm + t * 0.5, base)
    if ch == "m":
        mw = (w - t * 3) / 2
        return (
            bar(x0, top_x, x0 + t, base)
            + bar(x0, top_x, x0 + t + mw + t, top_x + t)
            + bar(x0 + t + mw, top_x + t * 0.4, x0 + t + mw + t, base)
            + bar(x0 + t + mw, top_x, x1, top_x + t)
            + bar(x1 - t, top_x + t * 0.4, x1, base)
        )
    if ch == "n":
        return (
            bar(x0, top_x, x0 + t, base)
            + bar(x0, top_x, x1 - t * 0.15, top_x + t)
            + bar(x1 - t, top_x + t * 0.4, x1, base)
        )
    if ch == "o":
        return _ring(fill, xm, top_x + xh / 2, (w - t) / 2, (xh - t) / 2, t)
    if ch == "p":
        return bar(x0, top_x, x0 + t, desc) + _ring(
            fill, xm + t * 0.1, top_x + xh / 2, (w - t * 1.8) / 2, (xh - t) / 2, t
        )
    if ch == "q":
        return bar(x1 - t, top_x, x1, desc) + _ring(
            fill, xm - t * 0.1, top_x + xh / 2, (w - t * 1.8) / 2, (xh - t) / 2, t
        )
    if ch == "r":
        return bar(x0, top_x, x0 + t, base) + bar(x0, top_x, x1, top_x + t)
    if ch == "s":
        ry = (xh - t) / 4
        return (
            _open_c(fill, xm, top_x + t / 2 + ry, (w - t) / 2 * 0.94, ry, t, gap=125, gap_center=28)
            + _open_c(fill, xm, top_x + xh / 2 + ry, (w - t) / 2, ry, t, gap=125, gap_center=208)
        )
    if ch == "t":
        return bar(xm - t * 0.45, y0 + h * 0.12, xm + t * 0.45, base) + bar(x0, top_x, x1, top_x + t * 0.85)
    if ch == "u":
        return (
            bar(x0, top_x, x0 + t, base)
            + bar(x1 - t, top_x, x1, base)
            + bar(x0, base - t, x1, base)
        )
    if ch == "v":
        hw = _half_w(t, w / 2, xh)
        return _slant(fill, x0 + hw, top_x, xm, base, t) + _slant(fill, x1 - hw, top_x, xm, base, t)
    if ch == "w":
        q = w / 4
        hw = _half_w(t, q, xh)
        return (
            _slant(fill, x0 + hw, top_x, x0 + q, base, t)
            + _slant(fill, xm, top_x, x0 + q, base, t)
            + _slant(fill, xm, top_x, x1 - q, base, t)
            + _slant(fill, x1 - hw, top_x, x1 - q, base, t)
        )
    if ch == "x":
        hw = _half_w(t, w, xh)
        return (
            _slant(fill, x0 + hw, top_x, x1 - hw, base, t)
            + _slant(fill, x1 - hw, top_x, x0 + hw, base, t)
        )
    if ch == "y":
        # Left arm to the baseline; right arm runs straight on into the descender.
        hw = _half_w(t, w / 2, xh)
        xr = x1 - hw
        slope = (xr - xm) / xh
        x_desc = xm - slope * (desc - base)
        return (
            _slant(fill, x0 + hw, top_x, xm, base, t)
            + _slant(fill, xr, top_x, x_desc, desc, t)
        )
    if ch == "z":
        return (
            bar(x0, top_x, x1, top_x + t)
            + bar(x0, base - t, x1, base)
            + _slant(fill, x1 - _half_w(t, w, xh), top_x + t, x0 + _half_w(t, w, xh), base - t, t)
        )
    if ch in "()":
        # Original stand-in parentheses (SI legends such as 818.4 "(B 3033)").
        # Tall shallow arcs, opening inward; not a C and not a Transport copy.
        rx = (w - t) * 0.85
        ry = (h - t) / 2
        if ch == "(":
            return _open_c(fill, xm + rx * 0.55, ym, rx, ry, t, gap=155, gap_center=0)
        return _open_c(fill, xm - rx * 0.55, ym, rx, ry, t, gap=155, gap_center=180)

    # Missing glyph: a 1-sw stem, never a filled cell.
    return bar(xm - t * 0.5, y0, xm + t * 0.5, y1)


def _numeral(ch: str, cx: float, cy: float, w: float, h: float, t: float, fill: str) -> str:
    """Sch17-style numerals: closed bowls and flags, not seven-segment. Full cap height."""
    x0, y0 = cx - w / 2, cy - h / 2
    x1, y1 = cx + w / 2, cy + h / 2
    xm, ym = cx, cy

    def bar(a: float, b: float, c: float, d: float) -> str:
        return _bar(fill, a, b, c, d)

    if ch == "0":
        return _ring(fill, xm, ym, (w - t) / 2, (h - t) / 2, t)
    if ch == "1":
        return (
            bar(xm - t * 0.15, y0, xm + t * 0.85, y1)
            + _poly(fill, [
                (xm - t * 0.15, y0),
                (xm - w * 0.42, y0 + h * 0.28),
                (xm - w * 0.18, y0 + h * 0.28),
                (xm + t * 0.85, y0),
            ])
        )
    if ch == "2":
        # Curved top bowl (never the Z form), diagonal from the bowl to the base, base bar.
        ry = h * 0.26
        cy2 = y0 + t / 2 + ry
        rx = (w - t) / 2
        a = math.radians(30)
        xs, ys = xm + rx * math.cos(a), cy2 + ry * math.sin(a)
        hw = _half_w(t, xs - x0, y1 - t - ys)
        return (
            _open_c(fill, xm, cy2, rx, ry, t, gap=140, gap_center=100)
            + _slant(fill, xs, ys, x0 + hw, y1 - t, t)
            + bar(x0, y1 - t, x1, y1)
        )
    if ch == "3":
        # Two bowls opening to the west; together exactly one cap height.
        ry = (h - t) / 4
        return (
            _open_c(fill, xm, y0 + t / 2 + ry, (w - t) / 2 * 0.95, ry, t, gap=110, gap_center=180)
            + _open_c(fill, xm, ym + ry, (w - t) / 2, ry, t, gap=110, gap_center=180)
        )
    if ch == "4":
        # Closed 4: full-height stem, diagonal from the stem top to the bar, full crossbar.
        sx0 = x1 - t * 1.6
        bar_y = y0 + h * 0.66
        hw = _half_w(t, w, h * 0.66)
        return (
            bar(sx0, y0, sx0 + t, y1)
            + _slant(fill, sx0 + t - hw, y0, x0 + hw, bar_y, t)
            + bar(x0, bar_y, x1, bar_y + t)
        )
    if ch == "5":
        # Top bar, short left stem, open lower bowl (distinct from the curved S).
        ry = h * 0.32 - t / 2
        bcy = y1 - t / 2 - ry
        return (
            bar(x0 + t * 0.2, y0, x1, y0 + t)
            + bar(x0 + t * 0.2, y0, x0 + t * 1.2, bcy - ry * 0.55)
            + _open_c(fill, xm, bcy, (w - t) / 2, ry, t, gap=115, gap_center=182)
        )
    if ch == "6":
        # Lower bowl + a slant stem rising from the bowl's left side to the cap line.
        rb_y = h * 0.30
        bcy = y1 - rb_y
        rx = (w - t) / 2
        return (
            _ring(fill, xm, bcy, rx, rb_y - t / 2, t)
            + _slant(fill, x0 + w * 0.62, y0, x0 + t * 0.5, bcy, t)
        )
    if ch == "7":
        return bar(x0, y0, x1, y0 + t) + _slant(fill, x1 - t * 0.6, y0 + t, x0 + w * 0.30, y1, t)
    if ch == "8":
        ru = (h - t) / 4 * 0.9
        rl = (h - t - 2 * ru) / 2
        return (
            _ring(fill, xm, y0 + t / 2 + ru, (w - t) / 2 * 0.9, ru, t)
            + _ring(fill, xm, y1 - t / 2 - rl, (w - t) / 2, rl, t)
        )
    if ch == "9":
        # Upper bowl + a slant stem falling from the bowl's right side to the baseline.
        rb_y = h * 0.30
        bcy = y0 + rb_y
        rx = (w - t) / 2
        return (
            _ring(fill, xm, bcy, rx, rb_y - t / 2, t)
            + _slant(fill, x1 - t * 0.5, bcy, x0 + w * 0.38, y1, t)
        )
    if ch == "%":
        r = min(w, h) * 0.16
        return (
            _ring(fill, x0 + r * 1.1, y0 + r * 1.3, r, r, t * 0.85)
            + _ring(fill, x1 - r * 1.1, y1 - r * 1.3, r, r, t * 0.85)
            + _poly(fill, [(x1 - t, y0), (x1, y0 + t * 0.6), (x0 + t, y1), (x0, y1 - t * 0.6)])
        )
    return bar(xm - t * 0.5, y0, xm + t * 0.5, y1)


# Every word() call appends (text, x0, y0, x1, y1, cap_h, tracking_sw) here when LOG is a list.
# render.py resets it per face so the validator can measure legends against fields.
LOG: list | None = None


def ink_box(text: str, cx: float, cy: float, cap_h: float, tracking_sw: float = 1.1) -> tuple[float, float, float, float]:
    """Ink bbox of a word: cap band, plus descenders when the text has any."""
    w = measure(text, cap_h, tracking_sw)
    top = cy - cap_h / 2
    bot = cy + cap_h / 2 + (cap_h * DESC_RATIO if any(c in "gjpqy" for c in text) else 0.0)
    return (cx - w / 2, top, cx + w / 2, bot)


def word(
    text: str,
    cx: float,
    cy: float,
    cap_h: float,
    fill: str,
    tracking_sw: float = 1.1,
    part: int = 2,
    narrow: float = 1.0,
) -> str:
    """Set mixed-case text. cy = centre of the cap-height band."""
    global NARROW
    if narrow != 1.0:
        prev, NARROW = NARROW, narrow
        try:
            return word(text, cx, cy, cap_h, fill, tracking_sw, part)
        finally:
            NARROW = prev
    sw = cap_h / CAP_SW
    if LOG is not None and text.strip():
        LOG.append((text,) + ink_box(text, cx, cy, cap_h, tracking_sw) + (cap_h, tracking_sw))
    widths = [advance_sw(ch) * sw for ch in text]
    gap = tracking_sw * sw
    total = sum(widths) + gap * max(len(text) - 1, 0)
    x = cx - total / 2
    out = []
    for ch, w in zip(text, widths):
        out.append(char(ch, x + w / 2, cy, cap_h, fill, part))
        x += w + gap
    return "".join(out)


def mph_pair(n: int, y: float = 0.0, cap_h: float = 0.373, fill: str | None = None, part: int = 2) -> str:
    n = int(n)
    ink = fill or "#141414"
    return word(f"{n:02d}", 0.0, y, cap_h, ink, tracking_sw=1.0, part=part)


def legend_10pct(cx: float, cy: float, cap_h: float, fill: str) -> str:
    return word("10%", cx, cy, cap_h, fill, tracking_sw=0.6, part=2)


def glyph_sheet_svg(cap_h: float = 0.55, fill: str = "#141414") -> str:
    """A–Z a–z 0–9 and punctuation on a grid. Used by the validator."""
    cols = 13
    cell = 1.15
    rows_n = math.ceil(len(SHEET_CHARS) / cols)
    parts = [f'<rect x="-0.6" y="-0.6" width="{cols * cell:.2f}" height="{rows_n * cell:.2f}" fill="#F7F7F7"/>']
    for i, ch in enumerate(SHEET_CHARS):
        r, c = divmod(i, cols)
        x = c * cell
        y = r * cell
        parts.append(f'<rect x="{x - 0.5:.3f}" y="{y - 0.5:.3f}" width="1.05" height="1.05" fill="none" stroke="#CCC" stroke-width="0.012"/>')
        parts.append(char(ch, x, y, cap_h, fill, part=2))
    vb_w = cols * cell
    vb_h = rows_n * cell
    inner = "".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-0.7 -0.7 {vb_w + 0.4:.2f} {vb_h + 0.4:.2f}" '
        f'width="780" height="{int(780 * vb_h / vb_w)}" role="img">{inner}</svg>'
    )


def glyph_mask(ch: str, n: int = 32, part: int = 2, box_w: float | None = None) -> list[list[int]]:
    """Rasterise one glyph from its analytic geometry on an n x n grid over the
    cap box (plus descender). Used by validate.py for confusable-pair tests."""
    global GEOM
    cap = 1.0
    prev, GEOM = GEOM, []
    try:
        char(ch, 0.0, 0.0, cap, "#000", part)
        geom = GEOM
    finally:
        GEOM = prev
    w = box_w if box_w else advance_sw(ch) / CAP_SW * cap
    xa, xb = -w / 2, w / 2
    ya, yb = -cap / 2, cap / 2 + cap * DESC_RATIO
    grid = []
    for j in range(n):
        y = ya + (j + 0.5) * (yb - ya) / n
        row = []
        for i in range(n):
            x = xa + (i + 0.5) * (xb - xa) / n
            row.append(1 if any(_hit(g, x, y) for g in geom) else 0)
        grid.append(row)
    return grid


def _hit(g: tuple, x: float, y: float) -> bool:
    kind = g[0]
    if kind == "rect":
        _, x0, y0, x1, y1 = g
        return x0 <= x <= x1 and y0 <= y <= y1
    if kind == "poly":
        pts = g[1]
        inside = False
        for k in range(len(pts)):
            (xa, ya), (xb, yb) = pts[k], pts[(k + 1) % len(pts)]
            if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya):
                inside = not inside
        return inside
    _, cx, cy, rx, ry, t, gc, gap = g
    dx, dy = x - cx, y - cy
    if rx <= 0 or ry <= 0:
        return False
    r = math.hypot(dx / rx, dy / ry)
    if r == 0:
        return False
    d = math.hypot(dx, dy)
    if abs(d - d / r) > t / 2:
        return False
    if gap <= 0:
        return True
    ang = math.degrees(math.atan2(dy / ry, dx / rx))
    diff = (ang - gc + 180.0) % 360.0 - 180.0
    return abs(diff) > gap / 2


def glyph_similarity(a: str, b: str, n: int = 32) -> float:
    """Intersection-over-union of two glyph masks (1.0 = identical ink)."""
    bw = max(advance_sw(a), advance_sw(b)) / CAP_SW
    ma, mb = glyph_mask(a, n, box_w=bw), glyph_mask(b, n, box_w=bw)
    inter = sum(p & q for ra, rb in zip(ma, mb) for p, q in zip(ra, rb))
    union = sum(p | q for ra, rb in zip(ma, mb) for p, q in zip(ra, rb))
    return inter / union if union else 1.0


CONFUSABLE = (("S", "5"), ("Z", "2"), ("O", "0"), ("I", "1"), ("&", "8"), ("&", "E"))
CONFUSABLE_MAX_IOU = 0.75
