"""Explicit owner colour fallbacks for official EPS faces.

Source: owner decision card relayed by Studio Manager, 2026-11-26 09:19 GMT.

Not a general palette snap. The pinned converter first emits exact fills
(Ghostscript pdfwrite in DeviceRGB with default_rgb.icc, then pdftocairo;
Art's fix from art/sign-pipeline-20261126 @ 4d859a4). These rules then
rewrite only the colours the owner named. Everything else is left as the
converter emitted it (blue, brown, greens, white, #ED1C24, #E31836 from
the ICC step on 2602.2, and true black). Pre-ICC #E51636 / #E51635 are
not kept as those hexes: the ICC converter emits #E31837 (10 faces) and
#E31836 (2602.2). That is the ICC step, not a rule, and no extra mapping
is added.

Sources:
- Official red: Department for Transport, "Road traffic sign images for
  reproduction", Colour palette, https://www.gov.uk/guidance/traffic-sign-images
  (updated 17 January 2018): Red, Pantone 186, RGB R227 G24 B55 → #E31837.
  The 66 published faces are those whose official EPS (1995 Illustrator 4.0)
  emit process RGB (1,0,0) → #FF0000. Listed in
  qa/EDGE-CASES-EXACT-COLOUR.md and confirmed in the 26 Nov 2026 Reviewer
  grade.
- Process black: owner ruling to map the CMYK K100 preview to true black
  #000000 on the 25 published faces listed in that edge-case doc. After
  Art's ICC step the converter emits #221F1F for the same ink (was #231F20
  without ColorConversionStrategy=RGB; within 1 per 8-bit channel of both
  the earlier hex and Ghostscript's png16m reference). Both hexes are
  mapped so the rule is stable either side of that fix.
- 4003.2 / 4003.5 backing discs: owner ruling, black (#000000) per SI 2016
  Sch 14 Pt 2 (black circular heads). After the ICC step the discs are
  #5A5B5D (the colour Ghostscript png16m already showed); before it they
  were #514E4F. Both hexes are mapped, and only on those two faces.
"""
from __future__ import annotations

# Official red, DfT palette (Pantone 186, R227 G24 B55).
DFT_RED = "#E31837"

# Each rule: source hex, replacement hex, optional face-id set (None = all
# faces), short id. Matching is case-insensitive; output is uppercase.
RULES: tuple[dict, ...] = (
    {
        "id": "official-red",
        "src": "#FF0000",
        "dst": DFT_RED,
        "faces": None,
        "reason": (
            "DfT traffic-sign-images palette, Pantone 186, RGB 227 24 55 "
            "(updated 2018-01-17). Process (1,0,0) in the 1995 AI EPS is not "
            "the pack's stated red."
        ),
    },
    {
        "id": "process-black",
        "src": "#221F1F",
        "dst": "#000000",
        "faces": None,
        "reason": (
            "CMYK K100 via GS default_rgb.icc (was reported as #231F20 before "
            "the ICC RGB step). Not a designed grey; SI / TSM intend black."
        ),
    },
    {
        "id": "process-black-pre-icc",
        "src": "#231F20",
        "dst": "#000000",
        "faces": None,
        "reason": "Same K100 ink as process-black, hex emitted without the ICC RGB step.",
    },
    {
        "id": "4003-discs",
        "src": "#5A5B5D",
        "dst": "#000000",
        "faces": frozenset({"4003.2", "4003.5"}),
        "reason": "SI 2016 Sch 14 Pt 2: black circular heads (ICC / png16m disc grey).",
    },
    {
        "id": "4003-discs-pre-icc",
        "src": "#514E4F",
        "dst": "#000000",
        "faces": frozenset({"4003.2", "4003.5"}),
        "reason": "SI 2016 Sch 14 Pt 2: black circular heads (pre-ICC disc grey).",
    },
)


def apply(hexv: str, face_id: str | None = None) -> str:
    """Return the owner-rule hex, or the original (uppercase) if no rule matches."""
    h = hexv.upper()
    if not h.startswith("#"):
        h = "#" + h
    for rule in RULES:
        if h != rule["src"]:
            continue
        faces = rule["faces"]
        if faces is not None and (face_id is None or face_id not in faces):
            continue
        return rule["dst"]
    return h


def applied_rule(hexv: str, face_id: str | None = None) -> str | None:
    """Id of the first matching rule, or None."""
    h = hexv.upper()
    if not h.startswith("#"):
        h = "#" + h
    for rule in RULES:
        if h != rule["src"]:
            continue
        faces = rule["faces"]
        if faces is not None and (face_id is None or face_id not in faces):
            continue
        return rule["id"]
    return None
