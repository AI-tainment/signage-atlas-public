#!/bin/bash
# Exit checks on the current working tree of signage-atlas. usage: checks.sh [baseref]
set -u
R=$(cd "$(dirname "$0")/../.." && pwd); BASE=${1:-HEAD}
# Scratch rebuild trees: $SA_SCRATCH (default <repo>/.gen-work/scratch, gitignored), via mktemp.
SCR=${SA_SCRATCH:-$R/.gen-work/scratch}; mkdir -p "$SCR"
cd $R
echo "== validate --strict"; python3 tools/validate.py --strict 2>&1 | tail -1
echo "== no-name"; python3 tools/no_name_check.py
echo "== test_validate"; python3 tools/test_validate.py 2>&1 | tail -3
for seed in 3 99; do
  W=$(mktemp -d "$SCR/rb-$seed.XXXXXX")
  git ls-files -co --exclude-standard -z | xargs -0 cp --parents -t $W 2>/dev/null
  (cd $W && export PYTHONHASHSEED=$seed && python3 tools/build_uk_index.py >/dev/null 2>&1 && python3 tools/extract_uk.py --all --force >/dev/null 2>&1 && rm -rf site/faces/uk/signs site/faces/uk/markings site/faces/uk/furniture site/assets/render.js && python3 tools/rebuild.py --all >/dev/null 2>&1)
  d=$(cd $W && for f in $(git -C $R ls-files -co --exclude-standard); do cmp -s $f $R/$f || echo $f; done; )
  rm -rf "$W"
  echo "== rebuild seed $seed: $( [ -z "$d" ] && echo 'byte-identical (0 files differ)' || echo "DIFF: $d")"
done
echo "== render.js sync"; python3 -c "
import sys; sys.path.insert(0,'tools')
from atlas import render; a=render.render_js(); b=open('site/assets/render.js').read()
print('byte-identical' if a==b else 'DIFF', len(a.encode()),'bytes')"
echo "== changed faces vs $BASE"; git diff --name-only $BASE -- site/faces | grep svg$ | tr '\n' ' '; echo
echo "== rows"; python3 -c "
import json; d=json.load(open('countries/uk/signs.json')); rows=d if isinstance(d,list) else d.get('signs',d.get('rows',[]))
print(len(rows))"
echo "== eps"; python3 tools/eps/fetch.py --verify | tail -1; python3 tools/eps/map.py --check
echo "== deploy guard (EPS attribution)"; python3 tools/eps/deploy_guard.py site
echo "== face-qa"; python3 tools/face_qa.py | head -1
echo "== reproduce (tools/gen/specs vs traced.py)"; python3 $R/tools/gen/reproduce.py 2>&1 | grep -v Warning
