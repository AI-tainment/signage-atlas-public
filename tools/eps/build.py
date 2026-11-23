#!/usr/bin/env python3
"""Convert every cached GOV.UK EPS to SVG, then place EPS-sourced atlas faces for the wiki.

  python3 tools/eps/build.py              # all 702 -> .cache/eps/svg/, faces -> site/faces-eps/uk/signs/
  python3 tools/eps/build.py --twice      # convert twice into separate trees and require byte-identical output
  python3 tools/eps/build.py --faces-only # only (re)place faces listed in countries/uk/face_sources.json

Inputs must already be in the cache (tools/eps/fetch.py). Outputs are gitignored and never committed:
the EPS artwork is Crown copyright (OGL v3.0) and, like GridForge's cooker, is cooked where it is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eps import convert, paths  # noqa: E402


def eps_files() -> list[Path]:
    return sorted(p for p in paths.RAW.rglob("*") if p.suffix.lower() == ".eps" and p.is_file())


def key(p: Path) -> str:
    """Crosswalk key: <zip>/<path inside zip>."""
    return p.relative_to(paths.RAW).as_posix()


def _one(args):
    src, dst = args
    try:
        svg, rep = convert.convert(Path(src))
    except Exception as e:  # noqa: BLE001
        return src, {"error": str(e)}
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(svg)
    rep["sha256"] = hashlib.sha256(svg.encode()).hexdigest()
    return src, rep


def convert_all(out: Path, jobs: int) -> dict:
    files = eps_files()
    work = [(str(p), str(out / (key(p) + ".svg"))) for p in files]
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        res = dict(ex.map(_one, work, chunksize=8))
    files_rep = {key(Path(s)): res[s] for s, _ in work}
    rep = {"tools": convert.tool_versions(), "count": len(files_rep),
           "errors": sum(1 for r in files_rep.values() if "error" in r),
           "with_fonts": sum(1 for r in files_rep.values() if r.get("fonts")),
           "with_images": sum(1 for r in files_rep.values() if r.get("images")),
           "with_text": sum(1 for r in files_rep.values() if r.get("text")),
           "files": files_rep}
    (out / "convert-report.json").write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
    return rep


def place_faces(svg_root: Path) -> int:
    fs = json.loads(paths.FACE_SOURCES.read_text()) if paths.FACE_SOURCES.exists() else {"faces": {}}
    dst = paths.OUT / "signs"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    n = 0
    for fid, f in sorted(fs["faces"].items()):
        if f.get("source") != "eps":
            continue
        src = svg_root / (f["eps"] + ".svg")
        if not src.exists():
            print(f"MISSING converted EPS for {fid}: {f['eps']}", file=sys.stderr)
            continue
        (dst / (fid.replace("/", "_") + ".svg")).write_bytes(src.read_bytes())
        n += 1
    (paths.OUT / "README.txt").write_text(
        "Converted from the GOV.UK traffic-sign EPS (Crown copyright, OGL v3.0). Committed with attribution\n"
        "under the owner's ruling (2026-11-23); the raw EPS and zips stay in the local cache, not in git.\n"
        "May be published with this attribution: Crown copyright, Open Government Licence v3.0\n"
        "(https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Each SVG carries it in <desc>;\n"
        "tools/eps/deploy_guard.py checks that before publishing.\n"
        "Rebuild: python3 tools/eps/fetch.py && python3 tools/eps/build.py\n")
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--twice", action="store_true")
    ap.add_argument("--faces-only", action="store_true")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--any-tools", action="store_true", help="convert with unpinned gs/pdftocairo versions (warns)")
    a = ap.parse_args(argv)
    bad = convert.version_problems(convert.tool_versions())
    if bad and not a.faces_only:
        print("converter version mismatch: " + "; ".join(bad), file=sys.stderr)
        if not a.any_tools:
            print("refusing to convert (pass --any-tools to override; output may not be byte-identical)", file=sys.stderr)
            return 1
    svg_root = paths.CACHE / "svg"
    if not a.faces_only:
        if not eps_files():
            print("no EPS in cache; run tools/eps/fetch.py first", file=sys.stderr)
            return 1
        rep = convert_all(svg_root, a.jobs)
        print(f"converted {rep['count']} EPS: errors {rep['errors']}, fonts {rep['with_fonts']}, "
              f"images {rep['with_images']}, text {rep['with_text']}; tools {rep['tools']}")
        if a.twice:
            alt = paths.CACHE / "svg-run2"
            shutil.rmtree(alt, ignore_errors=True)
            rep2 = convert_all(alt, a.jobs)
            diff = [k for k in rep["files"] if rep["files"][k].get("sha256") != rep2["files"].get(k, {}).get("sha256")]
            print(f"second run: {len(rep2['files']) - len(diff)}/{len(rep2['files'])} byte-identical")
            shutil.rmtree(alt, ignore_errors=True)
            if diff:
                print("DIFF: " + " ".join(diff[:20]))
                return 1
        if rep["errors"] or rep["with_fonts"]:
            return 1
    n = place_faces(svg_root)
    print(f"placed {n} EPS-sourced face(s) under {paths.OUT.relative_to(paths.ROOT)}/signs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
