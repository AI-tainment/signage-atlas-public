# Scope: GridForge signage library

This repo is GridForge's library for **everything signage-related on UK roads**. Everything should look real: drawn from the statutory diagram or a cited standard, never guessed. Anything not yet verified is marked UNVERIFIED and listed in `qa/UNVERIFIED-SOURCES.md`.

## In scope
1. **Signs**: every TSRGD 2016 diagram (SI 2002 only where 2016 has no diagram of that number), with the source of each face recorded.
2. **Road markings**: TSRGD 2016 Sch 7 and others.
3. **Street furniture, mountings and posts**: CHS posts, two-post mounts, street-name posts, Belisha beacons, wood poles (BS 1990), lattice pylons, etc. Each figure carries its source in `countries/uk/furniture.json`.
4. **UK motorway gantries**: portal and cantilever.
5. **Large motorway variable message signs (VMS)**: text panels (several lines of LED characters) and pictogram panels.
6. **Smart motorway lane signals (AMI)**: speed-limit roundels, red X, lane arrows, with flashing lamps.
7. **Smaller verge-mounted message signs.**

## Deliverables beyond static faces
- **Message render variants** that look like the real LED displays: pixelated national speed limit, reduced limits 60 / 50 / 40, red X, lane closed, and queue / congestion text.
- **LED flashing states**: amber flashing lamps that mark advisory vs mandatory displays, given either as animated frames or as a frame spec (on/off timing per lamp pair). TSRGD 2016 Sch 15 Pt 4 (printed p522) fixes the rate at 60–90 flashes per minute, with one horizontal pair lit while the other is off.
- **Look of LED matrices and pictograms**: Art will advise (pixel pitch, glow, off-pixel colour, pictogram style). No look is fixed in the repo until Art signs off.

## Sources to cite where they apply (verified status in brackets)
| Source | Use | Status |
|---|---|---|
| TSRGD 2016 (SI 2016/362), `refs/si2016.pdf` | All signs. Sch 14 (printed p425): light signals, crossings and lane control (Pt 1 para 16, printed p434: above-lane green arrow / red cross / white diagonal arrow, centre height 5.5–9 m). Sch 15 (printed p507): matrix signs and light signals on motorways and dual carriageways (Pt 2 items 1–16, diagrams 6001–6032.1; Pt 4 flashing lamps). Sch 16 (printed p524): VMS legends and performance classes | verified (pdftotext, this round) |
| Note on the brief | The brief named "Sch 13/14" for signals and VMS. Sch 13 is **temporary signs**; signals and VMS are Sch 14, 15 and 16 | verified |
| SI 2002/3113, `refs/si2002.pdf` | Diagrams absent from 2016 | verified (page images) |
| BS EN 12966 | VMS performance (named in TSRGD 2016 Sch 16) | named in TSRGD (verified); standard itself not opened (UNVERIFIED) |
| BS 1990-1:1984 | Wood poles | title verified (BSI Knowledge); Table 1 read from a supplier summary (UNVERIFIED against the standard) |
| BS EN 12899-1 | Fixed signs, posts | UNVERIFIED |
| DMRB (e.g. sign gantry structures, CD 127 / CD 365) | Gantry clearance and geometry | UNVERIFIED |
| National Highways MS4 / AMI / MCHW specifications | VMS and lane-signal equipment | UNVERIFIED |
| National Grid L12 (TS 43-11 / NGTS 3.4.3) | Pylon | figures via telcontar.net (secondary source) |

## Where things live
- Faces: `tools/atlas/render.py`, traced outlines in `tools/atlas/traced.py`. `site/assets/render.js` is generated.
- Furniture rows: `tools/extract_uk.py` `furniture()`, which writes `countries/uk/furniture.json`. The gantry/VMS section (`"section": "gantry-vms"`) has one row per type: `portal` (drawn), plus `cantilever`, `vms-text`, `vms-pictogram`, `lane-signal` and `verge-ms` as placeholders. Placeholders carry no figures, only `todo` and `sources_needed`, and are drawn with the neutral hatched placeholder face.
- `tools/validate.py` enforces this: one row per type, and each placeholder has a todo, sources_needed, and no figures. Tests are in `tools/test_validate.py`.
- Rules: local commits only; TSRGD 2016 wins over 2002; no DfT font (Schedule 17 stand-in lettering only); never invent a dimension or colour.
