#!/usr/bin/env python3
"""Bake wiki faces. One item or all.

Examples:
  python3 tools/rebuild.py --all
  python3 tools/rebuild.py --id 611.1
  python3 tools/rebuild.py --item 670 --item 602
  python3 tools/rebuild.py --kind markings
  python3 tools/rebuild.py --extract --id 611.1
  python3 tools/rebuild.py --list --kind signs
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from atlas import catalogue, render  # noqa: E402
import extract_uk  # noqa: E402

KINDS = list(catalogue.KINDS)


def parse_kinds(raw: list[str] | None) -> list[str]:
    if not raw:
        return list(KINDS)
    out = []
    for chunk in raw:
        for part in chunk.split(","):
            p = part.strip()
            if not p or p == "all":
                return list(KINDS)
            if p in ("sign", "signs"):
                out.append("signs")
            elif p in ("marking", "markings"):
                out.append("markings")
            elif p in ("furniture", "furn"):
                out.append("furniture")
            else:
                raise SystemExit(f"unknown kind {p!r} (signs, markings, furniture)")
    # preserve order, unique
    seen = []
    for k in out:
        if k not in seen:
            seen.append(k)
    return seen


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"country": "", "faces": {}}


def rebuild(args: argparse.Namespace) -> int:
    country = args.country
    kinds = parse_kinds(args.kind)
    ids = args.id or []
    out_root = Path(args.out) if args.out else ROOT / "site" / "faces"

    if args.extract:
        extract_uk.extract(ids=ids or None, dest=Path(args.dest) if args.dest else None)

    atlas = catalogue.load_country(country, ROOT)
    if ids:
        items = catalogue.resolve_ids(atlas, ids, kinds)
    else:
        items = list(catalogue.iter_items(atlas, kinds))

    if args.list:
        for kind, item in items:
            print(f"{kind}\t{item['id']}\t{item.get('name', '')}")
        print(f"{len(items)} item(s)", file=sys.stderr)
        return 0

    write_data = args.data or (not ids)
    if args.no_data:
        write_data = False

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest_path = out_root / country / "manifest.json"
    manifest = load_manifest(manifest_path)
    manifest["country"] = country
    manifest.setdefault("faces", {})
    if not ids:
        # full kind rebuild: drop stale ids for those kinds
        manifest["faces"] = {
            k: v for k, v in manifest["faces"].items()
            if v.get("kind") not in kinds
        }
    written = []

    for kind, item in items:
        svg = render.item_svg(kind, item)
        path = catalogue.face_path(out_root, country, kind, item["id"])
        if args.dry_run:
            print(f"dry-run {path}")
            written.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg + "\n")
        rel = str(path.relative_to(out_root / country))
        manifest["faces"][f"{kind}/{item['id']}"] = {
            "path": rel,
            "kind": kind,
            "id": item["id"],
            "name": item.get("name"),
            "glyph": bool(item.get("glyph")),
            "renderer": item.get("renderer"),
            "bytes": path.stat().st_size,
            "sha256": __import__("hashlib").sha256(path.read_bytes()).hexdigest(),
        }
        written.append(path)

    if not args.dry_run:
        manifest.pop("built", None)
        manifest["count"] = len(manifest["faces"])
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest["faces"] = dict(sorted(manifest["faces"].items()))
        if not ids:
            # full rebuild: delete baked faces that no longer have a row (e.g. renumbered 1003)
            keep = {Path(p) for p in written}
            for kind in kinds:
                kdir = out_root / country / kind
                for fp in sorted(kdir.glob("*.svg")) if kdir.exists() else []:
                    if fp not in keep:
                        fp.unlink()
                        print(f"removed orphan face {fp.relative_to(out_root)}")
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        if not ids and args.out is None:
            js_path = ROOT / "site" / "assets" / "render.js"
            js_path.write_text(render.render_js())
            print(f"render.js {js_path.relative_to(ROOT)} (generated)")
        if write_data:
            data_path = catalogue.write_data_js(atlas, country, ROOT)
            print(f"data {data_path.relative_to(ROOT)}")

    print(f"wrote {len(written)} face(s) under {out_root / country}")
    if not args.dry_run and not args.list and getattr(args, "validate", True):
        import validate as atlas_validate
        rc = atlas_validate.validate(country, strict=bool(getattr(args, "strict", False)))
        if rc:
            return rc
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rebuild.py",
        description="Render Signage Atlas wiki faces. One item (--id) or everything (--all).",
    )
    p.add_argument("--country", default="uk", help="Country folder under countries/ (default uk)")
    p.add_argument(
        "--kind",
        action="append",
        help="signs, markings, furniture (repeat or comma-separate). Default: all kinds.",
    )
    p.add_argument(
        "--id",
        "--item",
        dest="id",
        action="append",
        metavar="ID",
        help="Rebuild this id only (repeatable). Example: --id 611.1 --id 1003.4",
    )
    p.add_argument(
        "--all",
        action="store_true",
        help="Rebuild every item in the selected kinds (default when --id is omitted).",
    )
    p.add_argument(
        "--extract",
        action="store_true",
        help="Refresh countries/<id> JSON from GridForge dest first. With --id, merge those rows only.",
    )
    p.add_argument(
        "--dest",
        help="GridForge dest root or UkTsrgdCatalogue.cs (with --extract). Default: vendor snapshot.",
    )
    p.add_argument("--no-validate", dest="validate", action="store_false", default=True, help="Skip tools/validate.py")
    p.add_argument("--strict", action="store_true", help="Validator warnings fail the rebuild")
    p.add_argument("--data", action="store_true", help="Rewrite site/assets/data.js (on by default for --all).")
    p.add_argument("--no-data", action="store_true", help="Do not rewrite data.js.")
    p.add_argument("--out", help="Face output root (default site/faces)")
    p.add_argument("--list", action="store_true", help="Print matching ids and exit.")
    p.add_argument("--dry-run", action="store_true", help="Print paths, do not write.")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.all and args.id:
        print("using --id list; --all ignored", file=sys.stderr)
    return rebuild(args)


if __name__ == "__main__":
    raise SystemExit(main())
