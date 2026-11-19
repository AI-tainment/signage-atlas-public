"""Render a PLATES-like spec to standalone SVG for preview (uses repo render helpers)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__)); import paths as _P; sys.path.insert(0, str(_P.TOOLS))
from atlas import render, traced, lettering
C = render.C
def inner(paths, P):
    kind = P.get('kind', 'plate')
    body = ''.join(f'<path d="{paths[k]}" fill="{C[f]}" fill-rule="evenodd"/>' for f, k in P['layers'])
    leg = ''.join(lettering.word(t, cx, cy, cap, C[f], tracking_sw=0.5, part=part, narrow=nar) for t, cx, cy, cap, nar, f, part in P['text'])
    if kind == 'warn': return render._warn() + body + leg
    if kind == 'proh': return render._ring_roundel() + body + leg
    if kind == 'mand': return render._mand('') + body + leg
    return body + leg
def svg(paths, P, out):
    w, h = P['w'], P['h']
    if P.get('kind', 'plate') in ('warn',): w, h = 1.18, 1.06
    if P.get('kind') in ('proh', 'mand'): w, h = 1.0, 1.0
    m = 0.05
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-w/2-m} {-h/2-m} {w+2*m} {h+2*m}" width="400" height="{400*(h+2*m)/(w+2*m):.0f}">{inner(paths,P)}</svg>'
    open(out, 'w').write(s)
