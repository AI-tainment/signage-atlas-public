#!/usr/bin/env python3
"""Visual check of GOV.UK EPS faces against the atlas's procedural faces (traced from SI 2016).

For every face in countries/uk/face_sources.json with an EPS match (or the --ids given), render both with
rsvg-convert, crop to ink, resize to 128 px, classify pixels to the sign palette and score the legend
(all colour classes except the field and border) by IoU after a 2 px tolerance. A low score on a 2016 row
means either the 2002 artwork differs from the 2016 diagram or the hand trace is off; read the sheet.

Writes (gitignored; contains Crown artwork): qa/renders/eps/<set>/sheet-*.png and scores.json.
  python3 tools/eps/compare.py --family WarnTriangle --set warn-triangle
  python3 tools/eps/compare.py --set all
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eps import convert, paths  # noqa: E402

OUT = paths.ROOT / "qa" / "renders" / "eps"
N = 128


def raster(svg: Path, px: int = 256) -> Image.Image:
    with tempfile.NamedTemporaryFile(suffix=".png") as t:
        subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), "--keep-aspect-ratio", "-o", t.name, str(svg)],
                       check=True, capture_output=True)
        return Image.open(t.name).convert("RGBA").copy()


def crop_norm(im: Image.Image) -> Image.Image:
    a = np.array(im)
    ink = a[..., 3] > 32
    if not ink.any():
        return Image.new("RGBA", (N, N))
    ys, xs = np.where(ink)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return im.resize((N, N), Image.NEAREST)


def classes(im: Image.Image) -> np.ndarray:
    pal = np.array([c for _, c in convert.palette()], dtype=float)
    a = np.array(im).astype(float)
    d = ((a[..., None, :3] - pal[None, None]) ** 2).sum(-1)
    cl = d.argmin(-1)
    cl[a[..., 3] < 128] = -1
    return cl


def legend_iou(p: np.ndarray, e: np.ndarray) -> float:
    vals, counts = np.unique(e[e >= 0], return_counts=True)
    order = [v for _, v in sorted(zip(-counts, vals))]
    drop = order[:2] if len(order) >= 3 else order[:1]
    lm_e = (e >= 0) & ~np.isin(e, drop)
    lm_p = (p >= 0) & ~np.isin(p, drop)
    if not lm_e.any() and not lm_p.any():
        return 1.0
    dil = lambda m: np.array(Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5))) > 0
    inter = (lm_e & dil(lm_p)).sum() + (lm_p & dil(lm_e)).sum()
    return round(float(inter) / float(lm_e.sum() + lm_p.sum()), 3)


def sheet(rows, title: str, path: Path, cols: int = 6) -> None:
    """Grid of pairs: each cell shows the atlas procedural face (before, left) and the EPS (after, right)."""
    cw, ch = 2 * 104 + 12, 104 + 30
    nrow = (len(rows) + cols - 1) // cols
    img = Image.new("RGB", (cols * cw + 10, 26 + nrow * ch), "#EDEDED")
    d = ImageDraw.Draw(img)
    d.text((8, 7), title + "   each cell: atlas procedural (before) | GOV.UK EPS (after)", fill="black")
    for i, (fid, proc, eps, score, note) in enumerate(rows):
        x, y = 8 + (i % cols) * cw, 26 + (i // cols) * ch
        for j, im in enumerate((proc, eps)):
            if im is not None:
                t = crop_norm(im).resize((100, 100))
                img.paste(t, (x + j * 104, y), t)
        d.text((x, y + 103), f"{fid}  IoU {score}", fill="black")
        if note:
            d.text((x, y + 115), note[:34], fill="#A00000")
    img.save(path, optimize=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", action="append")
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--set", default="all")
    ap.add_argument("--per-sheet", type=int, default=36)
    a = ap.parse_args(argv)
    fs = json.loads(paths.FACE_SOURCES.read_text())["faces"]
    want = [(k, f) for k, f in fs.items() if "eps" in f
            and (not a.family or f["family"] in a.family) and (not a.ids or k in a.ids)]
    out = OUT / a.set
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("sheet-*.png"):
        old.unlink()
    scores, rows = {}, []
    for k, f in want:
        epsvg = paths.CACHE / "svg" / (f["eps"] + ".svg")
        procsvg = paths.ROOT / "site" / "faces" / "uk" / "signs" / (k.replace("/", "_") + ".svg")
        e = raster(epsvg)
        p = raster(procsvg)
        en, pn = crop_norm(e), crop_norm(p)
        ph = f.get("fallback", f["source"]) == "placeholder" or f["source"] == "placeholder"
        sc = None if ph else legend_iou(classes(pn), classes(en))
        scores[k] = {"eps": f["eps"], "legend_iou": sc, "source": f["source"], "placeholder_before": ph}
        note = ("placeholder before" if ph else "") + (" [EPS]" if f["source"] == "eps" else "")
        rows.append((k, p, e, sc, note.strip()))
    for i in range(0, len(rows), a.per_sheet):
        sheet(rows[i:i + a.per_sheet], f"{a.set} {i // a.per_sheet + 1}", out / f"sheet-{i // a.per_sheet + 1:02d}.png")
    (out / "scores.json").write_text(json.dumps(scores, indent=1, sort_keys=True) + "\n")
    print(f"{len(rows)} faces, {(len(rows) + a.per_sheet - 1) // a.per_sheet} sheet(s) in {out.relative_to(paths.ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
