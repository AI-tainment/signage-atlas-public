# Add a country

Copy this folder to `countries/<iso>/` (example: `countries/us`, `countries/de`).

Required files:

| File | Role |
| --- | --- |
| `country.json` | id, name, iso, licence, fonts, colours, counts |
| `signs.json` | array of sign objects (see UK) |
| `markings.json` | array of marking objects |
| `furniture.json` | posts / gantries / signals |
| `siting.json` | map of siting-id → rule text |

Minimum sign object:

```json
{
  "id": "R1-1",
  "kind": "sign",
  "diagram": "R1-1",
  "name": "Stop",
  "what": "…",
  "chapter": 0,
  "family": "Stop",
  "mount": "Post",
  "siting": "verge_std",
  "siting_note": "",
  "v1": "glyph",
  "glyph": true,
  "renderer": "R1-1",
  "dimensions_m": {
    "plate_width": 0.75,
    "plate_height": 0.75,
    "underside": 2.1,
    "post_diameter": 0.060,
    "verge_offset": 0.6
  },
  "font": {
    "official": "Highway Gothic / FHWA Series (US example)",
    "procedural": "Geometric strokes until a licensed face is approved"
  },
  "osm": "traffic_sign=US:R1-1",
  "colours": ["red", "white"]
}
```

Then:

1. Add a drawer in `site/assets/render.js` (or `render-<iso>.js`).
2. Emit `window.ATLAS_<ISO>` from the extract script into `site/assets/data-<iso>.js`.
3. Register the country in `site/assets/app.js` `COUNTRIES` / `ATLASES`.

Keep units in metres even if the national spec is in millimetres or inches.
