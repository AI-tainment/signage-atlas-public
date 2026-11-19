#!/bin/bash
# usage: dobatch.sh <batchname> <specs.json>   (gen/<id>.json must exist for every spec id)
set -e
B=$1; SPECS=$2
GEN=$(cd "$(dirname "$0")" && pwd); R=$(cd "$GEN/../.." && pwd); G=${SA_GEN_WORK:-$R/.gen-work}/gen
cd $R
IDS=$(python3 -c "import json;print(' '.join(x['id'] for x in json.load(open('$SPECS'))))")
D=qa/renders/$B; mkdir -p $D/before $D/after $D/evidence $D/compare
for i in $IDS; do git show HEAD:site/faces/uk/signs/$i.svg > $D/before/$i.svg; cp $G/$i-si.png $D/evidence/si-$i.png; done
python3 $GEN/commit_faces.py ${B#b} $IDS
python3 tools/extract_uk.py --all >/dev/null
python3 tools/rebuild.py --all | tail -1
for i in $IDS; do cp site/faces/uk/signs/$i.svg $D/after/$i.svg; done
python3 - <<P
import json
ids="$IDS".split()
rows=[[i,['$D/evidence/si-%s.png'%i,'$D/before/%s.svg'%i,'$D/after/%s.svg'%i]] for i in ids]
json.dump(rows,open('$G/../cmp.json','w'))
P
CELL=140 PER=4 python3 $GEN/sheet.py $D/compare/before_after.png "$B: SI crop | before | after" $G/../cmp.json
