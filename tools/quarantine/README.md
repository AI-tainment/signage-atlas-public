# Quarantined Highway Code caption maps

These files map Highway Code plate captions to dest catalogue ids. The
2026-11-10 re-review found many wrong ids (551 as aircraft, 552 as rocks,
544.1 as zebra, 811 as hospital, …).

**Do not use them as an id source.** `tools/build_uk_index.py` may copy a
caption when the SI wording is not yet in the index, and it flags
`caption_source: hc-map-unverified`.
