#!/usr/bin/env python3
"""Extract UK catalogue JSON from GridForge dest (spec 015 / 019 / UkTsrgdCatalogue)."""
from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

from uk_english_names import MARKING_NAMES, NAMES, FURNITURE_NAMES
from uk_english_names import blurb as english_blurb
from uk_english_names import caption as english_caption

ROOT = Path(__file__).resolve().parents[1]
UK = ROOT / "countries" / "uk"
VENDOR_CS = ROOT / "vendor" / "gridforge" / "UkTsrgdCatalogue.cs"
TRI_W_OVER_H = 1.1317  # P500: width from height

# TSRGD 2016 prescribed working colours (spec 015 / UkTsrgdFace).
COLOURS = {
    "red": "#CC1A1A",
    "blue": "#005CA6",
    "white": "#F7F7F7",
    "black": "#141414",
    "grey": "#8C8E94",
    "amber": "#F29E14",
    "green": "#1EB838",
    "brown": "#73451F",
    "primary_green": "#0D7338",
    "motorway_blue": "#00529E",
    "galvanised": "#9EA0A6",
    "creosote": "#472E1A",
    "marking_white": "#F4F4F0",
    "marking_yellow": "#E6C200",
    "yellow": "#E6C200",
    "fluorescent_yellow": "#F5D000",
}

FAMILY_SIZE = {
    "GiveWay": 0.75, "Stop": 0.75, "Prohibitory": 0.60, "National": 0.60,
    "Mandatory": 0.60, "WarnTriangle": 0.60, "InfoBlue": 0.70,
    "DirPrimary": 0.95, "DirLocal": 0.95, "DirMotorway": 2.40,
    "TouristBrown": 0.95, "WorksRed": 0.60, "SignalHead": 0.32,
    "PedHead": 0.32, "MatrixMS4": 2.40, "Countdown": 0.45, "Marker": 0.30,
    # r3: supplementary plates. 608 height = legend x-height 75 mm (SI 2016 Sch 9 Pt 2
    # item 3 allows 50-125) / 0.72 / 0.248 (cap / plate height in the SI diagram).
    "Plate": 0.42,
}
GLYPH_SIZE = {
    # r4: SI 2002 p120: 811.1 plate 700 wide (default size); height = 700 / 1.816 (measured aspect).
    "811.1": 0.385,
    "602": 0.75, "601.1": 0.75, "670": 0.60, "671": 0.60,
    "GANTRY_ADS": 2.40, "MS4": 2.40, "2025": 0.95, "2101": 0.95,
    "2701": 2.40, "2202": 0.95, "801": 0.70, "823": 0.45, "824": 0.45, "825": 0.45,
    "MARKER": 0.30, "3000": 0.32, "4003": 0.32, "STREET_NAME": 1.20,
}
FAMILY_PLATE_H = {
    "GiveWay": 0.866, "Stop": 1.0, "WarnTriangle": 0.866, "WorksRed": 0.866,
    "SignalHead": 2.6, "PedHead": 2.6, "Countdown": None, "Marker": None,
}
UNDERSIDE = {
    "verge_std": 1.50, "gw_stop": 1.50, "stack": 1.50, "both_kerbs": 1.50,
    "footway_dir": 2.10, "refuge": 0.55, "signals": 2.35, "crossing": 2.10,
    "portal": 5.50, "wigwag": 2.35, "marker": 0.15, "street_name": 0.80,
}
POST_DIA = {
    "Post": 0.076, "TwoPost": 0.076, "StreetName": 0.060, "Cantilever": 0.219,
    "PortalGantry": 0.219, "Belisha": 0.089, "SignalHead": 0.090,
    "Refuge610": 0.076, "MarkerPost": 0.080,
}

GLYPH_NAMES = NAMES

FAMILY_BLURB = {
    "WarnTriangle": "Red equilateral triangle, white interior, black pictogram. Warning.",
    "GiveWay": "Inverted red triangle, white interior. Give way to traffic on the major road.",
    "Stop": "Red octagon, white legend STOP. Must stop.",
    "Prohibitory": "Red ring on white disc (or red disc). Restriction.",
    "National": "White disc, black diagonal slash, thin red ring. National speed limit.",
    "Mandatory": "Blue disc, white pictogram. Instruction (keep left, mini-roundabout, bus gate).",
    "InfoBlue": "Blue rectangle, white legend/pictogram. Information.",
    "DirPrimary": "Green rectangle, white legend and chevron. Primary-route ADS.",
    "DirLocal": "White rectangle, black legend and chevron. Non-primary ADS.",
    "DirMotorway": "Blue rectangle, white legend. Motorway ADS.",
    "TouristBrown": "Brown rectangle, white legend. Tourist destination.",
    "WorksRed": "Red triangle or red/white works plate. Temporary / road works.",
    "SignalHead": "Vehicle traffic-signal head (red / amber / green).",
    "PedHead": "Pedestrian/cycle signal or Belisha.",
    "MatrixMS4": "Electronic matrix panel on a portal gantry.",
    "Countdown": "Three descending bars, motorway exit countdown.",
    "Marker": "Driver location / marker post on the hard-shoulder back.",
}

SITING = {
    "lede": {
        "text": "Plates face the stream that must obey them (painted face = travel + 180°). UK nearside is left of travel. Exceptions: offside/central-island duplicates, rear-facing end plates, cantilevers, side-road facing plates, mapped portal gantries in the running lane.",
        "source": "engine-default (TSM Ch.1/3/4 not in this tree)",
    },
    "verge_std": {
        "text": "UK nearside verge, half-width + 0.8 m (engine-default lateral offset). Face of flow (face normal opposes travel).",
        "source": "engine-default",
    },
    "gw_stop": {
        "text": "602 / 601.1: left of the minor approach, before diagram 1003A / 1002.1 (TSM Chapter 3 not read — distance unsourced). 611.1 at a mini-roundabout: 1.5 m before the give-way line, maximum 12 m (TSM5 §6.3.6).",
        "source": "TSM5 §6.3.6 (611.1); 602/601.1 TSM Ch.3 unread",
    },
    "stack": {
        "text": "Same post as a co-tagged plate (e.g. 530A over 629.2A). Verge.",
        "source": "engine-default",
    },
    "both_kerbs": {
        "text": "Both sides of the entry (616, bus gate when co-tagged).",
        "source": "unsourced (TSM Chapter 3 not read)",
    },
    "refuge": {
        "text": "On the refuge / island centre, not the verge (610 / 611). Underside 0.55 m is an engine-default.",
        "source": "engine-default",
    },
    "signals": {
        "text": "Primary head stands beyond (downstream of) the 1001 stop line. Secondary head on the far side of the junction. The cooker currently plants one kerbside head per approach (engine-default).",
        "source": "TSM Chapter 6 unread; engine-default placement",
    },
    "crossing": {
        "text": "Both kerbs. Zebra: Belisha (TSRGD 4007). Signal crossing: pedestrian heads.",
        "source": "TSRGD Sch14 Pt1 / Pt4",
    },
    "portal": {
        "text": "Mapped gantry only. Underside clearance 5.5 m (unsourced — DMRB not checked). Width = way length clamped 8–18 m (engine heuristic).",
        "source": "engine-default / heuristic",
    },
    "wigwag": {
        "text": "Both sides of a mapped level crossing, ~2 m before the running rail.",
        "source": "unsourced",
    },
    "marker": {
        "text": "Back of hard shoulder + 1.2 m. Never in the running lane. Not a TSRGD diagram.",
        "source": "unsourced; kind non-tsrgd",
    },
    "footway_dir": {
        "text": "Underside 2.1 m if a footway/cycleway/path is within 4 m; else 1.5 m verge. Distances are engine-defaults.",
        "source": "engine-default (TSM unread)",
    },
    "street_name": {
        "text": "Named OSM corner (≥3 arms, ≥2 names). Face the named street. Underside 0.80 m. Not a TSRGD diagram.",
        "source": "engine-default; kind non-tsrgd",
    },
}


def parse_catalogue(cs: Path):
    text = cs.read_text()
    rows = re.findall(
        r'new TsrgdRow\("([^"]+)",\s*(\d+),\s*TsrgdFamily\.(\w+),\s*TsrgdMount\.(\w+),\s*"([^"]+)",\s*"([^"]+)"\)',
        text,
    )
    if len(rows) != 412:
        raise SystemExit(f"expected 412 rows, got {len(rows)}")
    return rows


def plate_wh(family: str, size: float, code: str) -> tuple[float, float]:
    """Return (width, height) in metres. Triangles are sized by height (P500)."""
    if code in ("823", "824", "825"):
        return 0.70, 1.20
    if code == "MARKER":
        return 0.30, 1.00
    if code == "801":
        return size, size
    if family in ("GiveWay", "WarnTriangle", "WorksRed"):
        h = size
        return round(TRI_W_OVER_H * h, 3), round(h, 3)
    if family in ("DirPrimary", "DirLocal", "DirMotorway", "TouristBrown", "InfoBlue", "MatrixMS4"):
        return size, round(size * 0.55, 3)
    if family in ("SignalHead", "PedHead") and code not in ("BELISHA", "XING_PAR"):
        return size, round(size * 2.6, 3)
    return round(size, 3), round(size, 3)


SIZE_DIMS = ("diameter", "sign height")
NOT_TABULATED = "working size (SI 2016 tabulates no size for this diagram; see sources/si2016_sizes.json)"


def _si_sizes() -> dict:
    path = UK / "sources" / "si2016_sizes.json"
    return json.loads(path.read_text(encoding="utf8"))["sizes"] if path.exists() else {}


def si_plate(code: str, family: str, w: float, h: float, sizes: dict):
    """D1: snap the working plate to a permitted SI 2016 size where one is tabulated.

    Returns (w, h, source, permitted_mm, permitted_dim). Diagrams with no size
    column in SI 2016 keep the working size and say so; nothing is invented."""
    e = sizes.get(code)
    if not e or e["dim"] not in SIZE_DIMS:
        note = NOT_TABULATED if not e else f"working size (SI 2016 {e['ref']} gives {e['dim']}, not a plate size)"
        return w, h, note, (e or {}).get("mm") if e else None, (e or {}).get("dim") if e else None
    allowed = e["mm"]
    cur = round(h * 1000)
    pick = cur if cur in allowed else min(allowed, key=lambda m: (abs(m - cur), -m))
    nh = pick / 1000
    nw = nh if e["dim"] == "diameter" else (round(w * nh / h, 3) if h else nh)
    src = f"SI 2016 {e['ref']} item {e['item']}: {e['dim']} {', '.join(map(str, allowed))} mm; working {pick} mm"
    return nw, round(nh, 3), src, allowed, e["dim"]


def face_aspect(row: dict) -> None:
    """D1: a drawn row's plate width follows its drawn face (height kept).

    Rows with no drawer, or whose face this reader cannot measure, are left."""
    if not row.get("glyph"):
        return
    try:
        from atlas.render import drawn_aspect
    except Exception:
        return
    a = drawn_aspect(row["id"], row.get("renderer"), row.get("param"))
    dm = row["dimensions_m"]
    if a is None or not dm.get("plate_height"):
        return
    if abs((dm["plate_width"] / dm["plate_height"]) / a - 1) > 0.02:
        dm["plate_width"] = round(dm["plate_height"] * a, 3)
        row["source"]["plate_width"] = "plate height x drawn face aspect (" + f"{a:.3f}" + ")"


def _resize(row: dict) -> None:
    """Re-apply si_plate to a cloned row under its own (new) number."""
    dm = row["dimensions_m"]
    dm["plate_width"], dm["plate_height"], src, row["permitted_mm"], row["permitted_dim"] = si_plate(
        row["id"], row.get("family"), dm["plate_width"], dm["plate_height"], _si_sizes())
    row["source"]["plate_width"] = row["source"]["plate_height"] = src


def post_dia(mount: str, family: str) -> float:
    if family in ("DirMotorway", "MatrixMS4") and mount == "TwoPost":
        return 0.114
    return POST_DIA.get(mount, 0.076)


def _index() -> dict:
    path = UK / "tsrgd2016_index.json"
    if not path.exists():
        return {}
    blob = json.loads(path.read_text())
    return {e["id"]: e for e in blob.get("entries") or []}


# Name policy (QA r1): placeholders take the SI 2016 caption verbatim (their
# HC-style name is kept as name_alias). Drawn glyphs keep their hand-checked
# short name (uk_english_names / overlay); every row carries si_caption + si_ref.
SI_NAME_GLYPHS: set[str] = set()


def _si_caption(diagram: str) -> str | None:
    ent = _index_raw().get(diagram) or {}
    return ent.get("si_caption")


_INDEX_CACHE: dict | None = None


def _index_raw() -> dict:
    global _INDEX_CACHE
    if _INDEX_CACHE is None:
        _INDEX_CACHE = _index()
    return _INDEX_CACHE


def _sentence(cap: str) -> str:
    cap = re.sub(r"\s+,", ",", cap.strip())
    cap = re.sub(r"\s*\(Alternative types?\)\s*$", "", cap)
    return cap[:1].upper() + cap[1:]


def _overlay() -> dict:
    path = UK / "overlay.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _siting_text(key: str) -> str:
    row = SITING.get(key)
    if isinstance(row, dict):
        return row.get("text") or ""
    return row or ""


# Dest id → 2016 diagram. Wiki gets a row at the new number so search finds it.
WIKI_ALIAS_FROM = {
    "529": "526",
    "530A": "530",
    "629A": "629",
    "531.1A": "531.1",
    "811A": "811",
    "605.3": "642.2",
    "959B": "959",
    "4007": "BELISHA",
}


# Second 2016 targets of a split renumber (SI 2016 Sch10 Pt2 items 6-7; Sch11 Pt2
# item 1). No drawer yet: they get a neutral placeholder row, never an invented face.
RENUMBER_ALSO = {"675B": "675", "811B": "811"}
# r4: 827.1 (hospital) no longer clones 811.1 (now the 2002 priority plate); it gets its own drawn row
# seeded from the 811 InfoBlue row's mount/family data.
OWN_ROW_FROM = {"827.1": "811"}


def _colours_from_svg(svg: str) -> list[str]:
    """Named colours used by a face, in COLOURS order (deterministic across runs)."""
    hexes = {m.group(0).upper() for m in re.finditer(r"#[0-9A-Fa-f]{6}", svg)}
    names: list[str] = []
    for name, hexv in COLOURS.items():
        if str(hexv).upper() in hexes and name not in names and str(hexv).upper() not in {
            str(COLOURS[n]).upper() for n in names
        }:
            names.append(name)
    return names


def _paint_colours(item: dict) -> None:
    from atlas import render as atlas_render
    svg = atlas_render.item_svg("signs", item)
    cols = _colours_from_svg(svg)
    item["colours"] = cols


def build_signs(rows):
    signs = []
    index = _index()
    si_sizes = _si_sizes()
    overlay = (_overlay().get("signs") or {})
    try:
        from atlas.render import GLYPHS as RENDER_GLYPHS
    except Exception:
        RENDER_GLYPHS = {}
    for code, ch, family, mount, siting, v1 in rows:
        family = (overlay.get(code) or {}).get("family") or family
        size = GLYPH_SIZE.get(code, FAMILY_SIZE[family])
        underside = UNDERSIDE.get(siting, 1.50)
        w, h = plate_wh(family, size, code)
        w, h, size_src, permitted, permitted_dim = si_plate(code, family, w, h, si_sizes)
        ent = index.get(code) or {}
        ov = overlay.get(code) or {}
        caption = english_caption(code, ov.get("name") or ent.get("caption") or FAMILY_BLURB.get(family, "Traffic sign"))
        what = english_blurb(code, caption)
        glyph = bool(ov.get("glyph", v1 == "glyph")) or code in RENDER_GLYPHS
        diagram = ov.get("diagram") or ent.get("diagram_2016") or code
        status = ov.get("status") or ent.get("status") or "current"
        if status == "renumbered":
            # A1: the old row keeps its own number; the 2016 number is renumbered_to.
            diagram = code
        kind = ov.get("kind") or ent.get("kind") or "sign"
        if status == "current" and kind == "non-tsrgd":
            kind = "sign"
        si_cap = ent.get("si_caption")
        alias = None
        if si_cap and status == "current" and (not glyph or code in SI_NAME_GLYPHS):
            if _sentence(si_cap) != caption:
                alias = caption
            caption = _sentence(si_cap)
            what = caption
        signs.append({
            "id": code,
            "kind": kind,
            "diagram": diagram,
            "status": status,
            "renumbered_to": ent.get("renumbered_to"),
            "index_id": code,
            "name": caption,
            "name_alias": alias,
            "si_caption": si_cap,
            "si_ref": ent.get("schedule") or "",
            "what": what,
            "chapter": int(ch),
            "family": family,
            "mount": mount,
            "siting": siting,
            "siting_note": _siting_text(siting),
            "v1": "glyph" if glyph else "fallback",
            "glyph": glyph,
            "permitted_mm": permitted,
            "permitted_dim": permitted_dim,
            "renderer": code if glyph else (ov.get("renderer") or f"family:{family}"),
            "dimensions_m": {
                "plate_width": w,
                "plate_height": h,
                "underside": underside,
                "post_diameter": post_dia(mount, family),
                "verge_offset": 0.8 if siting not in ("refuge", "portal", "marker") else 0.0,
            },
            "source": {
                "plate_width": size_src,
                "plate_height": size_src,
                "underside": "engine-default",
                "post_diameter": "engine-default",
                "verge_offset": "engine-default",
            },
            "font": {
                "official": "Transport Heavy / Transport Medium (TSRGD). Not shipped.",
                "procedural": "Schedule 17 stand-in strokes (polygons, rects, arcs). No typeface file. Part 5 VMS on MS4 only.",
            },
            "osm": f"traffic_sign=GB:{code}" if code[0].isdigit() else code.lower(),
            "colours": ["red", "white", "black"] if family in ("Prohibitory", "GiveWay", "Stop", "WarnTriangle")
            else ["blue", "white"] if family in ("Mandatory", "InfoBlue", "DirMotorway")
            else ["primary_green", "white"] if family == "DirPrimary"
            else ["white", "black"] if family in ("DirLocal", "Plate")
            else ["brown", "white"] if family == "TouristBrown"
            else ["black", "red", "amber", "green"] if family in ("SignalHead", "PedHead")
            else ["grey", "white", "black"],
        })
        _paint_colours(signs[-1])
    # Clip-parity street name (spec 015 StreetName, not a TSRGD diagram number).
    signs.append({
        "id": "STREET_NAME",
        "kind": "sign",
        "diagram": "STREET_NAME",
        "name": english_caption("STREET_NAME", "Street-name plate"),
        "what": english_blurb("STREET_NAME"),
        "chapter": 15,
        "family": "DirLocal",
        "mount": "StreetName",
        "siting": "street_name",
        "siting_note": _siting_text("street_name"),
        "v1": "glyph",
        "glyph": True,
        "permitted_mm": None,
        "permitted_dim": None,
        "kind": "non-tsrgd",
        "status": "not-2016",
        "renderer": "STREET_NAME",
        "dimensions_m": {
            "plate_width": 1.20,
            "plate_height": round(1.20 * 0.28, 3),
            "underside": 0.80,
            "post_diameter": 0.060,
            "verge_offset": 1.4,
        },
        "font": {
            "official": "Transport Medium (street name). Not shipped.",
            "procedural": "Schedule 17 stand-in strokes. No typeface file.",
        },
        "osm": "named highway at a junction (≥3 arms, ≥2 names)",
        "colours": ["white", "black", "grey"],
        "source": {
            "plate_width": "engine-default",
            "plate_height": "engine-default",
            "underside": "engine-default",
            "post_diameter": "engine-default",
            "verge_offset": "engine-default",
        },
    })
    _paint_colours(signs[-1])

    by_id = {s["id"]: s for s in signs}
    _leg = json.loads((ROOT / "countries" / "uk" / "sources" / "legacy2002.json").read_text())
    merged = dict((_leg.get("merged") or {}).get("ids") or {})
    retired = set((_leg.get("retired") or {}).get("ids") or [])
    # r3: a merge target missing from the dest catalogue gets a row cloned from the old id.
    for new_id, old_id in list(WIKI_ALIAS_FROM.items()) + sorted((n, o) for o, n in merged.items()):
        if new_id in by_id or old_id not in by_id:
            continue
        clone = json.loads(json.dumps(by_id[old_id]))
        clone["id"] = new_id
        clone["diagram"] = new_id
        clone["index_id"] = new_id
        clone["status"] = "current"
        clone["renumbered_to"] = None
        clone["kind"] = "sign"
        clone["glyph"] = new_id in RENDER_GLYPHS
        clone["renderer"] = new_id if clone["glyph"] else f"family:{clone.get('family')}"
        clone["name"] = english_caption(new_id, clone.get("name"))
        clone["what"] = english_blurb(new_id, clone["name"])
        ent = _index_raw().get(new_id) or {}
        clone["si_caption"] = ent.get("si_caption")
        clone["si_ref"] = ent.get("schedule") or ""
        clone["name_alias"] = None
        if not clone["glyph"] and clone["si_caption"]:
            clone["name"] = clone["what"] = _sentence(clone["si_caption"])
        clone["osm"] = f"traffic_sign=GB:{new_id}"
        clone["v1"] = "glyph" if clone["glyph"] else "fallback"
        _resize(clone)
        _paint_colours(clone)
        signs.append(clone)
        by_id[new_id] = clone
    for new_id, old_id in RENUMBER_ALSO.items():
        if new_id in by_id or old_id not in by_id:
            continue
        ent = _index_raw().get(new_id) or {}
        clone = json.loads(json.dumps(by_id[old_id]))
        clone.update({
            "id": new_id, "diagram": new_id, "index_id": new_id, "status": "current",
            "kind": "sign", "glyph": new_id in RENDER_GLYPHS,
            "v1": "glyph" if new_id in RENDER_GLYPHS else "fallback",
            "renderer": new_id if new_id in RENDER_GLYPHS else f"family:{clone.get('family')}",
            "renumbered_to": None, "osm": f"traffic_sign=GB:{new_id}",
            "si_caption": ent.get("si_caption"), "si_ref": ent.get("schedule") or "",
        })
        _resize(clone)
        clone["name_alias"] = english_caption(new_id, ent.get("caption"))
        clone["name"] = _sentence(ent["si_caption"]) if ent.get("si_caption") else clone["name_alias"]
        clone["what"] = clone["name"]
        _paint_colours(clone)
        signs.append(clone)
        by_id[new_id] = clone
        by_id[old_id].setdefault("renumbered_also", [])
        if new_id not in by_id[old_id]["renumbered_also"]:
            by_id[old_id]["renumbered_also"].append(new_id)
    for new_id, seed_id in OWN_ROW_FROM.items():
        if new_id in by_id or seed_id not in by_id:
            continue
        ent = _index_raw().get(new_id) or {}
        ov = overlay.get(new_id) or {}
        row = json.loads(json.dumps(by_id[seed_id]))
        glyph = bool(ov.get("glyph")) and new_id in RENDER_GLYPHS
        cap = _sentence(ent["si_caption"]) if ent.get("si_caption") else english_caption(new_id, ov.get("name") or "")
        row.update({
            "id": new_id, "diagram": new_id, "index_id": new_id, "status": ent.get("status") or "current",
            "kind": "sign", "glyph": glyph, "v1": "glyph" if glyph else "fallback",
            "renderer": new_id if glyph else f"family:{row.get('family')}",
            "renumbered_to": None, "renumbered_also": [], "osm": f"traffic_sign=GB:{new_id}",
            "name": cap, "what": cap, "name_alias": None,
            "si_caption": ent.get("si_caption"), "si_ref": ent.get("schedule") or "",
        })
        row.pop("aliases", None)
        _resize(row)
        _paint_colours(row)
        signs.append(row)
        by_id[new_id] = row
    for row in signs:
        face_aspect(row)
    # r3: drop retired and merged dest ids; keep merged ids as aliases on the target row.
    for old_id, new_id in sorted(merged.items()):
        if new_id in by_id:
            by_id[new_id].setdefault("aliases", [])
            if old_id not in by_id[new_id]["aliases"]:
                by_id[new_id]["aliases"].append(old_id)
    signs = [s for s in signs if s["id"] not in retired and s["id"] not in merged]
    return signs


def _mark(id, name, what, renderer, dims, pair=None, schedule="", extra=None):
    if id in MARKING_NAMES:
        name, what = MARKING_NAMES[id]
    row = {
        "id": id, "kind": "marking", "diagram": id, "status": "current",
        "name": name, "what": what, "renderer": renderer,
        "dimensions_m": dims, "pair": pair, "schedule": schedule,
        "source": {k: schedule or "TSM Chapter 5" for k in dims},
    }
    if extra:
        row.update(extra)
    return row


def markings():
    return [
        _mark("1008", "Centre line", "Broken white centre line on two-way roads ≤ 40 mph.",
              "dash", {"width": 0.10, "mark": 2.0, "gap": 4.0}, schedule="S11-4-6; TSM T2-1"),
        _mark("1008.1", "Centre line (fast)", "Broken white centre line > 40 mph.",
              "dash", {"width": 0.10, "mark": 3.0, "gap": 6.0}, schedule="S11-4-7; TSM T2-1"),
        _mark("1004", "Warning line", "Replaces the centre line on the approach to give-way, stop, signals, roundabouts (≤ 40 mph).",
              "dash", {"width": 0.10, "mark": 4.0, "gap": 2.0, "approach": 30.0}, pair="602", schedule="S11-4-2; TSM T2-3"),
        _mark("1004.1", "Warning line (fast)", "Warning line > 40 mph.",
              "dash", {"width": 0.10, "mark": 6.0, "gap": 3.0, "approach": 63.0}, schedule="S11-4-3; TSM T2-3"),
        _mark("1005", "Lane line", "Lane division ≤ 40 mph.",
              "dash", {"width": 0.10, "mark": 1.0, "gap": 5.0}, schedule="S11-4-4; TSM T2-1"),
        _mark("1005.1", "Lane line (fast)", "Lane division > 40 mph.",
              "dash", {"width": 0.10, "mark": 2.0, "gap": 7.0}, schedule="S11-4-5; TSM T2-1"),
        _mark("1013.1", "Double white lines (type A)", "No overtaking. Each line 100 mm, gap ≥ 90 mm, overall ≤ 900 mm.",
              "double_solid", {"width": 0.10, "gap": 0.09}, schedule="S9-6-23"),
        _mark("1012.1", "Edge line", "Carriageway edge. 100 mm urban, 150 mm fast, 200 mm motorway. Inset 0.225 m.",
              "solid", {"width": 0.10, "width_fast": 0.15, "width_motorway": 0.20, "inset": 0.225}, schedule="S11-4-11; TSM 2.5.8, T2-5"),
        _mark("1010", "Edge across a junction mouth", "1 m mark / 1 m gap at lay-bys and minor mouths. Width 100/150/200 by speed.",
              "dash", {"width": 0.10, "mark": 1.0, "gap": 1.0}, schedule="S11-4-10; TSM T2-5"),
        _mark("1003A", "Give-way line", "Double broken transverse line. Pairs with 602 and 1023A.",
              "give_way", {"width": 0.20, "mark": 0.6, "gap": 0.3, "pair_gap": 0.30, "setback": 0.5},
              pair="602", schedule="S9-6-3"),
        _mark("1003.1", "Roundabout give-way line", "Single broken line, 1000 mm mark / 1000 mm gap, width 200 or 300 mm.",
              "dash", {"width": 0.20, "mark": 1.0, "gap": 1.0}, pair="510", schedule="S11-4-1; TSM 6.2.2"),
        _mark("1003.3", "Mini-roundabout give-way line", "Give-way line used with 611.1.",
              "dash", {"width": 0.20, "mark": 0.6, "gap": 0.3}, pair="611.1", schedule="S9-6-6; TSM 6.3.6"),
        _mark("1003.4", "Mini-roundabout disc", "White island disc (preset A: 2.5 m) with three white circulation arrows on the carriageway outside the disc.",
              "mini_disc", {"diameter": 2.5, "min": 1.0, "max": 4.0, "arrows": 3, "arrow_length": 2.2, "arrow_gap": 1.0},
              pair="611.1", schedule="S9-6-5; TSM 6.3.3–6.3.4"),
        _mark("1023A", "Give-way triangle", "Hollow triangle 3750 × 1250 mm, stroke 150 mm. Base nearest 1003A.",
              "gw_triangle", {"length": 3.75, "base": 1.25, "stroke": 0.15},
              pair="1003A", schedule="S9-6-4"),
        _mark("1002.1", "Stop line (STOP sign)", "Solid 400 mm transverse line. Pairs with 601.1 and 1022.",
              "solid", {"width": 0.40}, pair="601.1", schedule="S9-6-1"),
        _mark("1001", "Stop line (signals)", "Solid 200/300 mm line. Primary signal head stands beyond this line. Setback unsourced (TSM Ch.6 unread).",
              "solid", {"width": 0.30, "setback": 2.0}, pair="3000", schedule="S14-2-46"),
        _mark("1022", "STOP word marking", "Elongated STOP (Sch17 Part 7, 1600 mm) at a 601.1.",
              "stop_word", {"letter_height": 1.6}, pair="601.1", schedule="S9-6-2; Sch17 Pt7"),
        _mark("1014", "Deflection arrow", "Curved deflection arrow 6 m (also 4.5 / 9 m). Head 2.0 × 0.7 m, shaft 0.20 m.",
              "deflection", {"length": 6.0, "shaft": 0.20, "head_width": 0.70, "head_length": 2.0}, schedule="S11-4-14"),
        _mark("1038", "Lane destination arrow", "Straight / turn arrows in the lane.",
              "arrow", {"length": 6.0, "length_fast": 9.0, "shaft": 0.25, "head_width": 0.9, "head_ratio": 0.28}, schedule="S11-4-20"),
        _mark("1055.1", "Crossing studs / square marks", "Square marks or studs at a signal-controlled crossing (and zebra studs).",
              "studs", {"size": 0.10, "pitch": 0.50}, pair="1001.3", schedule="S14-2-55"),
        _mark("zebra-stripes", "Zebra crossing stripes", "Alternate black/white stripes 500–715 mm. First stripe ≤ 1300 mm. Crossing width 2.4–10 m.",
              "zebra", {"depth": 3.0, "stripe": 0.60, "stripe_min": 0.50, "stripe_max": 0.715},
              pair="4007", schedule="Sch14 Pt1 para 18", extra={"kind": "marking", "status": "current"}),
        _mark("1001.3", "Zig-zag lines (signal crossing)", "Keep the zigzag area clear at a Puffin/signal crossing. 8 marks × 2 m, width 100 mm.",
              "zigzag", {"width": 0.10, "mark": 2.0, "amplitude": 0.25, "count": 8}, pair="1055.1", schedule="S14-2-51"),
        _mark("1001.4", "Zig-zag lines (zebra)", "Zig-zag at a zebra. Amplitude is an engine-default (diagram label unread).",
              "zigzag", {"width": 0.10, "mark": 2.0, "amplitude": 0.25, "count": 8}, pair="zebra-stripes", schedule="S14-2-52"),
        _mark("1018.1", "Double yellow line", "No waiting. 50/75/100 mm each, equal gap. Inset unsourced.",
              "double_yellow", {"width": 0.075, "gap": 0.075, "inset": 0.25}, schedule="S7-4-1"),
        _mark("1017", "Single yellow line", "No waiting during the times on the plate. End (T) marks included.",
              "solid_yellow", {"width": 0.075, "inset": 0.25, "end_mark": 0.30}, schedule="S7-4-2"),
    ]


def _furn(id, name, what, renderer, spec, dims, source, extra=None):
    if id in FURNITURE_NAMES:
        name, what = FURNITURE_NAMES[id]
    row = {
        "id": id, "kind": "furniture", "name": name, "what": what,
        "renderer": renderer, "spec": spec, "dimensions_m": dims, "source": source,
    }
    if extra:
        row.update(extra)
    return row


def furniture():
    eng = "engine-default (spec 019/015 text not copied into this tree)"
    return [
        _furn("chs-76", "CHS Ø76 mm post", "UK roadside post (BS EN 12899-1 class). Galvanised grey, black cap.",
              "chs", "spec 019 §1 (not in repo)", 
              {"diameter": 0.076, "underside_verge": 1.50, "underside_footway": 2.10, "base": 0.20},
              {k: eng for k in ("diameter", "underside_verge", "underside_footway", "base")}),
        _furn("chs-114", "CHS Ø114 mm post", "Larger CHS for wide ADS plates.",
              "chs", "spec 019 §1 (not in repo)",
              {"diameter": 0.114, "underside_verge": 1.50, "base": 0.30},
              {k: eng for k in ("diameter", "underside_verge", "base")}),
        _furn("chs-219", "CHS Ø219 mm gantry / cantilever leg", "A single Ø219 mm leg. Portal gantry is a separate item.",
              "chs", "spec 019 §1 (not in repo)",
              {"diameter": 0.219, "clearance": 5.50},
              {"diameter": eng, "clearance": "unsourced (DMRB not checked)"}),
        _furn("two-post", "Two-post ADS mount", "Pair of CHS legs for green/white/blue/brown rectangles. Spacing 1.2 m is an engine-default.",
              "two_post", "spec 015/019 (not in repo)",
              {"diameter": 0.076, "spacing": 1.2, "underside": 1.50},
              {k: eng for k in ("diameter", "spacing", "underside")}),
        _furn("street-name-posts", "Street-name two-post", "Ø 60 mm pair, underside 0.80 m. Not a TSRGD diagram.",
              "two_post", "spec 015 StreetName (not in repo)",
              {"diameter": 0.060, "underside": 0.80, "spacing": 0.9},
              {k: eng for k in ("diameter", "underside", "spacing")},
              extra={"kind": "non-tsrgd", "status": "not-2016"}),
        _furn("belisha", "Belisha beacon (TSRGD 4007)", "Black-and-white banded post, yellow / fluorescent-yellow globe. Lowest band black. Both kerbs of a zebra.",
              "belisha", "TSRGD 2016 Sch 14 Pt 2 item 27 (diagram 4007), Pt 4 para 13",
              {"globe": 0.30, "post": 2.3, "band": 0.30, "lowest_band": 0.8},
              {"globe": "SI 2016 diagram 4007, printed p461: globe 275-335 mm (0.30 drawn)",
               "post": "SI 2016 diagram 4007, printed p461: 2100-3100 mm ground to globe (2.3 drawn)",
               "band": "SI 2016 Sch 14 Pt 4 para 13(3)(b), printed p494: 275-335 mm",
               "lowest_band": "SI 2016 Sch 14 Pt 4 para 13(3)(a)-(b), printed p494: black, up to 1 m (0.8 drawn)"}),
        _furn("telegraph", "Telegraph pole", "Wood pole, BS 1990 9 m medium class.",
              "telegraph", "BS 1990-1:1984 Table 1 (via TKW summary); IET guide to wood pole lines",
              {"exposed": 7.5, "planted": 1.5, "tip": 0.150, "ground": 0.220},
              {"exposed": "9 m nominal length (BS 1990-1 Table 1) minus 1.5 m planted",
               "planted": "IET guide (BS 1990 design data): ground line assumed 1.5 m from the butt",
               "tip": "BS 1990-1:1984 Table 1, 9 m medium pole, min top diameter 150 mm (tkw.biz.pl/sizes_of_poles)",
               "ground": "BS 1990-1:1984 Table 1, 9 m medium pole, min diameter 220 mm at 1.5 m from the butt (tkw.biz.pl/sizes_of_poles)"}),
        _furn("pylon-l12d", "L12 D pylon", "National Grid L12 D 400 kV lattice tower.",
              "pylon", "National Grid L12 (TS 43-11 / NGTS 3.4.3; figures via telcontar.net)",
              {"height": 46.5, "base_width": 7.1, "crossarm_width": 18.2},
              {k: "telcontar.net/Power/pylons/L12 tower table, L12 D (source: Hinkley Point C)" for k in ("height", "base_width", "crossarm_width")}),
        _furn("gantry-portal", "Portal gantry", "Two Ø219 mm legs. 5.5 m clearance unsourced (DMRB not checked). Width clamp 8–18 m is an engine heuristic.",
              "portal", "spec 015/019 (not in repo)",
              {"clearance": 5.50, "leg": 0.219, "width_min": 8.0, "width_max": 18.0},
              {"clearance": "unsourced (DMRB not checked)", "leg": eng, "width_min": "engine heuristic", "width_max": "engine heuristic"},
              extra={"section": "gantry-vms", "type": "portal"}),
    ] + gantry_vms_placeholders()


# Scope (SCOPE.md): gantries, VMS and lane signals. Placeholders carry no figures until a source is opened;
# validate.py requires todo + sources_needed on each and one row per GANTRY_VMS_TYPES entry.
def gantry_vms_placeholders():
    ph = lambda id, name, what, typ, todo, needed: _furn(
        id, name, what, "placeholder", "placeholder (no figures until sourced)", {}, {},
        extra={"section": "gantry-vms", "type": typ, "placeholder": True, "status": "placeholder",
               "todo": todo, "sources_needed": needed})
    return [
        ph("gantry-cantilever", "Cantilever gantry", "Single leg with an arm over one or more lanes. Placeholder.",
           "cantilever", "Leg/arm geometry, clearance and sign envelope from DMRB and National Highways standard details.",
           ["DMRB CD 365 / structures standards for sign gantries (UNVERIFIED)", "National Highways MCHW drawings (UNVERIFIED)"]),
        ph("vms-text", "Large text variable message sign", "Motorway text VMS (e.g. MS4 text panel): lines of LED characters. Placeholder.",
           "vms-text", "Panel size, character matrix and line count; legends from TSRGD 2016 Sch 16 Pts 3-6; performance classes BS EN 12966.",
           ["TSRGD 2016 Sch 16 (printed p524-532, verified)", "BS EN 12966 (named in Sch 16; standard not opened, UNVERIFIED)", "National Highways MS4 specification TR2516/TR2517 (UNVERIFIED)"]),
        ph("vms-pictogram", "Pictogram variable message sign", "Motorway VMS with a full-colour pictogram area beside the text. Placeholder.",
           "vms-pictogram", "Pictogram aperture size and pixel pitch; permitted pictograms from TSRGD 2016 Sch 15/16.",
           ["TSRGD 2016 Sch 15 Pt 2 (printed p509-520, verified)", "BS EN 12966 (UNVERIFIED)", "National Highways MS4 specification (UNVERIFIED)"]),
        ph("lane-signal", "Smart motorway lane signal (AMI)", "Above-lane signal: speed roundel, red X, lane arrows, with flashing amber or red lamps. Placeholder.",
           "lane-signal", "Aspect set (TSRGD 2016 Sch 15 items 1-16; Sch 14 Pt 1 para 16 lane control); flash timing Sch 15 Pt 4 (60-90 per minute, pairs alternate); enclosure size.",
           ["TSRGD 2016 Sch 15 Pts 2 and 4 (printed p509-522, verified)", "TSRGD 2016 Sch 14 Pt 1 para 16 (printed p434, verified)", "National Highways AMI/MS3 specification (UNVERIFIED)"]),
        ph("verge-ms", "Verge-mounted message sign", "Smaller post-mounted message sign beside the carriageway. Placeholder.",
           "verge-ms", "Panel size, post and mounting height; flashing lamps for post-mounted signs per TSRGD 2016 Sch 15 Pt 4 para 3.",
           ["TSRGD 2016 Sch 15 Pt 4 para 3 (printed p522, verified)", "National Highways verge VMS specification (UNVERIFIED)"]),
    ]


def country_meta(signs):
    n_signs = len(signs)
    n_glyph = sum(1 for s in signs if s.get("glyph"))
    ov = _overlay()
    licence = ov.get("licence") or {
        "diagrams": "Crown copyright. TSRGD 2016 diagrams: derived under Open Government Licence v3.0. Traffic Signs Manual: see LICENCE.md (non-commercial notice, not OGL). Faces are redrawn identification silhouettes; hex colours approximate BS EN 12899-1 classes.",
        "typeface": "The Transport typeface is not shipped. Legends are Schedule 17 stand-in strokes.",
        "osm": "OpenStreetMap contributors, ODbL.",
    }
    fonts = ov.get("fonts") or None
    meta = OrderedDict([
        ("id", "uk"),
        ("name", "United Kingdom"),
        ("iso", "GB"),
        ("applies", "England, Scotland and Wales (TSRGD). Northern Ireland uses a parallel TSRNI set."),
        ("spec", ["015-uk-know-your-traffic-signs", "019-street-posts"]),
        ("source_of_truth", "countries/uk/*.json plus tsrgd2016_index.json. Extract is the only JSON writer."),
        ("licence", licence),
        ("fonts", [
            {
                "id": "transport",
                "name": "Transport Heavy / Transport Medium",
                "role": "Official TSRGD legend",
                "shipped": False,
                "reason": "Commercial typeface. Spec 015 / DATA_SOURCES forbid bundling it.",
            },
            {
                "id": "sch17-standin",
                "name": "Schedule 17 stand-in (polygons / rects / arcs)",
                "role": "Procedural legends including lower case. Part 5 VMS seven-bar on MS4 only.",
                "shipped": True,
                "reason": "No Transport file. Tile 8 sw, cap 5.6 sw, stem 1.0/1.2 sw.",
            },
            {
                "id": "wiki-standin",
                "name": "Atlas stand-in (this site)",
                "role": "SVG recreation of the Unity drawers",
                "shipped": True,
                "reason": "Same colours and proportions. Iterate here, then port strokes back to C#.",
            },
        ]),
        ("colours", COLOURS),
        ("counts", {
            "signs": n_signs,
            "glyphs": n_glyph,
            "fallback": n_signs - n_glyph,
            "current": sum(1 for s in signs if s.get("status") == "current"),
            "non_tsrgd": sum(1 for s in signs if s.get("kind") == "non-tsrgd" or s.get("status") == "not-2016"),
        }),
        ("units", "metres"),
        ("renumber", json.loads((UK / "tsrgd2016_index.json").read_text()).get("renumber") if (UK / "tsrgd2016_index.json").exists() else {}),
    ])
    if fonts:
        meta["fonts"] = fonts
    return meta


def _merge(old: list, new: list, ids: set[str] | None) -> list:
    if not ids:
        return new
    by = {row["id"]: row for row in old}
    matched = []
    for row in new:
        if row["id"] in ids:
            by[row["id"]] = row
            matched.append(row["id"])
    if not matched:
        return old
    order = [row["id"] for row in old]
    for i in matched:
        if i not in order:
            order.append(i)
    return [by[i] for i in order if i in by]


def _load_list(path: Path) -> list:
    if path.exists():
        return json.loads(path.read_text())
    return []


def catalogue_cs(dest: Path | None = None) -> Path:
    """Resolve UkTsrgdCatalogue.cs. No machine-local default."""
    if dest is not None:
        p = Path(dest)
        if p.is_file():
            return p
        cs = p / "unity/GridForge/Assets/Scripts/UkTsrgdCatalogue.cs"
        if cs.exists():
            return cs
        raise SystemExit(f"extract: no UkTsrgdCatalogue.cs under {p}")
    if VENDOR_CS.exists():
        return VENDOR_CS
    raise SystemExit(
        "extract: pass --dest DIR (vendor/gridforge/UkTsrgdCatalogue.cs is missing)"
    )


STAMP = UK / ".extract-stamp.json"
GUARDED = ("country.json", "signs.json", "markings.json", "furniture.json", "siting.json")


def _sha(path: Path) -> str | None:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def _check_hand_edits(force: bool) -> None:
    """Refuse to overwrite JSON that changed since the last extract (a hand edit).

    Hand fixes belong in overlay.json, uk_english_names.py, sources/ or the
    index builder; a re-extract would silently revert them otherwise.
    """
    if force or not STAMP.exists():
        return
    stamp = json.loads(STAMP.read_text())
    edited = [n for n in GUARDED if stamp.get(n) and _sha(UK / n) != stamp[n]]
    data_js = ROOT / "site/assets/data.js"
    if stamp.get("data.js") and _sha(data_js) != stamp["data.js"]:
        edited.append("site/assets/data.js")
    if edited:
        raise SystemExit(
            "extract: refusing to overwrite hand-edited " + ", ".join(edited)
            + ". Move the fix into overlay.json / uk_english_names.py / sources/, "
            "or pass --force to discard it."
        )


def _write_stamp() -> None:
    stamp = {n: _sha(UK / n) for n in GUARDED}
    stamp["data.js"] = _sha(ROOT / "site/assets/data.js")
    STAMP.write_text(json.dumps(stamp, indent=2, sort_keys=True) + "\n")


def extract(ids: list[str] | None = None, dest: Path | None = None, force: bool = False) -> dict:
    """Write countries/uk JSON and site/assets/data.js.

    ids=None rebuilds the full catalogue. A non-empty ids list merges those
    rows into the existing JSON (dest is still parsed in full so counts stay honest).
    Names, glyph flags and licence come from overlay.json + tsrgd2016_index.json
    so a re-extract is idempotent.
    """
    _check_hand_edits(force)
    cs = catalogue_cs(dest)
    rows = parse_catalogue(cs)
    new_signs = build_signs(rows)
    new_marks = markings()
    new_furn = furniture()
    want = set(ids) if ids else None
    UK.mkdir(parents=True, exist_ok=True)
    if want:
        signs = _merge(_load_list(UK / "signs.json"), new_signs, want)
        marks = _merge(_load_list(UK / "markings.json"), new_marks, want)
        furn = _merge(_load_list(UK / "furniture.json"), new_furn, want)
        known = {r["id"] for r in new_signs + new_marks + new_furn}
        missing = sorted(want - known)
        if missing:
            raise SystemExit("extract: unknown id(s): " + ", ".join(missing))
    else:
        signs, marks, furn = new_signs, new_marks, new_furn
    meta = country_meta(signs)
    (UK / "country.json").write_text(json.dumps(meta, indent=2) + "\n")
    (UK / "signs.json").write_text(json.dumps(signs, indent=2) + "\n")
    (UK / "markings.json").write_text(json.dumps(marks, indent=2) + "\n")
    (UK / "furniture.json").write_text(json.dumps(furn, indent=2) + "\n")
    (UK / "siting.json").write_text(json.dumps(SITING, indent=2) + "\n")
    atlas = {
        "country": meta,
        "signs": signs,
        "markings": marks,
        "furniture": furn,
        "siting": SITING,
        "colours": COLOURS,
    }
    js = "window.ATLAS_UK = " + json.dumps(atlas) + ";\n"
    (ROOT / "site/assets/data.js").write_text(js)
    _write_stamp()
    scope = ",".join(ids) if ids else "all"
    print(f"extract [{scope}]: {len(signs)} signs, {len(marks)} markings, {len(furn)} furniture")
    return atlas


def main(argv: list[str] | None = None):
    import argparse
    p = argparse.ArgumentParser(description="Extract UK catalogue JSON from GridForge dest.")
    p.add_argument("--id", "--item", dest="id", action="append", help="Merge this id only (repeatable). Default: all.")
    p.add_argument("--all", action="store_true", help="Extract the full catalogue (default).")
    p.add_argument(
        "--dest",
        type=Path,
        help="GridForge dest root or path to UkTsrgdCatalogue.cs. Default: vendor/gridforge/UkTsrgdCatalogue.cs",
    )
    p.add_argument("--force", action="store_true", help="Overwrite JSON even if it was hand-edited since the last extract.")
    args = p.parse_args(argv)
    extract(ids=None if args.all or not args.id else args.id, dest=args.dest, force=args.force)


if __name__ == "__main__":
    main()
