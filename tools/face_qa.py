#!/usr/bin/env python3
"""Systemic face checks from qa/TODO-WARN-TRIANGLE-QA.md, applied to procedural sign faces.

(a) inset   : legend ink keeps a clear gap to the border colour (WarnTriangle / Prohibitory / Mandatory).
(b) overlap : legend word boxes (render.legend_log) never overlap each other on a glyph face.
(c) islands : small disconnected legend components inside a pictogram with no legend words
              (detached feet, stray dashes).
(d) pairs   : byte-identical baked faces must be listed in countries/uk/identical_pairs.json, and every
              listed pair must still be identical.

(a) and (c) rasterise the baked SVG with rsvg-convert at 256 px. Findings for still-procedural faces
must match qa/face-qa-baseline.json exactly (each entry is a known TODO item or an intended small part);
a new finding, or a baseline entry that no longer occurs, fails validate.py. EPS-sourced and placeholder
faces are skipped (the EPS face supersedes the trace; the procedural face is only the offline fallback).

  python3 tools/face_qa.py                    # print findings vs baseline
  python3 tools/face_qa.py --write-baseline   # rewrite the baseline (review the diff!)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from atlas import catalogue, render  # noqa: E402

FACES = ROOT / "site" / "faces" / "uk" / "signs"
BASELINE = ROOT / "qa" / "face-qa-baseline.json"
PAIRS = ROOT / "countries" / "uk" / "identical_pairs.json"
RASTER_FAMILIES = {"WarnTriangle", "Prohibitory", "Mandatory"}
# r12: procedural faces whose legend sits on a coloured inner panel with no frame (edge check only)
PANEL_FACES = {"787", "788"}
PX = 256
INSET_MIN = 3        # px at 256 px (~1.2 % of the face): legend ink this close to the border is crowding
ISLAND_MAX = 0.0012  # component area / face area below which a legend part counts as a small island


def _hex(h: str) -> tuple[int, int, int]:
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


_RASTER_MEMO: dict = {}


def raster(svg: Path):
    import numpy as np
    from PIL import Image
    key = hashlib.sha256(svg.read_bytes()).hexdigest()
    if key in _RASTER_MEMO:
        return _RASTER_MEMO[key]
    with tempfile.NamedTemporaryFile(suffix=".png") as t:
        subprocess.run(["rsvg-convert", "-w", str(PX), "-h", str(PX), "--keep-aspect-ratio", "-b", "none",
                        "-o", t.name, str(svg)], check=True, capture_output=True)
        _RASTER_MEMO[key] = np.array(Image.open(t.name).convert("RGBA"))
        return _RASTER_MEMO[key]


def _mask(a, rgb, tol=60):
    import numpy as np
    d = ((a[..., :3].astype(int) - np.array(rgb)) ** 2).sum(-1)
    return (d < tol * tol) & (a[..., 3] > 200)


def _components(m):
    """4-connected components; returns list of (area, ys, xs). Pure numpy/python flood fill."""
    import numpy as np
    seen = np.zeros_like(m, bool)
    out = []
    H, W = m.shape
    for y0, x0 in zip(*np.nonzero(m)):
        if seen[y0, x0]:
            continue
        stack, ys, xs = [(y0, x0)], [], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            ys.append(y)
            xs.append(x)
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        out.append((len(ys), ys, xs))
    return out


def _grow(m, k):
    g = m.copy()
    for _ in range(k):
        h = g.copy()
        h[1:] |= g[:-1]; h[:-1] |= g[1:]; h[:, 1:] |= g[:, :-1]; h[:, :-1] |= g[:, 1:]
        g = h
    return g


def edge_check(a, legend) -> list[str]:
    """(e) r12 (Reviewer r1 F6): legend ink keeps clear of the edge of the panel it sits on (the face's outer
    edge: a yellow inner panel such as 787, a Mandatory disc, an EPS face). Skipped when the legend colour
    is itself the outer frame (black-bordered plates), where touching the edge is the design."""
    import numpy as np
    opaque = a[..., 3] > 200
    if not legend.any() or not opaque.any():
        return []
    outside = ~opaque
    outside[0, :] = outside[-1, :] = True   # the raster's own edge counts as outside (a panel that fills it)
    outside[:, 0] = outside[:, -1] = True
    ring = opaque & _grow(outside, 2)
    if ring.any() and (legend & ring).sum() > 0.3 * ring.sum():
        return []
    for k in range(1, INSET_MIN + 1):
        if (_grow(outside, k) & legend).any():
            return [f"edge: legend ink within {k}px of the panel edge at {PX}px (min {INSET_MIN + 1}px)"]
    return []


def raster_checks(fid: str, family: str, has_words: bool = False, svg: Path | None = None,
                  islands: bool = True) -> list[str]:
    import numpy as np
    a = raster(svg or (FACES / (fid.replace("/", "_") + ".svg")))
    C = render.C
    border = _mask(a, _hex(C["red"])) if family != "Mandatory" else np.zeros(a.shape[:2], bool)
    legend = _mask(a, _hex(C["black"])) if family != "Mandatory" else _mask(a, _hex(C["white"]))
    out = []
    if border.any() and legend.any():
        # distance from legend ink to the border colour (Chebyshev, by dilation)
        grown = border.copy()
        for k in range(1, INSET_MIN + 1):
            g = grown.copy()
            g[1:] |= grown[:-1]; g[:-1] |= grown[1:]; g[:, 1:] |= grown[:, :-1]; g[:, :-1] |= grown[:, 1:]
            grown = g
            if (grown & legend).any():
                out.append(f"inset: legend ink within {k}px of the border at {PX}px (min {INSET_MIN + 1}px)")
                break
    out += edge_check(a, legend)
    if islands and legend.any() and not has_words:   # letters are separate components by nature; pictograms only
        face_area = int((a[..., 3] > 200).sum())
        comps = _components(legend)
        big = max(c[0] for c in comps)
        small = [c for c in comps if c[0] < ISLAND_MAX * face_area and c[0] < big]
        if small and len(comps) > 1:
            out.append(f"islands: {len(small)} small disconnected legend part(s) (< {ISLAND_MAX:.2%} of face)")
    return out


def overlap_checks(fid: str, param=None) -> list[str]:
    try:
        log = render.legend_log(fid, param)
    except Exception:  # noqa: BLE001
        return []
    out = []
    for i in range(len(log)):
        for j in range(i + 1, len(log)):
            a, b = log[i], log[j]
            ix = min(a[3], b[3]) - max(a[1], b[1])
            iy = min(a[4], b[4]) - max(a[2], b[2])
            if ix > 1e-6 and iy > 1e-6:
                out.append(f"overlap: legend {a[0]!r} overlaps {b[0]!r}")
    return out


def face_sources() -> dict:
    p = ROOT / "countries" / "uk" / "face_sources.json"
    return json.loads(p.read_text())["faces"] if p.exists() else {}


def findings(atlas: dict | None = None) -> dict[str, list[str]]:
    atlas = atlas or catalogue.load_country("uk", ROOT)
    fs = face_sources()
    have_rsvg = shutil.which("rsvg-convert") is not None
    out: dict[str, list[str]] = {}
    for s in atlas["signs"]:
        fid = s["id"]
        src = (fs.get(fid) or {}).get("source", "procedural")
        if src != "procedural":
            continue
        f = []
        if s.get("glyph"):
            f += overlap_checks(fid, s.get("param"))
        if have_rsvg and s["family"] in RASTER_FAMILIES and s.get("glyph"):
            words = bool(render.legend_log(fid, s.get("param")))
            f += raster_checks(fid, s["family"], words)
        elif have_rsvg and s.get("glyph") and s["id"] in PANEL_FACES:
            import numpy as np
            a = raster(FACES / (fid.replace("/", "_") + ".svg"))
            f += edge_check(a, _mask(a, _hex(render.C["black"])))
        if f:
            out[fid] = f
    # EPS faces (cooked SVGs, gitignored cache): same inset/edge checks; keyed "eps:<id>". Only when cached.
    eps_dir = ROOT / "site" / "faces-eps" / "uk" / "signs"
    if have_rsvg and eps_dir.exists():
        fam = {s["id"]: s["family"] for s in atlas["signs"]}
        for fid, f0 in sorted(fs.items()):
            p = eps_dir / (fid.replace("/", "_") + ".svg")
            if f0.get("source") != "eps" or not p.exists() or fam.get(fid) not in RASTER_FAMILIES:
                continue
            f = [x for x in raster_checks(fid, fam[fid], True, svg=p, islands=False)]
            if f:
                out["eps:" + fid] = f
    return dict(sorted(out.items()))


def pair_check() -> tuple[list[str], list[str]]:
    """(errors, groups found). Groups of byte-identical non-placeholder baked sign faces."""
    by = defaultdict(list)
    for f in sorted(FACES.glob("*.svg")):
        b = f.read_bytes()
        if b"data-placeholder" in b:
            continue
        by[hashlib.sha256(b).hexdigest()].append(f.stem)
    found = sorted(sorted(v) for v in by.values() if len(v) > 1)
    listed = json.loads(PAIRS.read_text())["groups"] if PAIRS.exists() else []
    want = sorted(sorted(g["faces"]) for g in listed)
    errs = []
    for g in found:
        if g not in want:
            errs.append(f"identical faces {g} not listed in countries/uk/identical_pairs.json")
    for g in want:
        if g not in found:
            errs.append(f"identical_pairs.json lists {g} but those faces are no longer byte-identical")
    return errs, found


def compare(atlas: dict | None = None) -> tuple[list[str], dict]:
    """Errors for findings that differ from the baseline (new or stale)."""
    cur = findings(atlas)
    base = json.loads(BASELINE.read_text())["faces"] if BASELINE.exists() else {}
    errs = []
    for fid, f in cur.items():
        known = base.get(fid, {}).get("findings", [])
        for x in f:
            if x not in known:
                errs.append(f"face-qa {fid}: new finding: {x}")
    eps_cached = (ROOT / "site" / "faces-eps" / "uk" / "signs").exists() and shutil.which("rsvg-convert")
    for fid, b in base.items():
        if fid.startswith("eps:") and not eps_cached:
            continue   # EPS faces are only checked when the local cache is built
        for x in b.get("findings", []):
            if x not in cur.get(fid, []):
                errs.append(f"face-qa {fid}: baseline finding no longer occurs (update qa/face-qa-baseline.json): {x}")
    return errs, cur


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-baseline", action="store_true")
    a = ap.parse_args(argv)
    if a.write_baseline:
        if not shutil.which("rsvg-convert"):
            raise SystemExit("rsvg-convert (Debian librsvg2-bin) is needed to write the baseline")
        cur = findings()
        old = json.loads(BASELINE.read_text())["faces"] if BASELINE.exists() else {}
        faces = {k: {"findings": v, "note": old.get(k, {}).get("note", "")} for k, v in cur.items()}
        BASELINE.write_text(json.dumps({"about": "Known face-qa findings on still-procedural sign faces "
                                        "(tools/face_qa.py). Each is a qa/TODO-WARN-TRIANGLE-QA.md item or an "
                                        "intended small part; a new finding fails validate.py.",
                                        "faces": faces}, indent=1, sort_keys=True) + "\n")
        print(f"baseline: {len(faces)} face(s), {sum(len(v['findings']) for v in faces.values())} finding(s)")
        return 0
    errs, cur = compare()
    perrs, groups = pair_check()
    print(f"face-qa: {sum(len(v) for v in cur.values())} finding(s) on {len(cur)} procedural face(s); "
          f"{len(errs)} differ from baseline; identical groups {len(groups)}, {len(perrs)} unlisted/stale")
    for e in errs + perrs:
        print("ERROR", e)
    return 1 if errs or perrs else 0


if __name__ == "__main__":
    raise SystemExit(main())
