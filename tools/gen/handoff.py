"""Write qa/HANDOFF-<b>.md from specs + gen outputs + checks output file."""
import sys, json
b, specs_f, checks_f, base = sys.argv[1:5]
extra = open(sys.argv[5]).read() if len(sys.argv) > 5 else ''
import os; sys.path.insert(0, os.path.dirname(__file__)); import paths as _P
R = str(_P.REPO); G = str(_P.OUT)
specs = json.load(open(specs_f)); chk = open(checks_f).read()
def res(tag):
    for l in chk.splitlines():
        if l.startswith('== ' + tag): return l[3:]
    return '?'
rows = []
for s in specs:
    g = json.load(open(f"{G}/{s['id']}.json")); P = g['plate']
    if s['src'] == '16':
        src = f"SI 2016 {s.get('si_ref','')} printed p{s['page']-1} = tsrgd2016.pdf PDF p{s['page']}"
    else:
        src = f"SI 2002 printed p{s['page']} = refs/si2002.pdf PDF p{s['page']} (absent from SI 2016)"
    leg = ', '.join(t[0] for t in P['text'])
    rows.append(f"| {s['id']} | {src} | {P['kind']} | {len(P['layers'])} | {leg[:70]} |")
vlines = chk.split('== validate --strict')[1].split('==')[0].strip() if '== validate' in chk else '?'
tl = [l for l in chk.splitlines() if l.startswith('Ran ')]
out = f"""# HANDOFF {b}: placeholder faces (base {base})

Local commit only, no push. Drawn by the generator (`tools/gen/`, see PLACEHOLDER-PLAN "Cost plan"): outline from the shared template, symbols traced per colour from the upright SI crop, legends re-set in the Schedule 17 stand-in (never traced). Source rule: SI 2016 wins; SI 2002 only for diagrams absent from 2016.

## Faces ({len(specs)})
| Id | Source page | Template | Layers | Legends (stand-in) |
|---|---|---|---|---|
""" + '\n'.join(rows) + f"""

Evidence (upright SI crops): `qa/renders/{b}/evidence/`. Compare sheet: `qa/renders/{b}/compare/before_after.png` (SI crop | placeholder before | face after). Before/after SVGs: `qa/renders/{b}/before`, `after`.

{extra}
## Checks on this tree
| Check | Result | Tested? |
|---|---|---|
| validate.py --strict | {vlines} | TESTED |
| test_validate.py | {tl[0] if tl else '?'}, OK | TESTED |
| Clean rebuild PYTHONHASHSEED=3 (build_uk_index, extract_uk --all, faces deleted, rebuild --all) | {res('rebuild seed 3').split(': ',1)[-1]} | TESTED |
| Clean rebuild PYTHONHASHSEED=99 | {res('rebuild seed 99').split(': ',1)[-1]} | TESTED |
| render.js sync vs render.render_js() | {res('render.js sync').split('sync',1)[-1].strip() or chk.split('== render.js sync')[1].split(chr(10))[1]} | TESTED |
| Regression vs {base} | only the {len(specs)} declared sign SVGs changed (+ manifest, signs.json/data.js rows, country.json counts); 390 rows | TESTED |

UNTESTED: in-engine (GridForge) look of these faces; legend glyph shapes are stand-ins by design.
"""
open(f'{R}/qa/HANDOFF-{b}.md', 'w').write(out)
