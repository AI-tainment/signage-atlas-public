#!/usr/bin/env python3
"""Build countries/uk/tsrgd2016_index.json from the live catalogue + status tables.

Captions for ids still named "TSRGD N" come from the quarantined Highway Code
maps as *unverified captions*, never as an id source. Re-IDs from the 2026-11-10
re-review are recorded as aliases; dest catalogue ids stay as `id` so extract
can merge dest rows.
"""
from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

from uk_english_names import NAMES

ROOT = Path(__file__).resolve().parents[1]
UK = ROOT / "countries" / "uk"
Q = ROOT / "tools" / "quarantine"

# dest id -> 2016 diagram (re-review WP1)
RENUMBER = {
    "675": "675A",
    "629": "629A",
    "531.1": "531.1A",
    "811": "811A",
    "642.2": "605.3",
    "959": "959B",
    "526": "529",
    "530": "530A",
    "1003": "1003A",
    "1023": "1023A",
    "BELISHA": "4007",
}

SOURCES = UK / "sources"


def _si2016() -> dict:
    blob = json.loads((SOURCES / "si2016_diagrams.json").read_text())
    return blob["diagrams"]


def _legacy() -> dict:
    return json.loads((SOURCES / "legacy2002.json").read_text())


SI2016 = _si2016()
_LEG = _legacy()
REG_14_4 = set(_LEG["reg_14_4"])
LEGACY_2002 = set(_LEG["legacy_2002"]) | (REG_14_4 - set(SI2016))
UNVERIFIED = set(_LEG["unverified"]["ids"])
# r3: the owner's 36-id decision. Merged dest ids become aliases on their target; retired ids are dropped.
MERGED = dict((_LEG.get("merged") or {}).get("ids") or {})
RETIRED = set((_LEG.get("retired") or {}).get("ids") or [])
# Engine ids that are not TSRGD diagram numbers at all.
NON_TSRGD = {"GANTRY_ADS", "MS4", "MARKER", "XING_PAR", "STREET_NAME"}

FAMILY_CAPTION = {
    "WarnTriangle": "Warning sign",
    "WorksRed": "Road works / temporary warning",
    "GiveWay": "Give way",
    "Stop": "Stop",
    "Prohibitory": "Prohibitory roundel",
    "National": "National speed limit",
    "Mandatory": "Mandatory roundel",
    "InfoBlue": "Information plate",
    "DirPrimary": "Primary-route direction",
    "DirLocal": "Non-primary direction",
    "DirMotorway": "Motorway direction",
    "TouristBrown": "Tourist destination",
    "SignalHead": "Traffic signal head",
    "PedHead": "Pedestrian signal / crossing furniture",
    "MatrixMS4": "Variable message / matrix",
    "Countdown": "Motorway exit countdown",
    "Marker": "Driver location / marker",
}

HAND_CAPTIONS = {
    **NAMES,
    "4007": "Belisha beacon",
    "1003A": "Give-way line",
    "1023A": "Give-way triangle",
    "1038": "Lane destination arrow",
    "1014": "Deflection arrow",
    "1001.4": "Zig-zag lines at a zebra",
    "1001.3": "Zig-zag lines at a signal crossing",
    "1055.1": "Crossing studs",
    "zebra-stripes": "Zebra crossing stripes",
    "1003.3": "Mini-roundabout give-way line",
    "675B": "End of 20 mph zone (national speed limit)",
    "629A": "No vehicles over the width shown",
    "531.1A": "Maximum headroom at an arch bridge",
    "811A": "Priority over oncoming vehicles",
    "811B": "Priority to oncoming vehicles",
    "827.1": "Hospital",
    "605.3": "School crossing patrol",
    "959B": "With-flow bus and cycle lane",
    "530A": "Maximum headroom",
}


def _load_json(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def _caption_maps() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in ("hc_highway_code_map.json", "hc_website_map.json"):
        blob = _load_json(Q / name)
        if not blob:
            continue
        for p in blob.get("plates") or []:
            cap = (p.get("caption") or "").strip()
            if cap and cap.lower() != "picture" and p.get("id") not in out:
                out[p["id"]] = cap
    out.update(HAND_CAPTIONS)
    return out


def _status(dest_id: str, kind: str) -> tuple[str, str | None]:
    """Status from the SI text, never from the number range.

    renumbered  dest id whose 2016 diagram has another number (RENUMBER)
    current     id is a diagram in SI 2016/362 (sources/si2016_diagrams.json)
    2002-legacy named in SI 2002/3113 (or the reg 14(4) list) but not in SI 2016
    not-2016    engine id, not a TSRGD diagram (kind non-tsrgd)
    unverified  in neither SI text; see sources/legacy2002.json
    """
    if dest_id in RENUMBER:
        return "renumbered", RENUMBER[dest_id]
    if dest_id in SI2016:
        return "current", None
    if dest_id in LEGACY_2002:
        return "2002-legacy", None
    if dest_id in NON_TSRGD or not dest_id[0].isdigit():
        return "not-2016", None
    return "unverified", None


def _si_ref(diagram: str) -> str:
    si = SI2016.get(diagram)
    if not si:
        return ""
    sch = si.get("schedule", "").replace("SCHEDULE", "Sch").strip()
    part = si.get("part", "").replace("PART", "Pt").strip()
    item = si.get("item")
    return " ".join(x for x in (sch, part, f"item {item}" if item else "") if x)


def build() -> dict:
    signs = json.loads((UK / "signs.json").read_text())
    marks = json.loads((UK / "markings.json").read_text())
    caps = _caption_maps()
    entries: list[dict] = []
    seen = set()

    def add(dest_id: str, *, kind: str, family: str = "", name: str = "", extra: dict | None = None):
        if dest_id in seen:
            return
        seen.add(dest_id)
        st, to = _status(dest_id, kind)
        diagram = to or dest_id
        si = SI2016.get(diagram) if st in ("current", "renumbered") else None
        caption = caps.get(dest_id) or caps.get(diagram)
        if not caption:
            if name and not name.startswith("TSRGD "):
                caption = name
            else:
                caption = FAMILY_CAPTION.get(family, "Traffic sign")
        row = OrderedDict([
            ("id", dest_id),
            ("diagram_2016", diagram),
            ("kind", "non-tsrgd" if st == "not-2016" else kind.rstrip("s")),
            ("status", st),
            ("caption", caption),
            ("si_caption", si["caption"] if si else None),
            ("schedule", _si_ref(diagram) or (extra.get("schedule") if extra else "")),
            ("permitted_mm", extra.get("permitted_mm") if extra else []),
            ("renumbered_to", to),
            ("reg_14_4", dest_id in REG_14_4),
            ("caption_source", "hand" if dest_id in HAND_CAPTIONS or diagram in HAND_CAPTIONS
             else "hc-map-unverified" if dest_id in caps else "family-fallback"),
        ])
        entries.append(row)
        if to and to not in seen:
            add(to, kind=kind, family=family, name=caption)

    for s in signs:
        if s["id"] in RETIRED or s["id"] in MERGED:
            continue
        add(s["id"], kind="signs", family=s.get("family") or "", name=s.get("name") or "")
    for _old, _new in sorted(MERGED.items()):
        add(_new, kind="signs")
    for m in marks:
        add(m["id"], kind="markings", name=m.get("name") or "")

    extra_ids = [
        ("675B", "signs", "End of 20 mph zone, national speed limit applies"),
        ("811B", "signs", "Priority to oncoming vehicles"),
        ("827.1", "signs", "Hospital ahead"),
        ("827.2", "signs", "Hospital (A & E)"),
        ("827.3", "signs", "Hospital"),
        ("1003.3", "markings", "Give-way line at a mini-roundabout"),
        ("1001.4", "markings", "Zig-zag lines at a zebra"),
        ("1001.5", "markings", "Zig-zag lines (variant)"),
        ("1009A", "markings", "Edge line at a junction"),
        ("1038", "markings", "Lane destination arrow"),
        ("1040", "markings", "Chevron marking"),
        ("1043", "markings", "Keep left hatched island"),
        ("1048", "markings", "BUS LANE marking"),
        ("1049B", "markings", "Boundary of a bus lane"),
        ("1057", "markings", "Cycle symbol"),
        ("1062", "markings", "Hump marking"),
        ("1065", "markings", "Speed limit roundel marking"),
        ("1019", "markings", "Waiting restriction mark"),
        ("1020.1", "markings", "Parking bay"),
        ("1025.1", "markings", "Box junction"),
        ("1028.1", "markings", "Parking bay (end)"),
        ("zebra-stripes", "markings", "Zebra crossing stripes"),
    ]
    for i, k, n in extra_ids:
        add(i, kind=k, name=n)

    counts = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1

    doc = OrderedDict([
        ("source", "TSRGD 2016 (SI 2016/362) plus dest-catalogue ids. Captions mixed: SI wording where known, otherwise HC map (unverified) or family fallback."),
        ("note", "Not a complete SI dump. Every wiki row must point at an entry. Validator fails on a missing id."),
        ("counts", counts),
        ("renumber", RENUMBER),
        ("entries", entries),
    ])
    path = UK / "tsrgd2016_index.json"
    path.write_text(json.dumps(doc, indent=2) + "\n")
    print(f"wrote {path} ({len(entries)} entries) {counts}")
    return doc


def overlay_from_live() -> dict:
    """Snapshot hand names/glyph flags so extract can re-apply them."""
    signs = json.loads((UK / "signs.json").read_text())
    country = json.loads((UK / "country.json").read_text())
    ov = {
        "licence": country.get("licence"),
        "fonts": country.get("fonts"),
        "signs": {},
    }
    for s in signs:
        rec = {}
        if s.get("name") and not str(s["name"]).startswith("TSRGD "):
            rec["name"] = s["name"]
            rec["what"] = s.get("what") or s["name"]
        if s.get("glyph"):
            rec["glyph"] = True
            rec["renderer"] = s.get("renderer") or s["id"]
        if rec:
            ov["signs"][s["id"]] = rec
    path = UK / "overlay.json"
    path.write_text(json.dumps(ov, indent=2) + "\n")
    print(f"wrote {path} ({len(ov['signs'])} sign overlays)")
    return ov


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Build tsrgd2016_index.json from sources/ + live rows.")
    ap.add_argument("--snapshot-overlay", action="store_true",
                    help="Also rewrite overlay.json from live signs.json (refuses if it exists, unless --force).")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.snapshot_overlay:
        if (UK / "overlay.json").exists() and not a.force:
            raise SystemExit("build_uk_index: overlay.json exists (hand fixes live there); pass --force to overwrite")
        overlay_from_live()
    build()
