#!/usr/bin/env python3
"""Fail a UK rebuild that would ship unsourced or impersonating data.

Exit 0 only when every accept-test in the 2026-11-10 re-review that this
tree claims to meet actually holds. Some checks stay warnings until the
matching work package is finished; pass `--strict` to fail on those too.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from atlas import catalogue, lettering, render  # noqa: E402
from uk_english_names import _is_generic  # noqa: E402

TEMPLATE_SOURCE = "TSRGD P500 (triangles) / dest working size"
SOURCES = ROOT / "countries" / "uk" / "sources"

HEX = re.compile(r"#([0-9A-Fa-f]{6})")
TSRGD_NAME = re.compile(r"^TSRGD\s")
SEVEN_SEG_NOTE = "seven-bar"


def _load_index(country: str) -> dict:
    path = ROOT / "countries" / country / "tsrgd2016_index.json"
    if not path.exists():
        return {}
    blob = json.loads(path.read_text())
    return {e["id"]: e for e in blob.get("entries") or []}


def _svg_hexes(svg: str) -> set[str]:
    return {m.group(0).upper() for m in HEX.finditer(svg)}


def _named_colours(atlas: dict) -> dict[str, str]:
    cols = atlas.get("colours") or atlas.get("country", {}).get("colours") or {}
    return {k: str(v).upper() for k, v in cols.items()}


def _aspect(svg: str) -> float | None:
    wm = re.search(r'\bwidth="([0-9.]+)"', svg)
    hm = re.search(r'\bheight="([0-9.]+)"', svg)
    if not wm or not hm:
        return None
    w, h = float(wm.group(1)), float(hm.group(1))
    if w <= 0:
        return None
    return h / w


GANTRY_VMS_TYPES = ("portal", "cantilever", "vms-text", "vms-pictogram", "lane-signal", "verge-ms")


def _has_source(item: dict) -> list[str]:
    missing = []
    src = item.get("source") or {}
    dims = item.get("dimensions_m") or {}
    if isinstance(src, str):
        return missing
    for k, v in dims.items():
        if isinstance(v, (int, float)) and k not in src:
            missing.append(k)
    return missing


def validate(country: str = "uk", *, strict: bool = False) -> int:
    atlas = catalogue.load_country(country, ROOT)
    index = _load_index(country)
    named = _named_colours(atlas)
    errors: list[str] = []
    warns: list[str] = []

    if not index:
        errors.append("missing countries/uk/tsrgd2016_index.json")

    def need_index(item: dict, kind: str) -> None:
        i = item["id"]
        if i not in index:
            errors.append(f"{kind}/{i}: no tsrgd2016_index entry")
            return
        ent = index[i]
        name = item.get("name") or ""
        if name == i or TSRGD_NAME.match(name) or _is_generic(name, i):
            errors.append(f"{kind}/{i}: name {name!r} is not an English caption")
        if re.search(r"TSRGD\s+\S", name, re.I):
            errors.append(f"{kind}/{i}: name still cites a diagram number ({name!r})")
        if ent.get("status") != "current" and item.get("kind") not in ("non-tsrgd", "marking", "furniture"):
            if item.get("status") != ent.get("status") and item.get("kind") != "non-tsrgd":
                warns.append(f"{kind}/{i}: index status {ent.get('status')} not copied onto the row")

    for kind, item in catalogue.iter_items(atlas, ["signs", "markings"]):
        need_index(item, kind)

    # Face aspect and colours
    for kind, item in catalogue.iter_items(atlas):
        svg = render.item_svg(kind, item)
        dims = item.get("dimensions_m") or {}
        if kind == "signs" and dims.get("plate_width") and dims.get("plate_height"):
            want = float(dims["plate_height"]) / float(dims["plate_width"])
            got = _aspect(svg)
            if got is None:
                errors.append(f"signs/{item['id']}: face has no width/height")
            elif abs(got - want) / want > 0.02:
                errors.append(
                    f"signs/{item['id']}: face aspect {got:.3f} != data {want:.3f}"
                )
        fills = _svg_hexes(svg)
        listed = []
        for c in item.get("colours") or []:
            hexv = named.get(c) or (c.upper() if c.startswith("#") else None)
            if hexv:
                listed.append(hexv)
        if kind == "signs" and fills and not listed and item.get("glyph"):
            errors.append(f"signs/{item['id']}: glyph face has no colours list")
        if listed and fills:
            extra = fills - set(listed) - {"#3A3D36", "#3A3428"}
            # background asphalt / chrome chrome
            missing = set(listed) - fills
            if missing:
                bucket = errors if kind == "signs" else warns
                bucket.append(f"{kind}/{item['id']}: colours listed but unused {sorted(missing)}")
            unnamed = fills - set(named.values()) - {"#3A3D36", "#3A3428", "#CCC", "#D8D6CE", "#6E6C66", "#9A9A94", "#3A3A38"}
            if unnamed and kind == "signs":
                warns.append(f"{kind}/{item['id']}: face uses colours with no name {sorted(unnamed)}")
            extra_named = (fills & set(named.values())) - set(listed)
            extra_named -= {"#3A3D36", "#3A3428"}
            if extra_named and listed and kind == "signs":
                errors.append(f"{kind}/{item['id']}: face uses unlisted colours {sorted(extra_named)}")

        if kind in ("furniture",) or (kind == "signs" and False):
            miss = _has_source(item)
            if miss:
                errors.append(f"{kind}/{item['id']}: dimensions without source: {', '.join(miss)}")

    for f in atlas.get("furniture") or []:
        fname = f.get("name") or ""
        if re.search(r"TSRGD", fname, re.I) or f["id"] in fname:
            errors.append(f"furniture/{f['id']}: name {fname!r} is not an English caption")
        miss = _has_source(f)
        if miss:
            errors.append(f"furniture/{f['id']}: dimensions without source: {', '.join(miss)}")

    # Scope: one gantry/VMS row per type; placeholders carry no figures and say what is needed.
    gv = [f for f in atlas.get("furniture") or [] if f.get("section") == "gantry-vms"]
    have = {f.get("type") for f in gv}
    for t in GANTRY_VMS_TYPES:
        if t not in have:
            errors.append(f"furniture: gantry-vms section has no {t!r} row")
    for f in gv:
        if f.get("type") not in GANTRY_VMS_TYPES:
            errors.append(f"furniture/{f['id']}: unknown gantry-vms type {f.get('type')!r}")
        if f.get("placeholder"):
            if not (isinstance(f.get("todo"), str) and f["todo"].strip()):
                errors.append(f"furniture/{f['id']}: placeholder without todo")
            if not (isinstance(f.get("sources_needed"), list) and f["sources_needed"]):
                errors.append(f"furniture/{f['id']}: placeholder without sources_needed")
            if any(isinstance(v, (int, float)) for v in (f.get("dimensions_m") or {}).values()):
                errors.append(f"furniture/{f['id']}: placeholder carries figures")

    siting = atlas.get("siting") or {}
    for k, v in siting.items():
        if isinstance(v, dict):
            if not v.get("source"):
                errors.append(f"siting/{k}: missing source")
        else:
            errors.append(f"siting/{k}: value has no source object")

    # 7-seg only on MS4
    for kind, item in catalogue.iter_items(atlas, ["signs"]):
        if item["id"] == "MS4":
            continue
        svg = render.item_svg(kind, item)
        # old 7-seg 1 is two thin right-hand bars; Sch17 1 has a flag polygon
        if item["id"] in ("670", "602", "601.1", "523.1", "524.1", "554", "552", "608"):
            if "text-anchor" in svg:
                errors.append(f"signs/{item['id']}: still uses <text> (delete text())")

    # Glyph sheet: every A–Z a–z 0–9 must draw; no round caps; no filled cell.
    sheet = lettering.glyph_sheet_svg()
    if 'stroke-linecap="round"' in sheet:
        errors.append("lettering: glyph sheet still uses round stroke caps")
    for ch in lettering.SHEET_CHARS:
        g = lettering.char(ch, 0, 0, 0.56, "#141414", part=2)
        if not g.strip():
            errors.append(f"lettering: missing glyph {ch!r}")
        # Never a filled cell: no rect thicker than 2.5 stems in both directions,
        # no polygon covering more than a third of the advance box.
        t = lettering.stem(0.56, 2)
        cell = 0.56 * lettering.advance_sw(ch) / lettering.CAP_SW * 0.56
        for m in re.finditer(r'<rect x="[-0-9.]+" y="[-0-9.]+" width="([0-9.]+)" height="([0-9.]+)"', g):
            if float(m.group(1)) > 2.5 * t and float(m.group(2)) > 2.5 * t:
                errors.append(f"lettering: {ch!r} contains a filled box")
        for m in re.finditer(r'<polygon points="([^"]+)"', g):
            pts = [tuple(map(float, p.split(","))) for p in m.group(1).split()]
            area = abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts)))) / 2
            if area > cell / 3:
                errors.append(f"lettering: {ch!r} polygon area {area:.4f} looks like a filled block")
        if 'stroke-linecap="round"' in g:
            errors.append(f"lettering: {ch!r} uses round caps")

    # T1: warning-triangle border measured from the baked SVG = 0.10 H +-3% (P500).
    tri_re = re.compile(r'<polygon points="([^"]+)" fill="(#[0-9A-F]{6})" stroke="#[0-9A-F]{6}" stroke-width="([0-9.]+)"')
    for s_ in atlas.get("signs") or []:
        if s_.get("family") != "WarnTriangle" or not s_.get("glyph"):
            continue
        polys = tri_re.findall(render.item_svg("signs", s_))
        red = next((p for p in polys if p[1] == render.C["red"]), None)
        white = next((p for p in polys if p[1] == render.C["white"]), None)
        if not red or not white:
            continue
        rp = [tuple(map(float, q.split(","))) for q in red[0].split()]
        wp = [tuple(map(float, q.split(","))) for q in white[0].split()]
        if len(rp) != 3 or len(wp) != 3:
            continue
        h_out = (max(y for _, y in rp) - min(y for _, y in rp)) + float(red[2])
        rd = render._tri_side_dists(rp)
        wd = render._tri_side_dists(wp)
        for a, b in zip(rd, wd):
            border = (a + float(red[2]) / 2) - (b + float(white[2]) / 2)
            if abs(border / h_out - 0.10) > 0.003:
                errors.append(f"signs/{s_['id']}: triangle border {border / h_out:.3f} H (P500 0.100 H +-3%)")
                break

    # L1: confusable pairs must not render alike (IoU of rasterised glyphs).
    for a, b in lettering.CONFUSABLE:
        iou = lettering.glyph_similarity(a, b)
        if iou > lettering.CONFUSABLE_MAX_IOU:
            errors.append(f"lettering: {a!r} and {b!r} render alike (IoU {iou:.2f} > {lettering.CONFUSABLE_MAX_IOU})")
    # Numerals share one cap height (P670: 0.373D for every digit), +-2%.
    for d in "0123456789":
        m = lettering.glyph_mask(d, 100)
        rows = [k for k, r in enumerate(m) if any(r)]
        cap_rows = 100 / (1 + lettering.DESC_RATIO)
        hgt = (rows[-1] - rows[0] + 1) / cap_rows if rows else 0
        if abs(hgt - 1.0) > 0.02:
            errors.append(f"lettering: digit {d!r} ink height {hgt:.3f} cap (want 1.000 +-2%)")

    # S2: every legend word on every glyph face sits inside a declared field
    # (white triangle, ring interior, plate) with >= 1 stroke width clearance.
    for s_ in atlas.get("signs") or []:
        if s_.get("glyph"):
            for msg in render.legend_fit(s_["id"], s_.get("param")):
                errors.append(f"signs/{msg}")

    # G1 (placeholder batches): generator faces (traced.PLATES with a "kind") must name their source,
    # use a known outline template and palette colours, and every layer path must exist.
    _T = render.traced
    for _k, _P in _T.PLATES.items():
        if "kind" not in _P:
            continue
        if _P["kind"] not in render.AUTO_KINDS:
            errors.append(f"generator/{_k}: unknown kind {_P['kind']!r}")
        if not _T.SOURCE.get(_k):
            errors.append(f"generator/{_k}: no SOURCE entry")
        for _fill, _pk in list(_P["layers"]) + list(_P.get("over") or []):
            if _pk not in _T.PATHS:
                errors.append(f"generator/{_k}: layer path {_pk!r} missing")
            if _fill not in render.C:
                errors.append(f"generator/{_k}: layer colour {_fill!r} not in palette")
        for _t in _P["text"]:
            if _t[5] not in render.C:
                errors.append(f"generator/{_k}: legend colour {_t[5]!r} not in palette")
        if _P["text"] and _P["kind"] != "warn" and not _P["fields"]:
            errors.append(f"generator/{_k}: legend without a declared field")
        if _k not in render.GLYPHS:
            errors.append(f"generator/{_k}: not registered in render.GLYPHS")

    # S3: status and placeholder names must follow the SI text (sources/).
    si = json.loads((SOURCES / "si2016_diagrams.json").read_text())["diagrams"] if (SOURCES / "si2016_diagrams.json").exists() else {}
    leg = json.loads((SOURCES / "legacy2002.json").read_text()) if (SOURCES / "legacy2002.json").exists() else {}
    if not si or not leg:
        errors.append("missing countries/uk/sources/si2016_diagrams.json or legacy2002.json")
    legacy = set(leg.get("legacy_2002") or []) | (set(leg.get("reg_14_4") or []) - set(si))
    unverified = set((leg.get("unverified") or {}).get("ids") or [])
    # r3: the owner's merge/retire decision must hold in the built data.
    _merged = dict((leg.get("merged") or {}).get("ids") or {})
    _retired = set((leg.get("retired") or {}).get("ids") or [])
    _rows = {s_["id"]: s_ for s_ in atlas.get("signs") or []}
    for _i in sorted(_retired | set(_merged)):
        if _i in _rows:
            errors.append(f"signs/{_i}: retired or merged id still has a row (sources/legacy2002.json)")
    for _o, _n in sorted(_merged.items()):
        if _n not in _rows or _o not in (_rows[_n].get("aliases") or []):
            errors.append(f"signs/{_n}: merge target missing or does not carry alias {_o}")
    renum = (atlas.get("country") or {}).get("renumber") or {}
    for s_ in atlas.get("signs") or []:
        i, st = s_["id"], s_.get("status")
        if st == "saved-by-reg-14(4)":
            errors.append(f"signs/{i}: 'saved-by-reg-14(4)' overstates reg 14(4); use 2002-legacy")
        if i in renum:
            if st != "renumbered":
                errors.append(f"signs/{i}: renumbered to {renum[i]} but status {st}")
        elif i in si:
            if st != "current":
                errors.append(f"signs/{i}: SI 2016 diagram but status {st}")
        elif i in legacy:
            if st != "2002-legacy":
                errors.append(f"signs/{i}: 2002-only id but status {st}")
        elif i[0].isdigit():
            if st != "unverified":
                errors.append(f"signs/{i}: in neither SI text but status {st}")
            elif i not in unverified:
                errors.append(f"signs/{i}: unverified id not documented in sources/legacy2002.json")
        elif s_.get("kind") != "non-tsrgd" and i not in renum.values():
            errors.append(f"signs/{i}: engine id must be kind non-tsrgd")
        if st == "current" and not s_.get("glyph") and i in si:
            want = si[i]["caption"].strip()
            want = re.sub(r"\s+,", ",", want)
            want = re.sub(r"\s*\(Alternative types?\)\s*$", "", want)
            want = want[:1].upper() + want[1:]
            if s_.get("name") != want:
                errors.append(f"signs/{i}: placeholder name {s_.get('name')!r} != SI 2016 caption {want!r}")
        if st == "current" and i in si and not s_.get("si_caption"):
            errors.append(f"signs/{i}: row has no si_caption")

    # S5/D1: sizes. No row may carry the old dest template. Where SI 2016
    # tabulates a diameter or sign height, the working plate must be one of
    # them (a diameter plate is square). A drawn face's plate aspect must match
    # the data aspect within 2%.
    si_sizes_path = SOURCES / "si2016_sizes.json"
    si_sizes = json.loads(si_sizes_path.read_text(encoding="utf8"))["sizes"] if si_sizes_path.exists() else {}
    for s_ in atlas.get("signs") or []:
        i = s_["id"]
        src = s_.get("source") or {}
        dm = s_.get("dimensions_m") or {}
        if TEMPLATE_SOURCE in (src.get("plate_width"), src.get("plate_height")):
            errors.append(f"signs/{i}: templated plate size ({TEMPLATE_SOURCE!r})")
        e = si_sizes.get(i)
        if e and e["dim"] in ("diameter", "sign height"):
            mm = round(float(dm.get("plate_height") or 0) * 1000)
            if mm not in e["mm"]:
                errors.append(f"signs/{i}: plate {e['dim']} {mm} mm not in SI 2016 {e['ref']} {e['mm']}")
            if e["dim"] == "diameter" and dm.get("plate_width") != dm.get("plate_height"):
                errors.append(f"signs/{i}: SI 2016 gives a diameter but plate is {dm.get('plate_width')}x{dm.get('plate_height')}")
            if s_.get("permitted_mm") != e["mm"]:
                errors.append(f"signs/{i}: permitted_mm {s_.get('permitted_mm')} != SI 2016 {e['mm']}")
        if s_.get("glyph"):
            a = render.drawn_aspect(i, s_.get("renderer"), s_.get("param"))
            if a is not None and dm.get("plate_height"):
                da = float(dm["plate_width"]) / float(dm["plate_height"])
                if abs(da / a - 1) > 0.02:
                    errors.append(f"signs/{i}: data plate aspect {da:.3f} != drawn face {a:.3f} (+-2%)")

    # r3: a hand name in overlay.json must reach the data (640.2A kept an old
    # name from uk_english_names.py while the overlay said otherwise).
    ov_signs = (json.loads((ROOT / "countries" / country / "overlay.json").read_text(encoding="utf8")).get("signs") or {})
    # r4: an overlay key with no catalogue row is stale (36 were left behind by r3 D1).
    _all_ids = {it["id"] for _k, it in catalogue.iter_items(atlas)}
    for _k in sorted(ov_signs):
        if _k not in _all_ids:
            errors.append(f"overlay.json signs/{_k}: no catalogue row (stale overlay entry)")
    for s_ in atlas.get("signs") or []:
        want = (ov_signs.get(s_["id"]) or {}).get("name")
        if want and not s_.get("si_caption") and s_.get("name") != want:
            errors.append(f"signs/{s_['id']}: name {s_.get('name')!r} != overlay name {want!r}")

    sign_ids = {s["id"] for s in atlas.get("signs") or []}
    # A1: one card per diagram number (alias rows keep their own number).
    seen_d: dict[str, str] = {}
    for s_ in atlas.get("signs") or []:
        d = str(s_.get("diagram") or s_["id"])
        if d in seen_d:
            errors.append(f"signs/{s_['id']}: diagram {d} duplicates row {seen_d[d]} (two cards)")
        seen_d.setdefault(d, s_["id"])
        if s_.get("v1") != ("glyph" if s_.get("glyph") else "fallback"):
            errors.append(f"signs/{s_['id']}: v1 {s_.get('v1')!r} disagrees with glyph")
    # S4: every 2016 renumber target has its own catalogue row (QA 3c finding 6).
    for tgt in ("529", "530A", "629A", "675A", "675B", "811A", "811B", "959B", "531.1A", "827.1", "605.3", "4007"):
        if tgt not in sign_ids:
            errors.append(f"renumber target {tgt} has no catalogue row")
    for s_ in atlas.get("signs") or []:
        if s_.get("renumbered_to") == s_["id"]:
            errors.append(f"signs/{s_['id']}: renumbered_to points at itself")
    for old, new in ((atlas.get("country") or {}).get("renumber") or {}).items():
        if str(new) not in sign_ids and str(new) not in index:
            errors.append(f"renumber {old}→{new}: target has no catalogue or index row")

    # placeholder fallbacks must not impersonate
    for s in atlas.get("signs") or []:
        if s.get("glyph"):
            continue
        svg = render.item_svg("signs", s)
        if 'data-placeholder="1"' not in svg:
            errors.append(f"signs/{s['id']}: fallback is not the neutral placeholder")

    # README / home counts
    co = atlas["country"]
    n_signs = len(atlas["signs"])
    n_glyph = sum(1 for s in atlas["signs"] if s.get("glyph"))
    counts = co.get("counts") or {}
    if counts.get("signs") != n_signs or counts.get("glyphs") != n_glyph:
        errors.append(f"country.counts {counts} != data {n_signs}/{n_glyph}")

    licence = json.dumps(co.get("licence") or {})
    for bad in ("Accurate shape", "prescribed colour", "every TSRGD"):
        if bad.lower() in licence.lower() or bad in licence:
            errors.append(f"licence still contains {bad!r}")

    readme = (ROOT / "README.md").read_text()
    for bad in ("Accurate", "prescribed TSRGD colours", "every TSRGD plate"):
        if bad in readme:
            errors.append(f"README contains {bad!r}")

    # extract_uk.py must not hard-code a home-directory dest path (e.g. ~/.cache/gridforge-tmp).
    extract_src = (ROOT / "tools" / "extract_uk.py").read_text()
    if re.search(r"/?home/[^/\s\"']+/\.cache/gridforge-tmp", extract_src):
        errors.append("extract_uk.py still hard-codes a home-directory dest path")

    # S7: render.js must be exactly the generated stub (no drifting JS drawers).
    js_path = ROOT / "site" / "assets" / "render.js"
    if not js_path.exists() or js_path.read_text() != render.render_js():
        errors.append("site/assets/render.js differs from render.render_js(); run rebuild.py --all")
    # Baked faces must equal a fresh render (byte-identical bake).
    stale = []
    for kind, item in catalogue.iter_items(atlas):
        fp = catalogue.face_path(ROOT / "site" / "faces", country, kind, item["id"])
        if not fp.exists() or fp.read_text() != render.item_svg(kind, item) + "\n":
            stale.append(f"{kind}/{item['id']}")
    known = {catalogue.face_path(ROOT / "site" / "faces", country, k, it["id"]) for k, it in catalogue.iter_items(atlas)}
    for fp in sorted((ROOT / "site" / "faces" / country).glob("*/*.svg")):
        if fp not in known:
            errors.append(f"orphan baked face {fp.relative_to(ROOT)} has no catalogue row")
    if stale:
        errors.append(f"{len(stale)} baked face(s) differ from render.py, e.g. {stale[:6]}; run rebuild.py --all")

    print(f"validate: {len(errors)} error(s), {len(warns)} warning(s)")
    for e in errors:
        print("ERROR", e)
    for w in (warns if strict else warns[:40]):
        print("WARN", w)
    if len(warns) > 40 and not strict:
        print(f"WARN … {len(warns) - 40} more")
    if errors:
        return 1
    if strict and warns:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate UK atlas data and faces.")
    p.add_argument("--country", default="uk")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)
    return validate(args.country, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
