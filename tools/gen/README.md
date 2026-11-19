# Placeholder face generator (tools/gen)

Not imported by `rebuild.py`/`validate.py`; its output is plain data in `tools/atlas/traced.py` (PATHS, SOURCE, PLATES with a `kind`), drawn by `render._auto`. This is the exact generator used for b3 onward (committed 19 Nov 2026 from the build box's working copy). All paths come from `paths.py`: repo-relative, or set by `SA_GEN_WORK` (cache/work dir, default `.gen-work/`), `SA_TSRGD2016`, `SA_SI2002` (default `refs/*.pdf`; `refs/` and `.gen-work/` are gitignored). Needs `opencv-python-headless`, `rapidocr_onnxruntime`, poppler (`pdftoppm`, `pdftotext`) and headless Chrome (sheets).

- `specs/bN.json`: the exact per-face specs (page, source, overrides) of every generated batch. **Every generated face in traced.py must be reproducible from these.**
- `reproduce.py [specs...]`: re-runs every spec into a temp dir, patches a temp copy of traced.py and compares byte-for-byte (exit 1 on any mismatch). Run by `checks.sh`.
- `data/`: `si2002-ocr.json.gz` (OCR labels of the SI 2002 diagram pages), `inv.json` / `seq.json` (placeholder inventory and batch order, used by `mkspecs.py`).
- `locate.py`, `autoplate.py` (isolate / `isolate_frame`, template, OCR legends re-set in the stand-in, trace symbol colours), `runbatch.py specs.json rows.json`, `commit_faces.py <batch> <ids...>`, `preview.py`, `sheet.py`, `tpatch.py`.
- `mkspecs.py out.json <plan batches>`, `dobatch.sh bN specs.json` (before/after/evidence + compare sheet), `handoff.py`, `checks.sh [base]` (validate --strict, tests, two-seed rebuild, render.js sync, changed faces, reproduce).
