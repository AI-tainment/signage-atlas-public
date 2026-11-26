#!/usr/bin/env python3
"""Deterministic EPS -> SVG for GOV.UK traffic-sign artwork.

Pipeline: Ghostscript (EPS, -dEPSCrop) -> PDF -> pdftocairo -svg -> normalise.
Normalising: viewBox from the EPS bounding box at origin 0 0 (2 dp), every number rounded to 2 dp,
rgb(%) colours snapped to the atlas sign palette (countries/uk/country.json; an off-palette colour is
kept and reported). Near-neutral colours (low chroma) only snap to black, white or grey, so a dark grey
cannot land on brown: Euclidean RGB can put (81,78,79) closer to brown than to black (found on 4003.2 /
4003.5 aspect backings, 2026-11-25; the raw EPS is process black, not brown). Default attributes, ids
and XML prolog removed, no metadata. Same input -> same bytes.

Checks per file (returned in the report dict): embedded fonts in the intermediate PDF (pdffonts),
<image> / <text> elements in the SVG, off-palette colours.

  python3 tools/eps/convert.py FILE.eps [-o OUT.svg]
  python3 tools/eps/convert.py --versions
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eps import paths  # noqa: E402

SIGN_PALETTE = ("red", "blue", "motorway_blue", "white", "black", "grey", "amber", "green", "brown",
                "primary_green", "yellow", "fluorescent_yellow")
SNAP = 110.0  # max RGB distance for a palette snap
# Near-neutral inks (max-min RGB at or below this) may only snap to black, white or grey.
# Without this, a dark grey such as pdftocairo's (81, 78, 79) is closer to brown #73451F
# (d≈59.5) than to black #141414 (d≈102.8) and was wrongly snapped to brown.
CHROMA_NEUTRAL = 16.0
NEUTRAL_PALETTE = ("black", "white", "grey")


# r12 (F7): the converter versions the byte-identical cache was made with. Other versions may round or
# order paths differently, so tools/eps/build.py refuses them (override: --any-tools) and validate warns
# (an error under --strict) when the cached conversion report was made with other versions.
PINNED_TOOLS = {"ghostscript": "10.05.1", "pdftocairo": "25.03.0"}
ATTRIBUTION = ("Crown copyright. GOV.UK traffic sign artwork (EPS), used under the Open Government Licence v3.0 "
               "(nationalarchives.gov.uk/doc/open-government-licence/version/3/). Converted locally by "
               "signage-atlas tools/eps; keep this notice with any copy.")


def version_problems(found: dict) -> list[str]:
    out = []
    for k, want in PINNED_TOOLS.items():
        got = found.get(k) or ""
        if want not in got.split() and got != want:
            out.append(f"{k} {got or 'missing'} (pinned {want})")
    return out


def tool_versions() -> dict:
    def out(cmd):
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or r.stderr).strip().splitlines()[0]
    return {"ghostscript": out(["gs", "--version"]), "pdftocairo": out(["pdftocairo", "-v"]),
            "pdffonts": out(["pdffonts", "-v"])}


def palette() -> list[tuple[str, tuple[int, int, int]]]:
    cols = json.loads((paths.ROOT / "countries" / "uk" / "country.json").read_text())["colours"]
    return [(k, tuple(int(cols[k][i:i + 2], 16) for i in (1, 3, 5))) for k in SIGN_PALETTE if k in cols]


_PAL = None


def snap(rgb: tuple[float, float, float]) -> tuple[str, str | None]:
    global _PAL
    _PAL = _PAL or palette()
    pal = _PAL
    if max(rgb) - min(rgb) <= CHROMA_NEUTRAL:
        pal = [kv for kv in _PAL if kv[0] in NEUTRAL_PALETTE]
    best = min(pal, key=lambda kv: sum((a - b) ** 2 for a, b in zip(kv[1], rgb)))
    d = sum((a - b) ** 2 for a, b in zip(best[1], rgb)) ** 0.5
    if d <= SNAP:
        return "#%02X%02X%02X" % best[1], None
    raw = "#%02X%02X%02X" % tuple(round(c) for c in rgb)
    return raw, raw


_NUM = re.compile(r"-?\d+\.\d+|-?\d+")


def _r(m: re.Match) -> str:
    v = round(float(m.group(0)), 2)
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def normalise(svg: str, report: dict) -> str:
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"<metadata.*?</metadata>", "", svg, flags=re.S)
    off = set()

    def col(m: re.Match) -> str:
        rgb = tuple(float(x) * 2.55 for x in m.groups())
        hexv, bad = snap(rgb)
        if bad:
            off.add(bad)
        return hexv
    svg = re.sub(r"rgb\(\s*([\d.]+)%\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)", col, svg)
    for attr in (' fill-opacity="1"', ' stroke-opacity="1"', ' fill-rule="nonzero"', ' stroke-miterlimit="10"'):
        svg = svg.replace(attr, "")
    # round every number inside geometry-bearing attributes
    svg = re.sub(r'\b(d|points|transform|x|y|width|height|viewBox|stroke-width|x1|y1|x2|y2|cx|cy|r|rx|ry)="([^"]*)"',
                 lambda m: f'{m.group(1)}="{_NUM.sub(_r, m.group(2))}"', svg)
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"', svg)
    vb = [float(x) for x in m.group(1).split()] if m else [0, 0, 1, 1]
    w, h = vb[2], vb[3]
    disp_w, disp_h = (160, round(160 * h / w)) if w >= h else (round(160 * w / h), 160)
    svg = re.sub(r"<svg\b[^>]*>",
                 f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                 f'viewBox="{_NUM.sub(_r, " ".join(map(str, vb)))}" width="{disp_w}" height="{disp_h}" '
                 f'role="img" data-source="eps"><desc>{ATTRIBUTION}</desc>', svg, count=1)
    svg = "\n".join(line.rstrip() for line in svg.strip().splitlines() if line.strip()) + "\n"
    report["off_palette"] = sorted(off)
    report["images"] = len(re.findall(r"<image\b", svg))
    report["text"] = len(re.findall(r"<text\b", svg))
    report["bytes"] = len(svg.encode())
    return svg


def convert(eps: Path) -> tuple[str, dict]:
    report: dict = {}
    with tempfile.TemporaryDirectory(prefix="sa-eps-") as td:
        pdf = Path(td) / "a.pdf"
        r = subprocess.run(["gs", "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dEPSCrop", "-sDEVICE=pdfwrite",
                            "-o", str(pdf), str(eps)], capture_output=True, text=True)
        if r.returncode or not pdf.exists():
            raise RuntimeError(f"gs failed on {eps.name}: {r.stderr.strip()[:200]}")
        fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
        report["fonts"] = [f.split()[0] for f in fonts if f.strip()]
        r = subprocess.run(["pdftocairo", "-svg", str(pdf), "-"], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"pdftocairo failed on {eps.name}: {r.stderr.strip()[:200]}")
        svg = r.stdout
    return normalise(svg, report), report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("eps", nargs="?", type=Path)
    ap.add_argument("-o", type=Path)
    ap.add_argument("--versions", action="store_true")
    a = ap.parse_args(argv)
    if a.versions or not a.eps:
        print(json.dumps(tool_versions(), indent=1))
        return 0
    svg, rep = convert(a.eps)
    (a.o.write_text(svg) if a.o else sys.stdout.write(svg))
    print(json.dumps(rep), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
