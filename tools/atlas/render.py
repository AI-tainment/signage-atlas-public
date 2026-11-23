"""Procedural SVG faces: the only drawing code in the atlas.

Identification follows Know Your Traffic Signs / Highway Code plates
(Crown / OGL v3.0). Legends are Schedule 17 stand-in strokes. Seven-bar
digits are Part 5 VMS (MS4) only. Transport is not shipped.
Page refs in comments: "printed pN" (and a bare "pN") is the page number printed
on the SI page, the same in every copy. A "PDF pN" names its file: tsrgd2016.pdf
(refs/tsrgd2016.pdf, a local copy with an extra cover note, PDF = printed + 1), refs/si2016.pdf (the
legislation.gov.uk file, PDF = printed) or refs/si2002.pdf (PDF = printed).
site/assets/render.js is GENERATED from this module by render_js() (palette
and face URLs only, no drawers), so the two cannot drift. After a drawer change:

    python3 tools/rebuild.py --id 611.1
    python3 tools/rebuild.py --all
"""
from __future__ import annotations

import re
import math
from typing import Any

from atlas import lettering, traced

C = {
    "red": "#CC1A1A",
    "blue": "#005CA6",
    "white": "#F7F7F7",
    "black": "#141414",
    "grey": "#8C8E94",
    "amber": "#F29E14",
    "green": "#1EB838",
    "brown": "#73451F",
    "primary": "#0D7338",
    "motorway": "#00529E",
    "yellow": "#E6C200",
    "fluorescent_yellow": "#F5D000",
    "galv": "#9EA0A6",
    "cap": "#1F1F21",
}

TRI_W_OVER_H = 1.1317  # P500: W from height H

TALL = {"3000", "4003", "4002.1", "BELISHA", "4007", "823", "824", "825", "3014", "MARKER"}
PORTRAIT = {
    "674", "675", "675A", "811", "811A", "827.1", "816", "953.2",
    "777", "778",
}
WIDE = {
    "GANTRY_ADS", "MS4", "STREET_NAME", "2025", "2101", "2701", "2202",
    "2901", "2911", "2931", "958", "959", "960",
}


def _svg(w: int, h: float, inner: str, vb: str = "-1 -1 2 2") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
        f'width="{w}" height="{h}" role="img">{inner}</svg>'
    )


def _digit_vms(n: int, x: float, y: float, w: float, h: float, fill: str | None = None) -> str:
    """Schedule 17 Part 5 / MS4 seven-bar. Do not use on static plates."""
    segs = {
        0: "abcedf", 1: "bc", 2: "abged", 3: "abgcd", 4: "fgbc",
        5: "afgcd", 6: "afgecd", 7: "abc", 8: "abcdefg", 9: "abfgcd",
    }.get(int(n), "")
    ink = fill or C["black"]
    t = min(w, h) * 0.20
    rx = t * 0.32
    x0, x1 = x - w / 2, x + w / 2
    y0, y1, ym = y - h / 2, y + h / 2, y
    bars = {
        "a": (x0 + t, y0, x1 - t, y0 + t),
        "b": (x1 - t, y0 + t, x1, ym - t / 2),
        "c": (x1 - t, ym + t / 2, x1, y1 - t),
        "d": (x0 + t, y1 - t, x1 - t, y1),
        "e": (x0, ym + t / 2, x0 + t, y1 - t),
        "f": (x0, y0 + t, x0 + t, ym - t / 2),
        "g": (x0 + t, ym - t / 2, x1 - t, ym + t / 2),
    }
    out = []
    for k in segs:
        a, b, c, d = bars[k]
        out.append(
            f'<rect x="{a}" y="{b}" width="{c - a}" height="{d - b}" rx="{rx}" fill="{ink}"/>'
        )
    return "".join(out)


def _digit(n: int, x: float, y: float, w: float, h: float, fill: str | None = None) -> str:
    return lettering.word(str(int(n)), x, y, h, fill or C["black"], part=2)


def _mph_pair(n: int, y: float = 0, scale: float = 1, fill: str | None = None) -> str:
    return lettering.mph_pair(int(n), y=y, cap_h=0.373 * scale, fill=fill or C["black"], part=2)


def _disc(fill: str, r: float, extra: str = "") -> str:
    extra = f" {extra}" if extra else ""
    return f'<circle cx="0" cy="0" r="{r}" fill="{fill}"{extra}/>'


def _rim_disc(fill: str, r: float = 0.5, rim: str | None = None, rw: float = 0.02) -> str:
    """Filled disc with a thin outer rim (G4: white border 0.02D). No grey outline."""
    rim = rim or C["white"]
    return _disc(rim, r) + _disc(fill, r - rw)


def _ring_roundel() -> str:
    """G2 prohibitory: red ring 0.10D, white interior, no outer white rim, no grey."""
    return _disc(C["red"], 0.5) + _disc(C["white"], 0.40)


_SQRT3_2 = 0.8660254037844386


def _eq_pts(s: float, upright: bool, *, by_height: bool = True) -> list[tuple[float, float]]:
    """P500: size by height H, width = 1.1317 H. s is H when by_height (default)."""
    if by_height:
        h = s
        w = TRI_W_OVER_H * h
    else:
        h = s * _SQRT3_2
        w = s
    if upright:
        return [(0.0, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return [(0.0, h / 2), (w / 2, -h / 2), (-w / 2, -h / 2)]


def _centroid(pts: list[tuple[float, float]]) -> tuple[float, float]:
    return (sum(p[0] for p in pts) / 3.0, sum(p[1] for p in pts) / 3.0)


def _scale_about(
    pts: list[tuple[float, float]], k: float, origin: tuple[float, float] | None = None
) -> list[tuple[float, float]]:
    ox, oy = origin if origin is not None else _centroid(pts)
    return [((x - ox) * k + ox, (y - oy) * k + oy) for x, y in pts]


def _poly(fill: str, pts: list[tuple[float, float]], round_sw: float = 0.0) -> str:
    s = " ".join(f"{x:.4f},{y:.4f}" for x, y in pts)
    extra = (
        f' stroke="{fill}" stroke-width="{round_sw}" stroke-linejoin="round"'
        if round_sw
        else ""
    )
    return f'<polygon points="{s}" fill="{fill}"{extra}/>'


def _nested_tri(
    upright: bool,
    *,
    red_s: float = 0.92,
    white_k: float = 0.68,
    round_sw: float = 0.11,
    grey_k: float = 1.05,
    grey_sw: float = 0.05,
    white_round: float | None = None,
) -> str:
    """Warning / give-way triangle sized by height (P500). Border ~0.1H."""
    red = _eq_pts(red_s, upright, by_height=True)
    c = _centroid(red)
    wr = round_sw * 0.45 if white_round is None else white_round
    grey = _poly(C["grey"], _scale_about(red, grey_k, c), grey_sw) if grey_sw > 0 else ""
    return grey + _poly(C["red"], red, round_sw) + _poly(C["white"], _scale_about(red, white_k, c), wr)


def _upright_tri(fill: str, s: float, round_sw: float = 0.0) -> str:
    return _poly(fill, _eq_pts(s, True), round_sw)


def _inverted_tri(fill: str, s: float, round_sw: float = 0.0) -> str:
    return _poly(fill, _eq_pts(s, False), round_sw)


def _octagon(fill: str, r: float) -> str:
    pts = []
    for i in range(8):
        a = (math.pi / 8) + i * math.pi / 4
        pts.append(f"{math.cos(a) * r:.4f},{math.sin(a) * r:.4f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def _arrow(fill: str, r: float, deg: float, size: float) -> str:
    rad = deg * math.pi / 180
    tx = math.sin(rad) * r
    ty = -math.cos(rad) * r
    return (
        f'<g transform="translate({tx} {ty}) rotate({deg})">'
        f'<polygon points="0,{-size} {size * 0.55},{size * 0.45} {-size * 0.55},{size * 0.45}" fill="{fill}"/>'
        f"</g>"
    )


def _fat_arrow(fill: str, deg: float, length: float = 0.62, shaft_w: float = 0.16, head: float = 0.34) -> str:
    """0 deg = up. Official 610 is ~225 (down-left)."""
    hw = head * 1.32
    shaft_h = length - head * 0.55
    return (
        f'<g transform="rotate({deg})">'
        f'<rect x="{-shaft_w / 2}" y="{-length / 2 + head * 0.72}" '
        f'width="{shaft_w}" height="{shaft_h}" fill="{fill}"/>'
        f'<polygon points="0,{-length / 2} {hw / 2},{-length / 2 + head} '
        f'{-hw / 2},{-length / 2 + head}" fill="{fill}"/>'
        f"</g>"
    )


def _polar(deg: float, r: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return math.sin(rad) * r, -math.cos(rad) * r


def _ring_seg(fill: str, r_in: float, r_out: float, start: float, sweep: float) -> str:
    """Filled annular sector. 0 deg = up, positive sweep = clockwise."""
    x0o, y0o = _polar(start, r_out)
    x1o, y1o = _polar(start + sweep, r_out)
    x1i, y1i = _polar(start + sweep, r_in)
    x0i, y0i = _polar(start, r_in)
    large = 1 if abs(sweep) > 180 else 0
    sf = 1 if sweep > 0 else 0
    isf = 0 if sf else 1
    return (
        f'<path d="M {x0o:.4f} {y0o:.4f} A {r_out:.4f} {r_out:.4f} 0 {large} {sf} {x1o:.4f} {y1o:.4f} '
        f'L {x1i:.4f} {y1i:.4f} A {r_in:.4f} {r_in:.4f} 0 {large} {isf} {x0i:.4f} {y0i:.4f} Z" fill="{fill}"/>'
    )


def _arc_stroke(fill: str, r: float, start: float, sweep: float, sw: float) -> str:
    """Open circular arc with round caps. 0 deg = up, positive sweep = clockwise."""
    x0, y0 = _polar(start, r)
    x1, y1 = _polar(start + sweep, r)
    large = 1 if abs(sweep) > 180 else 0
    sf = 1 if sweep > 0 else 0
    return (
        f'<path d="M {x0:.4f} {y0:.4f} A {r:.4f} {r:.4f} 0 {large} {sf} {x1:.4f} {y1:.4f}" '
        f'fill="none" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round"/>'
    )


def _circ_arrow(fill: str, r: float, start: float, sweep: float, sw: float = 0.10, head: float = 0.13) -> str:
    """Clockwise curved arrow. 0 deg = up."""
    body = _arc_stroke(fill, r, start, sweep, sw)
    x1, y1 = _polar(start + sweep, r)
    hd = start + sweep + (90 if sweep > 0 else -90)
    dx, dy = math.sin(math.radians(hd)), -math.cos(math.radians(hd))
    px, py = -dy, dx
    tipx, tipy = x1 + dx * head * 0.92, y1 + dy * head * 0.92
    b1x = x1 - dx * head * 0.05 + px * head * 0.62
    b1y = y1 - dy * head * 0.05 + py * head * 0.62
    b2x = x1 - dx * head * 0.05 - px * head * 0.62
    b2y = y1 - dy * head * 0.05 - py * head * 0.62
    return body + f'<polygon points="{tipx:.4f},{tipy:.4f} {b1x:.4f},{b1y:.4f} {b2x:.4f},{b2y:.4f}" fill="{fill}"/>'


# r3: 611.1 arrow measured on SI 2016 Sch 9 Pt 2 (printed p139 = tsrgd2016.pdf PDF p140) by radial sampling, D = 1:
# shaft r 0.284..0.342 from 16 deg to the notch at 84 deg; notched chevron head with barbs at
# r 0.213 / 0.404 (72-73 deg) and the tip at 105.5 deg, r 0.345. (angle, r) pairs, 0 = up, clockwise.
_MINI_HEAD = [(105.5, 0.345), (102, 0.349), (98, 0.357), (94, 0.368), (90, 0.385), (86, 0.404),
              (73, 0.404), (84, 0.343), (84, 0.285), (71.5, 0.213), (86, 0.213), (90, 0.219),
              (94, 0.227), (96, 0.243), (98, 0.263), (100, 0.285), (102, 0.31), (104, 0.34)]


def _mini_arrow(fill: str, rot: float) -> str:
    ri, ro, a0, a1 = 0.284, 0.342, 16 + rot, 84.5 + rot
    p0, p1, p2, p3 = _polar(a0, ro), _polar(a1, ro), _polar(a1, ri), _polar(a0, ri)
    shaft = (f'<path d="M {p0[0]:.4f} {p0[1]:.4f} A {ro} {ro} 0 0 1 {p1[0]:.4f} {p1[1]:.4f} '
             f'L {p2[0]:.4f} {p2[1]:.4f} A {ri} {ri} 0 0 0 {p3[0]:.4f} {p3[1]:.4f} Z" fill="{fill}"/>')
    pts = " ".join(f"{x:.4f},{y:.4f}" for x, y in (_polar(a + rot, r) for a, r in _MINI_HEAD))
    return shaft + f'<polygon points="{pts}" fill="{fill}"/>'


def _chequer_board(w: float = 1.0, h: float = 2 / 3, band: float = 0.087, nx: int = 7, ny: int = 5) -> str:
    """White board with a red/white chequer border band (red at the corners)."""
    x0, y0 = -w / 2, -h / 2
    out = [_rect(C["white"], x0, y0, -x0, -y0)]
    sx, sy = w / nx, h / ny
    for i in range(0, nx, 2):
        out.append(_rect(C["red"], round(x0 + i * sx, 4), round(y0, 4), round(x0 + (i + 1) * sx, 4), round(y0 + band, 4)))
        out.append(_rect(C["red"], round(x0 + i * sx, 4), round(-y0 - band, 4), round(x0 + (i + 1) * sx, 4), round(-y0, 4)))
    for j in range(0, ny, 2):
        out.append(_rect(C["red"], round(x0, 4), round(y0 + j * sy, 4), round(x0 + band, 4), round(y0 + (j + 1) * sy, 4)))
        out.append(_rect(C["red"], round(-x0 - band, 4), round(y0 + j * sy, 4), round(-x0, 4), round(y0 + (j + 1) * sy, 4)))
    return "".join(out)


def _bw_plate(w: float, h: float, text: str, cap: float, cy: float, narrow: float) -> str:
    """White supplementary plate with a thick (0.097 H) rounded black frame and one black line."""
    f = round(0.097 * h, 4)
    return (
        _rect(C["black"], -w / 2, -h / 2, w / 2, h / 2, rx=round(0.16 * h, 4))
        + _rect(C["white"], round(-w / 2 + f, 4), round(-h / 2 + f, 4), round(w / 2 - f, 4), round(h / 2 - f, 4), rx=round(0.07 * h, 4))
        + lettering.word(text, 0, round(cy, 4), cap, C["black"], tracking_sw=0.5, part=1, narrow=narrow)
    )


def _fit_word(text: str, cx: float, top: float, cap: float, width: float, fill: str) -> str:
    """Word with cap height `cap` (top of caps at `top`) narrowed to the measured line width."""
    nat = lettering.measure(text, cap, 0.5)
    return lettering.word(text, cx, round(top + cap / 2, 4), cap, fill, tracking_sw=0.5, part=1,
                          narrow=round(min(1.0, width / nat), 3))


def _sign646() -> str:
    h = 0.66
    w = round(1.549 * h, 4)
    x0, y0 = -w / 2, -h / 2
    X = lambda f: round(x0 + f * w, 4)
    Y = lambda f: round(y0 + f * h, 4)
    split = X(0.520)
    out = (
        _rect(C["black"], X(0), Y(0), X(1), Y(1), rx=0.025)
        + _rect(C["yellow"], X(0.0176), Y(0.027), X(0.9824), Y(0.609))
        + _rect(C["white"], X(0.0176), Y(0.637), split, Y(0.973))
        + f'<g transform="translate({X(0.135)} {Y(0.209)}) scale({round(0.147 * w, 4)})">'
        + _disc(C["red"], 0.5) + _disc(C["blue"], 0.40) + _slash(0.10, -45) + _slash(0.10, 45)
        + "</g>"
        + _fit_word("URBAN", X(0.588), Y(0.079), round(0.115 * h, 4), round(0.373 * w, 4), C["black"])
        + _fit_word("CLEARWAY", X(0.588), Y(0.265), round(0.115 * h, 4), round(0.597 * w, 4), C["black"])
        + _fit_word("Monday to Friday", X(0.588), Y(0.464), round(0.088 * h, 4), round(0.688 * w, 4), C["black"])
        + _fit_word("am", X(0.262), Y(0.699) - round((0.085 / 0.72 - 0.085) * h, 4), round(0.085 / 0.72 * h, 4), round(0.136 * w, 4), C["black"])
        + _fit_word("8.00 - 9.30", X(0.269), Y(0.852), round(0.093 * h, 4), round(0.40 * w, 4), C["black"])
        + _fit_word("pm", X(0.761), Y(0.699) - round((0.085 / 0.72 - 0.085) * h, 4), round(0.085 / 0.72 * h, 4), round(0.13 * w, 4), C["white"])
        + _fit_word("4.30 - 6.30", X(0.751), Y(0.85), round(0.093 * h, 4), round(0.40 * w, 4), C["white"])
    )
    return out


def _sign6262a() -> str:
    w = 0.5498
    X = lambda f: round(-w / 2 + f * w, 4)
    Y = lambda f: round(-0.5 + f * w, 4)
    k = lambda f: round(f * w, 4)
    return (
        _rect(C["black"], X(0), Y(0), X(1), Y(1.819), rx=0.02)
        + _rect(C["white"], X(0.021), Y(0.021), X(0.979), Y(0.536))
        + _rect(C["grey"], X(0.021), Y(0.557), X(0.979), Y(1.449))
        + _rect(C["white"], X(0.021), Y(1.47), X(0.979), Y(1.798))
        + f'<circle cx="0" cy="{Y(1.005)}" r="{k(0.348)}" fill="{C["white"]}" stroke="{C["red"]}" stroke-width="{k(0.076)}"/>'
        + _fit_word("WEAK", 0, Y(0.105), k(0.145), k(0.605), C["black"])
        + _fit_word("BRIDGE", 0, Y(0.31), k(0.145), k(0.79), C["black"])
        + _fit_word("18", X(0.429), Y(0.828), k(0.217), k(0.304), C["black"])
        + _fit_word("t", X(0.687), Y(0.828), k(0.163), k(0.078), C["black"])
        + _fit_word("mgw", 0, Y(1.12) - k(0.074 / 0.72 - 0.074), k(0.074 / 0.72), k(0.386), C["black"])
        + _fit_word("Except empty", 0, Y(1.518), k(0.088), k(0.832), C["black"])
        + _fit_word("vehicles", 0, Y(1.645), k(0.088), k(0.485), C["black"])
    )



def _plate(key: str) -> str:
    """r6: plate traced from its TSRGD diagram (atlas/traced.py PLATES); legends are stand-in lettering."""
    P = traced.PLATES[key]
    w, h = P["w"], P["h"]
    fill = C[P["plate"]] if P["plate"] else "none"  # None: shaped plate, the first traced layer is the silhouette
    out = _rect(fill, round(-w / 2, 4), round(-h / 2, 4), round(w / 2, 4), round(h / 2, 4), rx=P["rx"])
    for fill, k in P["layers"]:
        out += traced.path(k, C[fill])
    return out + _plate_legend(P)


def _plate_legend(P: dict) -> str:
    """Measured legend lines, then any traced layer that must sit over them (e.g. 675A end stripes)."""
    out = ""
    for text, cx, cy, cap, nar, fill, part in P["text"]:
        out += lettering.word(text, cx, cy, cap, C[fill], tracking_sw=0.5, part=part, narrow=nar)
    for fill, k in P.get("over", []):
        out += traced.path(k, C[fill])
    return out


def _traced_inner(key: str) -> str:
    """Traced symbol layers and legend only, for faces whose outline is drawn by a shared helper (_warn)."""
    P = traced.PLATES[key]
    return "".join(traced.path(k, C[fill]) for fill, k in P["layers"]) + _plate_legend(P)


def _sign660() -> str:
    h = 0.6
    w = round(1.896 * h, 4)
    X = lambda f: round(-w / 2 + f * w, 4)
    Y = lambda f: round(-h / 2 + f * h, 4)
    b = round(0.025 * w, 4)
    cap = round(0.183 * h, 4)
    def line(t: str, x0: float, x1: float, base: float) -> str:
        return _fit_word(t, round((X(x0) + X(x1)) / 2, 4), Y(base - 0.183), cap, round((x1 - x0) * w, 4), C["black"])
    return (
        _rect(C["black"], X(0), Y(0), X(1), Y(1), rx=round(0.06 * h, 4))
        + _rect(C["white"], round(X(0) + b, 4), round(Y(0) + b, 4), round(X(1) - b, 4), round(Y(1) - b, 4), rx=round(0.04 * h, 4))
        + _rect(C["blue"], X(0.069), Y(0.174), X(0.408), Y(0.817), rx=round(0.02 * h, 4))
        + lettering.word("P", X(0.2385), Y(0.4955), round(0.54 * h, 4), C["white"], tracking_sw=0.5, part=1)
        + line("Permit", 0.472, 0.913, 0.322)
        + line("holders", 0.468, 0.931, 0.583)
        + line("only", 0.55, 0.826, 0.843)
    )

def _rect(fill: str, x0: float, y0: float, x1: float, y1: float, rx: float = 0) -> str:
    extra = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{fill}"{extra}/>'


def _capsule(fill: str, cx: float, cy: float, thickness: float, length: float, rot: float = 0) -> str:
    """Stadium bar. rot=0 is vertical (along +y)."""
    rx = thickness / 2
    return (
        f'<g transform="translate({cx} {cy}) rotate({rot})">'
        f'<rect x="{-rx}" y="{-length / 2}" width="{thickness}" height="{length}" rx="{rx}" fill="{fill}"/>'
        f"</g>"
    )


def _fig(
    fill: str,
    x: float,
    y: float,
    h: float,
    *,
    child: bool = False,
    walk: bool = False,
    skirt: bool = False,
    hold: str | None = None,
    hand: tuple[float, float] | None = None,
    side: bool = False,
    run: bool = False,
    bulk: bool = False,
    lean: float = 0,
) -> str:
    """Solid pedestrian silhouette. y is figure centre. hold is 'L' or 'R'.
    hand is an optional local (x, y) for the holding hand.
    side=True draws a profile figure facing +x (Highway Code 545)."""
    hr = h * (0.132 if child else 0.110)
    tw = h * (0.148 if child else 0.118)
    if bulk:
        tw = h * (0.20 if child else 0.175)
    arm_t = h * 0.062
    leg_t = h * (0.090 if child else 0.082)
    rot = lean if lean else (18 if (side and run) else (8 if side else 0))
    out = [f'<g transform="translate({x} {y}) rotate({rot})">']

    def _arm_to(hx: float, hy: float, sx: float | None = None, sy: float | None = None) -> str:
        if sx is None:
            sx = tw * (0.9 if hx >= 0 else -0.9)
        if sy is None:
            sy = -h * 0.18
        mx, my = (sx + hx) / 2, (sy + hy) / 2
        length = math.hypot(hx - sx, hy - sy)
        ang = math.degrees(math.atan2(-(hx - sx), hy - sy))
        return _capsule(fill, mx, my, arm_t * 1.15, max(length, h * 0.14), ang)

    if side:
        # Profile, facing right — DfT 545 children going to or from school.
        out.append(f'<circle cx="{h * 0.06}" cy="{-h * 0.38}" r="{hr}" fill="{fill}"/>')
        out.append(
            f'<rect x="{-tw * 0.45}" y="{-h * 0.26}" width="{tw * 2.05}" height="{h * 0.40}" '
            f'rx="{tw * 0.55}" fill="{fill}"/>'
        )
        if run:
            out.append(_capsule(fill, -h * 0.11, h * 0.26, leg_t, h * 0.38, 42))
            out.append(_capsule(fill, h * 0.13, h * 0.22, leg_t, h * 0.36, -30))
        else:
            out.append(_capsule(fill, -h * 0.06, h * 0.26, leg_t, h * 0.36, 22))
            out.append(_capsule(fill, h * 0.11, h * 0.24, leg_t, h * 0.34, -18))
        if hand is not None or hold in ("L", "R"):
            if hand is not None:
                hx, hy = hand
            elif hold == "R":
                hx, hy = h * 0.42, -h * 0.06
            else:
                hx, hy = -h * 0.12, -h * 0.04
            out.append(_arm_to(hx, hy, sx=h * 0.10, sy=-h * 0.16))
            out.append(_capsule(fill, -h * 0.10, -h * 0.02, arm_t, h * 0.22, 36))
        else:
            out.append(_capsule(fill, h * 0.14, -h * 0.06, arm_t, h * 0.22, -40))
            out.append(_capsule(fill, -h * 0.10, -h * 0.02, arm_t, h * 0.22, 36))
        out.append("</g>")
        return "".join(out)

    out.append(f'<circle cx="0" cy="{-h * 0.38}" r="{hr}" fill="{fill}"/>')
    out.append(
        f'<rect x="{-tw}" y="{-h * 0.26}" width="{tw * 2}" height="{h * 0.32}" rx="{tw * 0.55}" fill="{fill}"/>'
    )
    if skirt:
        out.append(
            f'<polygon points="{-tw * 0.90},{-h * 0.00} {tw * 0.90},{-h * 0.00} '
            f'{tw * 1.65},{h * 0.24} {-tw * 1.65},{h * 0.24}" fill="{fill}"/>'
        )
        out.append(_capsule(fill, -h * 0.055, h * 0.32, leg_t * 0.80, h * 0.16, -6))
        out.append(_capsule(fill, h * 0.065, h * 0.32, leg_t * 0.80, h * 0.16, 8))
    elif walk:
        out.append(_capsule(fill, -h * 0.025, h * 0.25, leg_t, h * 0.36, 6))
        out.append(_capsule(fill, h * 0.08, h * 0.24, leg_t, h * 0.34, -18))
    else:
        out.append(_capsule(fill, -h * 0.06, h * 0.24, leg_t, h * 0.38, 4))
        out.append(_capsule(fill, h * 0.06, h * 0.24, leg_t, h * 0.38, -4))

    if hand is not None or hold in ("L", "R"):
        if hand is not None:
            hx, hy = hand
        elif hold == "R":
            hx, hy = h * 0.40, -h * 0.08
        else:
            hx, hy = -h * 0.40, -h * 0.04
        out.append(_arm_to(hx, hy))
        fx = -tw * 1.05 if hx >= 0 else tw * 1.05
        out.append(_capsule(fill, fx, h * 0.00, arm_t * 0.70, h * 0.18, -8 if fx > 0 else 8))
    elif walk:
        out.append(_capsule(fill, h * 0.10, -h * 0.04, arm_t, h * 0.24, -32))
        out.append(_capsule(fill, -h * 0.10, -h * 0.02, arm_t, h * 0.22, 28))
    else:
        out.append(_capsule(fill, -tw * 0.95, h * 0.00, arm_t * 0.62, h * 0.20, 8))
        out.append(_capsule(fill, tw * 0.95, h * 0.00, arm_t * 0.62, h * 0.20, -8))
    out.append("</g>")
    return "".join(out)


def _person(fill: str, x: float, y: float, h: float, child: bool = False) -> str:
    return _fig(fill, x, y, h, child=child)


def _stick(fill: str, x: float, y: float, h: float) -> str:
    return _fig(fill, x, y, h)


def _chevron(fill: str, hx: float, hy: float) -> str:
    return (
        f'<polygon points="{hx * 0.78},0 {hx * 0.28},{hy * 0.55} {hx * 0.28},{-hy * 0.55}" fill="{fill}"/>'
        + _rect(fill, -hx * 0.55, -hy * 0.18, hx * 0.32, hy * 0.18)
    )


def _letter_w(ch: str, h: float) -> float:
    return lettering.advance_sw(ch) / lettering.CAP_SW * h


def _letter(
    ch: str, cx: float, cy: float, w: float, h: float, fill: str, weight: float = 1.0
) -> str:
    """Schedule 17 stand-in. weight 1.2 ≈ Part 1 (light on dark)."""
    part = 1 if weight >= 1.2 else 2
    return lettering.word(ch, cx, cy, h, fill, part=part)


def _word(
    text: str,
    cx: float,
    cy: float,
    h: float,
    fill: str,
    tracking: float | None = None,
    weight: float = 1.0,
) -> str:
    part = 1 if weight >= 1.2 else 2
    tracking_sw = 1.1 if tracking is None else max(tracking / (h / lettering.CAP_SW), 0.2)
    return lettering.word(text, cx, cy, h, fill, tracking_sw=tracking_sw, part=part)


def _word_fit(
    text: str,
    cx: float,
    cy: float,
    fill: str,
    max_w: float,
    max_h: float,
    tracking_sw: float = 1.1,
    weight: float = 1.0,
    narrow: float = 1.0,
) -> str:
    """One x-height for the string, shrunk uniformly to fit max_w."""
    prev, lettering.NARROW = lettering.NARROW, narrow
    try:
        h = lettering.fit_cap_h(text, max_w, tracking_sw=tracking_sw, max_h=max_h)
    finally:
        lettering.NARROW = prev
    part = 1 if weight >= 1.2 else 2
    return lettering.word(text, cx, cy, h, fill, tracking_sw=tracking_sw, part=part, narrow=narrow)


def _legend_lines(
    lines: list[tuple[str, float]],
    fill: str,
    max_w: float,
    max_h: float,
    tracking_sw: float = 0.9,
    weight: float = 1.0,
) -> str:
    """Several lines, one shared x-height, each centred."""
    h = max_h
    for text, _cy in lines:
        h = min(h, lettering.fit_cap_h(text, max_w, tracking_sw=tracking_sw, max_h=max_h))
    part = 1 if weight >= 1.2 else 2
    return "".join(
        lettering.word(text, 0.0, cy, h, fill, tracking_sw=tracking_sw, part=part)
        for text, cy in lines
    )


# P500: overall height H (outer edge of the rounded red stroke), border B = H/10
# measured perpendicular to each side. The red polygon (height 0.92) is stroked
# 0.138 wide (outer +0.069) and the white one 0.0621 (outer +0.031), so k is solved
# for B = 0.10 H on the mean side instead of guessed (k=0.70 gave 0.12 H).
WARN_RED_H = 0.92
WARN_RED_SW = 0.138
WARN_WHITE_SW = WARN_RED_SW * 0.45


def _tri_side_dists(pts: list[tuple[float, float]]) -> list[float]:
    c = _centroid(pts)
    out = []
    for i in range(3):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % 3]
        ex, ey = xb - xa, yb - ya
        L = math.hypot(ex, ey)
        out.append(abs((c[0] - xa) * -ey / L + (c[1] - ya) * ex / L))
    return out


def warn_border_ratio(k: float) -> list[float]:
    """Perpendicular border / overall height, per side, for white scale k."""
    red = _eq_pts(WARN_RED_H, True)
    h_out = WARN_RED_H + WARN_RED_SW
    return [((d + WARN_RED_SW / 2) - (k * d + WARN_WHITE_SW / 2)) / h_out for d in _tri_side_dists(red)]


def _solve_warn_k(target: float = 0.10) -> float:
    red = _eq_pts(WARN_RED_H, True)
    h_out = WARN_RED_H + WARN_RED_SW
    ds = _tri_side_dists(red)
    d = sum(ds) / len(ds)
    return round((d + WARN_RED_SW / 2 - WARN_WHITE_SW / 2 - target * h_out) / d, 4)


WARN_K = _solve_warn_k()
# r3: 602 border measured 0.105 H on SI 2016 Sch 9 Pt 2 item 2 (was white_k 0.71 = 0.15 H).
GIVEWAY_K = _solve_warn_k(0.105)



def _legend_stack(lines: list[str], cy: float, cap: float, max_w: float) -> str:
    """Centred lines (first larger), shrunk to fit max_w. Pitch 1.55 cap."""
    caps = [cap] + [cap * 0.8] * (len(lines) - 1)
    for i, t in enumerate(lines):
        w = lettering.ink_box(t, 0, 0, caps[i], 0.6)[2] - lettering.ink_box(t, 0, 0, caps[i], 0.6)[0]
        if w > max_w:
            caps[i] *= max_w / w
    pitch = [c * 1.6 for c in caps]
    total = sum(caps) + sum(pitch[:-1]) - sum(caps[:-1])
    y = cy - total / 2 + caps[0] / 2
    out = ""
    for i, t in enumerate(lines):
        out += lettering.word(t, 0, y, caps[i], C["black"], tracking_sw=0.6, part=2)
        if i + 1 < len(lines):
            y += caps[i] / 2 + (pitch[i] - caps[i]) + caps[i + 1] / 2
    return out


def _limit_roundel(lines: list[str], vertical: bool) -> str:
    """629-family limit roundel: arrows at the limit edges, legend between (r2)."""
    k = C["black"]
    if vertical:
        arrows = (f'<polygon points="0,-0.24 0.06,-0.33 -0.06,-0.33" fill="{k}"/>'
                  f'<polygon points="0,0.24 0.06,0.33 -0.06,0.33" fill="{k}"/>')
        body = _legend_stack(lines, 0.0, 0.13, 0.56)
    else:
        arrows = (f'<polygon points="-0.27,0 -0.36,0.06 -0.36,-0.06" fill="{k}"/>'
                  f'<polygon points="0.27,0 0.36,0.06 0.36,-0.06" fill="{k}"/>')
        body = _legend_stack(lines, 0.0, 0.11, 0.46)
    return _ring_roundel() + arrows + body


def _headroom_tri(lines: list[str], lower_arrow: bool) -> str:
    """530-family headroom triangle (r3, per the SI diagrams).

    Large downward arrow above the legend; 530 (SI 2002 Sch 1) also has a small
    upward arrow below it, 530A (SI 2016 Sch 2 Pt 4 item 2) does not."""
    k = C["black"]
    cy = 0.16 if len(lines) == 1 else 0.17
    low = f'<polygon points="0,0.31 -0.035,0.37 0.035,0.37" fill="{k}"/>' if lower_arrow else ""
    return (
        _warn()
        + f'<polygon points="0,0.02 -0.075,-0.10 0.075,-0.10" fill="{k}"/>'
        + low
        + _legend_stack(lines, cy, 0.10 if len(lines) == 1 else 0.075, 0.42 if len(lines) == 1 else 0.36)
    )

# --- legend fields (S2): where a legend may sit, per glyph -------------------
# Shapes: ("poly", pts, grow) grow = outward stroke half-width on the field;
# ("circle", cx, cy, r); ("rect", x0, y0, x1, y1).

def _warn_white_pts() -> list[tuple[float, float]]:
    red = _eq_pts(WARN_RED_H, True, by_height=True)
    return _scale_about(red, WARN_K, _centroid(red))


WARN_FIELD = ("poly", _warn_white_pts(), WARN_WHITE_SW / 2)
RING_FIELD = ("circle", 0.0, 0.0, 0.40)
BLUE_DISC_FIELD = ("circle", 0.0, 0.0, 0.48)


def _octagon_pts(r: float) -> list[tuple[float, float]]:
    return [
        (math.cos(math.pi / 8 + i * math.pi / 4) * r, math.sin(math.pi / 8 + i * math.pi / 4) * r)
        for i in range(8)
    ]


def _poly_halfwidth(pts: list[tuple[float, float]], y: float) -> tuple[float, float] | None:
    xs = []
    n = len(pts)
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        if (ya - y) * (yb - y) <= 0 and ya != yb:
            xs.append(xa + (y - ya) * (xb - xa) / (yb - ya))
    if len(xs) < 2:
        return None
    return min(xs), max(xs)


def _pt_clearance(shape: tuple, x: float, y: float) -> float:
    """Signed distance from (x, y) to the field edge (positive = inside)."""
    kind = shape[0]
    if kind == "circle":
        _, cx, cy, r = shape
        return r - math.hypot(x - cx, y - cy)
    if kind == "rect":
        _, x0, y0, x1, y1 = shape
        return min(x - x0, x1 - x, y - y0, y1 - y)
    _, pts, grow = shape
    # convex polygon, either winding
    n = len(pts)
    sx = sum(p[0] for p in pts) / n
    sy = sum(p[1] for p in pts) / n
    best = float("inf")
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        ex, ey = xb - xa, yb - ya
        L = math.hypot(ex, ey)
        nx, ny = -ey / L, ex / L
        if (sx - xa) * nx + (sy - ya) * ny < 0:
            nx, ny = -nx, -ny
        best = min(best, (x - xa) * nx + (y - ya) * ny)
    return best + grow


def _shape_contains(shape: tuple, x: float, y: float) -> bool:
    return _pt_clearance(shape, x, y) >= 0


def _shape_area(shape: tuple) -> float:
    if shape[0] == "circle":
        return math.pi * shape[3] ** 2
    if shape[0] == "rect":
        return (shape[3] - shape[1]) * (shape[4] - shape[2])
    pts = shape[1]
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
                   for i in range(len(pts)))) / 2


_ROUND = set("0368OQCGSceos9%")


def _word_sample_points(text: str, x0: float, y0: float, x1: float, y1: float, cap_h: float,
                        tracking_sw: float) -> list[tuple[float, float]]:
    """Per-character ink samples: box corners, or an inscribed ellipse for round forms."""
    sw = cap_h / lettering.CAP_SW
    gap = tracking_sw * sw
    # Recover the advance scale (lettering.NARROW) the word was set with from its logged width.
    raw = sum(lettering.ADVANCE.get(ch, lettering.ADVANCE["default"]) for ch in text) * sw
    k = ((x1 - x0) - gap * max(len(text) - 1, 0)) / raw if raw else 1.0
    widths = [lettering.ADVANCE.get(ch, lettering.ADVANCE["default"]) * sw * k for ch in text]
    x = x0
    pts: list[tuple[float, float]] = []
    top = y0
    base = y0 + cap_h
    for ch, w in zip(text, widths):
        if ch != " ":
            cy0 = top
            cy1 = base + (cap_h * lettering.DESC_RATIO if ch in "gjpqy" else 0.0)
            if ch.islower() and ch not in "bdfhklt":
                cy0 = base - cap_h * lettering.X_RATIO
            if ch == ".":
                cy0 = base - sw
            if ch == "-":
                cy0, cy1 = (top + base) / 2 - sw / 2, (top + base) / 2 + sw / 2
            if ch in "!Iil1":
                tt = cap_h / lettering.CAP_SW * 1.2
                pts += [(x + w / 2 - tt / 2, cy0), (x + w / 2 + tt / 2, cy0), (x + w / 2 - tt / 2, cy1), (x + w / 2 + tt / 2, cy1)]
            elif ch in _ROUND:
                cx, cy, rx, ry = x + w / 2, (cy0 + cy1) / 2, w / 2, (cy1 - cy0) / 2
                pts += [(cx + rx * math.cos(a * math.pi / 12), cy + ry * math.sin(a * math.pi / 12)) for a in range(24)]
            else:
                pts += [(x, cy0), (x + w, cy0), (x, cy1), (x + w, cy1)]
        x += w + gap
    return pts


# Minimum clearance in stroke widths. Speed numerals follow P670 (0.373D tall),
# which leaves less than 1 sw to the ring; everything else needs >= 1 sw.
LEGEND_MIN_CLEAR_SW = {"670": 0.3, "672": 0.3, "673": 0.3,
                       # r3: SI 2016 Sch 9 Pt 2 item 1 sets STOP ~0.8 sw from the red edge.
                       "601.1": 0.7,
                       # r4: 626.2A "t" sits close to the ring as measured on SI 2016 printed p141 (box sampling of a lowercase t).
                       "626.2A": 0.7,
                       # r6: SI 2002 diagram 2717 (p275) sets the W of "A303W" ~0.6 sw from the panel edge.
                       "MARKER": 0.55,
                       # r7: SI 2002 diagram 660 (p100) sets the white P ~0.5 sw from the edge of its square.
                       "660": 0.5,
                       # r3: 602 positions as SI 2016 Sch 9 Pt 2 item 2; the box samples of
                       # the slanted V/W/A/Y over-state the ink near the sloping edges.
                       "602": 0.3}
LEGEND_FIELDS: dict[str, list[tuple]] = {}


def legend_fit(code: str, param: int | None = None) -> list[str]:
    """Return one message per legend word that leaves its field (empty list = fits)."""
    fields = LEGEND_FIELDS.get(code)
    log = legend_log(code, param)
    if not log:
        return []
    if not fields:
        return [f"{code}: legend {[w[0] for w in log]} has no declared field (LEGEND_FIELDS)"]
    out = []
    need = LEGEND_MIN_CLEAR_SW.get(code, 1.0)
    for text, x0, y0, x1, y1, cap_h, tracking_sw in log:
        cx, cy = (x0 + x1) / 2, y0 + cap_h / 2
        inside = [f for f in fields if _shape_contains(f, cx, cy)]
        if not inside:
            out.append(f"{code}: legend {text!r} centre is outside every field")
            continue
        field = min(inside, key=_shape_area)
        sw = cap_h / lettering.CAP_SW
        clear = min(_pt_clearance(field, x, y) for x, y in _word_sample_points(text, x0, y0, x1, y1, cap_h, tracking_sw))
        if clear < need * sw - 1e-6:
            out.append(f"{code}: legend {text!r} clearance {clear / sw:.2f} sw < {need:.2f} sw")
    return out


def _fit_warn_lines(lines: list[str], fill: str, *, max_h: float, bottom_pad_sw: float = 1.6,
                    tracking_sw: float = 1.0, lead: float = 1.55) -> str:
    """Set lines inside the warning triangle's white field: one cap height for all
    lines, the largest that keeps >= 1.5 sw clearance; block sits on the base."""
    _, pts, grow = WARN_FIELD
    base_y = max(p[1] for p in pts) + grow
    h = max_h
    while h > 0.02:
        sw = h / lettering.CAP_SW
        y = base_y - bottom_pad_sw * sw
        placed = []
        ok = True
        for text in reversed(lines):
            desc = h * lettering.DESC_RATIO if any(c in "gjpqy" for c in text) else 0.0
            cy = y - desc - h / 2
            x0, y0, x1, y1 = lettering.ink_box(text, 0.0, cy, h, tracking_sw)
            samples = _word_sample_points(text, x0, y0, x1, y1, h, tracking_sw)
            if min(_pt_clearance(WARN_FIELD, sx, sy) for sx, sy in samples) < 1.5 * sw:
                ok = False
                break
            placed.append((text, cy))
            y = cy - h / 2 - (lead - 1.0) * h
        if ok:
            return "".join(lettering.word(t, 0.0, cy, h, fill, tracking_sw=tracking_sw, part=2) for t, cy in placed)
        h -= 0.002
    raise ValueError(f"legend {lines!r} does not fit the warning triangle")




def _warn() -> str:
    return _nested_tri(True, red_s=WARN_RED_H, white_k=WARN_K, round_sw=WARN_RED_SW, grey_k=1.0, grey_sw=0.0)


def _lightning() -> str:
    coil = (
        f'<rect x="-0.045" y="-0.32" width="0.09" height="0.14" rx="0.02" fill="{C["black"]}"/>'
        + "".join(
            f'<rect x="-0.055" y="{-0.30 + i * 0.022}" width="0.11" height="0.010" fill="{C["white"]}"/>'
            for i in range(5)
        )
    )
    bolt = (
        f'<polygon points="-0.02,-0.16 0.12,-0.16 0.00,0.00 0.10,0.00 '
        f'-0.12,0.28 0.02,0.06 -0.10,0.06" fill="{C["black"]}"/>'
    )
    return coil + bolt


def _arch_bridge() -> str:
    hump = (
        f'<path d="M -0.32,0.20 L -0.32,0.06 Q -0.22,-0.20 0,-0.20 Q 0.22,-0.20 0.32,0.06 L 0.32,0.20 Z" '
        f'fill="{C["black"]}"/>'
    )
    slabs = _rect(C["black"], -0.34, 0.06, -0.12, 0.20) + _rect(C["black"], 0.12, 0.06, 0.34, 0.20)
    hole = f'<path d="M -0.11,0.20 Q -0.11,0.00 0,0.00 Q 0.11,0.00 0.11,0.20 Z" fill="{C["white"]}"/>'
    return hump + slabs + hole


def _bus(cx: float, cy: float, w: float, h: float, body: str | None = None, detail: str | None = None) -> str:
    body = body or C["white"]
    detail = detail or C["blue"]
    x0, y0 = cx - w / 2, cy - h / 2
    windows = ""
    for i in range(5):
        windows += _rect(
            detail,
            x0 + w * 0.26 + i * w * 0.13,
            y0 + h * 0.18,
            x0 + w * 0.36 + i * w * 0.13,
            y0 + h * 0.52,
            rx=0.012,
        )
    return (
        _rect(body, x0, y0, x0 + w, y0 + h * 0.90, rx=h * 0.16)
        + _rect(detail, x0 + w * 0.06, y0 + h * 0.16, x0 + w * 0.20, y0 + h * 0.82, rx=0.01)
        + windows
    )


def _cycle(cx: float, cy: float, s: float, ink: str | None = None) -> str:
    ink = ink or C["white"]
    wr = s * 0.24
    sw = s * 0.055
    return (
        f'<circle cx="{cx - s * 0.36}" cy="{cy + s * 0.14}" r="{wr}" fill="none" stroke="{ink}" stroke-width="{sw}"/>'
        f'<circle cx="{cx + s * 0.36}" cy="{cy + s * 0.14}" r="{wr}" fill="none" stroke="{ink}" stroke-width="{sw}"/>'
        f'<path d="M {cx - s * 0.36} {cy + s * 0.14} L {cx - s * 0.04} {cy + s * 0.14} '
        f'L {cx + s * 0.16} {cy - s * 0.18} L {cx - s * 0.10} {cy - s * 0.18} Z '
        f'M {cx - s * 0.04} {cy + s * 0.14} L {cx - s * 0.10} {cy - s * 0.18}" '
        f'fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>'
        f'<rect x="{cx + s * 0.06}" y="{cy - s * 0.24}" width="{s * 0.22}" height="{s * 0.045}" fill="{ink}"/>'
        f'<rect x="{cx - s * 0.16}" y="{cy - s * 0.22}" width="{s * 0.10}" height="{s * 0.04}" fill="{ink}"/>'
    )


def _slash(sw: float = 0.11, rot: float = -45) -> str:
    return (
        f'<g transform="rotate({rot})">'
        f'<rect x="-0.46" y="{-sw / 2}" width="0.92" height="{sw}" fill="{C["red"]}"/>'
        f"</g>"
    )


def _proh(inner: str = "", *, slash: bool = False, slash_rot: float = -45) -> str:
    out = _ring_roundel() + inner
    return out + (_slash(rot=slash_rot) if slash else "")


def _mand(inner: str) -> str:
    return _rim_disc(C["blue"], 0.5, rw=0.02) + inner


def _stk(x0: float, y0: float, x1: float, y1: float, w: float, fill: str | None = None) -> str:
    fill = fill or C["black"]
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    length = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(-(x1 - x0), y1 - y0))
    return _capsule(fill, mx, my, w, length, ang)


def _plan(d: str, w: float = 0.14, fill: str | None = None) -> str:
    """Thick plan-view road (Highway Code warning interiors)."""
    fill = fill or C["black"]
    return (
        f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" '
        f'stroke-linecap="butt" stroke-linejoin="miter"/>'
    )


def _elbow(fill: str, *, left: bool = True, sw: float = 0.15) -> str:
    """Turn-ahead L: stem from the bottom, then left or right."""
    s = -1.0 if left else 1.0
    d = f"M {-s * 0.16:.3f},0.24 L {-s * 0.16:.3f},{-0.16} L {s * 0.08:.3f},{-0.16}"
    head = (
        f'<polygon points="{s * 0.28:.3f},{-0.16:.3f} {s * 0.04:.3f},{-0.34:.3f} '
        f'{s * 0.04:.3f},{0.02:.3f}" fill="{fill}"/>'
    )
    return _plan(d, sw, fill) + head


def _front_car(cx: float, cy: float, s: float, fill: str) -> str:
    return (
        _rect(fill, cx - s * 0.22, cy - s * 0.08, cx + s * 0.22, cy + s * 0.16, rx=s * 0.04)
        + _rect(fill, cx - s * 0.16, cy - s * 0.22, cx + s * 0.16, cy - s * 0.04, rx=s * 0.04)
        + _rect(fill, cx - s * 0.20, cy + s * 0.14, cx - s * 0.06, cy + s * 0.22, rx=s * 0.02)
        + _rect(fill, cx + s * 0.06, cy + s * 0.14, cx + s * 0.20, cy + s * 0.22, rx=s * 0.02)
    )


def _moto(cx: float, cy: float, s: float, fill: str) -> str:
    return (
        f'<circle cx="{cx - s * 0.22}" cy="{cy + s * 0.12}" r="{s * 0.10}" fill="none" '
        f'stroke="{fill}" stroke-width="{s * 0.045}"/>'
        f'<circle cx="{cx + s * 0.22}" cy="{cy + s * 0.12}" r="{s * 0.10}" fill="none" '
        f'stroke="{fill}" stroke-width="{s * 0.045}"/>'
        + _stk(cx - s * 0.16, cy + s * 0.06, cx + s * 0.14, cy - s * 0.02, s * 0.05, fill)
        + _rect(fill, cx - s * 0.06, cy - s * 0.14, cx + s * 0.16, cy + s * 0.02, rx=s * 0.03)
        + _fig(fill, cx + s * 0.02, cy - s * 0.16, s * 0.34)
    )


def _tractor(cx: float, cy: float, s: float, fill: str) -> str:
    return (
        f'<circle cx="{cx - s * 0.16}" cy="{cy + s * 0.10}" r="{s * 0.16}" fill="{fill}"/>'
        f'<circle cx="{cx + s * 0.18}" cy="{cy + s * 0.14}" r="{s * 0.08}" fill="{fill}"/>'
        + _rect(fill, cx - s * 0.10, cy - s * 0.06, cx + s * 0.22, cy + s * 0.10, rx=s * 0.02)
        + _rect(fill, cx - s * 0.06, cy - s * 0.22, cx + s * 0.12, cy - s * 0.04, rx=s * 0.02)
    )


def _aircraft(cx: float = 0, cy: float = 0.02, s: float = 1.0, fill: str | None = None) -> str:
    fill = fill or C["black"]
    return (
        f'<polygon points="{cx - 0.26 * s},{cy + 0.02 * s} {cx + 0.10 * s},{cy + 0.02 * s} '
        f'{cx + 0.22 * s},{cy - 0.04 * s} {cx + 0.08 * s},{cy - 0.04 * s} {cx + 0.02 * s},{cy - 0.18 * s} '
        f'{cx - 0.10 * s},{cy - 0.18 * s} {cx - 0.06 * s},{cy - 0.04 * s} {cx - 0.26 * s},{cy - 0.04 * s}" '
        f'fill="{fill}"/>'
        f'<polygon points="{cx + 0.10 * s},{cy + 0.02 * s} {cx + 0.28 * s},{cy - 0.02 * s} '
        f'{cx + 0.22 * s},{cy + 0.08 * s}" fill="{fill}"/>'
        + _stk(cx - 0.04 * s, cy + 0.02 * s, cx - 0.10 * s, cy + 0.16 * s, 0.04 * s, fill)
        + _stk(cx + 0.06 * s, cy + 0.02 * s, cx + 0.04 * s, cy + 0.14 * s, 0.04 * s, fill)
    )


def _hump_bridge() -> str:
    return (
        f'<path d="M -0.30,0.22 L -0.30,0.08 Q 0,-0.18 0.30,0.08 L 0.30,0.22 Z" fill="{C["black"]}"/>'
        + _rect(C["black"], -0.32, 0.08, -0.18, 0.22)
        + _rect(C["black"], 0.18, 0.08, 0.32, 0.22)
    )


def _st_andrew() -> str:
    board = (
        _rect(C["red"], -0.42, -0.10, 0.42, 0.10, rx=0.02)
        + _rect(C["white"], -0.38, -0.06, 0.38, 0.06, rx=0.01)
    )
    return (
        f'<g transform="rotate(-32)">{board}</g>'
        f'<g transform="rotate(32)">{board}</g>'
    )


def _snowflake(cx: float = 0, cy: float = 0, s: float = 0.20, fill: str | None = None) -> str:
    fill = fill or C["black"]
    out = []
    for a in range(0, 180, 30):
        out.append(
            f'<g transform="translate({cx} {cy}) rotate({a})">'
            f'<rect x="{-s * 0.045}" y="{-s}" width="{s * 0.09}" height="{s * 2}" '
            f'rx="{s * 0.04}" fill="{fill}"/>'
            f'<rect x="{-s * 0.12}" y="{-s * 0.62}" width="{s * 0.24}" height="{s * 0.07}" '
            f'rx="{s * 0.03}" fill="{fill}"/>'
            f'<rect x="{-s * 0.12}" y="{s * 0.55}" width="{s * 0.24}" height="{s * 0.07}" '
            f'rx="{s * 0.03}" fill="{fill}"/>'
            f"</g>"
        )
    return "".join(out)


def _waves(y: float = 0.22, fill: str | None = None) -> str:
    fill = fill or C["black"]
    return (
        f'<path d="M -0.26,{y:.3f} Q -0.18,{y - 0.06:.3f} -0.10,{y:.3f} '
        f'Q -0.02,{y + 0.06:.3f} 0.06,{y:.3f} Q 0.14,{y - 0.06:.3f} 0.26,{y:.3f}" '
        f'fill="none" stroke="{fill}" stroke-width="0.035" stroke-linecap="round"/>'
    )


def _info_rect(inner: str, *, portrait: bool = False) -> str:
    if portrait:
        return _rect(C["blue"], -0.33, -0.45, 0.33, 0.45, rx=0.03) + inner
    return _rect(C["blue"], -0.39, -0.33, 0.39, 0.33, rx=0.03) + inner


def _car(cx: float, cy: float, s: float, fill: str) -> str:
    return (
        _rect(fill, cx - s * 0.30, cy - s * 0.06, cx + s * 0.24, cy + s * 0.10, rx=s * 0.04)
        + _rect(fill, cx - s * 0.06, cy - s * 0.20, cx + s * 0.18, cy - s * 0.04, rx=s * 0.05)
        + f'<circle cx="{cx - s * 0.16}" cy="{cy + s * 0.10}" r="{s * 0.07}" fill="{fill}"/>'
        + f'<circle cx="{cx + s * 0.12}" cy="{cy + s * 0.10}" r="{s * 0.07}" fill="{fill}"/>'
    )


def _lorry(cx: float, cy: float, s: float, fill: str) -> str:
    return (
        _rect(fill, cx - s * 0.32, cy - s * 0.16, cx + s * 0.06, cy + s * 0.10, rx=s * 0.03)
        + _rect(fill, cx + s * 0.04, cy - s * 0.06, cx + s * 0.30, cy + s * 0.10, rx=s * 0.03)
        + f'<circle cx="{cx - s * 0.18}" cy="{cy + s * 0.10}" r="{s * 0.07}" fill="{fill}"/>'
        + f'<circle cx="{cx + s * 0.18}" cy="{cy + s * 0.10}" r="{s * 0.07}" fill="{fill}"/>'
    )


def _beast(cx: float, cy: float, s: float, *, antlers: bool = False, horse: bool = False, rider: bool = False) -> str:
    fill = C["black"]
    body = _rect(fill, cx - s * 0.22, cy - s * 0.06, cx + s * 0.16, cy + s * 0.10, rx=s * 0.07)
    head_x = cx + s * 0.22
    head_y = cy - (s * 0.14 if horse else s * 0.08)
    head = f'<circle cx="{head_x}" cy="{head_y}" r="{s * 0.08}" fill="{fill}"/>'
    if horse:
        head = _stk(cx + s * 0.12, cy - s * 0.04, head_x, head_y, s * 0.07, fill) + head
    legs = (
        _capsule(fill, cx - s * 0.14, cy + s * 0.18, s * 0.055, s * 0.20, 8)
        + _capsule(fill, cx - s * 0.04, cy + s * 0.18, s * 0.055, s * 0.20, -6)
        + _capsule(fill, cx + s * 0.06, cy + s * 0.18, s * 0.055, s * 0.20, 10)
        + _capsule(fill, cx + s * 0.14, cy + s * 0.16, s * 0.055, s * 0.18, -12)
    )
    extra = ""
    if antlers:
        extra = (
            f'<path d="M {head_x - s * 0.02:.3f} {head_y - s * 0.06:.3f} '
            f'L {head_x - s * 0.10:.3f} {head_y - s * 0.22:.3f} M {head_x + s * 0.02:.3f} {head_y - s * 0.06:.3f} '
            f'L {head_x + s * 0.12:.3f} {head_y - s * 0.22:.3f}" fill="none" stroke="{fill}" '
            f'stroke-width="{s * 0.04}" stroke-linecap="round"/>'
        )
    if rider:
        extra += _fig(fill, cx - s * 0.02, cy - s * 0.22, s * 0.36)
    return body + head + legs + extra


def _turn_arrow(deg: float, fill: str | None = None) -> str:
    fill = fill or C["black"]
    return _fat_arrow(fill, deg, 0.52, 0.14, 0.28)


def _mway_symbol(x: float = 0, y: float = 0, s: float = 0.42, slash: bool = False) -> str:
    """Two tapering carriageways + overbridge (diagram 2901). Wider at the bottom."""
    left = (
        f'<polygon points="{x - s * 0.62},{y + s * 0.64} {x - s * 0.28},{y + s * 0.64} '
        f'{x - s * 0.40},{y - s * 0.64} {x - s * 0.54},{y - s * 0.64}" fill="{C["white"]}"/>'
    )
    right = (
        f'<polygon points="{x + s * 0.28},{y + s * 0.64} {x + s * 0.62},{y + s * 0.64} '
        f'{x + s * 0.54},{y - s * 0.64} {x + s * 0.40},{y - s * 0.64}" fill="{C["white"]}"/>'
    )
    deck = _rect(C["white"], x - s * 0.76, y - s * 0.05, x + s * 0.76, y + s * 0.07)
    band = ""
    if slash:
        band = (
            f'<g transform="translate({x} {y}) rotate(-40)">'
            f'<rect x="{-s * 0.82}" y="{-s * 0.08}" width="{s * 1.64}" height="{s * 0.16}" fill="{C["red"]}"/>'
            f"</g>"
        )
    return f'<g>{left}{right}{deck}{band}</g>'


def _icon_pump(cx: float, cy: float, s: float) -> str:
    w = C["white"]
    return (
        _rect(w, cx - s * 0.16, cy - s * 0.20, cx + s * 0.14, cy + s * 0.26, rx=s * 0.04)
        + _rect(C["motorway"], cx - s * 0.10, cy - s * 0.14, cx + s * 0.08, cy + s * 0.00, rx=s * 0.02)
        + _rect(w, cx - s * 0.20, cy + s * 0.22, cx + s * 0.18, cy + s * 0.32, rx=s * 0.02)
        + f'<path d="M {cx + s * 0.14:.3f} {cy - s * 0.06:.3f} '
        f'Q {cx + s * 0.32:.3f} {cy - s * 0.04:.3f} {cx + s * 0.30:.3f} {cy + s * 0.14:.3f}" '
        f'fill="none" stroke="{w}" stroke-width="{s * 0.055}" stroke-linecap="round"/>'
        + _rect(w, cx + s * 0.24, cy + s * 0.10, cx + s * 0.36, cy + s * 0.22, rx=s * 0.03)
    )


def _icon_cup(cx: float, cy: float, s: float) -> str:
    w = C["white"]
    return (
        f'<path d="M {cx - s * 0.16:.3f} {cy - s * 0.08:.3f} L {cx - s * 0.12:.3f} {cy + s * 0.20:.3f} '
        f'Q {cx:.3f} {cy + s * 0.28:.3f} {cx + s * 0.12:.3f} {cy + s * 0.20:.3f} '
        f'L {cx + s * 0.16:.3f} {cy - s * 0.08:.3f} Z" fill="{w}"/>'
        + f'<path d="M {cx + s * 0.14:.3f} {cy - s * 0.02:.3f} Q {cx + s * 0.32:.3f} {cy + s * 0.06:.3f} '
        f'{cx + s * 0.14:.3f} {cy + s * 0.14:.3f}" fill="none" stroke="{w}" stroke-width="{s * 0.055}" '
        f'stroke-linecap="round"/>'
        + _rect(w, cx - s * 0.18, cy - s * 0.14, cx + s * 0.18, cy - s * 0.06, rx=s * 0.02)
    )


def _icon_bed(cx: float, cy: float, s: float) -> str:
    w = C["white"]
    return (
        _rect(w, cx - s * 0.30, cy - s * 0.22, cx - s * 0.16, cy + s * 0.16, rx=s * 0.03)
        + _rect(w, cx - s * 0.30, cy + s * 0.00, cx + s * 0.30, cy + s * 0.16, rx=s * 0.04)
        + _rect(w, cx - s * 0.12, cy - s * 0.12, cx + s * 0.06, cy + s * 0.02, rx=s * 0.03)
        + _rect(w, cx - s * 0.32, cy + s * 0.14, cx - s * 0.24, cy + s * 0.26, rx=s * 0.02)
        + _rect(w, cx + s * 0.24, cy + s * 0.14, cx + s * 0.32, cy + s * 0.26, rx=s * 0.02)
    )


def _icon_info(cx: float, cy: float, s: float) -> str:
    w = C["white"]
    return (
        f'<circle cx="{cx}" cy="{cy - s * 0.16}" r="{s * 0.075}" fill="{w}"/>'
        + _rect(w, cx - s * 0.055, cy - s * 0.04, cx + s * 0.055, cy + s * 0.24, rx=s * 0.03)
    )


def _zone_plate(ends: bool = False) -> str:
    # Inner white of the roundel r=0.19; "20" at cap 0.14 keeps >= 1 sw to the ring (validator).
    body = (
        _rect(C["white"], -0.37, -0.59, 0.37, 0.59, rx=0.03)
        + f'<circle cx="0" cy="-0.18" r="0.26" fill="{C["red"]}"/>'
        + f'<circle cx="0" cy="-0.18" r="0.19" fill="{C["white"]}"/>'
        + lettering.mph_pair(20, y=-0.18, cap_h=0.14, fill=C["black"], part=2)
    )
    if ends:
        body += (
            f'<g transform="translate(0 -0.18) rotate(-38)">'
            f'<rect x="-0.34" y="-0.04" width="0.68" height="0.08" fill="{C["red"]}"/>'
            f"</g>"
            + _word("ZONE", 0, 0.28, 0.09, C["black"])
            + _word("ENDS", 0, 0.42, 0.10, C["black"])
        )
    else:
        body += _word("ZONE", 0, 0.36, 0.12, C["black"])
    return body


def _countdown(n: int) -> str:
    plate = _rect(C["motorway"], -0.32, -0.58, 0.32, 0.58, rx=0.04)
    bars = ""
    # Official 823–825: white bars sloping down-right (\), stacked from the bottom.
    y_bottom = 0.30
    for i in range(n):
        y = y_bottom - i * 0.22
        bars += (
            f'<g transform="translate(0 {y}) rotate(38)">'
            f'<rect x="-0.20" y="-0.045" width="0.44" height="0.09" rx="0.02" fill="{C["white"]}"/>'
            f"</g>"
        )
    return plate + bars


def _placeholder(label: str) -> str:
    """Neutral fallback: grey hatch + id. Must not impersonate a real plate."""
    cid = "ph" + "".join(c if c.isalnum() else "x" for c in (label or "x"))[:16]
    hatch = "".join(
        f'<line x1="{-0.55 + i * 0.12:.3f}" y1="-0.55" x2="{-0.15 + i * 0.12:.3f}" y2="0.55" '
        f'stroke="#9A9A94" stroke-width="0.035"/>'
        for i in range(10)
    )
    return (
        f'<g data-placeholder="1">'
        f'<rect x="-0.55" y="-0.55" width="1.10" height="1.10" rx="0.04" fill="#D8D6CE" stroke="#6E6C66" stroke-width="0.03"/>'
        f'<clipPath id="{cid}"><rect x="-0.55" y="-0.55" width="1.10" height="1.10" rx="0.04"/></clipPath>'
        f'<g clip-path="url(#{cid})">{hatch}</g>'
        f'<rect x="-0.46" y="-0.14" width="0.92" height="0.32" rx="0.03" fill="#D8D6CE"/>'
        + _word(label[:10], 0, 0.02, 0.11, "#3A3A38", tracking=0.01)
        + "</g>"
    )


def _family_plate(family: str, param: int | None = None) -> str:
    """Dedicated family-coloured plates (direction stacks). Not used for fallbacks."""
    if family == "DirPrimary":
        return _rect(C["primary"], -0.5, -0.28, 0.5, 0.28, rx=0.03) + _chevron(C["white"], 0.5, 0.28)
    if family == "DirLocal":
        return (
            _rect(C["white"], -0.5, -0.28, 0.5, 0.28, rx=0.03)
            + _rect(C["black"], -0.48, -0.26, 0.48, 0.26)
            + _rect(C["white"], -0.45, -0.22, 0.32, 0.22)
            + _chevron(C["white"], 0.5, 0.28)
        )
    if family == "DirMotorway":
        return _rect(C["motorway"], -0.5, -0.28, 0.5, 0.28, rx=0.03) + _chevron(C["white"], 0.5, 0.28)
    if family == "TouristBrown":
        return (
            _rect(C["brown"], -0.5, -0.28, 0.5, 0.28, rx=0.03)
            + f'<circle cx="-0.22" cy="0" r="0.12" fill="{C["white"]}"/>'
            + _rect(C["white"], 0.02, -0.06, 0.36, 0.06)
        )
    return _placeholder(family[:8])


def family_face(family: str, param: int | None = None, label: str = "") -> str:
    return _placeholder(label or family[:8])


def _belisha(_p=None) -> str:
    # Sign glyph for 4007 / BELISHA / XING_PAR (furniture uses _belisha_furniture). Laid out like SI 2016
    # diagram 4007 (printed p461): yellow globe seated on the post with no gap, post drawn with a height break
    # (not to scale; the SI gives 2100-3100 mm), ground line, alternate black/white bands with the lowest black
    # (Sch 14 Pt 4 para 13(3), printed p494). Post/globe width ratio 0.26 as measured on the 4007 diagram.
    # Everything sits inside the square sign viewBox (-0.7..0.7).
    r = 0.19
    w = round(0.26 * 2 * r / 2, 4)
    top, ground = -0.26, 0.62
    k = C["black"]
    out = ""
    for y0, y1, fill in ((top, -0.06, C["white"]), (-0.06, 0.14, k), (0.20, 0.40, C["white"]), (0.40, ground, k)):
        out += (f'<rect x="{-w}" y="{y0}" width="{2 * w}" height="{round(y1 - y0, 4)}" fill="{fill}" '
                f'stroke="{k}" stroke-width="0.012"/>')
    # height break (as drawn in 4007): two parallel S-curves across the post with a gap between them
    for y in (0.14, 0.20):
        out += (f'<path d="M{-w - 0.05},{y + 0.02} C{-w + 0.02},{y - 0.04} {w - 0.02},{y + 0.04} {w + 0.05},{y - 0.02}" '
                f'fill="none" stroke="{k}" stroke-width="0.012"/>')
    # r11: the ground line spans the face width so the whole face is square (1.278 x 1.278), keeping the
    # 0.32 m plate (globe 275-335 mm) and a square viewBox; the ground-line length is illustrative.
    out += _rect(k, -0.639, ground, 0.639, round(ground + 0.012, 4))
    out += (f'<circle cx="0" cy="{round(top - r, 4)}" r="{r}" fill="{C["fluorescent_yellow"]}" '
            f'stroke="{k}" stroke-width="0.012"/>')
    return out


def glyph(code: str, param: int | None = None) -> str:
    fn = GLYPHS.get(code)
    if fn is None:
        return ""
    return fn(param)


def legend_log(code: str, param: int | None = None) -> list:
    """Draw one glyph and return every legend word's ink box (see lettering.LOG)."""
    prev = lettering.LOG
    lettering.LOG = []
    try:
        glyph(code, param)
        return list(lettering.LOG)
    finally:
        lettering.LOG = prev


GLYPHS = {
    "670": lambda p: _ring_roundel() + _mph_pair(p or 30),
    "671": lambda p: (
        f'<defs><clipPath id="nsl"><circle cx="0" cy="0" r="0.50"/></clipPath></defs>'
        + _disc(C["white"], 0.50)
        + f'<g clip-path="url(#nsl)"><g transform="rotate(-45)">'
        f'<rect x="-0.75" y="-0.1335" width="1.50" height="0.267" fill="{C["black"]}"/>'
        f"</g></g>"
    ),
    "602": lambda p: (
        # TSRGD 602 = Highway Code / KYTS Give Way: inverted white, thick
        # rounded red, black GIVE WAY (SurePass FAQ saying red text is wrong).
        _nested_tri(
            False,
            red_s=WARN_RED_H,
            white_k=GIVEWAY_K,
            round_sw=WARN_RED_SW,
            grey_k=1.0,
            grey_sw=0.0,
            white_round=WARN_WHITE_SW,
        )
        # r3: flat caps GIVE 0.179 H, WAY 0.122 H, measured on SI 2016 Sch 9 Pt 2 item 2
        # (diagram 602). (r2 used 76/600 and 50/600, which are x-heights, not caps.)
        + _word_fit("GIVE", 0, -0.287, C["black"], max_w=0.632, max_h=0.179 * 1.06, tracking_sw=0.6, weight=1.28, narrow=0.86)
        + _word_fit("WAY", 0, -0.049, C["black"], max_w=0.405, max_h=0.122 * 1.06, tracking_sw=0.6, weight=1.28, narrow=0.86)
    ),
    "601.1": lambda p: (
        _octagon(C["white"], 0.50) + _octagon(C["red"], 0.455)
        # r3: STOP flat caps 0.235 W (W = 0.924 units), word 0.84 W, measured on SI 2016 Sch 9 Pt 2 item 1 (diagram 601.1).
        + _word_fit("STOP", 0, 0.0, C["white"], max_w=0.776, max_h=0.235 * 0.924, tracking_sw=0.5, weight=1.2, narrow=0.86)
    ),
    "611.1": lambda p: (
        _rim_disc(C["blue"], 0.5)
        + "".join(_mini_arrow(C["white"], a) for a in (0, 120, 240))
    ),
    "616": lambda p: (
        _rim_disc(C["red"], 0.5, rw=0.02)
        + _rect(C["white"], -0.426, -0.10, 0.426, 0.10, rx=0.027)
    ),
    "610": lambda p: _rim_disc(C["blue"], 0.5) + _fat_arrow(C["white"], 225, 0.68, 0.18, 0.38),
    "611": lambda p: (
        _rim_disc(C["blue"], 0.5)
        + f'<g transform="translate(-0.26 0.10)">{_fat_arrow(C["white"], 225, 0.44, 0.125, 0.24)}</g>'
        + f'<g transform="translate(0.26 0.10)">{_fat_arrow(C["white"], 135, 0.44, 0.125, 0.24)}</g>'
    ),
    "543": lambda p: (
        _warn()
        + _rect(C["black"], -0.085, -0.28, 0.085, 0.28, rx=0.08)
        + f'<circle cx="0" cy="-0.16" r="0.062" fill="{C["red"]}"/>'
        + f'<circle cx="0" cy="0" r="0.062" fill="{C["amber"]}"/>'
        + f'<circle cx="0" cy="0.16" r="0.062" fill="{C["green"]}"/>'
    ),
    "544": lambda p: (
        _warn()
        + _fig(C["black"], 0.02, -0.04, 0.46, walk=True, side=True)
        + _rect(C["black"], -0.24, 0.22, -0.10, 0.28)
        + _rect(C["white"], -0.10, 0.22, 0.04, 0.28)
        + _rect(C["black"], 0.04, 0.22, 0.18, 0.28)
        + _rect(C["white"], 0.18, 0.22, 0.26, 0.28)
    ),
    "545": lambda p: (
        _warn()
        + _fig(
            C["black"], -0.105, 0.115, 0.36, child=True, side=True, run=True, lean=12,
            hold="R", hand=(0.087, -0.095),
        )
        + _fig(
            C["black"], 0.115, 0.095, 0.40, child=True, side=True, lean=6,
            hold="L", hand=(-0.120, -0.043),
        )
    ),
    "510": lambda p: _warn()
    + "".join(_circ_arrow(C["black"], 0.175, a, 78, 0.068, 0.12) for a in (18, 138, 258)),
    "3000": lambda p: (
        _rect(C["black"], -0.28, -0.72, 0.28, 0.72, rx=0.08)
        + f'<circle cx="0" cy="-0.42" r="0.16" fill="{C["red"]}"/>'
        + f'<circle cx="0" cy="0" r="0.16" fill="{C["amber"]}"/>'
        + f'<circle cx="0" cy="0.42" r="0.16" fill="{C["green"]}"/>'
    ),
    "4002.1": lambda p: (
        _rect(C["black"], -0.26, -0.54, 0.26, 0.54, rx=0.06)
        + _fig(C["red"], 0, -0.24, 0.34)
        + _fig(C["green"], 0, 0.24, 0.34, walk=True)
    ),
    "4003": lambda p: (
        _rect(C["black"], -0.26, -0.48, 0.26, 0.48, rx=0.04)
        + _rect(C["amber"], -0.18, -0.34, 0.18, -0.04, rx=0.02)
        + _word_fit("WAIT", 0, -0.19, C["black"], max_w=0.29, max_h=0.09, tracking_sw=1.0, weight=1.15)
        + f'<circle cx="0" cy="0.22" r="0.10" fill="{C["grey"]}"/>'
        + f'<circle cx="0" cy="0.22" r="0.06" fill="{C["black"]}"/>'
    ),
    "BELISHA": _belisha,
    "801": lambda p: _info_rect(_letter("P", 0, 0.0, 0.36, 0.46, C["white"], weight=1.15), portrait=False),
    "2025": lambda p: _family_plate("DirPrimary"),
    "2101": lambda p: _family_plate("DirLocal"),
    "2701": lambda p: _plate("2701"),
    "2202": lambda p: _family_plate("TouristBrown"),
    "GANTRY_ADS": lambda p: _family_plate("DirMotorway"),
    # r3 sources (legislation.gov.uk PDFs; see countries/uk/sources/diagram_refs.json):
    # 530 = SI 2002/3113 Sch 1 diagram 530 (p57): imperial sign "14'-6"", the
    #   metric "4.4 m" sign "may be omitted or placed to the right" (item 4).
    # 530A = SI 2016/362 Sch 2 Pt 4 item 2 (p55): "4.4 m" over "14'6"".
    "530": lambda p: _headroom_tri(["14'-6\""], lower_arrow=True),
    "530A": lambda p: _headroom_tri(["4.4 m", "14'-6\""], lower_arrow=False),
    # 629.1 = SI 2016/362 Sch 3 Pt 2 item 25 (p73), first alternative: lorry,
    #   "32'-6"", outward arrows (also SI 2002 Sch 2 diagram 629.1, p89).
    "629.1": lambda p: (
        _ring_roundel()
        + f'<g transform="scale(-1 1)">{_lorry(0.0, -0.13, 0.62, C["black"])}</g>'
        + lettering.word("32'-6\"", 0, 0.07, 0.10, C["black"], tracking_sw=0.6, part=2)
        + _stk(-0.20, 0.20, -0.05, 0.20, 0.025)
        + f'<polygon points="-0.25,0.20 -0.19,0.165 -0.19,0.235" fill="{C["black"]}"/>'
        + _stk(0.05, 0.20, 0.20, 0.20, 0.025)
        + f'<polygon points="0.25,0.20 0.19,0.165 0.19,0.235" fill="{C["black"]}"/>'
    ),
    "779": lambda p: _warn() + _lightning(),
    "532.2": lambda p: _warn() + _arch_bridge(),
    "629.2A": lambda p: _limit_roundel(["4.4 m", "14'-6\""], vertical=True),
    "629.2": lambda p: _limit_roundel(["14'-6\""], vertical=True),
    "629A": lambda p: _limit_roundel(["2.0 m", "6'-6\""], vertical=False),
    "629": lambda p: _limit_roundel(["6'-6\""], vertical=False),
    "674": lambda p: _zone_plate(False),
    # r7: SI 2016 Sch 10 Pt 2 item 6, diagram 675A (printed p179 = tsrgd2016.pdf PDF p180): 30 mph roundel over the Zone ENDS
    # panel. 675 is the pre-2016 number (alias below).
    "675": lambda p: _plate("675A"),
    "823": lambda p: _countdown(3),
    "824": lambda p: _countdown(2),
    "825": lambda p: _countdown(1),
    # r3: SI 2016 Sch 13 (printed p446 = tsrgd2016.pdf PDF p447), measured with board width W = 1: board H 0.667 W, red/white
    # chequer border 0.087 W wide (7 squares across, 5 down, red corners), black panel inset 0.087 W,
    # red lamps at (+-0.216, -0.087), amber at (0, +0.087), lamp diameter 0.149 W.
    "3014": lambda p: _chequer_board() + (
        _rect(C["black"], -0.413, -0.2467, 0.413, 0.2467)
        + f'<circle cx="-0.216" cy="-0.087" r="0.0745" fill="{C["red"]}"/>'
        + f'<circle cx="0.216" cy="-0.087" r="0.0745" fill="{C["red"]}"/>'
        + f'<circle cx="0" cy="0.087" r="0.0745" fill="{C["amber"]}"/>'
    ),
    "953": lambda p: (
        _rim_disc(C["blue"], 0.5)
        # r2: cycle beside the bus, not behind it.
        + _bus(-0.15, -0.12, 0.40, 0.20)
        + _cycle(0.24, -0.12, 0.17)
        + _word_fit("TAXI", 0, 0.28, C["white"], max_w=0.62, max_h=0.09, tracking_sw=0.9, weight=1.2)
    ),
    "2911": lambda p: (
        _rect(C["grey"], -0.70, -0.36, 0.70, 0.36, rx=0.04)
        + _rect(C["motorway"], -0.67, -0.33, 0.67, 0.33, rx=0.03)
        + _icon_pump(-0.48, 0.00, 0.44)
        + _icon_cup(-0.14, 0.00, 0.44)
        + _icon_bed(0.20, 0.02, 0.44)
        + _icon_info(0.50, 0.00, 0.42)
    ),
    "2901": lambda p: (
        _rect(C["motorway"], -0.50, -0.50, 0.50, 0.50, rx=0.03)
        # r2: route number below the symbol, clear of the carriageways.
        + _mway_symbol(0, -0.10, 0.40, False)
        + _word("M25", 0, 0.30, 0.10, C["white"])
    ),
    "2931": lambda p: (
        _rect(C["motorway"], -0.50, -0.50, 0.50, 0.50, rx=0.03)
        + _mway_symbol(0, 0, 0.46, True)
    ),
    "MS4": lambda p: (
        _rect(C["grey"], -0.72, -0.30, 0.72, 0.30, rx=0.03)
        + _rect(C["black"], -0.70, -0.28, 0.70, 0.28)
        + _digit_vms(2, -0.16, 0, 0.22, 0.36, C["amber"])
        + _digit_vms(0, 0.16, 0, 0.22, 0.36, C["amber"])
    ),
    # r6: MARKER drawn from SI 2002 diagram 2717 (absent from SI 2016); see atlas/traced.py.
    "MARKER": lambda p: _plate("MARKER"),
    "STREET_NAME": lambda p: (
        _rect(C["grey"], -0.62, -0.18, 0.62, 0.18, rx=0.03)
        + _rect(C["white"], -0.60, -0.16, 0.60, 0.16, rx=0.02)
        + _rect(C["black"], -0.58, -0.14, 0.58, 0.14)
        + _rect(C["white"], -0.54, -0.10, 0.54, 0.10)
        + _rect(C["black"], -0.40, -0.035, 0.40, 0.035)
    ),
    # Highway Code UK plates: thick filled road-plans (highwaycodeuk.co.uk).
    "504.1": lambda p: (
        _warn()
        # r3: stem 0.167 H where H = outer warn height 0.92 + WARN_RED_SW = 1.058 units.
        + _plan("M 0,0.28 L 0,-0.26", 0.167 * (WARN_RED_H + WARN_RED_SW))
        + f'<polygon points="-0.0883,-0.26 0,-0.34 0.0883,-0.26" fill="{C["black"]}"/>'
        + _plan("M -0.21,0.00 L 0.21,0.00", 0.08)
    ),
    "504.2": lambda p: _warn() + _plan("M 0,0.28 L 0,-0.26", 0.10) + _plan("M -0.24,0.00 L 0.24,0.00", 0.15),
    "505.1": lambda p: _warn() + _plan("M -0.24,-0.08 L 0.24,-0.08", 0.15) + _plan("M 0,-0.08 L 0,0.28", 0.15),
    "506.1": lambda p: (
        _warn()
        + _plan("M 0,0.28 L 0,-0.26", 0.15)
        + f'<polygon points="-0.075,-0.26 0,-0.34 0.075,-0.26" fill="{C["black"]}"/>'
        + _plan("M 0.00,0.00 L 0.24,0.00", 0.10)
    ),
    # r3: SI 2016 Sch 2 Pt 2 item 4 (printed p40 = tsrgd2016.pdf PDF p41), second alternative, measured in warn units:
    # stem x -0.063..0.111 with a 45-degree point (apex y -0.162); arms 0.09 thick, square-cut.
    "507.1": lambda p: (
        _warn()
        + f'<polygon points="-0.063,0.405 -0.063,-0.075 0.024,-0.162 0.111,-0.075 0.111,0.405" fill="{C["black"]}"/>'
        + _rect(C["black"], -0.194, 0.012, -0.063, 0.102)
        + _rect(C["black"], 0.111, 0.191, 0.242, 0.281)
    ),
    "508.1": lambda p: (
        _warn()
        + _plan("M 0.10,-0.26 L 0.10,0.28", 0.16)
        + _plan("M -0.22,0.22 L 0.10,0.00", 0.09)
    ),
    # r3: SI 2016 Sch 2 Pt 2 item 6 (printed p41 = tsrgd2016.pdf PDF p42), measured: 45-degree main carriageway 0.177 wide,
    # upper end cut by x -0.128 and y ~-0.10 (top edge +-0.02), lower end square; slip road 0.083 wide.
    "509.1": lambda p: (
        _warn()
        + f'<polygon points="-0.128,-0.10 -0.008,-0.10 0.318,0.226 0.193,0.351 -0.128,0.030" fill="{C["black"]}"/>'
        + _rect(C["black"], -0.027, 0.10, 0.056, 0.405)
    ),
    "512": lambda p: (
        _warn()
        + f'<path d="M -0.04,0.28 Q -0.04,0.04 0.22,-0.16" fill="none" stroke="{C["black"]}" '
        f'stroke-width="0.16" stroke-linecap="butt" stroke-linejoin="round"/>'
        + f'<polygon points="0.22,-0.16 0.08,-0.04 0.34,-0.04" fill="{C["black"]}"/>'
    ),
    # r3: SI 2016 Sch 2 Pt 2 items 9-10 (printed p41 = tsrgd2016.pdf PDF p42), first alternative, measured: stem x 0.045..0.158
    # (centre 0.10, 0.113 wide) bending to the upper left, ends cut square to the road (no arrowhead).
    "512.1": lambda p: (
        _warn()
        + f'<path d="M 0.10,0.405 L 0.10,0.15 Q 0.10,0.05 0.00,0.01 L -0.155,-0.035" fill="none" stroke="{C["black"]}" '
        f'stroke-width="0.113" stroke-linecap="butt" stroke-linejoin="round"/>'
        + _plan("M 0.11,0.10 L 0.20,0.012", 0.10)
    ),
    "512.2": lambda p: (
        _warn()
        + f'<path d="M 0.10,0.405 L 0.10,0.15 Q 0.10,0.05 0.00,0.01 L -0.155,-0.035" fill="none" stroke="{C["black"]}" '
        f'stroke-width="0.113" stroke-linecap="butt" stroke-linejoin="round"/>'
        + _plan("M 0.06,0.12 L -0.035,0.175", 0.09)
    ),
    "513": lambda p: (
        _warn()
        + f'<path d="M -0.16,0.26 Q -0.16,0.04 0.00,0.04 Q 0.16,0.04 0.16,-0.22" fill="none" '
        f'stroke="{C["black"]}" stroke-width="0.13" stroke-linecap="butt" stroke-linejoin="round"/>'
        + f'<polygon points="0.16,-0.22 0.04,-0.10 0.28,-0.10" fill="{C["black"]}"/>'
    ),
    "516": lambda p: (
        _warn()
        + _plan("M -0.18,-0.26 L -0.06,0.28", 0.13)
        + _plan("M 0.18,-0.26 L 0.06,0.28", 0.13)
    ),
    "517": lambda p: (
        _warn()
        + _plan("M -0.12,-0.26 L -0.12,0.28", 0.13)
        + _plan("M 0.16,-0.26 L 0.16,0.00 L 0.04,0.28", 0.13)
    ),
    "521": lambda p: (
        _warn()
        + f'<g transform="translate(-0.12 0)">{_fat_arrow(C["black"], 0, 0.52, 0.09, 0.20)}</g>'
        + f'<g transform="translate(0.12 0)">{_fat_arrow(C["black"], 180, 0.52, 0.09, 0.20)}</g>'
    ),
    "522": lambda p: (
        _warn()
        + f'<g transform="translate(0.06 -0.10)">{_fat_arrow(C["black"], 90, 0.46, 0.08, 0.16)}</g>'
        + f'<g transform="translate(-0.06 0.10)">{_fat_arrow(C["black"], -90, 0.46, 0.08, 0.16)}</g>'
    ),
    "523.1": lambda p: (
        _warn()
        # Slope wedge kept inside the white field (high side on the left).
        + f'<polygon points="-0.21,0.10 0.338,0.33 -0.21,0.33" fill="{C["black"]}"/>'
        + lettering.legend_10pct(-0.01, 0.03, 0.095, C["black"])
    ),
    "524.1": lambda p: (
        _warn()
        + f'<polygon points="0.21,0.10 -0.338,0.33 0.21,0.33" fill="{C["black"]}"/>'
        + lettering.legend_10pct(0.01, 0.03, 0.095, C["black"])
    ),
    "526": lambda p: (
        _warn()
        + _rect(C["black"], -0.26, 0.10, 0.08, 0.18)
        + f'<polygon points="-0.04,0.10 0.26,-0.16 0.26,-0.06 -0.04,0.18" fill="{C["black"]}"/>'
        + _rect(C["black"], 0.18, -0.22, 0.28, -0.04)
        + _waves(0.24)
    ),
    "528": lambda p: _warn() + _hump_bridge(),
    "529.1": lambda p: (
        _warn()
        + _rect(C["black"], -0.24, -0.04, 0.24, 0.24)
        + f'<path d="M -0.24,-0.04 Q 0,-0.30 0.24,-0.04 Z" fill="{C["black"]}"/>'
        + f'<path d="M -0.12,0.24 Q -0.12,0.00 0,0.00 Q 0.12,0.00 0.12,0.24 Z" fill="{C["white"]}"/>'
    ),
    # r7: SI 2016 Sch 2 Pt 4 item 3, diagram 531.1A (printed p56 = tsrgd2016.pdf PDF p57): arch, headroom pointer and
    # height (first alternative, 12'-6"; the SI also shows 3.8 m). 531.1 is the pre-2016 number (alias below).
    "531.1": lambda p: _warn() + _traced_inner("531.1A"),
    "544.1": lambda p: (
        _warn()
        + _fig(C["black"], -0.145, 0.125, 0.34, child=True, bulk=True, hold="R", hand=(0.13, 0.01))
        + _fig(C["black"], 0.085, 0.055, 0.54, bulk=True, hold="L", hand=(-0.10, 0.08))
    ),
    # r12: SI 2016 Sch 14 Pt 2 item 8, diagram 777 (printed p447 = tsrgd2016.pdf PDF p448): black-bordered plate,
    # four lines "ANOTHER TRAIN / COMING / if lights / continue to show" (aspect ~2:1), our stand-in lettering.
    "777": lambda p: (
        _rect(C["black"], -0.80, -0.40, 0.80, 0.40, rx=0.06)
        + _rect(C["white"], -0.76, -0.36, 0.76, 0.36, rx=0.04)
        + lettering.word("ANOTHER TRAIN", 0, -0.235, 0.11, C["black"], tracking_sw=0.5, part=2)
        + lettering.word("COMING", 0, -0.075, 0.11, C["black"], tracking_sw=0.5, part=2)
        + lettering.word("if lights", 0, 0.085, 0.10, C["black"], tracking_sw=0.5, part=2)
        + lettering.word("continue to show", 0, 0.245, 0.10, C["black"], tracking_sw=0.5, part=2)
    ),
    "818.2": lambda p: _warn() + _fit_warn_lines(["Ford"], C["black"], max_h=0.13),
    "547": lambda p: _warn() + _fig(C["black"], -0.12, 0.10, 0.36, child=True, hold="R", hand=(0.10, 0.04)) + _fig(C["black"], 0.08, 0.04, 0.52, hold="L", hand=(-0.08, 0.10)),
    "548": lambda p: _warn() + _beast(0, 0.06, 0.58),
    "549": lambda p: _warn() + _beast(0, 0.06, 0.56),
    "550": lambda p: _warn() + _beast(0, 0.04, 0.56, horse=True),
    "550.1": lambda p: _warn() + _beast(0, 0.06, 0.54, horse=True, rider=True),
    "550.2": lambda p: (
        _warn()
        + _beast(-0.10, 0.04, 0.46, horse=True)
        + _rect(C["black"], 0.04, -0.04, 0.28, 0.12, rx=0.03)
        + f'<circle cx="0.22" cy="0.14" r="0.05" fill="{C["black"]}"/>'
    ),
    # r6: deer traced from SI 2016 diagram 551 (printed p47 = tsrgd2016.pdf PDF p48), see atlas/traced.py.
    "551": lambda p: _warn() + traced.path("551", C["black"]),
    "552": lambda p: _warn() + _fit_warn_lines(["Cattle", "grid"], C["black"], max_h=0.12),
    "553.1": lambda p: _warn() + _tractor(0, 0.02, 0.58, C["black"]),
    "554": lambda p: _warn() + _fit_warn_lines(["Ford"], C["black"], max_h=0.13),
    "554.1": lambda p: _warn() + _fit_warn_lines(["Try your", "brakes"], C["black"], max_h=0.12),
    "554.2": lambda p: _warn() + _snowflake(0, 0.02, 0.20),
    # r6: quay, car and water traced from SI 2016 diagram 555 (printed p48 = tsrgd2016.pdf PDF p49).
    "555": lambda p: _warn() + traced.path("555", C["black"]),
    "556": lambda p: (
        _warn()
        + f'<path d="M -0.28,0.20 Q -0.14,-0.08 0.00,0.12 Q 0.14,-0.08 0.28,0.20 L 0.28,0.24 L -0.28,0.24 Z" '
        f'fill="{C["black"]}"/>'
    ),
    "556.1": lambda p: (
        _warn()
        + f'<g transform="rotate(-22)">{_car(0.02, -0.04, 0.48, C["black"])}</g>'
        + _plan("M -0.26,0.18 L 0.26,0.22", 0.05)
    ),
    "557": lambda p: (
        _warn()
        + _car(-0.06, -0.04, 0.50, C["black"])
        + f'<path d="M 0.04,0.16 Q 0.18,0.22 0.22,0.08 Q 0.16,-0.02 0.08,0.04" fill="none" '
        f'stroke="{C["black"]}" stroke-width="0.045" stroke-linecap="round"/>'
    ),
    "558": lambda p: _warn() + _aircraft(),
    "559": lambda p: (
        _warn()
        + f'<polygon points="-0.26,-0.20 -0.04,-0.22 -0.08,0.22 -0.26,0.22" fill="{C["black"]}"/>'
        + f'<polygon points="-0.02,-0.08 0.10,-0.20 0.16,-0.02" fill="{C["black"]}"/>'
        + f'<polygon points="0.04,0.02 0.18,-0.08 0.22,0.10" fill="{C["black"]}"/>'
        + f'<polygon points="0.00,0.10 0.12,0.00 0.16,0.20" fill="{C["black"]}"/>'
    ),
    "562": lambda p: _warn() + _letter("!", 0, 0.06, 0.10, 0.28, C["black"]),
    "583": lambda p: (
        _warn()
        + f'<polygon points="-0.26,0.20 0.26,0.08 0.26,0.22 -0.26,0.22" fill="{C["black"]}"/>'
        + f'<g transform="translate(0 -0.06) rotate(-12)">{_lorry(0, 0, 0.55, C["black"])}</g>'
    ),
    "584": lambda p: (
        _warn()
        + _front_car(0.00, -0.16, 0.36, C["black"])
        + _front_car(0.00, 0.00, 0.40, C["black"])
        + _front_car(0.00, 0.16, 0.44, C["black"])
    ),
    # r6: gate traced from SI 2016 diagram 770 (printed p51 = tsrgd2016.pdf PDF p52).
    "770": lambda p: _warn() + traced.path("770", C["black"]),
    # r6: steam locomotive traced from SI 2016 diagram 771 (printed p51 = tsrgd2016.pdf PDF p52).
    "771": lambda p: _warn() + traced.path("771", C["black"]),
    "774": lambda p: _st_andrew(),
    "778": lambda p: (
        _rect(C["grey"], -0.40, -0.48, 0.40, 0.48, rx=0.04)
        + _rect(C["white"], -0.37, -0.45, 0.37, 0.45, rx=0.03)
        + _rect(C["black"], -0.22, -0.02, 0.16, 0.12, rx=0.03)
        + _rect(C["black"], -0.04, -0.16, 0.08, 0.00, rx=0.02)
        + f'<polygon points="-0.04,-0.16 -0.18,-0.24 0.04,-0.24 0.10,-0.16" fill="{C["black"]}"/>'
        + f'<circle cx="-0.14" cy="0.14" r="0.055" fill="{C["black"]}"/>'
        + f'<circle cx="0.10" cy="0.14" r="0.055" fill="{C["black"]}"/>'
        + _stk(-0.08, -0.24, -0.08, -0.32, 0.04)
    ),
    "606": lambda p: _mand(_fat_arrow(C["white"], 0, 0.62, 0.18, 0.32)),
    # r3: SI 2002 diagram 607 "One-way traffic" plate (printed p78 = refs/si2002.pdf PDF p78), measured: W/H 2.694, frame 0.097 H,
    # "One way" from 0.29 H, 0.784 W wide.
    "607": lambda p: _bw_plate(1.347, 0.5, "One way", 0.17, -0.25 + 0.5 * 0.29 + 0.085, 0.90),

    # r3: SI 2016 Sch 9 Pt 2 item 3 (printed p138 = tsrgd2016.pdf PDF p139), measured: plate W/H 2.354, frame 0.061 H,
    # "Dual" cap 0.248 H from 0.188 H; "carriageway" x-height from 0.597 H; one x-height.
    # r3: SI 2002 diagram 546 "School ahead" plate (printed p63 = refs/si2002.pdf PDF p63), measured: W/H 2.315, frame 0.098 H,
    # "School" cap 0.38 H from 0.283 H, 0.742 W wide.
    "546": lambda p: _bw_plate(1.157, 0.5, "School", 0.19, -0.25 + 0.5 * 0.283 + 0.095, 0.87),
    "608": lambda p: (
        _rect(C["black"], -0.706, -0.30, 0.706, 0.30, rx=0.05)
        + _rect(C["white"], -0.6694, -0.2634, 0.6694, 0.2634, rx=0.025)
        + lettering.word("Dual", 0, -0.30 + 0.6 * 0.188 + 0.149 / 2, 0.149, C["black"], tracking_sw=0.5, part=1, narrow=0.82)
        + lettering.word("carriageway", 0, -0.30 + 0.6 * 0.597 - 0.149 / 2 + 0.149 * lettering.X_RATIO, 0.149,
                         C["black"], tracking_sw=0.5, part=1, narrow=0.82)
    ),
    "609": lambda p: _mand(_elbow(C["white"], left=True)),
    "612": lambda p: _proh(_elbow(C["black"], left=False, sw=0.12), slash=True),
    "613": lambda p: _proh(_elbow(C["black"], left=True, sw=0.12), slash=True, slash_rot=45),
    "614": lambda p: (
        _proh(
            f'<path d="M 0.12,0.16 L 0.12,-0.04 Q 0.12,-0.20 -0.04,-0.20 Q -0.20,-0.20 -0.20,-0.04" '
            f'fill="none" stroke="{C["black"]}" stroke-width="0.08" stroke-linecap="round"/>'
            + f'<polygon points="-0.20,-0.04 -0.30,0.08 -0.08,0.06" fill="{C["black"]}"/>',
            slash=True,
            slash_rot=45,
        )
    ),
    "615": lambda p: (
        _proh(
            f'<g transform="translate(-0.12 0)">{_fat_arrow(C["red"], 0, 0.40, 0.11, 0.20)}</g>'
            + f'<g transform="translate(0.12 0)">{_fat_arrow(C["black"], 180, 0.40, 0.11, 0.20)}</g>'
        )
    ),
    "617": lambda p: _ring_roundel(),
    "619": lambda p: _proh(
        _front_car(0, 0.14, 0.40, C["black"]) + _moto(0, -0.16, 0.42, C["black"])
    ),
    "622.1A": lambda p: _proh(
        _lorry(0, -0.06, 0.50, C["black"])
        + _digit(7, -0.12, 0.20, 0.10, 0.14)
        + f'<circle cx="-0.02" cy="0.26" r="0.016" fill="{C["black"]}"/>'
        + _digit(5, 0.06, 0.20, 0.10, 0.14)
        + _letter("T", 0.18, 0.20, 0.08, 0.12, C["black"])
    ),
    "622.7": lambda p: _proh(
        _car(-0.10, 0.04, 0.40, C["black"])
        + _rect(C["black"], 0.04, -0.06, 0.26, 0.14, rx=0.04)
        + f'<circle cx="0.18" cy="0.14" r="0.05" fill="{C["black"]}"/>'
    ),
    # 622.8-fix (b2 round, restores r6): SI 2016 Sch 3 Pt 2 item 16, diagram 622.8 (printed p71 = tsrgd2016.pdf PDF p72):
    # orange burst, black burst detail and front-view vehicle traced (atlas/traced.py). The sign-table page is landscape and
    # printed sideways WITH its diagram column, so upright = page rotated 90 deg clockwise: burst ABOVE the vehicle (r6).
    # The r7 re-trace read the raw page and was rotated 90 deg (Reviewer b1 ruling AGREE).
    # Orange: SI print sample #F89C22, drawn in palette amber #F29E14 (shade UNVERIFIED).
    "622.8": lambda p: _proh(traced.path("622.8/orange", C["amber"]) + traced.path("622.8/black", C["black"])),
    # r4: SI 2016 Sch 9 Pt 4 item 2, diagram 626.2A (printed p141 = tsrgd2016.pdf PDF p142), measured in board widths W (H 1.819 W):
    # border 0.021 W; WEAK / BRIDGE cap 0.145 W from 0.105 / 0.31 W; dividers 0.536-0.557 and 1.449-1.47 W;
    # grey panel with red ring d 0.772 W (ring 0.076 W) centred 1.005 W; "18" 0.217 W high, "t" 0.163 W,
    # "mgw" x-height ~0.074 W; "Except empty" / "vehicles" cap ~0.088 W from 1.518 / 1.645 W.
    # Grey shade: country "grey" (the SI print shade is lighter; unverified).
    "626.2A": lambda p: _sign6262a(),
    # b1 (placeholder batch 1): SI 2016 Sch 3 Pt 2 prohibitory roundels, symbols traced at 600 dpi with the page
    # upright (atlas/traced.py SOURCE); red ring / white disc from _proh.
    "619.1": lambda p: _proh(traced.path("619.1", C["black"])),
    "619.2": lambda p: _proh(traced.path("619.2", C["black"])),
    "625.1": lambda p: _proh(traced.path("625.1", C["black"])),
    "622.5": lambda p: _proh(traced.path("622.5", C["black"])),
    "622.6": lambda p: _proh(traced.path("622.6", C["black"])),
    # 622.2 end of goods-vehicle prohibition: white disc, grey ring and lorry, black bands (traced).
    "622.2": lambda p: _disc(C["white"], 0.5) + traced.path("622.2/grey", C["grey"]) + traced.path("622.2/black", C["black"]),
    "632": lambda p: _proh(
        _front_car(-0.14, 0.02, 0.38, C["black"]) + _front_car(0.14, 0.02, 0.38, C["red"])
    ),
    # r7: SI 2002 diagram 660 "Parking place reserved for permit holders" (p100; absent from SI 2016), measured on
    # the 150 dpi scan with plate H = 1: W/H 1.896, black border 0.025 W, P square x 0.069-0.408 W, y 0.174-0.817 H
    # with a white P cap 0.54 H; "Permit / holders / only" cap 0.183 H, baselines 0.322 / 0.583 / 0.843 H.
    # The scan is greyscale: the square is drawn blue as the TSRGD parking P (e.g. 2016 diagram 801); colour UNVERIFIED.
    "660": lambda p: _sign660(),
    "642": lambda p: (
        _disc(C["red"], 0.5)
        + _disc(C["blue"], 0.40)
        + _slash(0.10, -45)
        + _slash(0.10, 45)
    ),
    "642.2": lambda p: (
        _disc(C["red"], 0.5)
        + _disc(C["yellow"], 0.40)
        + _word("STOP", 0, -0.14, 0.10, C["black"], tracking=0.016, weight=1.2)
        + _rect(C["black"], -0.04, 0.02, 0.04, 0.36)
        + _fig(C["black"], -0.08, 0.16, 0.22, child=True, side=True, run=True, lean=10)
        + _fig(C["black"], 0.10, 0.14, 0.26, child=True, side=True, lean=6)
    ),
    # r4: SI 2016 Sch 7 Pt 2 item 6, diagram 646 (printed p111 = tsrgd2016.pdf PDF p112), measured with H = 1 (W/H 1.549):
    # border 0.027 H; yellow panel to 0.609 H; divider to 0.637 H; am (white) | pm (black) split at 0.520 W.
    # URBAN / CLEARWAY cap 0.115 H from 0.079 / 0.265 H; "Monday to Friday" cap 0.088 H from 0.464 H;
    # am/pm x-height 0.085 H from 0.699 H; times cap 0.093 H from 0.852 H; roundel d 0.147 W at (0.135 W, 0.209 H).
    # Legend days and times are the SI's example values (permitted variants 1-2).
    "646": lambda p: _sign646(),
    "652": lambda p: (
        _rect(C["grey"], -0.28, -0.48, 0.28, 0.48, rx=0.04)
        + _rect(C["blue"], -0.25, -0.45, 0.25, 0.45, rx=0.03)
        + _fat_arrow(C["white"], 0, 0.62, 0.16, 0.28)
    ),
    "672": lambda p: _mand(_mph_pair(p or 30, fill=C["white"])),
    "673": lambda p: _mand(_mph_pair(p or 30, fill=C["white"])) + _slash(0.10),
    "951": lambda p: _proh(_cycle(0, 0.00, 0.55, C["black"])),
    "952": lambda p: _proh(_bus(0, 0.00, 0.55, 0.28, C["black"], C["white"])),
    "955": lambda p: _mand(_cycle(0, 0.02, 0.62, C["white"])),
    "956": lambda p: (
        _mand(
            _cycle(-0.02, -0.14, 0.40, C["white"])
            + _fig(C["white"], 0.10, 0.12, 0.36)
        )
    ),
    # r6: tram traced from SI 2016 diagram 953.1 (printed p75 = tsrgd2016.pdf PDF p76, Sch 3 Pt 2 item 36).
    "953.1": lambda p: _mand(traced.path("953.1", C["white"])),
    "816": lambda p: (
        _rect(C["grey"], -0.40, -0.42, 0.40, 0.42, rx=0.04)
        + _rect(C["blue"], -0.37, -0.39, 0.37, 0.39, rx=0.03)
        + _rect(C["white"], -0.08, -0.12, 0.08, 0.28)
        + _rect(C["red"], -0.22, -0.28, 0.22, -0.12)
    ),
    "811": lambda p: (
        _rect(C["grey"], -0.36, -0.48, 0.36, 0.48, rx=0.04)
        + _rect(C["blue"], -0.33, -0.45, 0.33, 0.45, rx=0.03)
        + f'<g transform="translate(-0.10 0)">{_fat_arrow(C["white"], 0, 0.62, 0.14, 0.24)}</g>'
        + f'<g transform="translate(0.12 0)">{_fat_arrow(C["red"], 180, 0.42, 0.12, 0.20)}</g>'
    ),
    # r4: SI 2002 diagram 811.1 "Explanatory plate for the sign shown in diagram 811" (printed p120 = refs/si2002.pdf PDF p120;
    # crop si2002-crops/811.1-p120.png), measured: W/H 1.816, frame 0.046 H, three lines, cap 0.17 H,
    # baselines 0.314 / 0.569 / 0.842 H. Sizes: width (525) 700 (875) (1050) (1400), x-height (37.5) 50 ...
    "811.1": lambda p: (
        _rect(C["black"], -0.65, -0.3579, 0.65, 0.3579, rx=0.06)
        + _rect(C["white"], -0.6171, -0.325, 0.6171, 0.325, rx=0.035)
        + lettering.word("Priority over", 0, -0.194, 0.1217, C["black"], tracking_sw=0.5, part=1, narrow=0.87)
        + lettering.word("oncoming", 0, -0.0115, 0.1217, C["black"], tracking_sw=0.5, part=1, narrow=0.87)
        + lettering.word("vehicles", 0, 0.184, 0.1217, C["black"], tracking_sw=0.5, part=1, narrow=0.87)
    ),
    # r6: 827.1 redrawn from SI 2016 Sch 11 Pt 2 item 66 (printed p213 = tsrgd2016.pdf PDF p214): blue plate, white H, "No A & E".
    "827.1": lambda p: _plate("827.1"),
    "953.2": lambda p: (
        _rect(C["grey"], -0.40, -0.42, 0.40, 0.42, rx=0.04)
        + _rect(C["blue"], -0.37, -0.39, 0.37, 0.39, rx=0.03)
        + _rect(C["white"], -0.22, -0.06, 0.22, 0.12, rx=0.05)
        + _stk(-0.16, -0.14, 0.16, -0.14, 0.04, C["white"])
        + f'<circle cx="-0.12" cy="0.14" r="0.05" fill="{C["white"]}"/>'
        + f'<circle cx="0.12" cy="0.14" r="0.05" fill="{C["white"]}"/>'
    ),
    "967": lambda p: _info_rect(_cycle(0, 0.02, 0.55, C["white"])),
    "4007": None,  # filled below
}
GLYPHS["4007"] = GLYPHS["BELISHA"]
# r7: XING_PAR (parallel crossing, not a diagram number) is drawn as its prescribed roadside device: SI 2016
# diagram 4007, "Yellow or fluorescent yellow globe to indicate presence of a Parallel, or Zebra crossing".
GLYPHS["XING_PAR"] = GLYPHS["4007"]
GLYPHS["675A"] = GLYPHS["675"]
GLYPHS["529"] = GLYPHS["526"]
GLYPHS["531.1A"] = GLYPHS["531.1"]
GLYPHS["811A"] = GLYPHS["811"]
GLYPHS["605.3"] = GLYPHS["642.2"]
# r6: 958, 959B and 960 are drawn from their SI 2016 diagrams (traced.PLATES); 959 keeps its old drawer.
for _k in ("958", "959B", "960"):
    GLYPHS[_k] = (lambda k: (lambda p: _plate(k)))(_k)
# r7: 959 is the pre-2016 number of 959B (country.json renumber); draw the 959B diagram.
GLYPHS["959"] = GLYPHS["959B"]


# Placeholder batches (b2+): faces made by the parametric generator. Each traced.PLATES entry with a
# "kind" is one SI diagram: outline from the shared template (warn = _warn triangle, proh = _ring_roundel,
# mand = _mand disc, plate = traced silhouette of any shape), symbols traced per colour, and legends
# re-set in the Schedule 17 stand-in at their measured place (never traced). Source per key in traced.SOURCE.
AUTO_KINDS = ("warn", "proh", "mand", "plate")


def _auto(key: str) -> str:
    kind = traced.PLATES[key].get("kind", "plate")
    if kind == "warn":
        return _warn() + _traced_inner(key)
    if kind == "proh":
        return _ring_roundel() + _traced_inner(key)
    if kind == "mand":
        return _mand(_traced_inner(key))
    return _plate(key)


for _k, _P in traced.PLATES.items():
    if _P.get("kind") in AUTO_KINDS:
        GLYPHS.setdefault(_k, (lambda k: (lambda p: _auto(k)))(_k))


# r12 (WarnTriangle TODO, 2026-11-23): hand fixes after checking each SI page. These override the generator
# (traced.PLATES) drawers for the face only; the traced data stays in traced.py.
def _clip_layer(key: str, fill: str, y_max: float, cid: str) -> str:
    return (f'<clipPath id="{cid}"><rect x="-2" y="-2" width="4" height="{2 + y_max:.4f}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{traced.path(key, fill)}</g>')


# 530.1 = SI 2016 Sch 2 Pt 5 diagram 530.1 (printed p58 = tsrgd2016.pdf PDF p59): two lines, never touching.
GLYPHS["530.1"] = lambda p: (
    traced.path("530.1/0", C["black"]) + traced.path("530.1/1", C["white"])
    + lettering.word("Overhanging", 0, -0.18, 0.20, C["black"], tracking_sw=0.5, part=1)
    + lettering.word("building", 0, 0.14, 0.20, C["black"], tracking_sw=0.5, part=1)
)
# 572 = SI 2016 Sch 2 Pt 5 diagram 572 (printed p60 = tsrgd2016.pdf PDF p61): "1/2 mile" with a stacked fraction
# (1 above-left, 2 below-right, visible slash), set in our Schedule 17 stand-in lettering.
GLYPHS["572"] = lambda p: (
    traced.path("572/0", C["black"]) + traced.path("572/1", C["white"])
    # the traced white layer has knock-outs where the traced fraction was; cover them, then set our own 1/2
    + _rect(C["white"], -0.90, -0.33, -0.36, 0.33)
    + lettering.word("1", -0.79, -0.105, 0.18, C["black"], part=2)
    + lettering._slant(C["black"], -0.60, -0.225, -0.715, 0.225, round(0.18 / lettering.CAP_SW, 4))
    + lettering.word("2", -0.52, 0.115, 0.18, C["black"], part=2)
    + lettering.word("mile", 0.2682, -0.0196, 0.3799, C["black"], tracking_sw=0.5, part=2, narrow=0.814)
)
# 787 = SI 2016 Sch 11 Pt 2 diagram 787 (printed p215 = tsrgd2016.pdf PDF p216), SOS alternative type
# (150 x 325): handset kept inside the yellow panel (traced handset, scaled to 0.78 about its centre), "SOS" below.
GLYPHS["787"] = lambda p: (
    traced.path("787/0", C["yellow"])
    + '<g transform="translate(0.0 -0.25) scale(0.78) translate(0.0 0.25)">'
    + _clip_layer("787/1", C["black"], 0.58, "c787") + "</g>"
    + lettering.word("SOS", 0, 0.74, 0.26, C["black"], tracking_sw=0.6, part=2)
)
# 778 = SI 2016 Sch 9 Pt 2 diagram 778 (printed p138 = tsrgd2016.pdf PDF p139): steam locomotive on a white square
# plate with a black border. The locomotive is the one traced from SI 2016 diagram 771 (same pictogram).
GLYPHS["778"] = lambda p: (
    _rect(C["black"], -0.48, -0.48, 0.48, 0.48, rx=0.06)
    + _rect(C["white"], -0.43, -0.43, 0.43, 0.43, rx=0.03)
    + '<g transform="scale(1.32) translate(0.002 -0.2515)">' + traced.path("771", C["black"]) + "</g>"
)
# 526 (pre-2016 number; SI 2016 renumbered it 529, Sch 2 Pt 2, printed p44 = tsrgd2016.pdf PDF p45): same opening
# bridge, the symbol scaled 0.74 and nudged down-left so it keeps clear of the red frame.
_OPEN_BRIDGE = GLYPHS["526"]
GLYPHS["526"] = lambda p: (
    _warn() + '<g transform="translate(-0.05 0.16) scale(0.74) translate(0 -0.10)">'
    + _OPEN_BRIDGE(p).replace(_warn(), "", 1) + "</g>"
)
GLYPHS["529"] = GLYPHS["526"]
# 532.3 = SI 2002 Sch 1 diagram 532.3 (printed p61 = refs/si2002.pdf PDF p61): the headroom triangle as mounted at
# an arch bridge; face = large pointer, 14'-6", small pointer, all inside the white field (no dimension lines).
GLYPHS["532.3"] = lambda p: _headroom_tri(["14'-6\""], lower_arrow=True)


# Declared legend fields (validator: every legend word must sit in one, with clearance).
_GIVEWAY_PTS = _scale_about(_eq_pts(WARN_RED_H, False, by_height=True), GIVEWAY_K, _centroid(_eq_pts(WARN_RED_H, False, by_height=True)))
for _ids, _fields in (
    (("530", "530A", "523.1", "524.1", "552", "554", "554.1", "562", "818.2"), [WARN_FIELD]),
    (("670", "629.2A", "629.2", "622.1A", "629", "629A", "629.1"), [RING_FIELD]),
    (("672", "673", "953"), [BLUE_DISC_FIELD]),
    (("674",), [("rect", -0.37, -0.59, 0.37, 0.59), ("circle", 0.0, -0.18, 0.19)]),
    (("602",), [("poly", _GIVEWAY_PTS, WARN_WHITE_SW / 2)]),
    (("601.1",), [("poly", _octagon_pts(0.455), 0.0)]),
    (("4003",), [("rect", -0.18, -0.34, 0.18, -0.04)]),
    (("801",), [("rect", -0.39, -0.33, 0.39, 0.33)]),
    (("2901",), [("rect", -0.50, -0.50, 0.50, 0.50)]),
    (("642.2", "605.3"), [("circle", 0.0, 0.0, 0.40)]),
    (("646",), [("rect", -0.4932, -0.3122, 0.4932, 0.3122)]),
    (("626.2A",), [("rect", -0.2634, -0.4885, 0.2634, -0.2053), ("rect", -0.2634, 0.3082, 0.2634, 0.4885), ("circle", 0.0, 0.0525, 0.1704)]),
    (("777",), [("rect", -0.76, -0.36, 0.76, 0.36)]),
    (("787",), [("rect", -0.46, 0.52, 0.46, 0.98)]),
    (("811.1",), [("rect", -0.617, -0.325, 0.617, 0.325)]),
    (("660",), [("rect", -0.5688, -0.3, 0.5688, 0.3), ("rect", -0.4903, -0.1956, -0.1047, 0.1902)]),
    (("608",), [("rect", -0.6694, -0.2634, 0.6694, 0.2634)]),
    (("607",), [("rect", -0.625, -0.2015, 0.625, 0.2015)]),
    (("546",), [("rect", -0.5300, -0.2015, 0.5300, 0.2015)]),
):
    for _i in _ids:
        LEGEND_FIELDS[_i] = _fields
for _k, _P in traced.PLATES.items():
    if _P["fields"]:
        LEGEND_FIELDS[_k] = [tuple(f) for f in _P["fields"]]
for _a, _b in (("959", "959B"), ("675", "675A")):
    LEGEND_FIELDS[_a] = LEGEND_FIELDS[_b]
for _k in ("531.1", "531.1A"):
    LEGEND_FIELDS[_k] = [WARN_FIELD]
for _k, _P in traced.PLATES.items():
    if _P.get("kind") == "warn":
        LEGEND_FIELDS[_k] = [WARN_FIELD]


def _first_shape_bbox(inner: str):
    """Bounding box of the first top-level shape (the plate) of a face, or None.

    None when the face opens with a transformed group or a path, which this
    cheap reader does not measure."""
    body = re.sub(r"<defs>.*?</defs>", "", inner, flags=re.S)
    m = re.search(r"<(g|path|circle|rect|polygon|ellipse)\b[^>]*>", body)
    if not m or m.group(1) in ("g", "path"):
        return None
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(0)))
    sw = float(a.get("stroke-width") or 0) / 2 if a.get("stroke", "none") != "none" else 0.0
    k = m.group(1)
    if k == "circle":
        cx, cy, r = float(a["cx"]), float(a["cy"]), float(a["r"])
        return cx - r - sw, cy - r - sw, cx + r + sw, cy + r + sw
    if k == "ellipse":
        cx, cy, rx, ry = (float(a[q]) for q in ("cx", "cy", "rx", "ry"))
        return cx - rx - sw, cy - ry - sw, cx + rx + sw, cy + ry + sw
    if k == "rect":
        x, y, w, h = (float(a[q]) for q in ("x", "y", "width", "height"))
        return x - sw, y - sw, x + w + sw, y + h + sw
    pts = [tuple(map(float, q.split(","))) for q in a["points"].split()]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs) - sw, min(ys) - sw, max(xs) + sw, max(ys) + sw


_NUM = r'-?\d*\.?\d+(?:e-?\d+)?'
def _whole_bbox(inner: str):
    """r11 D1: bbox of every shape in the face (stroke included). Returns "T" when the face uses a
    transform and "P" for a path with relative or arc commands (not measured here), else None/(x0,y0,x1,y1)."""
    body=re.sub(r"<defs>.*?</defs>","",inner,flags=re.S)
    body=re.sub(r"<clipPath\b.*?</clipPath>","",body,flags=re.S)
    if 'transform=' in body: return 'T'
    xs=[];ys=[]
    for m in re.finditer(r"<(path|circle|rect|polygon|polyline|ellipse|line)\b[^>]*>",body):
        a=dict(re.findall(r'([\w-]+)="([^"]*)"',m.group(0)))
        sw=float(a.get("stroke-width") or 0)/2 if a.get("stroke","none")!="none" else 0.0
        k=m.group(1)
        if k=="circle":
            cx,cy,r=float(a["cx"]),float(a["cy"]),float(a["r"]); b=[(cx-r,cy-r),(cx+r,cy+r)]
        elif k=="ellipse":
            cx,cy,rx,ry=(float(a[q]) for q in("cx","cy","rx","ry")); b=[(cx-rx,cy-ry),(cx+rx,cy+ry)]
        elif k=="rect":
            x,y,w,h=(float(a.get(q,0)) for q in("x","y","width","height")); b=[(x,y),(x+w,y+h)]
        elif k=="line":
            b=[(float(a["x1"]),float(a["y1"])),(float(a["x2"]),float(a["y2"]))]
        elif k in("polygon","polyline"):
            v=[float(t) for t in re.findall(_NUM, a["points"])]; b=list(zip(v[::2],v[1::2]))
        else:
            d=a.get("d","")
            if re.search(r"[a-ln-zA-LN-Z]",re.sub(r"[MLCQZz]","",d)) or re.search(r"[mlcqhvsta]",d): return 'P'
            v=[float(t) for t in re.findall(_NUM, d)]; b=list(zip(v[::2],v[1::2]))
        for x,y in b: xs+= [x-sw,x+sw]; ys+=[y-sw,y+sw]
    if not xs: return None
    return min(xs),min(ys),max(xs),max(ys)


# r12 overrides drawn from traced layers this bbox reader cannot measure (clip paths, traced path data):
# the aspect of the traced plate layer (/0), i.e. what the face had before the override.
_PLATE_ASPECT = {"530.1": 2.441, "572": round(1.274 / 0.6, 4), "787": round(0.278 / 0.6, 4)}


def drawn_aspect(sign_id: str, renderer: str | None = None, param=None) -> float | None:
    """D1: width/height of the whole drawn face (bbox of all shapes, r11); faces this reader cannot measure
    (transforms, relative/arc paths) fall back to the first shape (the plate). None if unmeasured."""
    if sign_id in _PLATE_ASPECT:
        return _PLATE_ASPECT[sign_id]
    inner = glyph(sign_id, param) or (glyph(str(renderer), param) if renderer else "")
    if not inner:
        return None
    b = _whole_bbox(inner)
    if not isinstance(b, tuple):
        b = _first_shape_bbox(inner)
    if not b or b[3] <= b[1]:
        return None
    return (b[2] - b[0]) / (b[3] - b[1])


def sign_svg(sign: dict[str, Any], size: int = 160) -> str:
    renderer = sign.get("renderer") or sign["id"]
    param = sign.get("param")
    inner = glyph(sign["id"], param)
    if not inner:
        inner = glyph(str(renderer), param)
    if not inner:
        inner = family_face(sign.get("family") or "", param, label=str(sign.get("id") or ""))
    d = sign.get("dimensions_m") or {}
    pw = float(d.get("plate_width") or 1.0)
    ph = float(d.get("plate_height") or pw)
    aspect = ph / pw if pw else 1.0
    px = size
    py = max(1, round(size * aspect))
    # Letterbox the drawing so glyphs stay undistorted while the canvas
    # aspect matches plate_width / plate_height.
    if aspect >= 1:
        vb_h = 1.4 * aspect
        vb = f"-0.7 {-vb_h / 2:.4f} 1.4 {vb_h:.4f}"
    else:
        vb_w = 1.4 / aspect
        vb = f"{-vb_w / 2:.4f} -0.7 {vb_w:.4f} 1.4"
    return _svg(px, py, inner, vb)


def _dashes(w: float) -> str:
    s = ""
    for i in range(5):
        s += _rect("#F4F4F0", -0.75 + i * 0.32, -w / 2, -0.58 + i * 0.32, w / 2)
    return s


def _dash_pair(w: float, gap: float, mark: float, n: int) -> str:
    s = ""
    for row in range(2):
        y = -gap / 2 - w if row == 0 else gap / 2
        for i in range(n):
            s += _rect("#F4F4F0", -0.6 + i * (mark + 0.15), y, -0.6 + i * (mark + 0.15) + mark, y + w)
    return s


MARK_SPAN_M = 12.0  # longitudinal faces show this many metres
MARK_INK = "#F4F4F0"


def _u(metres: float, span: float = MARK_SPAN_M) -> float:
    """Metres → viewBox x units (viewBox width 2 = span metres)."""
    return metres * (2.0 / span)


def marking_svg(m: dict[str, Any], size: int = 220) -> str:
    px = size
    mid = m["id"]
    r = m.get("renderer") or ""
    d = m.get("dimensions_m") or {}
    inner = ""

    def dash_from_dims(colour=MARK_INK):
        mark = float(d.get("mark") or 2.0)
        gap = float(d.get("gap") or 4.0)
        width = float(d.get("width") or 0.10)
        mu, gu, wu = _u(mark), _u(gap), _u(width)
        x = -0.95
        s = ""
        while x < 0.95:
            x1 = min(x + mu, 0.95)
            s += _rect(colour, x, -wu / 2, x1, wu / 2)
            x = x1 + gu
        return s

    def solid_from_dims(colour=MARK_INK, vertical=True):
        width = float(d.get("width") or 0.30)
        wu = _u(width, span=6.0)
        if vertical:
            # transverse stop line: bar across the carriageway
            return _rect(colour, -wu / 2, -0.45, wu / 2, 0.45)
        return _rect(colour, -0.9, -wu / 2, 0.9, wu / 2)

    if r == "dash" or mid in ("1008", "1008.1", "1004", "1004.1", "1005", "1005.1", "1010", "1003.1", "1003.3"):
        inner = dash_from_dims()
    elif r == "give_way" or mid in ("1003", "1003A"):
        mark = float(d.get("mark") or 0.6)
        gap = float(d.get("gap") or 0.3)
        width = float(d.get("width") or 0.20)
        pair = float(d.get("pair_gap") or 0.30)
        mu, gu, wu, pu = _u(mark, 4), _u(gap, 4), _u(width, 4), _u(pair, 4)
        s = ""
        for row, y0 in enumerate((-pu / 2 - wu, pu / 2)):
            x = -0.7
            while x < 0.7:
                s += _rect(MARK_INK, x, y0, x + mu, y0 + wu)
                x += mu + gu
        inner = s
    elif r == "solid" or mid in ("1001", "1002.1", "1012.1"):
        inner = solid_from_dims(vertical=mid in ("1001", "1002.1"))
    elif r == "double_solid" or mid == "1013.1":
        width = float(d.get("width") or 0.10)
        gap = float(d.get("gap") or 0.09)
        wu, gu = _u(width), _u(gap)
        inner = _rect(MARK_INK, -0.9, -wu - gu / 2, 0.9, -gu / 2) + _rect(MARK_INK, -0.9, gu / 2, 0.9, wu + gu / 2)
    elif r == "mini_disc" or mid == "1003.4":
        rad = 0.22
        inner = f'<circle cx="0" cy="0" r="{rad}" fill="{MARK_INK}"/>' + "".join(
            _circ_arrow(MARK_INK, 0.38, a, 70, 0.06, 0.10) for a in (20, 140, 260)
        )
    elif r == "gw_triangle" or mid in ("1023", "1023A"):
        length = float(d.get("length") or 3.75)
        base = float(d.get("base") or 1.25)
        stroke = float(d.get("stroke") or 0.15)
        # scale triangle into the viewBox by length
        k = 0.9 / max(length, 1)
        h, b, st = length * k, base * k, stroke * k
        inner = (
            f'<polygon points="0,{-h/2:.3f} {b/2:.3f},{h/2:.3f} {-b/2:.3f},{h/2:.3f}" '
            f'fill="none" stroke="{MARK_INK}" stroke-width="{st:.3f}" stroke-linejoin="round"/>'
        )
    elif r == "zebra" or mid == "zebra-stripes":
        stripe = float(d.get("stripe") or 0.60)
        su = _u(stripe, span=8)
        inner = ""
        x = -0.9
        i = 0
        while x < 0.9:
            if i % 2 == 0:
                inner += _rect(MARK_INK, x, -0.35, min(x + su, 0.9), 0.35)
            x += su
            i += 1
    elif r == "studs" or mid == "1055.1":
        size_m = float(d.get("size") or 0.10)
        pitch = float(d.get("pitch") or 0.50)
        su, pu = _u(size_m, 6), _u(pitch, 6)
        inner = ""
        y = -0.3
        while y < 0.3:
            x = -0.8
            while x < 0.8:
                inner += _rect(MARK_INK, x, y, x + su, y + su)
                x += pu
            y += pu
    elif r == "zigzag" or mid in ("1001.3", "1001.4"):
        amp = float(d.get("amplitude") or 0.25)
        n = int(d.get("count") or 8)
        au = _u(amp, 8)
        pts = []
        for i in range(n + 1):
            x = -0.85 + i * (1.7 / n)
            y = au if i % 2 else -au
            pts.append(f"{x:.3f},{y:.3f}")
        inner = f'<polyline points="{" ".join(pts)}" fill="none" stroke="{MARK_INK}" stroke-width="0.04"/>'
    elif r == "double_yellow" or mid == "1018.1":
        width = float(d.get("width") or 0.075)
        gap = float(d.get("gap") or 0.075)
        wu, gu = _u(width), _u(gap)
        inner = _rect(C["yellow"], -0.9, -wu - gu / 2, 0.9, -gu / 2) + _rect(C["yellow"], -0.9, gu / 2, 0.9, wu + gu / 2)
    elif r == "solid_yellow" or mid == "1017":
        width = float(d.get("width") or 0.075)
        wu = _u(width)
        end = float(d.get("end_mark") or 0.30)
        eu = _u(end)
        inner = (
            _rect(C["yellow"], -0.9, -wu / 2, 0.9, wu / 2)
            + _rect(C["yellow"], -0.9, -eu / 2, -0.9 + wu, eu / 2)
            + _rect(C["yellow"], 0.9 - wu, -eu / 2, 0.9, eu / 2)
        )
    elif r == "deflection" or mid == "1014":
        inner = (
            f'<path d="M -0.15,0.45 Q 0.05,0.10 0.22,-0.05" fill="none" stroke="{MARK_INK}" '
            f'stroke-width="0.07" stroke-linecap="butt"/>'
            f'<polygon points="0.28,-0.22 0.08,0.02 0.36,0.00" fill="{MARK_INK}"/>'
        )
    elif r == "arrow" or mid == "1038":
        inner = _rect(MARK_INK, -0.08, -0.15, 0.08, 0.45) + f'<polygon points="0,-0.5 0.22,-0.05 -0.22,-0.05" fill="{MARK_INK}"/>'
    elif r == "stop_word" or mid == "1022":
        h = 0.28
        inner = f'<g transform="scale(1,1.75)">{_word("STOP", 0, 0.02, h / 1.75, MARK_INK, tracking=0.02)}</g>'
    else:
        inner = dash_from_dims() if d.get("mark") else solid_from_dims(vertical=False)
    bg = '<rect x="-1" y="-0.65" width="2" height="1.3" fill="#3a3d36"/>'
    return _svg(px, 90, bg + inner, "-1 -0.65 2 1.3")


# r9: furniture faces. Each is drawn to one scale per face (metres -> face units) with the base standing on a
# ground line at y = GROUND; sources per face below and in countries/uk/furniture.json.
GROUND = 0.95


def _ground() -> str:
    return _rect(C["cap"], -0.78, GROUND, 0.78, GROUND + 0.012)


def _belisha_furniture() -> str:
    # SI 2016 diagram 4007 (Sch 14 Pt 2 item 27, printed p461): globe 275-335 mm sitting directly on the post,
    # post 2100-3100 mm from the ground to the globe. Sch 14 Pt 4 para 13(3) (printed p494): alternate black and
    # white bands 275-335 mm, lowest band black and up to 1 m. Drawn: globe 0.30 m, post 2.3 m (inside the
    # 2.1-3.1 m range), lowest black band 0.8 m then five 0.3 m bands (W B W B W). Post width 0.078 m is the
    # 4007 diagram's post/globe ratio (0.26) x 0.30 m.
    k = 1.8 / 2.6
    w = 0.078 * k / 2
    out = ""
    y = GROUND
    for i, h in enumerate([0.8] + [0.3] * 5):
        fill = C["black"] if i % 2 == 0 else C["white"]
        out += _rect(fill, round(-w, 4), round(y - h * k, 4), round(w, 4), round(y, 4))
        y -= h * k
    out += (f'<rect x="{-w:.4f}" y="{y:.4f}" width="{2 * w:.4f}" height="{GROUND - y:.4f}" fill="none" '
            f'stroke="{C["black"]}" stroke-width="0.006"/>')
    r = 0.15 * k
    out += (f'<circle cx="0" cy="{y - r:.4f}" r="{r:.4f}" fill="{C["fluorescent_yellow"]}" '
            f'stroke="{C["black"]}" stroke-width="0.006"/>')
    return out + _ground()


def _chs(d_m: float) -> str:
    # CHS posts: outside diameters in true ratio (76 : 114 : 219, one scale for all three, 219 mm -> 0.20);
    # the post height is schematic (not to scale). Planted post standing on the ground line; black cap.
    d = round(d_m * 0.20 / 0.219, 4)
    return (
        _rect(C["galv"], -d / 2, -0.70, d / 2, GROUND)
        + _rect(C["cap"], round(-d * 0.6, 4), -0.74, round(d * 0.6, 4), -0.68)
        + _ground()
    )


def _two_post(spacing: float, dia: float, underside: float, plate_w: float, plate_h: float, border: bool) -> str:
    # True scale from furniture.json (spacing, diameter, underside); posts run from the ground to the plate top.
    k = min(1.8 / (underside + plate_h), 1.5 / max(plate_w, spacing + dia))
    top = GROUND - (underside + plate_h) * k
    out = ""
    for cx in (-spacing / 2, spacing / 2):
        out += _rect(C["galv"], round((cx - dia / 2) * k, 4), round(top, 4), round((cx + dia / 2) * k, 4), GROUND)
    x0, x1 = round(-plate_w / 2 * k, 4), round(plate_w / 2 * k, 4)
    y1 = round(GROUND - underside * k, 4)
    if border:
        out += (f'<rect x="{x0}" y="{round(top, 4)}" width="{round(x1 - x0, 4)}" height="{round(y1 - top, 4)}" '
                f'fill="{C["white"]}" stroke="{C["black"]}" stroke-width="0.012"/>')
    else:
        out += _rect(C["white"], x0, round(top, 4), x1, y1)
    return out + _ground()


def _telegraph() -> str:
    # BS 1990-1:1984 Table 1 (preferred sizes, via the TKW summary), 9 m medium pole: top diameter >= 150 mm,
    # >= 220 mm at 1.5 m from the butt; the ground line is taken 1.5 m from the butt (BS 1990 design data, IET
    # guide to wood pole lines), so 7.5 m stands above ground. Drawn true-scale (slight taper, flat top with a
    # rounded weathering). The crossarm with insulators near the top is illustrative: its size and position are
    # UNVERIFIED (no Openreach/BT drawing in the repo); the pole class used by Openreach is also UNVERIFIED.
    k = 1.8 / 7.5
    top = GROUND - 7.5 * k
    wt, wg = 0.15 * k / 2, 0.22 * k / 2
    wood = "#472E1A"
    out = (f'<path d="M{-wg:.4f},{GROUND} L{-wt:.4f},{top + wt:.4f} Q0,{top - wt * 0.6:.4f} {wt:.4f},{top + wt:.4f} '
           f'L{wg:.4f},{GROUND} Z" fill="{wood}"/>')
    ay = top + 0.35 * k
    out += _rect(wood, round(-0.6 * k, 4), round(ay, 4), round(0.6 * k, 4), round(ay + 0.08 * k, 4))
    for x in (-0.5, -0.25, 0.25, 0.5):
        out += _rect("#F2F2F2", round((x - 0.025) * k, 4), round(ay - 0.09 * k, 4), round((x + 0.025) * k, 4), round(ay, 4))
    return out + _ground()


def _pylon() -> str:
    # National Grid L12 D (400 kV double circuit): 46.5 m high, 7.1 m base width, 18.2 m crossarm width
    # (telcontar.net/Power/pylons/L12, figures from the Hinkley Point C submissions). Outline measured from the
    # site's to-scale L12 D STD drawing: bend line at 0.50 H, earthwire peak, three crossarms (13.1 / 18.7 /
    # 14.7 m), lattice bracing simplified to one X per panel. 600 drawing px = 46.5 m.
    u = 1.8 / 600
    X = lambda px: round(px * u, 4)
    Y = lambda py: round(-0.85 + py * u, 4)
    hw = lambda py: 6.5 + (11.5 * py / 300) if py <= 300 else 18 + (27 * (py - 300) / 299)
    st = f'stroke="{C["galv"]}" fill="none" stroke-linejoin="round"'
    pts = [(-hw(0), 0), (hw(0), 0), (hw(300), 300), (hw(599), 599), (-hw(599), 599), (-hw(300), 300)]
    out = f'<polygon points="{" ".join(f"{X(x)},{Y(y)}" for x, y in pts)}" {st} stroke-width="0.018"/>'
    for (t, b, tipy, tip) in ((52, 62, 57, 85), (167, 186, 177, 121.5), (282, 295, 289, 95)):
        for sgn in (-1, 1):
            p = [(sgn * hw(t), t), (sgn * tip, tipy), (sgn * hw(b), b)]
            out += f'<polygon points="{" ".join(f"{X(x)},{Y(y)}" for x, y in p)}" {st} stroke-width="0.014"/>'
    lv = [0, 52, 120, 167, 230, 282, 300, 375, 450, 525, 599]
    for a, b in zip(lv, lv[1:]):
        out += (f'<path d="M{X(-hw(a))},{Y(a)} L{X(hw(b))},{Y(b)} M{X(hw(a))},{Y(a)} L{X(-hw(b))},{Y(b)} '
                f'M{X(-hw(a))},{Y(a)} L{X(hw(a))},{Y(a)}" {st} stroke-width="0.009"/>')
    return out + _ground()


def _portal() -> str:
    # Portal gantry from furniture.json: two 219 mm legs, 8 m minimum span (engine heuristic), 5.5 m clearance to
    # the sign underside (UNVERIFIED, DMRB not checked); panel 2.4 x 1.32 m from the GANTRY_ADS row (working
    # size). Beam depth 0.6 m is illustrative (UNVERIFIED).
    span, leg, clr, pw, ph, beam = 8.0, 0.219, 5.5, 2.4, 1.32, 0.6
    k = min(1.5 / (span + leg), 1.8 / (clr + ph + beam))
    top = GROUND - (clr + ph + beam) * k
    hx = (span / 2 + leg) * k
    out = (_rect(C["galv"], round(-hx, 4), round(top, 4), round(-hx + leg * k, 4), GROUND)
           + _rect(C["galv"], round(hx - leg * k, 4), round(top, 4), round(hx, 4), GROUND)
           + _rect(C["galv"], round(-hx, 4), round(top, 4), round(hx, 4), round(top + beam * k, 4))
           + _rect(C["motorway"], round(-pw / 2 * k, 4), round(top + beam * k, 4), round(pw / 2 * k, 4),
                   round(GROUND - clr * k, 4)))
    return out + _ground()


def furniture_svg(f: dict[str, Any], size: int = 120) -> str:
    px = size
    fid = f["id"]
    d = f.get("dimensions_m") or {}
    if f.get("placeholder"):
        # Scope placeholder (no figures until sourced); must not impersonate real equipment.
        inner = _placeholder({"cantilever": "CANTILEVER", "vms-text": "VMS TEXT", "vms-pictogram": "VMS PICTO",
                              "lane-signal": "LANE SIG", "verge-ms": "VERGE MS"}.get(f.get("type"), "TODO"))
    elif fid == "belisha":
        inner = _belisha_furniture()
    elif fid in ("chs-76", "chs-114", "chs-219"):
        inner = _chs(float(d.get("diameter")))
    elif fid == "two-post":
        # Plate 1.6 x 0.9 m is illustrative (UNVERIFIED): a generic direction plate wider than the 1.2 m spacing.
        inner = _two_post(d["spacing"], d["diameter"], d["underside"], 1.6, 0.9, False)
    elif fid == "street-name-posts":
        # Plate 1.157 x 0.336 m is the STREET_NAME row (engine-default height x drawn aspect).
        inner = _two_post(d["spacing"], d["diameter"], d["underside"], 1.157, 0.336, True)
    elif fid == "telegraph":
        inner = _telegraph()
    elif fid == "pylon-l12d":
        inner = _pylon()
    elif fid == "gantry-portal":
        inner = _portal()
    else:
        inner = _rect(C["galv"], -0.06, -0.7, 0.06, GROUND) + _ground()
    return _svg(px, px * 1.2, inner, "-0.8 -0.95 1.6 2.0")


def item_svg(kind: str, item: dict[str, Any], size: int | None = None) -> str:
    if kind == "signs":
        return sign_svg(item, size or 160)
    if kind == "markings":
        return marking_svg(item, size or 220)
    if kind == "furniture":
        return furniture_svg(item, size or 120)
    raise ValueError(f"unknown kind {kind}")


def render_js() -> str:
    """Generated site/assets/render.js: palette + baked-face URLs, no drawers.

    The browser never redraws faces; it loads site/faces/<country>/<kind>/<id>.svg
    baked by this module. validate.py fails if render.js differs from this output.
    """
    import json as _json
    pal = _json.dumps(C, indent=2, sort_keys=False).replace("\n", "\n  ")
    return (
        "/* GENERATED by tools/atlas/render.py render_js(); do not edit.\n"
        "   Faces are drawn only by render.py and baked to site/faces/. This file holds\n"
        "   the same palette and the baked-face URL rule, so it cannot drift from the\n"
        "   Python drawing code. Regenerate: python3 tools/rebuild.py --all */\n"
        "(function (global) {\n"
        f"  const C = {pal};\n"
        "  function faceSrc(kind, id, country) {\n"
        "    return \"faces/\" + (country || \"uk\") + \"/\" + kind + \"/\" + encodeURIComponent(id) + \".svg\";\n"
        "  }\n"
        "  // Live drawers were removed in QA r1 (they had drifted: 384/413 faces differed).\n"
        "  function none() { return \"\"; }\n"
        "  global.AtlasRender = { signSVG: none, markingSVG: none, furnitureSVG: none, familyFace: none, faceSrc, colours: C };\n"
        "})(window);\n"
    )
