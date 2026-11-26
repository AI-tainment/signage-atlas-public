#!/usr/bin/env python3
"""Deterministic EPS -> SVG for GOV.UK traffic-sign artwork.

Pipeline: Ghostscript (EPS, -dEPSCrop, pdfwrite in DeviceRGB with default_rgb.icc)
-> PDF -> pdftocairo -svg -> normalise, then the explicit owner colour-rule table.
The ICC step is Art's fix from art/sign-pipeline-20261126 @ 4d859a4, so SVG fills
match Ghostscript's png16m reference exactly or within 1 per 8-bit channel.
Normalising: viewBox from the EPS bounding box at origin 0 0 (2 dp), every number rounded to 2 dp,
rgb(%) colours converted to exact 8-bit hex, then tools/eps/colour_rules.py is applied
(owner, 2026-11-26: official red, process black, 4003 discs only — not a general
palette snap). Other colours stay as the converter emitted them. Off-palette colours
are reported after the rules. Default attributes, ids and XML prolog removed, no
metadata. Same input -> same bytes.

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
from eps import colour_rules, paths  # noqa: E402

SIGN_PALETTE = ("red", "blue", "motorway_blue", "white", "black", "grey", "amber", "green", "brown",
                "primary_green", "yellow", "fluorescent_yellow")


# r12 (F7): the converter versions the byte-identical cache was made with. Other versions may round or
# order paths differently, so tools/eps/build.py refuses them (override: --any-tools) and validate warns
# (an error under --strict) when the cached conversion report was made with other versions.
PINNED_TOOLS = {"ghostscript": "10.05.1", "pdftocairo": "25.03.0"}
ATTRIBUTION = ("Crown copyright. GOV.UK traffic sign artwork (EPS), used under the Open Government Licence v3.0 "
               "(nationalarchives.gov.uk/doc/open-government-licence/version/3/). Converted locally by "
               "signage-atlas tools/eps; keep this notice with any copy.")

# Colour conversion that matches Ghostscript's png16m reference raster.
# Ported from tools/sign_pipeline/convert_raw.py in art/sign-pipeline-20261126
# @ 4d859a4 (Art). Do not reimplement: same flags, same ICC lookup.
COLOUR_METHOD = (
    "gs pdfwrite -sColorConversionStrategy=RGB -dProcessColorModel=/DeviceRGB "
    "-sOutputICCProfile=default_rgb.icc (Ghostscript default RGB ICC, same "
    "family as the png16m device), then pdftocairo -svg. No palette snap. "
    "Chosen so SVG fills match the GS png16m raster exactly or within 1 per "
    "8-bit channel (blue #0079C1, brown #794400, green #00703C / #006F3C)."
)


def default_rgb_icc() -> Path:
    """Return the default_rgb.icc path Ghostscript can read under -dSAFER.

    Do not Path.resolve() this: on this image the file is also visible under
    /usr/share/color/icc/ghostscript/, and -dSAFER refuses that path
    (Permission denied / rangecheck in .installpagedevice). The path under
    /usr/share/ghostscript/<ver>/iccprofiles/ is readable and is the same ICC.
    """
    ver = PINNED_TOOLS["ghostscript"]
    candidates = [
        Path(f"/usr/share/ghostscript/{ver}/iccprofiles/default_rgb.icc"),
    ]
    root = Path("/usr/share/ghostscript")
    if root.exists():
        candidates.extend(sorted(root.glob("*/iccprofiles/default_rgb.icc")))
    for p in candidates:
        if p.is_file():
            return p
    raise FileNotFoundError(
        "Ghostscript default_rgb.icc not found under /usr/share/ghostscript"
    )


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


def rgb_hex(rgb: tuple[float, float, float]) -> str:
    """Exact 8-bit hex of a pdftocairo RGB triple in 0–255. No palette substitution."""
    return "#%02X%02X%02X" % tuple(round(c) for c in rgb)


def is_palette(hexv: str) -> bool:
    global _PAL
    _PAL = _PAL or palette()
    return hexv.upper() in {"#%02X%02X%02X" % c for _, c in _PAL}


_NUM = re.compile(r"-?\d+\.\d+|-?\d+")


def _r(m: re.Match) -> str:
    v = round(float(m.group(0)), 2)
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def normalise(svg: str, report: dict, face_id: str | None = None) -> str:
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"<metadata.*?</metadata>", "", svg, flags=re.S)
    off = set()
    used = set()

    def col(m: re.Match) -> str:
        rgb = tuple(float(x) * 2.55 for x in m.groups())
        raw = rgb_hex(rgb)
        hexv = colour_rules.apply(raw, face_id)
        if hexv != raw:
            used.add(colour_rules.applied_rule(raw, face_id))
        if not is_palette(hexv):
            off.add(hexv)
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
    report["colour_rules"] = sorted(x for x in used if x)
    report["images"] = len(re.findall(r"<image\b", svg))
    report["text"] = len(re.findall(r"<text\b", svg))
    report["bytes"] = len(svg.encode())
    return svg


def convert(eps: Path) -> tuple[str, dict]:
    report: dict = {}
    face_id = eps.stem
    with tempfile.TemporaryDirectory(prefix="sa-eps-") as td:
        pdf = Path(td) / "a.pdf"
        icc = default_rgb_icc()
        report["colour_method"] = COLOUR_METHOD
        report["output_icc"] = str(icc)
        r = subprocess.run(
            ["gs", "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dEPSCrop",
             "-sDEVICE=pdfwrite",
             "-sColorConversionStrategy=RGB",
             "-dProcessColorModel=/DeviceRGB",
             f"-sOutputICCProfile={icc}",
             "-o", str(pdf), str(eps)],
            capture_output=True, text=True,
        )
        if r.returncode or not pdf.exists():
            raise RuntimeError(f"gs failed on {eps.name}: {r.stderr.strip()[:200]}")
        fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
        report["fonts"] = [f.split()[0] for f in fonts if f.strip()]
        r = subprocess.run(["pdftocairo", "-svg", str(pdf), "-"], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"pdftocairo failed on {eps.name}: {r.stderr.strip()[:200]}")
        svg = r.stdout
    return normalise(svg, report, face_id=face_id), report


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
