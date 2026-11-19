"""Locate a diagram on a tsrgd2016.pdf page by its number label; return upright crop.
loc(pdfpage, diag) -> list of PIL images (upright = rotated -90)."""
import re, subprocess, os, functools
import numpy as np
from PIL import Image
import sys; sys.path.insert(0, os.path.dirname(__file__)); import paths as _P
PDF=str(_P.TSRGD2016); PG=str(_P.WORK)
_bb=None
def words(pg):
    global _bb
    if _bb is None:
        f=f'{PG}/t16bbox.html'
        if not os.path.exists(f):
            subprocess.run(['pdftotext','-bbox',PDF,f],check=True)
        _bb=open(f).read().split('<page ')[1:]
    out=[]
    for m in re.finditer(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<',_bb[pg-1]):
        out.append((m.group(5),)+tuple(float(x) for x in m.groups()[:4]))
    return out
@functools.lru_cache(None)
def page(pg, dpi=300):
    f=f'{PG}/t16-{dpi}-{pg:03d}.png'
    if not os.path.exists(f):
        subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(pg),'-l',str(pg),'-png','-singlefile',PDF,f[:-4]],check=True)
    return Image.open(f).convert('RGB')
def labels(pg):
    W=words(pg); out=[]
    for i,(w,x0,y0,x1,y1) in enumerate(W):
        if re.match(r'^\d{3,4}(\.\d+)?[A-Z]?$',w) and i>0 and W[i-1][0]=='Diagram':
            out.append((w,x0,y0,x1,y1))
    return out
def find(diag, pages=None):
    pages=pages or range(39,544)
    return [(pg,l) for pg in pages for l in labels(pg) if l[0]==diag]
def crop(pg, diag, dpi=300, pad=3):
    L=sorted(labels(pg), key=lambda l:l[1])
    for i,l in enumerate(L):
        if l[0]==diag:
            x0=l[1]-pad
            sp=sorted(b[1]-a[1] for a,b in zip(L,L[1:])) or [120]
            x1=(L[i+1][1]-pad) if i+1<len(L) else 575
            y1=l[2]-2
            im=page(pg,dpi); s=dpi/72
            c=im.crop((int(x0*s),int(30*s),int(x1*s),int(y1*s)))
            a=np.array(c.convert('L'))<200
            ys=np.where(a.any(1))[0]; xs=np.where(a.any(0))[0]
            if len(ys): c=c.crop((max(0,xs[0]-8),max(0,ys[0]-8),xs[-1]+8,ys[-1]+8))
            return c.rotate(-90,expand=True), c
    return None, None

MINC=40
def cell(img):
    """Pick the table cell (between vertical rules) with the most ink in an upright crop."""
    a=np.array(img.convert('L'))<128
    rgb=np.array(img.convert('RGB'))
    h=a.shape[0]
    rules=[x for x in range(a.shape[1]) if a[:,x].sum()>0.96*h]
    edges=[0]+rules+[a.shape[1]]
    import cv2
    dpi_s=img.height/1.0
    best=None
    for x0,x1 in zip(edges,edges[1:]):
        if x1-x0<20: continue
        sub=a[:,x0+3:x1-3].astype(np.uint8).copy()
        sub[sub.mean(1)>0.6]=0
        k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        m=cv2.morphologyEx(sub,cv2.MORPH_CLOSE,k)
        n,lab,st,_=cv2.connectedComponentsWithStats(m,8)
        big=0
        for i in range(1,n):
            cw,ch=st[i,2],st[i,3]
            if min(cw,ch)>MINC and st[i,4]>0.05*cw*ch and max(cw,ch)<0.98*max(sub.shape): big+=cw*ch
        col=((rgb[:,x0+2:x1-2].astype(int).max(2)-rgb[:,x0+2:x1-2].astype(int).min(2))>60).sum()
        sc=big+col*3
        if best is None or sc>best[0]: best=(sc,x0,x1)
    _,x0,x1=best
    c=img.crop((x0+3,0,x1-2,h))
    b=np.array(c.convert('L'))<200
    ys=np.where(b.any(1))[0]; xs=np.where(b.any(0))[0]
    if len(ys): c=c.crop((max(0,xs[0]-6),max(0,ys[0]-6),xs[-1]+6,ys[-1]+6))
    return c
def upright(diag, pg=None, dpi=300):
    if pg is None:
        f=find(diag)
        if not f: return None, None
        pg=f[0][0]
    u,_=crop(pg,diag,dpi)
    return (cell(u) if u is not None else None), pg
