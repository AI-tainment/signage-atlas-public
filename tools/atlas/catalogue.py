"""Load country JSON and write site/assets/data.js."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

KINDS = ("signs", "markings", "furniture")
ROOT = Path(__file__).resolve().parents[2]


def country_dir(country: str, root: Path | None = None) -> Path:
    return (root or ROOT) / "countries" / country


def load_country(country: str, root: Path | None = None) -> dict[str, Any]:
    d = country_dir(country, root)
    if not (d / "country.json").exists():
        raise FileNotFoundError(f"no catalogue at {d}")
    atlas = {
        "country": json.loads((d / "country.json").read_text()),
        "signs": json.loads((d / "signs.json").read_text()),
        "markings": json.loads((d / "markings.json").read_text()),
        "furniture": json.loads((d / "furniture.json").read_text()),
        "siting": json.loads((d / "siting.json").read_text()) if (d / "siting.json").exists() else {},
        "colours": {},
    }
    atlas["colours"] = atlas["country"].get("colours") or {}
    return atlas


def face_sources(country: str, root: Path | None = None) -> dict[str, Any]:
    """countries/<id>/face_sources.json (written by tools/eps/map.py); {} when the country has none."""
    p = country_dir(country, root) / "face_sources.json"
    return json.loads(p.read_text())["faces"] if p.exists() else {}


def with_face_sources(atlas: dict[str, Any], country: str, root: Path | None = None) -> dict[str, Any]:
    """Copy of atlas whose sign rows carry face_source {source, fallback, eps, superseded, why_not_eps}.
    The JSON source rows (extract_uk.py output) are not modified."""
    fs = face_sources(country, root)
    if not fs:
        return atlas
    out = dict(atlas)
    rows = []
    for r in atlas["signs"]:
        f = fs.get(r["id"])
        r = dict(r)
        if f:
            r["face_source"] = {k: f[k] for k in ("source", "fallback", "eps", "superseded", "why_not_eps", "conflict")
                                if k in f}
        rows.append(r)
    out["signs"] = rows
    return out


def write_data_js(atlas: dict[str, Any], country: str, root: Path | None = None) -> Path:
    root = root or ROOT
    atlas = with_face_sources(atlas, country, root)
    var = "ATLAS_" + country.upper()
    path = root / "site" / "assets" / "data.js"
    if country != "uk":
        path = root / "site" / "assets" / f"data-{country}.js"
    path.write_text(f"window.{var} = " + json.dumps(atlas) + ";\n")
    return path


def safe_id(item_id: str) -> str:
    return item_id.replace("/", "_").replace(" ", "_")


def face_path(out: Path, country: str, kind: str, item_id: str) -> Path:
    return out / country / kind / f"{safe_id(item_id)}.svg"


def iter_items(atlas: dict[str, Any], kinds: list[str] | None = None):
    for kind in kinds or list(KINDS):
        for item in atlas.get(kind) or []:
            yield kind, item


def resolve_ids(atlas: dict[str, Any], ids: list[str], kinds: list[str] | None = None) -> list[tuple[str, dict[str, Any]]]:
    want = list(ids)
    found: list[tuple[str, dict[str, Any]]] = []
    seen = set()
    index: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for kind, item in iter_items(atlas, kinds):
        index.setdefault(item["id"], []).append((kind, item))
        index.setdefault(item["id"].lower(), []).append((kind, item))
    missing = []
    for raw in want:
        key = raw
        hits = index.get(key) or index.get(key.lower())
        if not hits:
            missing.append(raw)
            continue
        for kind, item in hits:
            mark = (kind, item["id"])
            if mark in seen:
                continue
            seen.add(mark)
            found.append((kind, item))
    if missing:
        raise SystemExit("unknown id(s): " + ", ".join(missing))
    return found
