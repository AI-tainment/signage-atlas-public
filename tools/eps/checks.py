"""EPS checks called by tools/validate.py.

Always (committed data):
  E1 manifest.csv / crosswalk.csv SHA-256 equal the pinned values (sources/eps/README.md).
  E2 face_sources.json is what tools/eps/map.py would write now (not stale), and covers every sign row.
  E3 an eps-sourced face names an EPS file listed in the crosswalk, has a baked procedural or placeholder
     fallback, is not an owner-held item and carries no conflict.
  E4 no raw EPS artwork is tracked (no *.eps, nothing under .cache/). Converted SVGs may be tracked only under
     site/faces-eps/uk/signs/ (owner ruling 2026-11-23), each with the Crown/OGL <desc>, for an eps-sourced face
     in face_sources.json, and byte-identical to the fresh conversion when the cache is present.
When the EPS cache exists (.cache/eps or $SA_EPS_CACHE):
  E5 every cached zip matches the manifest size and SHA-256.
  E6 every eps-sourced face resolves to a cached EPS file and its converted SVG.
  E7 no embedded fonts: the raw EPS has no font program / Transport or Calvert name, the conversion report
     lists no fonts, and the converted SVG has no <text> or <image>.
Without a cache the eps faces fall back to their procedural faces (noted, not a warning), so a fresh clone
still validates; set SA_REQUIRE_EPS=1 to make a missing cache an error.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess

from eps import map as eps_map
from eps import paths

PINNED = {
    "manifest.csv": "5c99976e02e4b4383aba46f00b354be35a32564f43027b1899a2babba4f433f2",
    "crosswalk.csv": "8975c83cbc0868e400027cc5f6e6012f8f6d4f7d5255cb5aafe267a6ea07bbc9",
}
# A font program embedded in the EPS (Illustrator procsets mention /FontType in their code; that is not one).
FONT_PROGRAM = re.compile(rb"%%BeginFont|%%BeginResource:\s*font|currentfile\s+eexec|\bTransport\b|\bCalvert\b", re.I)


_SHA_MEMO: dict = {}


def _sha(p) -> str:
    st = os.stat(p)
    key = (str(p), st.st_size, st.st_mtime_ns)
    if key in _SHA_MEMO:
        return _SHA_MEMO[key]
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    _SHA_MEMO[key] = h.hexdigest()
    return _SHA_MEMO[key]


def check(signs: list[dict], errors: list[str], notes: list[str], warns: list[str] | None = None) -> None:
    for name, want in PINNED.items():
        p = paths.SRC / name
        if not p.exists():
            errors.append(f"eps: {name} missing")
        elif _sha(p) != want:
            errors.append(f"eps: {name} SHA-256 differs from the pinned value")
    if not paths.FACE_SOURCES.exists():
        errors.append("eps: countries/uk/face_sources.json missing; run python3 tools/eps/map.py --report")
        return
    fs = json.loads(paths.FACE_SOURCES.read_text())
    if json.dumps(eps_map.build(), indent=1, sort_keys=True) + "\n" != paths.FACE_SOURCES.read_text():
        errors.append("eps: face_sources.json is stale; run python3 tools/eps/map.py --report")
    faces = fs["faces"]
    ids = {s["id"] for s in signs}
    for i in sorted(ids - set(faces)):
        errors.append(f"eps: sign {i} has no face_sources entry")
    for i in sorted(set(faces) - ids):
        errors.append(f"eps: face_sources entry {i} has no sign row")
    with open(paths.CROSSWALK, newline="") as fh:
        cw = {r["eps_file"] for r in csv.DictReader(fh)}
    eps_faces = {k: f for k, f in faces.items() if f.get("source") == "eps"}
    for k, f in eps_faces.items():
        if f.get("eps") not in cw:
            errors.append(f"eps: {k} names {f.get('eps')!r}, not in the crosswalk")
        if f.get("conflict") or f.get("why_not_eps"):
            errors.append(f"eps: {k} is eps-sourced but carries a conflict/reason")
        if k in eps_map.OWNER_HELD:
            errors.append(f"eps: owner-held item {k} must not change source")
        if not (paths.ROOT / "site" / "faces" / "uk" / "signs" / (k.replace("/", "_") + ".svg")).exists():
            errors.append(f"eps: {k} has no baked fallback face")
    tracked = subprocess.run(["git", "-C", str(paths.ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n")
    have_cache = paths.ZIPS.exists() and any(paths.ZIPS.glob("*.zip"))
    eps_dir = "site/faces-eps/uk/signs/"
    for t in tracked:
        if not t:
            continue
        if t.lower().endswith(".eps") or t.startswith(".cache/"):
            errors.append(f"eps: EPS artwork is tracked: {t}")
        elif t.startswith("site/faces-eps/"):
            if t == "site/faces-eps/uk/README.txt":
                continue
            fp = paths.ROOT / t
            fid = t[len(eps_dir):-4] if t.startswith(eps_dir) and t.endswith(".svg") else None
            f = next((v for k, v in eps_faces.items() if k.replace("/", "_") == fid), None) if fid else None
            if f is None:
                errors.append(f"eps: tracked {t} is not an eps-sourced face in face_sources.json")
                continue
            b = fp.read_bytes() if fp.exists() else b""
            if b"<desc>Crown copyright" not in b or b"Open Government Licence v3.0" not in b:
                errors.append(f"eps: tracked {t} lacks the Crown copyright / OGL v3.0 <desc>")
            if have_cache:
                src = paths.CACHE / "svg" / (f["eps"] + ".svg")
                if src.exists() and src.read_bytes() != b:
                    errors.append(f"eps: tracked {t} differs from the fresh conversion of {f['eps']}")
        elif t.endswith(".svg"):
            fp = paths.ROOT / t
            if fp.exists() and b'data-source="eps"' in fp.read_bytes():
                errors.append(f"eps: converted EPS SVG is tracked outside site/faces-eps/: {t}")

    if not paths.ZIPS.exists() or not any(paths.ZIPS.glob("*.zip")):
        msg = f"eps: cache absent; {len(eps_faces)} eps face(s) use their procedural fallback"
        (errors if os.environ.get("SA_REQUIRE_EPS") == "1" else notes).append(msg)
        return
    with open(paths.MANIFEST, newline="") as fh:
        man = list(csv.DictReader(fh))
    for r in man:
        p = paths.ZIPS / r["file"]
        if not p.exists():
            errors.append(f"eps: cached zip missing: {r['file']}")
        elif p.stat().st_size != int(r["bytes"]) or _sha(p) != r["sha256"]:
            errors.append(f"eps: cached zip {r['file']} does not match the manifest SHA-256")
    rep_p = paths.CACHE / "svg" / "convert-report.json"
    rep = json.loads(rep_p.read_text())["files"] if rep_p.exists() else {}
    if not rep:
        errors.append("eps: cache has zips but no conversions; run python3 tools/eps/build.py")
    else:
        from eps import convert
        bad = convert.version_problems(json.loads(rep_p.read_text()).get("tools") or {})
        if bad:
            (warns if warns is not None else errors).append("eps: cache converted with unpinned tools: " + "; ".join(bad))
    for k, f in sorted(eps_faces.items()):
        raw = paths.RAW / f["eps"]
        svg = paths.CACHE / "svg" / (f["eps"] + ".svg")
        if not raw.exists():
            errors.append(f"eps: {k}: cached EPS missing ({f['eps']})")
            continue
        if FONT_PROGRAM.search(raw.read_bytes()):
            errors.append(f"eps: {k}: EPS contains a font program or Transport/Calvert name")
        if not svg.exists():
            errors.append(f"eps: {k}: converted SVG missing; run python3 tools/eps/build.py")
            continue
        r = rep.get(f["eps"], {})
        if r.get("fonts"):
            errors.append(f"eps: {k}: embedded fonts {r['fonts']}")
        body = svg.read_text()
        if "<text" in body or "<image" in body:
            errors.append(f"eps: {k}: converted SVG has <text> or <image>")
        if "<desc>Crown copyright" not in body:
            errors.append(f"eps: {k}: converted SVG lacks the Crown copyright / OGL <desc>; rebuild with tools/eps/build.py")
    notes.append(f"eps: {len(man)} zips verified; {len(eps_faces)} eps face(s) resolve to cached EPS + SVG, 0 fonts")
