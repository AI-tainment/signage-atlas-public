#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# EPS-first faces: cook GOV.UK EPS into site/faces-eps/ (gitignored) when the local cache allows.
#   SA_EPS_FETCH=1 ./tools/serve.sh   also fetches missing zips once (polite, SHA-256 checked).
# Without a cache the wiki serves the procedural faces (the offline fallback).
if [ "${SA_EPS_FETCH:-0}" = "1" ]; then python3 "$ROOT/tools/eps/fetch.py" || true; fi
if python3 "$ROOT/tools/eps/fetch.py" --verify >/dev/null 2>&1; then
  if [ ! -f "$ROOT/.cache/eps/svg/convert-report.json" ]; then python3 "$ROOT/tools/eps/fetch.py" >/dev/null && python3 "$ROOT/tools/eps/build.py"; else python3 "$ROOT/tools/eps/build.py" --faces-only; fi
else
  echo "EPS cache not present: serving procedural faces (run SA_EPS_FETCH=1 ./tools/serve.sh to cook EPS faces)"
fi
cd "$ROOT/site"
PORT="${PORT:-8765}"
echo "Signage Atlas  http://127.0.0.1:${PORT}/"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
