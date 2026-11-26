# Signage Atlas

A wiki of traffic signs, road markings, and street furniture.

**EPS first.** Fixed pictogram sign faces come from the official GOV.UK traffic sign images (EPS, Crown
copyright, OGL v3.0), fetched once and converted on your machine. The 164 in-use converted faces (116 fixed pictograms and 48 example layouts for route, direction and tourist signs) are committed under
`site/faces-eps/` with a Crown copyright / OGL v3.0 notice (owner ruling, 2026-11-23); the raw EPS and zips are not. Signs with
variable text, composites, plates whose wording we set in our own primitive lettering, and gaps stay
**procedural**, and the procedural face is the offline fallback for every EPS face. See `docs/EPS.md` and
`docs/EPS-COVERAGE.md`.

Iterate faces and dimensions here. Port strokes back into the game cooker after the wiki looks right. Do not QA glyphs inside Unity.

## Open the wiki

```bash
cd path/to/signage-atlas-public
SA_EPS_FETCH=1 ./tools/serve.sh   # first run: fetch + convert the GOV.UK EPS faces (needs gs, poppler-utils)
./tools/serve.sh                  # later runs, or offline: procedural faces where no EPS is cooked
# http://127.0.0.1:8765/
```

Hash routes (no server required beyond static files):

- `#/uk` — country home
- `#/uk/signs/611.1` — mini-roundabout plate
- `#/uk/markings/1003.4` — mini disc
- `#/uk/furniture/chs-76` — 76 mm circular post
- `#/uk/fonts` — Transport (not shipped) vs Schedule 17 stand-in strokes
- `#/uk/siting` — siting keys with a source on every number
- `#/uk/about` — sources, licences, method, limitations

`site/assets/data.js` is a `window.ATLAS_UK` dump so `file://` also works.

## Rebuild (one item or all)

The bake tools live in this tree. Wiki cards load `site/faces/<country>/<kind>/<id>.svg`. After you change a drawer or the dest catalogue, rebuild:

```bash
# every sign, marking, and furniture face + data.js
python3 tools/rebuild.py --all

# one item (repeat --id / --item)
python3 tools/rebuild.py --id 611.1
python3 tools/rebuild.py --item 670 --item 602 --item 1003.4

# one kind
python3 tools/rebuild.py --kind markings
python3 tools/rebuild.py --kind signs --id 611.1

# re-read GridForge dest, then bake (full catalogue, or merge listed ids)
python3 tools/rebuild.py --extract --all
python3 tools/rebuild.py --extract --id 611.1

python3 tools/rebuild.py --list --kind furniture
```

`tools/atlas/render.py` is the only drawing code; `site/assets/render.js` is generated from it by `rebuild.py --all` (palette + face URLs, no drawers) and `validate.py` fails if it differs. `tools/extract_uk.py` is the only JSON writer. English display names live in `tools/uk_english_names.py` (Highway Code annex wording; see `docs/SOURCES.md`) and are copied into `countries/uk/overlay.json`; diagram numbers stay as `id` / `diagram` only. Glyph flags and licence also live in overlay + `countries/uk/tsrgd2016_index.json`, so a re-extract does not wipe hand fixes. Pass `--dest` for a GridForge tree; the default catalogue is `vendor/gridforge/UkTsrgdCatalogue.cs`. `python3 tools/rebuild.py --all` runs `tools/validate.py` (`--strict` counts warnings as failures; `python3 tools/test_validate.py` seeds faults that must fail it). `extract_uk.py` refuses to overwrite JSON hand-edited since the last extract (`--force` discards). Statuses come from `countries/uk/sources/` (SI 2016/362 consolidated text; 2002 legacy lists).

## Layout (other countries later)

```
countries/
  uk/                 live GB catalogue (JSON source of truth)
    country.json
    signs.json        dest catalogue rows + street-name plate
    markings.json     TSM Chapter 5 / TSRGD Sch 9/11/14
    furniture.json    posts / Belisha / gantry / pylon (each value sourced)
    siting.json
    overlay.json      hand names, glyph flags, licence (applied by extract)
    tsrgd2016_index.json
  _template/          copy to countries/us, countries/de, …
site/
  index.html
  assets/{wiki.css,render.js,app.js,data.js}
tools/extract_uk.py     rebuilds JSON from GridForge dest UkTsrgdCatalogue
tools/rebuild.py        bake one (--id) or all faces into site/faces/
tools/atlas/render.py   SVG drawers used by rebuild
site/faces/uk/          baked SVG + manifest.json
tools/eps/              GOV.UK EPS fetch / convert / map / compare / checks (EPS-first faces)
countries/uk/face_sources.json   per-face source: eps | procedural | placeholder
site/faces-eps/uk/      converted EPS faces in use (committed with the Crown/OGL notice)
```

A new country is a folder under `countries/` with the same five JSON files, plus a renderer module. The wiki already lists US and DE as placeholders.

## UK source

JSON is written by `tools/extract_uk.py` from a vendored `UkTsrgdCatalogue.cs` snapshot (412 `TsrgdRow`s) plus `overlay.json` and `tsrgd2016_index.json`. Specs 015 and 019 are cited only where a `source` field says so; their full text is not in this tree.

```bash
python3 tools/extract_uk.py --all
python3 tools/extract_uk.py --dest /path/to/gridforge-dest --all
python3 tools/rebuild.py --all
```

Counts on the home page and in `country.json` come from the JSON. Glyph vs fallback is the `glyph` flag. Rows that are not a current 2016 diagram have `status` / `kind: non-tsrgd`.

## What each article shows

- Caption from the 2016 index (or overlay), not a raw id
- Working dimensions in metres, each with a `source`
- Official font (Transport, not shipped) and the Schedule 17 stand-in
- Mount, underside clearance, verge offset, OSM tag
- SVG face from `tools/atlas/render.py` (hex colours are screen approximations of BS EN 12899-1 classes)

Fallback faces are a grey hatched placeholder with the id. They do not impersonate another diagram.

## Licence

See `LICENCE.md`. TSRGD 2016 is OGL v3.0. The Traffic Signs Manual has its own non-commercial notice and is not OGL. Faces are redrawn. Transport is not shipped.

OSM tags: © OpenStreetMap contributors, ODbL.

The atlas's own compilation, code and original content are CC BY-ND 4.0 (`LICENCE`); third-party notices in `LICENCE.md` apply to their own parts.

GitHub Pages is not wired. Serve locally.

## Repo

https://github.com/AI-tainment/signage-atlas-public
