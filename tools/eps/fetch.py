#!/usr/bin/env python3
"""Fetch the 18 GOV.UK traffic-sign EPS zips once, politely, into the gitignored cache.

Policy (GridForge docs/sources/uk-traffic-signs.md): honest User-Agent, serial downloads,
>= 1 s between requests (default 3 s), up to 3 retries with backoff, SHA-256 verified against
countries/uk/sources/eps/manifest.csv. A zip already cached with the right hash is not re-fetched.

  python3 tools/eps/fetch.py            # fetch missing zips, verify all, unzip into the cache
  python3 tools/eps/fetch.py --verify   # offline: verify cached zips only
  python3 tools/eps/fetch.py --seed-from DIR   # reuse zips already on this machine (hash-checked), fetch the rest
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eps import paths  # noqa: E402

UA = "SignageAtlas-EPS-fetch/1.0 (AI-tainment; one-off cache of GOV.UK traffic-sign EPS; https://github.com/AI-tainment/signage-atlas)"


def manifest() -> list[dict]:
    with open(paths.MANIFEST, newline="") as fh:
        return list(csv.DictReader(fh))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def verify(row: dict) -> str | None:
    p = paths.ZIPS / row["file"]
    if not p.exists():
        return "missing"
    if p.stat().st_size != int(row["bytes"]):
        return f"size {p.stat().st_size} != {row['bytes']}"
    if sha256(p) != row["sha256"]:
        return "sha256 mismatch"
    return None


def fetch(row: dict, delay: float) -> None:
    dst = paths.ZIPS / row["file"]
    tmp = dst.with_suffix(".part")
    for attempt in range(3):
        try:
            req = urllib.request.Request(row["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as fh:
                while b := r.read(1 << 20):
                    fh.write(b)
            tmp.replace(dst)
            return
        except Exception as e:  # noqa: BLE001
            print(f"  retry {attempt + 1} {row['file']}: {e}", file=sys.stderr)
            time.sleep(delay * (2 ** attempt))
    raise SystemExit(f"fetch failed: {row['file']} (cached copy, if any, left in place)")


def unzip(row: dict) -> int:
    dst = paths.RAW / row["file"]
    if dst.exists():
        return sum(1 for _ in dst.rglob("*") if _.suffix.lower() == ".eps")
    dst.mkdir(parents=True)
    n = 0
    with zipfile.ZipFile(paths.ZIPS / row["file"]) as z:
        for info in z.infolist():
            if info.is_dir() or "__MACOSX" in info.filename:
                continue
            out = dst / info.filename
            if not out.resolve().is_relative_to(dst.resolve()):
                raise SystemExit(f"unsafe path in {row['file']}: {info.filename}")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(info))
            n += out.suffix.lower() == ".eps"
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="offline: verify cached zips, fetch nothing")
    ap.add_argument("--seed-from", type=Path, help="copy zips from a local folder first if their SHA-256 matches")
    ap.add_argument("--delay", type=float, default=3.0, help="seconds between requests (min 1)")
    a = ap.parse_args(argv)
    delay = max(1.0, a.delay)
    paths.ZIPS.mkdir(parents=True, exist_ok=True)
    rows = manifest()
    bad = 0
    first = True
    for row in rows:
        why = verify(row)
        if why and a.seed_from and (a.seed_from / row["file"]).exists():
            src = a.seed_from / row["file"]
            if sha256(src) == row["sha256"]:
                (paths.ZIPS / row["file"]).write_bytes(src.read_bytes())
                print(f"seed {row['file']} (local copy, hash ok)")
                why = verify(row)
        if why and not a.verify:
            if not first:
                time.sleep(delay)
            first = False
            print(f"fetch {row['file']} ({int(row['bytes']):,} B)")
            fetch(row, delay)
            why = verify(row)
        if why:
            bad += 1
            print(f"FAIL {row['file']}: {why}")
            continue
        n = unzip(row) if not a.verify else 0
        print(f"ok   {row['file']}" + (f"  {n} EPS" if n else ""))
    total = sum(1 for p in paths.RAW.rglob("*") if p.suffix.lower() == ".eps") if paths.RAW.exists() else 0
    print(f"{len(rows) - bad}/{len(rows)} zips verified; {total} EPS in cache")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
