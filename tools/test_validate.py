#!/usr/bin/env python3
"""Negative tests: validate.py must FAIL on each seeded fault (QA r1, WP5).

    python3 tools/test_validate.py
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

ROOT = Path(__file__).resolve().parent.parent
import validate  # noqa: E402
from atlas import catalogue, lettering, render  # noqa: E402

_REAL_LOAD = catalogue.load_country


def run(mutate=None, strict=False):
    """Run validate with the atlas mutated in memory; return (exit, output)."""
    def fake(country, root):
        atlas = copy.deepcopy(_REAL_LOAD(country, root))
        if mutate:
            mutate(atlas)
        return atlas
    validate.catalogue.load_country = fake
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            code = validate.validate("uk", strict=strict)
    finally:
        validate.catalogue.load_country = _REAL_LOAD
    return code, out.getvalue()


def sign(atlas, sid):
    return next(s for s in atlas["signs"] if s["id"] == sid)


class ValidateFails(unittest.TestCase):
    def test_clean_tree_passes_default(self):
        code, out = run()
        self.assertEqual(code, 0, out)

    def test_colour_listed_but_unused(self):
        code, out = run(lambda a: sign(a, "670")["colours"].append("blue"))
        self.assertEqual(code, 1)
        self.assertIn("signs/670: colours listed but unused", out)

    def test_colour_used_but_unlisted(self):
        code, out = run(lambda a: sign(a, "670")["colours"].remove("red"))
        self.assertEqual(code, 1)
        self.assertIn("signs/670: face uses unlisted colours", out)

    def test_templated_size_fails(self):
        code, out = run(lambda a: sign(a, "543")["source"].update(plate_width=validate.TEMPLATE_SOURCE))
        self.assertEqual(code, 1)
        self.assertIn("signs/543: templated plate size", out)

    def test_size_not_permitted_fails(self):
        code, out = run(lambda a: sign(a, "616")["dimensions_m"].update(plate_width=0.65, plate_height=0.65))
        self.assertEqual(code, 1)
        self.assertIn("signs/616: plate diameter 650 mm not in SI 2016", out)

    def test_drawn_aspect_mismatch_fails(self):
        code, out = run(lambda a: sign(a, "2901")["dimensions_m"].update(plate_width=2.4))
        self.assertEqual(code, 1)
        self.assertIn("signs/2901: data plate aspect", out)

    def test_strict_clean(self):
        code, out = run(strict=True)
        self.assertEqual(code, 0, out)

    def test_wrong_status_current_for_2002_id(self):
        code, out = run(lambda a: sign(a, "513.1").update(status="current"))
        self.assertEqual(code, 1)
        self.assertIn("signs/513.1: 2002-only id but status current", out)

    def test_saved_label_rejected(self):
        code, out = run(lambda a: sign(a, "532.2").update(status="saved-by-reg-14(4)"))
        self.assertEqual(code, 1)
        self.assertIn("overstates reg 14(4)", out)

    def test_placeholder_name_must_be_si_caption(self):
        # any current placeholder with an SI caption (880 was drawn in b3)
        rows = json.loads((ROOT / "countries" / "uk" / "signs.json").read_text())
        # default once every placeholder is drawn: any current row with an SI caption, made a placeholder here
        pid = next((r["id"] for r in rows if not r.get("glyph") and r.get("status") == "current" and r.get("si_caption")),
                   next(r["id"] for r in rows if r.get("status") == "current" and r.get("si_caption")))
        code, out = run(lambda a: sign(a, pid).update(name="Home Zone Entry", glyph=False))
        self.assertEqual(code, 1)
        self.assertIn(f"signs/{pid}: placeholder name", out)

    def test_missing_renumber_target(self):
        code, out = run(lambda a: a.__setitem__("signs", [s for s in a["signs"] if s["id"] != "675B"]))
        self.assertEqual(code, 1)
        self.assertIn("renumber target 675B has no catalogue row", out)

    def test_legend_overflow(self):
        real = render.GLYPHS["552"]
        render.GLYPHS["552"] = lambda p: render._warn() + render._word("Cattle grid", 0, 0, 0.12, "#141414")
        try:
            code, out = run()
        finally:
            render.GLYPHS["552"] = real
        self.assertEqual(code, 1)
        self.assertIn("signs/552: legend 'Cattle grid' clearance", out)

    def test_filled_box_glyph(self):
        real = lettering.char

        def boxy(ch, cx, cy, cap_h, fill, part=2):
            if ch == "q":
                w = cap_h * 0.9
                return f'<rect x="{cx - w / 2}" y="{cy - cap_h / 2}" width="{w}" height="{cap_h}" fill="{fill}"/>'
            return real(ch, cx, cy, cap_h, fill, part)
        validate.lettering.char = boxy
        try:
            code, out = run()
        finally:
            validate.lettering.char = real
        self.assertEqual(code, 1)
        self.assertIn("lettering: 'q' contains a filled box", out)


class OverlayNameFails(unittest.TestCase):
    def test_stale_name(self):
        code, out = run(lambda a: sign(a, "640.2A").update(name="Clean air zone"))
        self.assertEqual(code, 1)
        self.assertIn("signs/640.2A: name 'Clean air zone' != overlay name", out)


class StaleOverlayFails(unittest.TestCase):
    def test_overlay_key_without_row(self):
        code, out = run(lambda a: a.__setitem__("signs", [s for s in a["signs"] if s["id"] != "546"]))
        self.assertEqual(code, 1)
        self.assertIn("overlay.json signs/546: no catalogue row", out)


class TriangleBorderFails(unittest.TestCase):
    def test_old_k_070_fails(self):
        real = render.WARN_K
        render.WARN_K = 0.70
        try:
            code, out = run()
        finally:
            render.WARN_K = real
        self.assertEqual(code, 1)
        self.assertIn("triangle border 0.12", out)


class ConfusableFails(unittest.TestCase):
    def test_s_drawn_as_5_fails(self):
        real = lettering.char

        def s_as_5(ch, cx, cy, cap_h, fill, part=2):
            return real("5" if ch == "S" else ch, cx, cy, cap_h, fill, part)
        lettering.char = s_as_5
        try:
            code, out = run()
        finally:
            lettering.char = real
        self.assertEqual(code, 1)
        self.assertIn("'S' and '5' render alike", out)



class GantryVmsFails(unittest.TestCase):
    def _row(self, atlas, fid):
        return next(f for f in atlas["furniture"] if f["id"] == fid)

    def test_missing_type(self):
        code, out = run(lambda a: a.__setitem__("furniture", [f for f in a["furniture"] if f["id"] != "verge-ms"]))
        self.assertNotEqual(code, 0)
        self.assertIn("no 'verge-ms' row", out)

    def test_placeholder_without_todo(self):
        code, out = run(lambda a: self._row(a, "vms-text").pop("todo"))
        self.assertNotEqual(code, 0)
        self.assertIn("placeholder without todo", out)

    def test_placeholder_without_sources_needed(self):
        code, out = run(lambda a: self._row(a, "verge-ms").pop("sources_needed"))
        self.assertNotEqual(code, 0)
        self.assertIn("placeholder without sources_needed", out)

    def test_placeholder_with_empty_sources_needed(self):
        code, out = run(lambda a: self._row(a, "vms-pictogram").__setitem__("sources_needed", []))
        self.assertNotEqual(code, 0)
        self.assertIn("placeholder without sources_needed", out)

    def test_placeholder_with_figures(self):
        def m(a):
            r = self._row(a, "lane-signal")
            r["dimensions_m"] = {"width": 1.0}
            r["source"] = {"width": "x"}
        code, out = run(m)
        self.assertNotEqual(code, 0)
        self.assertIn("placeholder carries figures", out)


class WholeFaceAspect(unittest.TestCase):
    def test_bbox_covers_all_shapes(self):
        inner = '<rect x="-0.1" y="0" width="0.2" height="0.5" fill="#000"/><circle cx="0" cy="-0.2" r="0.2" fill="#fff"/>'
        self.assertEqual(render._whole_bbox(inner), (-0.2, -0.4, 0.2, 0.5))

    def test_belisha_face_is_square(self):
        for sid in ("4007", "BELISHA", "XING_PAR"):
            self.assertAlmostEqual(render.drawn_aspect(sid), 1.0, places=2)

    def test_transformed_face_falls_back_to_first_shape(self):
        self.assertEqual(render._whole_bbox('<g transform="scale(2)"><rect x="0" y="0" width="1" height="1"/></g>'), "T")


class GeneratorFaces(unittest.TestCase):
    """Placeholder batches: faces from the parametric generator (traced.PLATES with a kind)."""
    KEY = "_TEST_AUTO"

    def setUp(self):
        T = render.traced
        T.PATHS[self.KEY + "/0"] = "M-0.1,-0.1 0.1,-0.1 0.1,0.1 -0.1,0.1Z"
        T.SOURCE[self.KEY] = "test"
        T.PLATES[self.KEY] = {"w": 1.0, "h": 1.0, "rx": 0.0, "plate": None, "layers": [("black", self.KEY + "/0")],
                              "text": [], "over": [], "fields": [], "kind": "warn"}
        render.GLYPHS[self.KEY] = (lambda p: render._auto(self.KEY))

    def tearDown(self):
        T = render.traced
        for d, k in ((T.PATHS, self.KEY + "/0"), (T.SOURCE, self.KEY), (T.PLATES, self.KEY), (render.GLYPHS, self.KEY)):
            d.pop(k, None)

    def test_warn_kind_uses_shared_triangle(self):
        self.assertTrue(render._auto(self.KEY).startswith(render._warn()))

    def test_proh_and_mand_kinds_use_shared_outlines(self):
        render.traced.PLATES[self.KEY]["kind"] = "proh"
        self.assertTrue(render._auto(self.KEY).startswith(render._ring_roundel()))
        render.traced.PLATES[self.KEY]["kind"] = "mand"
        self.assertTrue(render._auto(self.KEY).startswith(render._mand("")))

    def test_every_generator_face_is_registered(self):
        for k, P in render.traced.PLATES.items():
            if P.get("kind") in render.AUTO_KINDS:
                self.assertIn(k, render.GLYPHS, k)

    def test_missing_source_fails(self):
        render.traced.SOURCE.pop(self.KEY)
        code, out = run()
        self.assertNotEqual(code, 0)
        self.assertIn(f"generator/{self.KEY}: no SOURCE entry", out)

    def test_missing_layer_path_fails(self):
        render.traced.PATHS.pop(self.KEY + "/0")
        code, out = run()
        self.assertNotEqual(code, 0)
        self.assertIn("layer path", out)

    def test_unknown_kind_fails(self):
        render.traced.PLATES[self.KEY]["kind"] = "hexagon"
        code, out = run()
        self.assertNotEqual(code, 0)
        self.assertIn("unknown kind", out)

    def test_off_palette_legend_fails(self):
        render.traced.PLATES[self.KEY]["text"] = [("A", 0.0, 0.0, 0.1, 1.0, "magenta", 2)]
        render.traced.PLATES[self.KEY]["kind"] = "plate"
        render.traced.PLATES[self.KEY]["fields"] = [("rect", -0.5, -0.5, 0.5, 0.5)]
        code, out = run()
        self.assertNotEqual(code, 0)
        self.assertIn("not in palette", out)
class EpsChecks(unittest.TestCase):
    """EPS-first pipeline (tools/eps/checks.py): each seeded fault must fail validate."""

    def setUp(self):
        from eps import checks, map as eps_map, paths
        self.checks, self.map, self.paths = checks, eps_map, paths

    def test_manifest_hash_pinned(self):
        old = dict(self.checks.PINNED)
        self.checks.PINNED["manifest.csv"] = "0" * 64
        try:
            code, out = run()
        finally:
            self.checks.PINNED.clear(); self.checks.PINNED.update(old)
        self.assertEqual(code, 1)
        self.assertIn("manifest.csv SHA-256 differs", out)

    def test_stale_face_sources(self):
        real = self.map.build
        def fake():
            d = real(); d["faces"]["671"]["source"] = "procedural"; return d
        self.map.build = fake
        try:
            code, out = run()
        finally:
            self.map.build = real
        self.assertEqual(code, 1)
        self.assertIn("face_sources.json is stale", out)

    def _with_faces(self, mutate):
        import tempfile
        real_path, real_build = self.paths.FACE_SOURCES, self.map.build
        d = json.loads(real_path.read_text()); mutate(d)
        tmp = Path(tempfile.mkdtemp()) / "face_sources.json"
        tmp.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")
        self.paths.FACE_SOURCES = tmp
        self.map.build = lambda: d
        try:
            return run()
        finally:
            self.paths.FACE_SOURCES, self.map.build = real_path, real_build

    def test_eps_face_with_conflict_fails(self):
        def m(d):
            d["faces"]["671"]["conflict"] = True
        code, out = self._with_faces(m)
        self.assertEqual(code, 1)
        self.assertIn("671 is eps-sourced but carries a conflict", out)

    def test_eps_file_not_in_crosswalk_fails(self):
        def m(d):
            d["faces"]["671"]["eps"] = "nowhere.zip/671.eps"
        code, out = self._with_faces(m)
        self.assertEqual(code, 1)
        self.assertIn("not in the crosswalk", out)

    def test_owner_held_cannot_be_eps(self):
        def m(d):
            d["faces"]["953.2"].update({"source": "eps", "eps": d["faces"]["671"]["eps"], "fallback": "procedural"})
            d["faces"]["953.2"].pop("why_not_eps", None); d["faces"]["953.2"].pop("conflict", None)
        code, out = self._with_faces(m)
        self.assertEqual(code, 1)
        self.assertIn("owner-held item 953.2", out)

    def test_tracked_eps_fails(self):
        import subprocess as sp
        real = self.checks.subprocess.run
        class R:  # noqa: D401
            stdout = "README.md\nrefs/x/616.EPS\n"
        self.checks.subprocess.run = lambda *a, **k: R()
        try:
            code, out = run()
        finally:
            self.checks.subprocess.run = real
        self.assertEqual(code, 1)
        self.assertIn("EPS artwork is tracked", out)

    def _with_tracked(self, listing):
        real = self.checks.subprocess.run
        class R:  # noqa: D401
            stdout = listing
        self.checks.subprocess.run = lambda *a, **k: R()
        try:
            return run()
        finally:
            self.checks.subprocess.run = real

    def test_tracked_cache_file_fails(self):
        code, out = self._with_tracked("README.md\n.cache/eps/zips/x.zip\n")
        self.assertEqual(code, 1)
        self.assertIn("EPS artwork is tracked", out)

    def test_tracked_eps_svg_without_attribution_fails(self):
        p = self.paths.ROOT / "site" / "faces-eps" / "uk" / "signs" / "671.svg"
        if not p.exists():
            self.skipTest("site/faces-eps/ absent")
        orig = p.read_bytes()
        p.write_bytes(orig.replace(b"<desc>Crown copyright", b"<desc>Anon"))
        try:
            code, out = self._with_tracked("site/faces-eps/uk/signs/671.svg\n")
        finally:
            p.write_bytes(orig)
        self.assertEqual(code, 1)
        self.assertIn("lacks the Crown copyright", out)

    def test_tracked_eps_svg_for_non_eps_face_fails(self):
        code, out = self._with_tracked("site/faces-eps/uk/signs/969.svg\n")
        self.assertEqual(code, 1)
        self.assertIn("is not an eps-sourced face", out)

    def test_eps_svg_tracked_elsewhere_fails(self):
        p = self.paths.ROOT / "site" / "faces-eps" / "uk" / "signs" / "671.svg"
        if not p.exists():
            self.skipTest("site/faces-eps/ absent")
        q = self.paths.ROOT / "docs" / "_eps_copy_test.svg"
        q.write_bytes(p.read_bytes())
        try:
            code, out = self._with_tracked("docs/_eps_copy_test.svg\n")
        finally:
            q.unlink()
        self.assertEqual(code, 1)
        self.assertIn("tracked outside site/faces-eps", out)

    def test_font_program_in_eps_fails(self):
        import re
        if not any(self.paths.ZIPS.glob("*.zip")):
            self.skipTest("EPS cache absent")
        real = self.checks.FONT_PROGRAM
        self.checks.FONT_PROGRAM = re.compile(rb"%!PS")
        try:
            code, out = run()
        finally:
            self.checks.FONT_PROGRAM = real
        self.assertEqual(code, 1)
        self.assertIn("font program", out)

    def test_missing_cache_required_fails(self):
        import os, tempfile
        real = self.paths.ZIPS
        self.paths.ZIPS = Path(tempfile.mkdtemp())
        os.environ["SA_REQUIRE_EPS"] = "1"
        try:
            code, out = run()
        finally:
            self.paths.ZIPS = real
            os.environ.pop("SA_REQUIRE_EPS")
        self.assertEqual(code, 1)
        self.assertIn("cache absent", out)


class FaceQa(unittest.TestCase):
    """qa/TODO-WARN-TRIANGLE-QA.md systemic checks (a)-(d) via tools/face_qa.py."""

    def test_new_finding_fails(self):
        import face_qa
        real = face_qa.findings
        def fake(atlas=None):
            d = real(atlas); d.setdefault("616", []).append("islands: seeded"); return d
        face_qa.findings = fake
        try:
            code, out = run()
        finally:
            face_qa.findings = real
        self.assertEqual(code, 1)
        self.assertIn("face-qa 616: new finding", out)

    def test_overlap_detects_colliding_words(self):
        import face_qa
        real = render.legend_log
        render.legend_log = lambda c, p=None: [("A", 0, 0, 1, 1, 1, 1), ("B", 0.5, 0.5, 2, 2, 1, 1)]
        try:
            self.assertTrue(face_qa.overlap_checks("x"))
        finally:
            render.legend_log = real

    def test_inset_and_islands_detect_faults(self):
        import shutil, tempfile, face_qa
        if not shutil.which("rsvg-convert"):
            self.skipTest("rsvg-convert absent")
        d = Path(tempfile.mkdtemp())
        (d / "t.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">'
            '<rect x="0" y="0" width="100" height="100" fill="#CC1A1A"/><rect x="10" y="10" width="80" height="80" fill="#F7F7F7"/>'
            '<rect x="10" y="40" width="40" height="20" fill="#141414"/><rect x="70" y="70" width="2" height="2" fill="#141414"/></svg>')
        real = face_qa.FACES
        face_qa.FACES = d
        try:
            f = face_qa.raster_checks("t", "WarnTriangle")
        finally:
            face_qa.FACES = real
        self.assertTrue(any(x.startswith("inset") for x in f), f)
        self.assertTrue(any(x.startswith("islands") for x in f), f)

    def test_edge_check_flags_ink_leaving_a_panel(self):
        import shutil, tempfile, face_qa
        if not shutil.which("rsvg-convert"):
            self.skipTest("rsvg-convert absent")
        d = Path(tempfile.mkdtemp())
        (d / "p.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 100" width="50" height="100">'
            '<rect x="0" y="0" width="50" height="100" fill="#E6C300"/><rect x="20" y="0" width="10" height="40" fill="#141414"/></svg>')
        a = face_qa.raster(d / "p.svg")
        f = face_qa.edge_check(a, face_qa._mask(a, face_qa._hex(face_qa.render.C["black"])))
        self.assertTrue(f and f[0].startswith("edge"), f)

    def test_unpinned_converter_versions_are_reported(self):
        from eps import convert
        self.assertEqual(convert.version_problems({"ghostscript": "10.05.1", "pdftocairo": "pdftocairo version 25.03.0"}), [])
        self.assertEqual(len(convert.version_problems({"ghostscript": "10.02.1", "pdftocairo": "pdftocairo version 24.02.0"})), 2)

    def test_near_neutral_grey_snaps_to_black_not_brown(self):
        from eps import convert
        convert._PAL = None
        # 4003.2 unsapped aspect backing: pdftocairo rgb(81,78,79), chroma 3
        hexv, bad = convert.snap((81.0, 78.0, 79.0))
        self.assertEqual(hexv, "#141414")
        self.assertIsNone(bad)
        # Official tourist brown from 2201.eps must still snap to brown
        hexv, bad = convert.snap((113.0, 57.0, 7.0))
        self.assertEqual(hexv, "#73451F")
        self.assertIsNone(bad)

    def test_deploy_guard_requires_attribution(self):
        import tempfile
        from eps import convert, deploy_guard
        d = Path(tempfile.mkdtemp())
        (d / "a.svg").write_text(f'<svg data-source="eps"><desc>{convert.ATTRIBUTION}</desc></svg>')
        self.assertEqual(deploy_guard.main([str(d)]), 0)
        (d / "b.svg").write_text('<svg data-source="eps"></svg>')
        self.assertEqual(deploy_guard.main([str(d)]), 1)

    def test_unverified_crosswalk_is_not_a_conflict(self):
        import json
        fs = json.loads((ROOT / "countries" / "uk" / "face_sources.json").read_text())["faces"]
        for f in fs.values():
            for w in f.get("why_not_eps", []):
                self.assertFalse(w.startswith("conflict: crosswalk could not verify"), w)

    def test_unlisted_identical_pair_fails(self):
        import tempfile, face_qa
        real = face_qa.PAIRS
        d = json.loads(real.read_text()); d["groups"] = d["groups"][1:]
        tmp = Path(tempfile.mkdtemp()) / "p.json"; tmp.write_text(json.dumps(d))
        face_qa.PAIRS = tmp
        try:
            code, out = run()
        finally:
            face_qa.PAIRS = real
        self.assertEqual(code, 1)
        self.assertIn("not listed in countries/uk/identical_pairs.json", out)


class NoPersonalName(unittest.TestCase):
    def test_tracked_files_have_no_owner_name(self):
        import no_name_check
        n, hits = no_name_check.scan()
        self.assertGreater(n, 0)
        self.assertEqual(hits, [], "personal name found (masked): %r" % hits[:10])

    def test_no_absolute_machine_paths(self):
        import no_name_check
        n, hits, _ = no_name_check.scan_paths()
        self.assertEqual(hits, [], "absolute paths found: %r" % hits[:10])
        self.assertIsNotNone(no_name_check.PATH_PAT.search("x /" + "tmp/y"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
