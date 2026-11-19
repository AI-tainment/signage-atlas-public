"""Run autoplate over a list of specs -> $SA_GEN_WORK/gen/<id>.json + preview svg + si png.
spec: id, src ('16' or '02'), page, kind, family, opts"""
import sys, json, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import autoplate as A, preview as V
from PIL import Image
import paths as _P
G = str(_P.OUT)
def run(spec):
    id_, src, pg, kind, fam = spec['id'], spec['src'], spec['page'], spec.get('kind', 'auto'), spec.get('family', '')
    diag = spec.get('diag', id_)
    if src == '16':
        cell = A.src16(diag, pg); pcx = None
    else:
        r = A.src02(spec.get('label', diag), pg, up=spec.get('up', 1400), half=spec.get('half', 560))
        if r is None: return None, 'label not found'
        cell, pcx = r
    if 'crop' in spec:
        x0, y0, x1, y1 = spec['crop']; cell = cell.crop((x0, y0, x1, y1)); pcx = None
    cell.save(f'{G}/{id_}-cell.png')
    iso = A.isolate_frame(cell) if spec.get('isolate') == 'frame' else A.isolate(cell, prefer_cx=pcx)
    if iso is None: return None, 'no sign found'
    sign, sil = iso
    o = spec.get('opts', {})
    paths, P, notes = A.build(id_, sign, sil, kind, fam, **o)
    Image.fromarray(sign).save(f'{G}/{id_}-si.png')
    V.svg(paths, P, f'{G}/{id_}.svg')
    json.dump({'spec': spec, 'paths': paths, 'plate': P, 'notes': notes}, open(f'{G}/{id_}.json', 'w'))
    return P, None
if __name__ == '__main__':
    specs = json.load(open(sys.argv[1])); rows = []
    for sp in specs:
        try:
            P, err = run(sp)
        except Exception as e:
            P, err = None, repr(e)[:120]
        if err:
            print('FAIL', sp['id'], err); rows.append([sp['id'] + ' FAIL', [f"{G}/{sp['id']}-cell.png" if os.path.exists(f"{G}/{sp['id']}-cell.png") else '', '']]); continue
        print(sp['id'], P['kind'], 'layers', [l[0] for l in P['layers']], 'text', [t[0] for t in P['text']])
        for n_ in json.load(open(f"{G}/{sp['id']}.json")).get('notes', []): print('   NOTE', n_)
        rows.append([sp['id'], [f"{G}/{sp['id']}-si.png", f"{G}/{sp['id']}.svg"]])
    json.dump(rows, open(sys.argv[2], 'w'))
