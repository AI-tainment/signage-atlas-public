"""Shared paths for the EPS pipeline. Everything under CACHE and OUT is gitignored."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "countries" / "uk" / "sources" / "eps"
MANIFEST = SRC / "manifest.csv"          # SHA-256 of the 18 GOV.UK zips (from GridForge docs/sources)
CROSSWALK = SRC / "crosswalk.csv"        # 702 EPS -> 2002 / 2016 diagram status (from GridForge docs/sources)
FACE_SOURCES = ROOT / "countries" / "uk" / "face_sources.json"
# $SA_EPS_CACHE overrides the cache root (default <repo>/.cache/eps, gitignored).
CACHE = Path(os.environ.get("SA_EPS_CACHE") or (ROOT / ".cache" / "eps"))
ZIPS = CACHE / "zips"
RAW = CACHE / "raw"                       # unzipped EPS, one folder per zip
# Converted faces the wiki can show; gitignored, rebuilt by tools/eps/build.py (or tools/serve.sh).
OUT = ROOT / "site" / "faces-eps" / "uk"
