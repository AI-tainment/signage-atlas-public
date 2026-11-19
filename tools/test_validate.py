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
