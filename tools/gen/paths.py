"""Paths for the face generator. Everything is relative to the repo unless an env var says otherwise.

SA_GEN_WORK   work/cache dir (page renders, bbox text, per-face gen JSON)   default <repo>/.gen-work (gitignored)
SA_TSRGD2016  SI 2016 PDF, tsrgd2016.pdf numbering (PDF page = printed + 1)  default <repo>/refs/tsrgd2016.pdf
SA_SI2002     SI 2002 PDF (PDF page = printed)                                default <repo>/refs/si2002.pdf
<repo>/refs is gitignored: point it (or the env vars) at local copies of the SI PDFs.
"""
import os, pathlib
REPO = pathlib.Path(__file__).resolve().parents[2]
TOOLS = REPO / 'tools'
GEN = TOOLS / 'gen'
SPECS = GEN / 'specs'
WORK = pathlib.Path(os.environ.get('SA_GEN_WORK', REPO / '.gen-work'))
OUT = WORK / 'gen'
TSRGD2016 = pathlib.Path(os.environ.get('SA_TSRGD2016', REPO / 'refs' / 'tsrgd2016.pdf'))
SI2002 = pathlib.Path(os.environ.get('SA_SI2002', REPO / 'refs' / 'si2002.pdf'))
SI2002_OCR = GEN / 'data' / 'si2002-ocr.json.gz'   # OCR of the SI 2002 diagram pages (labels), committed
TRACED = TOOLS / 'atlas' / 'traced.py'
WORK.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
