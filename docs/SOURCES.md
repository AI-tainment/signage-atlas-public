# Sources for UK captions and diagrams

Display names are English. Diagram numbers are index ids only.

Highway Code annex wording is the player-facing caption where it matches the dest id’s **2016 meaning**. Highway Code plate→id maps are **not** an id source (many plates on those pages sit on the wrong dest number). TSRGD 2016 plus the 2026-11-10 QA meaning swaps decide which meaning belongs on which id.

Copy of this list also lives in GridForge spec 015 §24.

## Highway Code (OGL)

Canonical: https://www.gov.uk/guidance/the-highway-code  
Mirror used here: https://www.highwaycodeuk.co.uk/ (2026 edition, Crown / OGL)

- Hub: https://www.highwaycodeuk.co.uk/signs-and-signals.html
- Warning: https://www.highwaycodeuk.co.uk/warning-signs-on-the-road.html
- Orders: https://www.highwaycodeuk.co.uk/road-signs-giving-orders.html
- Direction: https://www.highwaycodeuk.co.uk/direction-signs-on-roads-motorways.html
- Information: https://www.highwaycodeuk.co.uk/information-signs.html
- Light signals: https://www.highwaycodeuk.co.uk/light-signals-controlling-traffic.html
- Road markings: https://www.highwaycodeuk.co.uk/road-markings.html
- Road works: https://www.highwaycodeuk.co.uk/road-works-signs.html
- Signals by authorised persons: https://www.highwaycodeuk.co.uk/signals-authorised-persons.html
- Signals to other road users: https://www.highwaycodeuk.co.uk/signals-other-road-users.html
- Vehicle markings: https://www.highwaycodeuk.co.uk/vehicle-markings.html

PDFs on that site:

- https://www.highwaycodeuk.co.uk/uploads/3/2/9/2/3292309/the-highway-code-road-traffic-signs.pdf
- https://www.highwaycodeuk.co.uk/uploads/3/2/9/2/3292309/the-highway-code-traffic-signs.pdf
- https://www.highwaycodeuk.co.uk/uploads/3/2/9/2/3292309/the-highway-code-road-markings.pdf
- https://www.highwaycodeuk.co.uk/uploads/3/2/9/2/3292309/the-highway-code-light-signals-controlling-traffic.pdf
- https://www.highwaycodeuk.co.uk/uploads/3/2/9/2/3292309/know-road-traffic-signs.pdf

Quarantined maps (captions only): `tools/quarantine/hc_highway_code_map.json`, `tools/quarantine/hc_website_map.json`.

## Prescribed diagrams

- TSRGD 2016 (SI 2016/362): https://www.legislation.gov.uk/uksi/2016/362
- Know Your Traffic Signs 2023: https://www.gov.uk/government/publications/know-your-traffic-signs
- Traffic Signs Manual Ch.1, 3, 4, 5 (not OGL), 6, 7, 8
- Working drawings P500 / P670 / P602 / …

## Other wording lists (not id truth)

- Hirst Signs DoT SKU titles: https://hirstsigns.co.uk/tsrgd/
- SABRE Wiki TSRGD galleries
- TSM Chapter 7 (stack / map / flag / confirmatory types)

## This tree

- English names: `tools/uk_english_names.py` → `countries/uk/overlay.json`
- Extract is the only JSON writer: `tools/extract_uk.py`
- Licence: `LICENCE.md`
