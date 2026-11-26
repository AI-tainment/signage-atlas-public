# EPS-first faces

Decided 2026-11-23 on the owner's instruction: the GOV.UK traffic-sign EPS files are the primary source for
fixed pictogram faces. Procedural drawing stays for variable-text and composite signs, coverage gaps, and as
the offline fallback for every EPS face. No Transport font is shipped.

## What is committed, and what is not

The atlas is a CC BY-ND 4.0 repository of our own work. The EPS artwork is Crown copyright, reusable under the
Open Government Licence v3.0 with attribution, but to match GridForge's rule (cook at use time, never ship) the
atlas commits the pipeline, mappings and metadata, and (owner ruling 09:18, 2026-11-23: "We can re publish with
attribution and cite ogl licenses") the converted faces in use, each with the Crown copyright / OGL v3.0 `<desc>`:

| Committed | Not committed (gitignored, rebuilt locally) |
|---|---|
| `tools/eps/` (fetch, convert, build, map, compare, checks) | `.cache/eps/zips/` the 18 GOV.UK zips |
| `countries/uk/sources/eps/manifest.csv` (SHA-256 of the zips) | `.cache/eps/raw/` the 702 EPS files |
| `countries/uk/sources/eps/crosswalk.csv` (2002 to 2016 status) | `.cache/eps/svg/` converted SVG + `convert-report.json` |
| `countries/uk/sources/eps/review.json` (visual-review verdicts) | |
| `countries/uk/face_sources.json` (per-face source) | `qa/renders/eps/` contact sheets (they show Crown artwork) |
| `docs/EPS-COVERAGE.md` (generated report) | |
| `site/faces-eps/uk/` the in-use converted faces + `README.txt` notice | |

`tools/validate.py` (E4) fails if any `.eps` or anything under `.cache/` is tracked, if a tracked SVG under
`site/faces-eps/` lacks the Crown/OGL `<desc>`, is not an eps-sourced face in `face_sources.json`, or differs from
the fresh conversion (when the cache is present), and if a converted EPS SVG is tracked anywhere else.

## Pipeline

```bash
python3 tools/eps/fetch.py              # once: 18 zips, serial, honest User-Agent, >= 3 s apart, SHA-256 checked
python3 tools/eps/fetch.py --verify     # offline re-check of the cache
python3 tools/eps/build.py --twice      # convert all 702, twice, require byte-identical output; place EPS faces
python3 tools/eps/map.py --report       # face_sources.json + docs/EPS-COVERAGE.md (deterministic, committed inputs only)
python3 tools/eps/compare.py --family WarnTriangle --set warn-triangle   # before/after contact sheets
./tools/serve.sh                        # cooks EPS faces when the verified cache exists, then serves
```

`fetch.py --seed-from DIR` reuses zips already on the machine when their SHA-256 matches, so the GOV.UK
servers are not asked twice. The first cache on the build box was seeded this way from the copy fetched for
the GridForge source review; no zip was downloaded again.

### Converter (`tools/eps/convert.py`)

Ghostscript `pdfwrite` with `-dEPSCrop` turns each EPS into a one-page PDF, `pdftocairo -svg` writes SVG, then
the SVG is normalised: viewBox from the EPS bounding box at origin 0 0, every number rounded to 2 dp,
`rgb(%)` colours converted to exact 8-bit hex, then the explicit owner rule table in
`tools/eps/colour_rules.py` is applied. There is **no atlas-palette substitution**.
Colour fallbacks: owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT.
Default attributes, comments, metadata and the XML prolog are removed, display size 160 px on the long
side. The Illustrator `%%For` / `%%Title` header lines never reach the SVG.

The pdfwrite step uses Art's colour conversion from `art/sign-pipeline-20261126` @ `4d859a4`:
`-sColorConversionStrategy=RGB -dProcessColorModel=/DeviceRGB -sOutputICCProfile=default_rgb.icc`
(Ghostscript's default RGB ICC, the same family as the png16m device). SVG fills then match
Ghostscript's png16m reference exactly or within 1 per 8-bit channel (blue `#0079C1`, brown
`#794400`). Without that step, pdftocairo's CMYK preview diverged (blue `#1476C6`, brown `#713907`).

After that exact conversion, three owner fallbacks rewrite only named colours
(owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT).
They are not a general palette snap; the table is in `tools/eps/colour_rules.py` and is unit-tested.

| Rule | From | To | Scope | Source |
|---|---|---|---|---|
| Official red | `#FF0000` | `#E31837` | every face (66 published signs emit this process red) | DfT "Road traffic sign images for reproduction" colour palette, Pantone 186, RGB 227 24 55 (`https://www.gov.uk/guidance/traffic-sign-images`, updated 17 January 2018); owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT |
| Process black | `#221F1F` (ICC) and `#231F20` (pre-ICC) | `#000000` | every face (25 published signs) | Owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT: CMYK K100 preview is not a designed grey; SI / TSM intend black |
| 4003 discs | `#5A5B5D` (ICC) and `#514E4F` (pre-ICC) | `#000000` | 4003.2 and 4003.5 only | Owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT, per SI 2016 Sch 14 Pt 2 (black circular heads) |

Main colours otherwise stay as the ICC converter emits them: official blue, brown,
greens, white, `#ED1C24` (10 faces), and true `#000000`. The pre-ICC darker reds
`#E51636` and `#E51635` are not kept as those hexes — after the ICC step they
come out as `#E31837` on 10 faces (2601.1, 2606, 2930, 4003.3, 642, 667.2, 668.2,
811, 811A, 816) and `#E31836` on 2602.2. That is Ghostscript-faithful conversion
(within 1 per channel of official red), not a colour-rule mapping, and no extra
mapping is added. Off-palette colours after the rules are reported in
`convert-report.json` as `off_palette`, never further recoloured.

Tool versions recorded in `convert-report.json` (Debian 13 apt packages): Ghostscript 10.05.1,
pdftocairo / pdffonts (poppler-utils) 25.03.0. Contact sheets and face QA also use `rsvg-convert`
(librsvg2-bin) 2.60.0.

Result on 2026-11-23: 702/702 converted, 0 errors, 0 embedded fonts (pdffonts), 0 `<text>`, 2 files with an
embedded raster image (`530.eps`, `543.eps`; never used as EPS faces), 702/702 byte-identical on a second run.

## Which faces use the EPS

`tools/eps/map.py` decides per sign row, from committed inputs only:

- **eps** when the face is a fixed pictogram (family WarnTriangle, Prohibitory, Mandatory, GiveWay, Stop,
  National, or another family confirmed by a `pass` verdict), the crosswalk says the 2002 number is the same
  diagram in SI 2016 (or the row is itself 2002-legacy and the EPS is that 2002 artwork), there is no conflict,
  and the face passed the visual review (`review.json`, verdict `pass`).
- **procedural** for variable values or wording set per site (speed, height, width, weight, distance, times,
  arrow direction, mode lists, SI "alternative types" the atlas draws differently), wording-led plates and
  composites (wording stays in our primitive Schedule 17 stand-in lettering), signal heads, gaps, conflicts,
  and the owner-held items (2911, 953.2, 818.2, MARKER).
- **placeholder** where nothing is drawn yet and no EPS qualifies.
- **eps + example: true** for a route, direction or tourist sign whose official GOV.UK image is kept as an
  example layout, standing in until a per-site generated face replaces it (review verdict `example`).

**2016 wins.** A conflict is flagged and the EPS is not used when: the atlas row is renumbered or not-2016; the
crosswalk says the 2002 diagram was removed; the row is 2002-legacy
but the crosswalk finds the number in SI 2016; 2016 renumbered another diagram to this number (unless the
EPS was checked by eye and shows this face); or the visual review found the 2002 artwork differs
(`2016-check`). A crosswalk that could not confirm the number in SI 2016 is **not yet verified**, not a
conflict (r12): it needs an eye check against the SI 2016 page. Eye-check verdicts in `review.json` carry the
page (`si_page`): `pass-si2016` (EPS matches the 2016 page; used), `matches-2016` (matches, but kept
procedural/placeholder: value set per site, or owner-held), `outdated` (superseded 2002 face; 2016 wins,
procedural kept, difference recorded) and `fail` (an extra or missing element rules the EPS out). The table
is in `docs/EPS-COVERAGE.md`.

Every EPS face keeps its procedural face (`fallback`), and a hand-traced face it replaces is marked
`superseded`. The generator and the traced data are not deleted. The wiki loads `site/faces-eps/` first and
falls back to the procedural face, then to the placeholder, so it still works offline or without a cache.

## Owner rulings (r12, relayed by Reviewer, 2026-11-23)

- **Data source:** GOV.UK is accepted as a data source for sign faces.
- **Lettering in the EPS:** acceptable, because the EPS draws its lettering as paths and no real font is
  shipped (the font checks still apply). So the EPS is used for fixed-wording faces wherever it matches SI
  2016 (776, 777, 778, 968.1, 827.1, 823-825, 833-836).
- **Varying wording:** where wording must vary or differ from the EPS, the face is drawn in our own
  primitive font (never Transport).
- **Publishing:** EPS-derived faces may be republished with attribution and an OGL v3.0 citation. Each
  converted SVG embeds a Crown copyright / OGL v3.0 `<desc>` (`tools/eps/convert.py` ATTRIBUTION); the atlas
  viewer and the street wiki show the attribution on the page; `tools/eps/deploy_guard.py <dir>` (run by
  `tools/gen/checks.sh`) and the wiki `tests/check.py` fail if a published EPS face lacks it. The EPS
  in-use converted faces are committed under `site/faces-eps/` (owner, 09:49); the raw EPS and zips are not.
- **781 (09:24):** "use the official unless it has dynamic text". SI 2016 diagram 781 (tsrgd2016.pdf PDF
  p64 = printed p63, Sch 2 Pt 6 item 5) has no text on the sign; its variants are the number of bells (by
  road width) and the bell colour. So 781 uses the EPS (`pass-si2016`).
- **783 (09:42 rule, recorded after r2; eye-checked 2026-11-25):** goes to EPS. SI 2016 diagram 783
  (tsrgd2016.pdf PDF p215 = printed p214, Sch 11 Pt 2 item 68) is a blue plate with white lettering (the
  earlier r12 note that the EPS is blue where the atlas expects white was a misread — the SI diagram is
  also blue). SI shows two alternative types (LONG LOW VEHICLES and LARGE OR SLOW VEHICLES). The GOV.UK
  EPS is the LONG LOW type and matches the left-hand SI diagram, so it is used (`pass-si2016`); the
  procedural fallback remains the LARGE OR SLOW type.

- **Still excluded:** 969, 958.1 and 959.1 (the EPS differs from SI 2016: extra P sign / missing time panel).
  No owner-held EPS questions remain (the long-standing held rows 2911, 953.2, 818.2 and MARKER are a
  separate decision list and stay procedural).
- **Example layouts (2026-11-23):** the owner, in his own words, "Yes, add the 48 as example faces now" —
  the 48 route, direction and tourist placeholders that have a GOV.UK EPS (DirMotorway 25, TouristBrown 13,
  DirLocal 10). They are stored as `source: "eps"` with `"example": true` (an example layout, not a per-site
  generated sign). The wiki labels them "Example layout (official GOV.UK image) — to be generated per site",
  alongside the Crown copyright / OGL v3.0 attribution. Contact sheets: `qa/renders/eps/r4/` (gitignored). A design for official-art font slots (not implemented) is in `docs/EPS-FONT-SLOTS.md`; per-face fit issues are listed in `qa/EDGE-CASES-EXACT-COLOUR.md` section (d).

- **Exact EPS colours (owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT):**
  drop the atlas-palette colour snap entirely. Main colours (blue, brown, greens, white,
  `#ED1C24`, true black) stay as the pinned converter emits them, now via Art's Ghostscript
  RGB + default_rgb.icc step so fills match the png16m reference. The ICC step itself
  turns former `#E51636` into `#E31837` on 10 faces and former `#E51635` into `#E31836`
  on 2602.2 — not a rule, and no extra mapping is added. Three explicit fallbacks, only,
  are then applied (see `tools/eps/colour_rules.py`): process `#FF0000` → official DfT red
  `#E31837` (Pantone 186) on the 66 signs that emit it; CMYK process black → `#000000` on
  the 25 listed faces; 4003.2 / 4003.5 backing discs → `#000000` per SI 2016. See
  `qa/EDGE-CASES-EXACT-COLOUR.md`.

## Converter versions


`tools/eps/build.py` refuses to convert with anything but Ghostscript 10.05.1 and pdftocairo 25.03.0
(`--any-tools` overrides, with a warning), since other versions may not be byte-identical. `validate.py`
warns (an error under `--strict`) when the cached conversion report names other versions.

## Attribution

> Traffic sign images © Crown copyright, Department for Transport, from GOV.UK "Traffic sign images"
> (https://www.gov.uk/guidance/traffic-sign-images), used under the Open Government Licence v3.0. Converted
> from EPS; the in-use faces are committed in `site/faces-eps/`, each SVG carrying this notice.

See `LICENCE.md` (third-party notices). The images must be reproduced accurately and not in a misleading
context; we never change a legend or meaning, and never present a placeholder as an official image.
