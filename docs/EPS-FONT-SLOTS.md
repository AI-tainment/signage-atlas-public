# Font slots on official route and tourist EPS (design only)

Owner request, 2026-11-26: for the 48 route / direction / tourist example
faces, plan to use the government originals as the primary drawing, with
font slots for the per-site text, and keep the existing generated
(procedural) versions as fallback. Do not ship Transport; slots take the
atlas’s own font.

This note is the design and a cost estimate. The work is **not implemented**:
it is not clearly bounded (see Cost, and the per-face list in
`qa/EDGE-CASES-EXACT-COLOUR.md` section (d)).

The 48 faces are already stored as `source: "eps"` with `"example": true`
(DirMotorway 25, TouristBrown 13, DirLocal 10). See `docs/EPS.md`.

## What the official files actually contain

The converter reports **0 fonts** and **0 live `<text>` elements** across
all 702 EPS files, including these 48. Official lettering has already been
converted to outlines in the GOV.UK EPS (the intermediate PDF has no
embedded fonts either).

So a slot is not “replace the official font in place”. Any implementation
has to:

1. find the lettering region in the outlined art,
2. remove or mask those paths,
3. draw the atlas’s own font into a measured box,
4. fall back to the procedural generator when a site’s wording will not
   fit, or when the official example’s layout does not match the site.

## Text-region detection

Because there is no typography left in the file, detection is a geometry
problem, not a font problem.

Options:

- **Semi-manual measurement** of axis-aligned boxes (and, where needed,
  route-number patches) on each official example, stored in the slot
  schema below. Accurate, reviewable, and slow on stacked motorway
  plates.
- **Automatic path clustering** (group outlines by fill colour, y-band
  and x-gap; treat dense text-coloured path groups as a slot). This is
  research-grade: it will misfire on symbols that sit next to lettering,
  on route-number patches, on chevrons, and on map-type or roundabout
  layouts (2706, 2925, 2902, 2903). Not a bounded first step.

Recommended, if the work is later approved: semi-manual boxes, starting
with the simpler TouristBrown fingerposts, and treat the motorway stacks
and map-type faces as a later, separate tranche.

## Slot schema in `face_sources.json`

A sketch only; not wired up. Per EPS example face, an optional `slots`
array, for example:

```json
"2201": {
  "source": "eps",
  "example": true,
  "eps": "tourist-signs-eps.zip/tourist-signs-eps/2201.eps",
  "slots": [
    {
      "id": "attraction",
      "box": [x, y, w, h],
      "align": "center",
      "valign": "middle",
      "cap_height": 1.0,
      "colour": "#FFFFFF",
      "max_chars": 18,
      "max_lines": 2,
      "sample": "Steam railway",
      "font": "atlas-standin"
    },
    {
      "id": "distance",
      "box": [x, y, w, h],
      "align": "center",
      "colour": "#FFFFFF",
      "max_chars": 10,
      "sample": "300 yds",
      "font": "atlas-standin"
    }
  ]
}
```

Coordinates would be in the converted SVG’s user units (the same viewBox
as `site/faces-eps/…/2201.svg`). `font` is always the atlas stand-in,
never Transport. Route-number patches (2601.1, 2602.2, 2910) need a
slot kind that paints the patch and the number, because the official
patch typography is outlined and the patch colour can vary (regional
blue vs national red on 2602.2).

The schema would also need a `fallback: "procedural"` policy when
`max_chars` / `max_lines` is exceeded, or when a required slot is
missing at render time.

## Renderer support

A later renderer would:

1. load the official converted SVG for the face,
2. subtract or cover the official lettering paths that occupy each slot
   (those paths are not tagged; they have to be identified from the
   measured box, or stored as a clip/mask produced at measurement time),
3. draw the site’s strings in the atlas font, clipped to the box,
4. if any slot overflows, or the face is one of the map-type / junction
   stacks that has no reliable box, use the existing `_family_plate` /
   procedural generator.

Nothing in `tools/render.js` or the wiki renderer does this today. The
wiki already labels these 48 “Example layout (official GOV.UK image) —
to be generated per site”.

## Cost estimate

| Piece | Estimate | Bound? |
|---|---|---|
| Detection for the simpler tourist / local fingerposts (~20 faces) | a few hours of careful measurement and review | maybe, as a later dedicated job |
| Detection for motorway confirmatory / junction lists / map-type plates (~25 faces, including 2902, 2902.1, 2903, 2915, 2706, 2924–2927) | a day or more, plus review, and some faces may never get a clean box | no |
| Automatic path clustering | open-ended | no |
| `face_sources.json` schema + validation | a few hours, once the first measured boxes exist | yes, after measurement |
| Renderer: axis-aligned boxes on a stripped official SVG, plus procedural fallback | around a day, once the schema is frozen | maybe |
| Renderer: route-number patches, variable line counts, roundabout/map geometry | more than a day; several of those faces may have to stay “example only” | no |

Taken together this is not a clearly bounded add-on to the exact-colour
branch, so it stops at this design. The existing procedural generators
remain the way to produce per-site wording; the official EPS stay as
example layouts.

## Faces that do not fit cleanly

Every one of the 48 fails a clean font-slot substitution, at least
because the official lettering is outlined paths. Many also have
site-variable stacks, number patches, or map-type geometry. The
full per-face reasons are in `qa/EDGE-CASES-EXACT-COLOUR.md` section (d).
