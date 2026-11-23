# Licence

Signage Atlas © 2026 AI-tainment (https://github.com/AI-tainment), licensed under
CC BY-ND 4.0 (https://creativecommons.org/licenses/by-nd/4.0/).

## This repository's own work: CC BY-ND 4.0

The atlas's own compilation, code and original content (HTML, CSS, SVG renderer,
extract and generator scripts, data structure and redrawn faces as original work)
are licensed under the Creative Commons Attribution-NoDerivatives 4.0 International
licence. You may use and share them unmodified, with credit; no derivatives. The full
legal code is in `LICENCE` (verbatim from
https://creativecommons.org/licenses/by-nd/4.0/legalcode.txt, sha256
`9cc97638cf0185884ac800144b6246c7772f94ff2cc70686afa9574aaea4fa2b`).

**Scope:** CC BY-ND 4.0 covers the atlas's own compilation, code and original content
only. It does not relicense the third-party material below; each notice applies to its
own parts.

## Third-party notices (each applies to its own parts)

Faces in this repository are **redrawn** identification silhouettes.
They are not manufacturing drawings and they do not copy Crown artwork
pixel-for-pixel. EPS-sourced faces (below) are cooked locally and are not
part of this repository.

### TSRGD 2016 (SI 2016/362) and SI 2002/3113: OGL v3.0

Traffic Signs Regulations and General Directions diagrams, working
sizes, and prescribed colour *classes* are Crown copyright. This
project derives from those instruments under the Open Government
Licence v3.0:

https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

Attribution when you reuse the diagram data:

> Contains public sector information licensed under the Open Government Licence v3.0.

Hex colours here are screen approximations of BS EN 12899-1 classes
(TSRGD reg 11). The licence does not grant the Transport typeface.

### GOV.UK traffic sign images (EPS): Crown copyright, OGL v3.0

Fixed pictogram faces marked `eps` in `countries/uk/face_sources.json` are taken from the Department
for Transport "Traffic sign images" EPS files (https://www.gov.uk/guidance/traffic-sign-images).
They are Crown copyright and are used under the Open Government Licence v3.0:

> Traffic sign images © Crown copyright, Department for Transport. Contains public sector
> information licensed under the Open Government Licence v3.0.

That artwork is **not covered by the CC BY-ND 4.0 licence**. The tools in `tools/eps/` fetch the zips from
GOV.UK (SHA-256 checked against `countries/uk/sources/eps/manifest.csv`) and convert them locally. Under
the owner's ruling (2026-11-23) the converted faces in use are committed in `site/faces-eps/uk/signs/`,
each carrying "Crown copyright ... Open Government Licence v3.0" in its `<desc>`, with a `README.txt`
notice; they remain Crown copyright under OGL v3.0. The raw EPS files and zips are not committed. The EPS lettering is outlined artwork, not a font; no Transport font file is used or shipped.
GOV.UK asks that the images are reproduced accurately and not in a misleading context.

### OpenStreetMap: ODbL

OSM tag values (e.g. `traffic_sign=GB:670`) are cross-references to OpenStreetMap
tagging. Where OSM data is used: © OpenStreetMap contributors, Open Database Licence
(ODbL) 1.0. No OSM geodata is included.

### Traffic Signs Manual: not OGL

The Traffic Signs Manual (including Chapter 5, 2018) is Crown
copyright and is **not** released under the Open Government Licence.

The TSM5 (2018) notice allows free reproduction for non-commercial
research, private study, and internal circulation. Other uses need
permission from the copyright holder (DfT / TSO).

This repository quotes TSM tables only as source citations on marking and
siting rows. Do not treat TSM text in this tree as OGL.

### The Highway Code: OGL v3.0

The Official Highway Code (2026) is Crown copyright and released
under OGL v3.0. This repository uses the annex pages on
https://www.highwaycodeuk.co.uk/ (and the GOV.UK original) for
**English captions only**. Those pages are not an id source: several
Highway Code plates are bound to the wrong dest diagram number.

See `docs/SOURCES.md`.

### Know Your Traffic Signs

KYTS is Crown copyright. Confirm its licence before reuse; this
project does not treat it as OGL by default.

### Typeface

Transport Heavy and Transport Medium are commercial. They are not in
this repository. Legends are Schedule 17 stand-in strokes (polygons,
rects, arcs). Seven-bar numerals appear only on MS4 (Sch17 Part 5 VMS).
