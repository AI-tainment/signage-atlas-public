"""Write accepted generator outputs into tools/atlas/traced.py (PATHS, SOURCE, PLATES)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import tpatch
import paths as _P
G = str(_P.OUT)

def fmt_plate(key, P):
    keys = ['w', 'h', 'rx', 'plate', 'layers', 'text', 'over', 'fields', 'kind']
    body = ''.join(f"        {k!r}: {P[k]!r},\n" for k in keys)
    return f"    {key!r}: {{\n{body}    }},\n"

def set_plate(src, key, P):
    i = src.index("\nPLATES: dict")
    j = src.index("\n}\n", i) + 1
    import re
    m = re.compile(r"    " + re.escape(repr(key)) + r": \{\n(?:        .*\n)*?    \},\n").search(src, i, j)
    new = fmt_plate(key, P)
    if m: return src[:m.start()] + new + src[m.end():]
    return src[:j] + new + src[j:]

def source_text(spec, P):
    d = spec.get('diag', spec['id'])
    kind = P['kind']
    what = {'warn': 'warning triangle from render._warn; symbol layers', 'proh': 'red ring from render._ring_roundel; inner layers',
            'mand': 'blue disc from render._mand; inner layers', 'plate': 'plate silhouette and symbol layers'}[kind]
    leg = '; legends in stand-in lettering at measured positions' if P['text'] else ''
    if spec['src'] == '16':
        pdfp = spec['page']; pr = pdfp - 1
        ref = spec.get('si_ref', '')
        return (f"SI 2016/362 {ref}{', ' if ref else ''}diagram {d} (printed p{pr} = tsrgd2016.pdf PDF p{pdfp}), 400 dpi, "
                f"page rotated 90 deg clockwise to read (table printed sideways): {what} traced by colour (generator b{spec['batch']}){leg}")
    return (f"SI 2002/3113 diagram {d} (printed p{spec['page']} = refs/si2002.pdf PDF p{spec['page']}), 300 dpi colour render, "
            f"portrait page; diagram absent from SI 2016: {what} traced by colour (generator b{spec['batch']}){leg}")

def apply(ids, batch):
    src = tpatch.T.read_text()
    for id_ in ids:
        g = json.load(open(f'{G}/{id_}.json'))
        spec, P, paths = g['spec'], g['plate'], g['paths']
        spec['batch'] = batch
        P = dict(P); P['layers'] = [tuple(l) for l in P['layers']]; P['text'] = [tuple(t) for t in P['text']]
        P['fields'] = [tuple(f) for f in P['fields']]
        src = tpatch.del_paths(src, id_)
        for k, d in paths.items():
            src = tpatch.set_path(src, k, d)
        src = tpatch.set_source(src, id_, source_text(spec, P))
        src = set_plate(src, id_, P)
    tpatch.T.write_text(src)

if __name__ == '__main__':
    apply(sys.argv[2:], sys.argv[1])
