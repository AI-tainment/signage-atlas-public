"""Prove the committed specs reproduce the committed generated faces byte-for-byte.

usage: python3 tools/gen/reproduce.py [specs/bN.json ...]   (default: every tools/gen/specs/b*.json)
Re-runs the generator on every spec into a temp dir, writes the results into a temp copy of
tools/atlas/traced.py with commit_faces, and compares it with the committed traced.py.
Needs the SI PDFs (see paths.py). Exit 0 = every face identical."""
import sys, os, json, glob, tempfile, shutil, pathlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths as P
import runbatch, commit_faces, tpatch

def entry(src, id_):
    """Every traced.py line that belongs to face id_ (paths id_/n, SOURCE, PLATES)."""
    keys = {repr(id_)} | set(re.findall(r"    ('" + re.escape(id_) + r"/\d+'):", src))
    out, cur = [], None
    for line in src.splitlines():
        m = re.match(r"    ('[^']*'): ", line)
        if m: cur = m.group(1)
        elif not line.startswith('        '): cur = None
        if cur in keys: out.append(line)
    return out

def main(files):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='sa-repro-'))
    try:
        out = tmp / 'gen'; out.mkdir()
        runbatch.G = str(out); commit_faces.G = str(out)
        t = tmp / 'traced.py'; shutil.copy(P.TRACED, t); tpatch.T = t
        bad, n = [], 0
        for f in files:
            for sp in json.load(open(f)):
                n += 1
                try:
                    Pl, err = runbatch.run(dict(sp))
                except Exception as e:
                    Pl, err = None, repr(e)[:100]
                if err:
                    bad.append((sp['id'], 'generator failed: ' + err)); continue
                commit_faces.apply([sp['id']], sp['batch'])
        a, b = P.TRACED.read_text(), t.read_text()
        for f in files:
            for sp in json.load(open(f)):
                if any(x[0] == sp['id'] for x in bad): continue
                if entry(a, sp['id']) != entry(b, sp['id']):
                    bad.append((sp['id'], 'differs from committed traced.py'))
        whole = 'whole file byte-identical' if a == b else 'whole file differs (re-applied faces move to the end of each table; the check is per face)'
        print(f'reproduce: {n - len(bad)}/{n} faces byte-identical (their PATHS, SOURCE and PLATES lines in traced.py); {whole}')
        for i, why in bad: print('  MISMATCH', i, why)
        return 0 if not bad else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    fs = sys.argv[1:] or sorted(glob.glob(str(P.SPECS / 'b*.json')))
    sys.exit(main(fs))
