#!/usr/bin/env python3
"""Map GOV.UK EPS files to atlas faces and decide each sign face's source.

Inputs (all committed): countries/uk/signs.json, countries/uk/sources/eps/crosswalk.csv,
countries/uk/sources/eps/manifest.csv, countries/uk/sources/eps/review.json (visual-review verdicts),
and site/faces/uk/manifest.json + baked faces (to tell procedural from placeholder faces).
Output: countries/uk/face_sources.json (deterministic; sorted keys) and, with --report, docs/EPS-COVERAGE.md.

Source per face: "eps" | "procedural" | "placeholder".
  eps          a fixed pictogram face whose GOV.UK EPS is the same diagram in SI 2016 (or the same 2002 diagram
               for a 2002-legacy row), with no conflict, no raster, and a visual-review pass. The procedural face
               is kept as the offline fallback ("fallback": "procedural" or "placeholder").
               An eps face may also be an example layout ("example": true): official GOV.UK art for a route,
               direction or tourist sign, standing in until a per-site generated face replaces it (review
               verdict "example"; owner, 2026-11-23: "Yes, add the 48 as example faces now").
  procedural   drawn by tools/atlas (variable text, composites, plates whose wording we set, gaps, conflicts).
  placeholder  no drawing yet (hatched placeholder face).
The EPS artwork itself is never committed; tools/eps/build.py cooks it into gitignored site/faces-eps/.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eps import paths  # noqa: E402

# Fixed pictogram families. Everything else (direction, tourist, info panels, plates, signals, matrix,
# countdown) is wording-led or composite and stays procedural in our own primitive lettering.
EPS_FAMILIES = {"WarnTriangle", "Prohibitory", "Mandatory", "GiveWay", "Stop", "National"}
# A face whose SI caption names a value set per site (speed, height, width, weight, distance, time) is
# variable: the EPS shows one example value, so the face stays procedural.
VARIABLE = re.compile(r"\b(mph|speed limit|maximum speed|height|headroom|width|weight|length|distance|miles?|yards?|"
                      r"metres?|tonnes?|indicated|shown|times?|hours?|days?|period|number of)\b", re.I)
OWNER_HELD = {"2911", "953.2", "818.2", "MARKER"}   # qa/DECISIONS-PENDING.md: untouched until the owner decides
VARIANT = re.compile(r"^(?P<num>\d+(?:[.X]\d+)?[A-Z]?)(?P<var>.*)$")


def load_csv(p: Path) -> list[dict]:
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))


def placeholder_ids() -> set[str]:
    out = set()
    d = paths.ROOT / "site" / "faces" / "uk" / "signs"
    for f in sorted(d.glob("*.svg")):
        if 'data-placeholder="1"' in f.read_text():
            out.add(f.stem)
    return out


def eps_variant(eps_file: str, num: str) -> str:
    stem = eps_file.rsplit("/", 1)[1].rsplit(".", 1)[0].replace("X", ".")
    return stem[len(num):] if stem.upper().startswith(num.upper()) else stem


def build() -> dict:
    signs = json.loads((paths.ROOT / "countries" / "uk" / "signs.json").read_text())
    cw = load_csv(paths.CROSSWALK)
    zip_date = {r["file"]: r["last_modified"] for r in load_csv(paths.MANIFEST)}
    rv_path = paths.SRC / "review.json"
    review = json.loads(rv_path.read_text())["faces"] if rv_path.exists() else {}
    ph = placeholder_ids()

    by_num: dict[str, list[dict]] = defaultdict(list)
    for c in cw:
        by_num[c["tsrgd2002_no"]].append(c)
    reused = set()   # 2016 numbers that another row was renumbered to: a same-number 2002 EPS is a different sign
    for r in signs:
        for t in [r.get("renumbered_to")] + list(r.get("renumbered_also") or []):
            if t:
                reused.add(t)

    def rank(c: dict, num: str):
        z = c["eps_file"].split("/", 1)[0]
        return (eps_variant(c["eps_file"], num) != "", len(eps_variant(c["eps_file"], num)),
                "-" + zip_date.get(z, ""), c["eps_file"])

    faces = {}
    for r in signs:
        fid, num = r["id"], r["diagram"]
        rv0 = review.get(fid) or {}
        enum = rv0.get("eps_number") or num   # r12: a renumbered 2016 row may take the EPS checked for its old number
        cands = sorted(by_num.get(enum) or [], key=lambda c: rank(c, enum))
        current = "placeholder" if fid.replace("/", "_") in ph else "procedural"
        f: dict = {"source": current, "family": r["family"], "row_status": r["status"]}
        if cands:
            best = cands[0]
            f["eps"] = best["eps_file"]
            f["eps_crosswalk"] = best["status"]
            if len(cands) > 1:
                f["eps_variants"] = [c["eps_file"] for c in cands[1:]]
        why = []
        is_example = False
        if not cands:
            why.append("no GOV.UK EPS for this diagram number")
        else:
            cws = best["status"]
            st = r["status"]
            rv = review.get(fid)
            v = (rv or {}).get("verdict")
            # r12: an eye check of the EPS against the SI 2016 page settles the crosswalk/renumbering question:
            #   pass-si2016  EPS matches the 2016 diagram -> use it (clears the conflict)
            #   matches-2016 EPS matches 2016 but the face stays procedural/placeholder (per-site value, owner-held)
            #   outdated     EPS is the superseded 2002 face; 2016 wins, procedural kept (difference recorded)
            settled = v in ("pass-si2016", "matches-2016", "outdated")
            if fid in OWNER_HELD:
                why.append("owner-held decision item (qa/DECISIONS-PENDING.md)")
            if settled:
                pass
            elif st in ("renumbered", "not-2016"):
                why.append(f"conflict: atlas row is {st}; the 2002 EPS is not the 2016 face")
            elif st == "current" and cws == "removed":
                why.append("conflict: crosswalk says the 2002 diagram was removed in 2016")
            elif st == "current" and cws != "same":
                # r12 (F2): an unverified crosswalk is a gap in our evidence, not evidence of a different face
                why.append("not yet verified: crosswalk could not confirm the number in SI 2016 (atlas index lists it); "
                           "needs an eye check against the SI 2016 page")
            elif st == "2002-legacy" and cws == "same":
                why.append("conflict: crosswalk finds the number in SI 2016 but the atlas row is 2002-legacy")
            if st == "current" and num in reused and not settled and v != "pass":
                why.append("conflict: 2016 reassigned this number (another row was renumbered to it); "
                           "the 2002 EPS shows a different sign")
            confirmed = v in ("pass", "pass-si2016")
            is_example = v == "example"
            if r["family"] not in EPS_FAMILIES and not confirmed and not is_example:
                why.append(f"family {r['family']}: wording-led or composite, kept procedural")
            elif not confirmed and not is_example and VARIABLE.search(r.get("si_caption") or r.get("name") or ""):
                why.append("variable value or wording set per site (caption); EPS shows one example")
            if rv and not confirmed and not is_example:
                why.append(f"visual review: {rv['verdict']}: {rv.get('note', '')}".rstrip(": "))
            elif not why and not rv:
                why.append("not yet visually reviewed against the SI 2016 diagram")
        conflict = [w for w in why if w.startswith("conflict") or w.startswith("visual review: 2016-check")]
        rvf = review.get(fid) or {}
        if rvf.get("si_page"):
            f["si_page"] = rvf["si_page"]
        if rvf.get("verdict") in ("pass-si2016", "matches-2016", "outdated"):
            f["si2016_verdict"] = rvf["verdict"]
        if r["status"] == "current" and num in reused and cands and (review.get(fid) or {}).get("verdict") == "pass":
            f["note"] = "2016 renumbered another diagram to this number; the EPS was checked by eye and shows this face"
        if not why:
            f["source"] = "eps"
            f["fallback"] = current
            f["superseded"] = current == "procedural"   # hand-traced face kept only as the offline fallback
            if is_example:
                f["example"] = True
                f["basis"] = ("example layout from the official GOV.UK image "
                              "(route, direction or tourist); to be generated per site")
            else:
                f["basis"] = ("same diagram number in SI 2016 (crosswalk same; visual review pass)"
                              if r["status"] == "current" else "2002 artwork for a 2002-legacy row (visual review pass)")
        else:
            f["why_not_eps"] = why
            if conflict:
                f["conflict"] = True
        faces[fid] = f
    return {"generated_by": "tools/eps/map.py", "rule": __doc__.split("Source per face:")[1].split("The EPS")[0].strip(),
            "faces": dict(sorted(faces.items()))}


def coverage(fs: dict) -> dict:
    cw = load_csv(paths.CROSSWALK)
    signs = json.loads((paths.ROOT / "countries" / "uk" / "signs.json").read_text())
    nums_atlas = {r["diagram"] for r in signs}
    faces = fs["faces"]
    mapped_eps = {f["eps"] for f in faces.values() if "eps" in f} | {
        v for f in faces.values() for v in f.get("eps_variants", [])}
    return {
        "eps_files": len(cw),
        "eps_files_mapped_to_atlas": len(mapped_eps),
        "eps_files_not_in_atlas": sum(1 for c in cw if c["tsrgd2002_no"] not in nums_atlas),
        "atlas_sign_faces": len(faces),
        "atlas_faces_with_eps_match": sum(1 for f in faces.values() if "eps" in f),
        "atlas_faces_no_eps": sum(1 for f in faces.values() if "eps" not in f),
        "source": dict(sorted(Counter(f["source"] for f in faces.values()).items())),
        "eps_replacing_placeholder": sum(1 for f in faces.values() if f["source"] == "eps" and f["fallback"] == "placeholder"),
        "eps_example": sum(1 for f in faces.values() if f["source"] == "eps" and f.get("example")),
        "superseded_hand_traced": sum(1 for f in faces.values() if f.get("superseded")),
        "conflicts_2016": sum(1 for f in faces.values() if f.get("conflict")),
        "si2016_eye_checked": sum(1 for f in faces.values() if f.get("si2016_verdict")),
        "not_yet_verified": sum(1 for f in faces.values() if any(w.startswith("not yet verified") for w in f.get("why_not_eps", []))),
    }


def report_md(fs: dict) -> str:
    cv = coverage(fs)
    faces = fs["faces"]
    cw = load_csv(paths.CROSSWALK)
    nums_atlas = {r["diagram"] for r in json.loads((paths.ROOT / "countries" / "uk" / "signs.json").read_text())}
    L = ["# EPS coverage (generated by `python3 tools/eps/map.py --report`; do not edit)", "",
         "| Measure | Count |", "|---|---:|"]
    L += [f"| {k.replace('_', ' ')} | {v} |" for k, v in cv.items() if not isinstance(v, dict)]
    L += [f"| source = {k} | {v} |" for k, v in cv["source"].items()]
    def table(title, rows, cols):
        out = ["", f"## {title} ({len(rows)})", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        out += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
        return out
    L += table("Atlas faces now EPS-sourced (fixed pictogram)", [(k, f["family"], f["row_status"], f["fallback"], f["eps"])
               for k, f in faces.items() if f["source"] == "eps" and not f.get("example")],
               ["Face", "Family", "Row", "Fallback", "EPS"])
    L += table("EPS example layouts (official GOV.UK image; to be generated per site)",
               [(k, f["family"], f["row_status"], f["eps"])
                for k, f in faces.items() if f.get("example")],
               ["Face", "Family", "Row", "EPS"])
    rvw = json.loads((paths.SRC / "review.json").read_text()).get("faces", {}) if (paths.SRC / "review.json").exists() else {}
    L += table("SI 2016 eye-check verdicts (EPS vs the SI 2016 page)", [(k, f["si2016_verdict"], f["source"], f.get("si_page", ""),
               (rvw.get(k) or {}).get("note", "")) for k, f in faces.items() if f.get("si2016_verdict")],
               ["Face", "Verdict", "Source now", "SI page", "Finding"])
    L += table("Conflicts (2016 wins; EPS not used)", [(k, f["family"], f["eps"], "; ".join(w for w in f["why_not_eps"] if "conflict" in w or "2016" in w))
               for k, f in faces.items() if f.get("conflict")], ["Face", "Family", "EPS", "Why"])
    L += table("EPS match, kept procedural/placeholder (no conflict)", [(k, f["family"], f["source"], f["eps"], "; ".join(f["why_not_eps"]))
               for k, f in faces.items() if "eps" in f and f["source"] != "eps" and not f.get("conflict")],
               ["Face", "Family", "Source", "EPS", "Why"])
    L += table("Atlas faces with no EPS (stay procedural or placeholder)", [(k, f["family"], f["source"])
               for k, f in faces.items() if "eps" not in f], ["Face", "Family", "Source"])
    by = defaultdict(list)
    for c in cw:
        if c["tsrgd2002_no"] not in nums_atlas:
            by[c["eps_file"].split("/", 1)[0]].append(c["eps_file"].rsplit("/", 1)[1])
    L += ["", f"## EPS not in the atlas ({sum(len(v) for v in by.values())} files)", ""]
    L += [f"- `{z}` ({len(v)}): " + ", ".join(sorted(v)) for z, v in sorted(by.items())]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="also write docs/EPS-COVERAGE.md")
    ap.add_argument("--check", action="store_true", help="exit 1 if face_sources.json is stale")
    a = ap.parse_args(argv)
    fs = build()
    text = json.dumps(fs, indent=1, sort_keys=True) + "\n"
    if a.check:
        ok = paths.FACE_SOURCES.exists() and paths.FACE_SOURCES.read_text() == text
        print("face_sources.json " + ("up to date" if ok else "STALE: run python3 tools/eps/map.py --report"))
        return 0 if ok else 1
    paths.FACE_SOURCES.write_text(text)
    if a.report:
        (paths.ROOT / "docs" / "EPS-COVERAGE.md").write_text(report_md(fs))
    print(json.dumps(coverage(fs), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
