import json, sys
import os; sys.path.insert(0, os.path.dirname(__file__)); import paths as _P
P = str(_P.WORK)
inv = {x['id']: x for x in json.load(open(_P.GEN / 'data/inv.json'))}
seq = json.load(open(_P.GEN / 'data/seq.json'))
rows = {r['id']: r for r in json.load(open(_P.REPO / 'countries/uk/signs.json'))}
def specs(batches, ids=None):
    out, miss = [], []
    for b, i in seq:
        if (ids and i not in ids) or (not ids and b not in batches): continue
        x = inv[i]; r = rows[i]
        if x['p16']:
            out.append({'id': i, 'diag': x['diag'], 'src': '16', 'page': x['p16'][0], 'family': x['family'], 'si_ref': r.get('si_ref') or ''})
        elif x['p02']:
            out.append({'id': i, 'diag': x['diag'], 'label': i, 'src': '02', 'page': x['p02'], 'family': x['family']})
        else:
            miss.append(i)
    return out, miss
if __name__ == '__main__':
    bs = [int(a) for a in sys.argv[2].split(',')]
    o, m = specs(bs)
    json.dump(o, open(sys.argv[1], 'w'), indent=0)
    print(len(o), 'specs; no page:', m)
