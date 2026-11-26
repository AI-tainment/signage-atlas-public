#!/bin/bash
# Exit checks on the current working tree of signage-atlas. usage: checks.sh [baseref]
#
# Exit non-zero if any check fails. Several tools already print a failure
# (rebuild seed DIFF, render.js DIFF, reproduce MISMATCH) or exit 1, but this
# script used to use `set -u` only and lost exit codes behind pipes, so a
# reproduce MISMATCH still exited 0. Honour each command's exit status, and
# also the text-only DIFF / MISMATCH markers from seed rebuild, render.js and
# reproduce.
#
# Do not grep the whole log for the word FAIL: tools/test_validate.py prints
# "deploy-guard: FAIL" from a test that expects a missing notice, even when
# the suite passes.
set -u
R=$(cd "$(dirname "$0")/../.." && pwd); BASE=${1:-HEAD}
# Scratch rebuild trees: $SA_SCRATCH (default <repo>/.gen-work/scratch, gitignored), via mktemp.
SCR=${SA_SCRATCH:-$R/.gen-work/scratch}; mkdir -p "$SCR"
cd "$R"

failed=0
fail() {
  echo "CHECK FAIL: $*" >&2
  failed=1
}

echo "== validate --strict"
vlog=$(mktemp)
if python3 tools/validate.py --strict >"$vlog" 2>&1; then
  tail -1 "$vlog"
else
  tail -1 "$vlog"
  fail "validate --strict"
fi
rm -f "$vlog"

echo "== no-name"
if ! python3 tools/no_name_check.py; then
  fail "no-name / abs-paths"
fi

echo "== test_validate"
tlog=$(mktemp)
if python3 tools/test_validate.py >"$tlog" 2>&1; then
  tail -3 "$tlog"
else
  tail -3 "$tlog"
  fail "test_validate"
fi
rm -f "$tlog"

for seed in 3 99; do
  W=$(mktemp -d "$SCR/rb-$seed.XXXXXX")
  git ls-files -co --exclude-standard -z | xargs -0 cp --parents -t "$W" 2>/dev/null
  (cd "$W" && export PYTHONHASHSEED=$seed && python3 tools/build_uk_index.py >/dev/null 2>&1 && python3 tools/extract_uk.py --all --force >/dev/null 2>&1 && rm -rf site/faces/uk/signs site/faces/uk/markings site/faces/uk/furniture site/assets/render.js && python3 tools/rebuild.py --all >/dev/null 2>&1)
  d=$(cd "$W" && for f in $(git -C "$R" ls-files -co --exclude-standard); do cmp -s "$f" "$R/$f" || echo "$f"; done; )
  rm -rf "$W"
  if [ -z "$d" ]; then
    echo "== rebuild seed $seed: byte-identical (0 files differ)"
  else
    echo "== rebuild seed $seed: DIFF: $d"
    fail "rebuild seed $seed DIFF"
  fi
done

echo "== render.js sync"
rjs=$(python3 -c "
import sys; sys.path.insert(0,'tools')
from atlas import render; a=render.render_js(); b=open('site/assets/render.js').read()
print('byte-identical' if a==b else 'DIFF', len(a.encode()),'bytes')
sys.exit(0 if a==b else 1)
")
ec=$?
echo "$rjs"
case "$rjs" in
  *DIFF*) fail "render.js DIFF" ;;
esac
if [ "$ec" -ne 0 ]; then
  fail "render.js"
fi

echo "== changed faces vs $BASE"; git diff --name-only "$BASE" -- site/faces | grep svg$ | tr '\n' ' '; echo
echo "== rows"; python3 -c "
import json; d=json.load(open('countries/uk/signs.json')); rows=d if isinstance(d,list) else d.get('signs',d.get('rows',[]))
print(len(rows))"

echo "== eps"
flog=$(mktemp)
if python3 tools/eps/fetch.py --verify >"$flog" 2>&1; then
  tail -1 "$flog"
else
  tail -1 "$flog"
  fail "eps fetch --verify"
fi
rm -f "$flog"
if ! python3 tools/eps/map.py --check; then
  fail "eps map --check"
fi

echo "== deploy guard (EPS attribution)"
if ! python3 tools/eps/deploy_guard.py site; then
  fail "deploy guard"
fi

echo "== face-qa"
qlog=$(mktemp)
if python3 tools/face_qa.py >"$qlog" 2>&1; then
  head -1 "$qlog"
else
  head -1 "$qlog"
  fail "face-qa"
fi
rm -f "$qlog"

echo "== reproduce (tools/gen/specs vs traced.py)"
rlog=$(mktemp)
python3 "$R/tools/gen/reproduce.py" >"$rlog" 2>&1
rec=$?
grep -v Warning "$rlog" || true
if [ "$rec" -ne 0 ] || grep -q 'MISMATCH' "$rlog"; then
  fail "reproduce MISMATCH"
fi
rm -f "$rlog"

if [ "$failed" -ne 0 ]; then
  echo "== RESULT: FAIL"
  exit 1
fi
echo "== RESULT: PASS"
exit 0
