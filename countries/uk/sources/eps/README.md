# GOV.UK traffic-sign EPS: committed metadata only

- `manifest.csv`: the 18 GOV.UK "traffic sign images" EPS zips (file, bytes, SHA-256, Last-Modified, URL),
  checked anonymously on 23 Nov 2026. Copied unchanged from GridForge `docs/sources/uk-traffic-signs-eps-manifest.csv`
  (main 5af2dda). SHA-256 of this file: `5c99976e02e4b4383aba46f00b354be35a32564f43027b1899a2babba4f433f2`
  (checked by `tools/validate.py`).
- `crosswalk.csv`: each of the 702 EPS files against its TSRGD 2002 number and SI 2016/362 status
  (`same` / `removed` / `unverified`), from GridForge `docs/sources/uk-traffic-signs-eps-crosswalk.csv` (main 5af2dda).
  SHA-256: `8975c83cbc0868e400027cc5f6e6012f8f6d4f7d5255cb5aafe267a6ea07bbc9`.

The zips, the EPS files and every SVG converted from them live only in gitignored folders
(`.cache/eps/`, `site/faces-eps/`). See `docs/EPS.md`.
