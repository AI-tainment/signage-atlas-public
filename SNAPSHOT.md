# Public snapshot notes

Single-commit snapshot of the Signage Atlas tracked tree (source: merged private main 1f664e2), prepared for a possible public release.

## Left out, and why

- **SI PDFs (`refs/`)**: never tracked in the working repo, and SI 2002/3113 is about
  305 MB, over GitHub's 100 MB file limit. Both instruments are OGL v3.0 and can be
  downloaded from legislation.gov.uk (SI 2016/362 and SI 2002/3113). Page references use
  the "printed pN" convention, which is the same in every copy. `tools/gen/reproduce.py`
  (and the face generator) needs them locally: put `refs/tsrgd2016.pdf` (the 548-page
  copy with a cover note, PDF p = printed + 1) and `refs/si2002.pdf` in place first
  (`refs/` is gitignored). The other checks need no PDFs.
- **`qa/` working notes and renders** (handoffs, resume notes, review contact sheets,
  rotation audit, placeholder plan): internal process records of past rounds. Kept:
  `qa/UNVERIFIED-SOURCES.md`, `qa/DECISIONS-PENDING.md` and the SI evidence crops it cites
  (`qa/renders/r6/evidence/`).

- **Raw GOV.UK EPS and zips** (`.cache/`): not included. The 156 converted official faces in use (108 fixed pictograms and 48 example layouts) ARE
  included in `site/faces-eps/uk/signs/`, each with a Crown copyright / Open Government Licence v3.0
  notice in its `<desc>` (see `LICENCE.md` and `docs/EPS.md`).

## Checks

`tools/gen/checks.sh` runs validate --strict, the name and absolute-path check
(`tools/no_name_check.py`), test_validate, two byte-identical rebuilds (PYTHONHASHSEED 3
and 99; scratch under `$SA_SCRATCH`, default `.gen-work/scratch`, gitignored), render.js
sync and the generator reproduce check. The path check's allow-list names only qa working
notes that are not in this snapshot.

Licence: `LICENCE.md` (CC BY-ND 4.0 for the atlas's own work; third-party notices apply
to their own parts) and `LICENCE` (CC BY-ND 4.0 legal code).
