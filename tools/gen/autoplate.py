"""Parametric face generator (Signage Atlas placeholder batches, 18 Nov 2026).

source crop -> isolate sign -> classify colours -> OCR legends (masked, re-set in the
Schedule 17 stand-in, never traced) -> trace symbol layers -> traced.PLATES entry.
Outline templates: warn (render._warn), proh (_proh ring), mand (_mand disc), plate
(traced silhouette, any shape). Only symbols are traced.
"""
import sys, json, re, os, subprocess, functools
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import paths as _P
REPO = str(_P.REPO)
sys.path.insert(0, str(_P.TOOLS))
from atlas import lettering
import locate

PG = str(_P.WORK)
S02 = str(_P.SI2002)

# ---------- sources ----------
def src16(diag, pg, dpi=400):
    u, _ = locate.crop(pg, diag, dpi)
    return locate.cell(u)

@functools.lru_cache(None)
def page02(pg, dpi=300):
    f = f'{PG}/s02-{dpi}-{pg:03d}.png'
    if not os.path.exists(f):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(pg), '-l', str(pg), '-png', '-singlefile', S02, f[:-4]], check=True)
    return Image.open(f).convert('RGB')

_ocr02 = None
def label02(id_, pg):
    global _ocr02
    if _ocr02 is None:
        import gzip
        _ocr02 = json.load(gzip.open(_P.SI2002_OCR, 'rt'))
    for b, t, s in _ocr02.get(f'p-{pg:03d}.png', []):
        if t.strip() == id_:
            xs = [p[0] for p in b]; ys = [p[1] for p in b]
            return min(xs) * 2, min(ys) * 2, max(xs) * 2, max(ys) * 2
    return None

def src02(id_, pg, dpi=300, up=1400, half=560):
    im = page02(pg, dpi)
    lb = label02(id_, pg)
    if lb is None:
        return None
    cx = (lb[0] + lb[2]) / 2
    x0 = max(0, int(cx - half)); x1 = min(im.width, int(cx + half))
    y0 = max(0, int(lb[1] - up)); y1 = int(lb[1] - 6)
    return im.crop((x0, y0, x1, y1)), cx - x0

# ---------- colour ----------
def classify(rgb, family=''):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(int)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    lab = np.full(rgb.shape[:2], 'white', dtype=object)
    chrom = (s > 70) & (v > 60)
    lab[(~chrom) & (v < 90)] = 'black'
    lab[(~chrom) & (v >= 90) & (v < 205)] = 'grey'
    hh = h * 2
    lab[chrom & ((hh < 14) | (hh >= 330))] = 'red'
    lab[chrom & (hh >= 14) & (hh < 40) & (v < 150)] = 'brown'
    lab[chrom & (hh >= 14) & (hh < 40) & (v >= 150)] = 'amber'
    lab[chrom & (hh >= 40) & (hh < 75)] = 'yellow'
    lab[chrom & (hh >= 75) & (hh < 180)] = 'primary' if family != 'Signal' else 'green'
    blue = 'motorway' if family == 'DirMotorway' else 'blue'
    lab[chrom & (hh >= 180) & (hh < 270)] = blue
    lab[chrom & (hh >= 270) & (hh < 330)] = 'red'
    return lab

# ---------- isolate ----------
def isolate(img, prefer_cx=None, pick='largest', _lines=None):
    if _lines is None:
        a0 = np.array(img.convert('RGB'))
        img = Image.fromarray(cv2.copyMakeBorder(a0, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value=(255, 255, 255)))
        prefer_cx = None if prefer_cx is None else prefer_cx + 30
    a = np.array(img.convert('RGB'))
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    ink = ((hsv[..., 2] < 200) | (hsv[..., 1] > 60)).astype(np.uint8)
    # remove long table / dimension rules (thin straight lines)
    hl = cv2.morphologyEx(ink, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (max(60, ink.shape[1] // 3), 1)))
    vl = cv2.morphologyEx(ink, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(60, ink.shape[0] // 2))))
    thin = cv2.morphologyEx(ink, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    lines = ((hl | vl) > 0) & (thin == 0)
    if _lines is None:
        r = isolate(img, prefer_cx, pick, _lines=False)
        if r is not None:
            sh = r[1].shape
            if sh[0] < 0.97 * ink.shape[0] and sh[1] < 0.97 * ink.shape[1]:
                return r
        return isolate(img, prefer_cx, pick, _lines=True)
    if _lines:
        ink[lines] = 0
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    m = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, k)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    if n <= 1:
        return None
    def ok(i):
        w, h = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
        return min(w, h) > 30 and st[i, cv2.CC_STAT_AREA] > 0.08 * w * h
    cand = [(st[i, cv2.CC_STAT_WIDTH] * st[i, cv2.CC_STAT_HEIGHT], i) for i in range(1, n) if ok(i)]
    if not cand:
        return None
    big = max(c[0] for c in cand)
    cand = [c for c in cand if c[0] > 0.25 * big]
    if prefer_cx is not None:
        i = min(cand, key=lambda c: abs(cen[c[1]][0] - prefer_cx) - c[0] * 1e-7)[1]
    else:
        i = max(cand)[1]
    x, y, w, h = st[i, :4]
    sil = (lab == i).astype(np.uint8)
    # fill holes -> silhouette
    cs, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fill = np.zeros_like(sil); cv2.drawContours(fill, cs, -1, 1, -1)
    if fill.sum() < 0.6 * w * h:  # outline with a gap (crop edge): close harder before filling
        big = cv2.morphologyEx(sil, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31)))
        cs, _ = cv2.findContours(big, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        f2 = np.zeros_like(sil); cv2.drawContours(f2, cs, -1, 1, -1)
        if f2.sum() > fill.sum():
            fill = f2
    pad = 2
    x0, y0 = max(0, x - pad), max(0, y - pad); x1, y1 = min(a.shape[1], x + w + pad), min(a.shape[0], y + h + pad)
    return a[y0:y1, x0:x1].copy(), fill[y0:y1, x0:x1]

# ---------- OCR ----------
_eng = None
def ocr(a):
    global _eng
    if _eng is None:
        from rapidocr_onnxruntime import RapidOCR
        _eng = RapidOCR()
    r, _ = _eng(a)
    return [(np.array(b), t, float(s)) for b, t, s in (r or [])]

# ---------- trace ----------
def trace(mask, xf, eps=0.9):
    m = mask.astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        if cv2.contourArea(c) < 6:
            continue
        p = cv2.approxPolyDP(c, eps, True)[:, 0, :]
        if len(p) < 3:
            continue
        pts = [xf(float(x), float(y)) for x, y in p]
        out.append('M' + ' '.join(f'{x:.4f},{y:.4f}'.replace('-0.0000', '0.0000') for x, y in pts) + 'Z')
    return ''.join(out)

def _num(x):
    return float(f'{x:.4f}')

# ---------- build ----------
KIND_BOX = {'warn': (-0.5896, -0.529, 0.5896, 0.529), 'proh': (-0.5, -0.5, 0.5, 0.5), 'mand': (-0.5, -0.5, 0.5, 0.5)}
FIELD = {'warn': None, 'proh': ('circle', 0.0, 0.0, 0.40), 'mand': ('circle', 0.0, 0.0, 0.48)}

def build(key, sign, sil, kind='auto', family='', texts=None, drop=(), ocr_min=0.3, no_ocr=False, eps=0.9, keep_text=(), add=(), fix=None, merge=(), subst=None, chars=None, single=True, addf=None, keep_other=False, pad=2, drop_layers=(), merge_single=True):
    """sign: HxWx3 crop of the sign only; sil: silhouette mask. Returns (paths, plate, notes)."""
    H, W = sil.shape
    if kind == 'auto':
        kind = detect_kind(sign, sil, family)
    ys, xs = np.where(sil > 0)
    bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    if kind in KIND_BOX:
        fx0, fy0, fx1, fy1 = KIND_BOX[kind]
        sx = (fx1 - fx0) / (bx1 - bx0); sy = (fy1 - fy0) / (by1 - by0)
        s = (sx + sy) / 2
        ox, oy = (bx0 + bx1) / 2, (by0 + by1) / 2
    else:
        s = 1.0 / min(bx1 - bx0, by1 - by0)
        ox, oy = (bx0 + bx1) / 2, (by0 + by1) / 2
    xf = lambda x, y: ((x - ox) * s, (y - oy) * s)
    lab = classify(sign, family)
    lab[sil == 0] = 'none'
    notes = []
    # interior region to trace
    if kind == 'warn':
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        inner = (lab == 'white').astype(np.uint8)
        # white field = the largest white component
        n, L, st, _ = cv2.connectedComponentsWithStats(inner, 4)
        i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        cs, _ = cv2.findContours((L == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        region = np.zeros_like(inner); cv2.drawContours(region, cs, -1, 1, -1)
        region = cv2.erode(region, k)
        bg = 'white'
    elif kind == 'proh':
        yy, xx = np.mgrid[0:H, 0:W]
        region = (((xx - ox) * s) ** 2 + ((yy - oy) * s) ** 2 < 0.385 ** 2).astype(np.uint8)
        bg = 'white'
    elif kind == 'mand':
        yy, xx = np.mgrid[0:H, 0:W]
        region = (((xx - ox) * s) ** 2 + ((yy - oy) * s) ** 2 < 0.46 ** 2).astype(np.uint8)
        bg = 'motorway' if family == 'DirMotorway' else 'blue'
    else:
        region = sil.copy(); bg = None
    # ---- OCR legends ----
    items = []
    if not no_ocr:
        for b, t, sc in ocr(sign):
            t = t.strip()
            if sc < ocr_min or not t or t in drop:
                continue
            x0, y0 = b[:, 0].min(), b[:, 1].min(); x1, y1 = b[:, 0].max(), b[:, 1].max()
            if (x1 - x0) * (y1 - y0) < 30:
                continue
            items.append([t, int(x0), int(y0), int(x1) + 1, int(y1) + 1])
    for i, j, t in merge:
        a, b = items[i], items[j]
        items[i] = [t, min(a[1], b[1]), min(a[2], b[2]), max(a[3], b[3]), max(a[4], b[4])]
        items[j] = [''] + b[1:]
    items = [it for it in items if it[0]]
    if fix:
        for i, t in fix.items():
            items[int(i)][0] = t
        items = [it for it in items if it[0]]
    for t in add:
        items.append(list(t))
    for t, fx0, fy0, fx1, fy1 in (addf or ()):
        items.append([t, int(fx0 / s + ox), int(fy0 / s + oy), int(fx1 / s + ox) + 1, int(fy1 / s + oy) + 1])
    if texts is not None:  # explicit overrides: list of (text, x0,y0,x1,y1) in crop px, or (text, idx) to rename OCR item
        new = []
        for t in texts:
            if len(t) == 2:
                new.append([t[0]] + items[t[1]][1:])
            else:
                new.append(list(t))
        items = new
    text_out = []
    boxes = []
    lab0 = lab.copy()
    def place(t, x0, y0, x1, y1):
        x0, y0 = max(0, x0 - pad), max(0, y0 - pad); x1, y1 = min(W, x1 + pad), min(H, y1 + pad)
        box = lab0[y0:y1, x0:x1]
        vals, cnt = np.unique(box[box != 'none'], return_counts=True)
        if len(vals) < 2:
            return False
        order = list(vals[np.argsort(-cnt)])
        back = order[0]
        fore = [v for v in order if v != back][0]
        fm = (box == fore)
        rows = np.where(fm.any(1))[0]; cols = np.where(fm.any(0))[0]
        if not len(rows):
            return False
        it, ib = rows[0] + y0, rows[-1] + 1 + y0
        il, ir = cols[0] + x0, cols[-1] + 1 + x0
        hasdesc = any(c in 'gjpqy' for c in t)
        hasasc = any(c.isupper() or c.isdigit() or c in "bdfhklt'\"&%/()" for c in t)
        ink_h = ib - it
        if hasasc:
            cap = ink_h / (1 + (lettering.DESC_RATIO if hasdesc else 0))
            top = it
        else:
            xh = ink_h / (1 + (lettering.DESC_RATIO / lettering.X_RATIO if hasdesc else 0))
            cap = xh / lettering.X_RATIO
            top = it + xh - cap
        cy = top + cap / 2
        cx = (il + ir) / 2
        capf = cap * s
        w1 = lettering.measure(t, capf, 0.5)
        nar = max(0.55, min(1.5, ((ir - il) * s) / w1)) if w1 > 0 else 1.0
        lettering.NARROW = nar; w2 = lettering.measure(t, capf, 0.5); lettering.NARROW = 1.0
        if w2 > 0:
            nar = max(0.55, min(1.5, nar * ((ir - il) * s) / w2))
        X, Y = xf(cx, cy)
        part = 1 if fore == 'white' else 2
        text_out.append((t, _num(X), _num(Y), _num(capf), _num(nar), fore, part))
        boxes.append((x0, y0, x1, y1))
        sub = lab[y0:y1, x0:x1]
        if keep_other:
            sub[sub == fore] = back
        else:
            sub[(sub != back) & (sub != 'none')] = back
        return True
    for t, x0, y0, x1, y1 in items:
        place(t, x0, y0, x1, y1)
    # single characters the line OCR missed (e.g. a lone P, a figure next to 'am')
    if not no_ocr and not texts and single:
        k3_ = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        caps = [t[3] / s for t in text_out]
        mside = min(H, W)
        lo, hi = (0.6 * np.median(caps), 1.5 * np.median(caps)) if caps else (0.08 * mside, 0.75 * mside)
        for c in [c for c in np.unique(lab[(region > 0)]) if c not in ('none',)]:
            m = ((lab == c) & (region > 0)).astype(np.uint8)
            n_, L_, st_, _ = cv2.connectedComponentsWithStats(m, 8)
            for i in range(1, n_):
                x, y, w_, h_, a_ = st_[i]
                if not (lo <= h_ <= hi) or w_ > 1.3 * h_ or w_ < 0.15 * h_ or a_ < 0.15 * w_ * h_:
                    continue
                pad = int(0.4 * h_)
                ya, yb, xa, xb = max(0, y - pad), min(H, y + h_ + pad), max(0, x - pad), min(W, x + w_ + pad)
                crop = np.full((yb - ya, xb - xa, 3), 255, np.uint8)
                crop[(L_[ya:yb, xa:xb] == i)] = 0
                crop = cv2.resize(crop, (max(8, int(48 * crop.shape[1] / crop.shape[0])), 48), interpolation=cv2.INTER_AREA)
                ocr(crop[:4, :4])  # make sure the engine exists
                (r, _t) = _eng.text_recognizer([crop])
                if r:
                    t, sc = r[0]
                    t = t.strip(); sc = float(sc)
                    if sc > 0.3 and re.fullmatch(r'[A-Z0-9]', t) and (chars is None or t in chars):
                        # a capital the line OCR dropped from the front of a word: merge
                        hit = None
                        for j, (bx0_, by0_, bx1_, by1_) in enumerate(boxes):
                            ov = min(by1_, y + h_) - max(by0_, y)
                            if ov > 0.5 * h_ and 0 <= bx0_ - (x + w_) < 0.8 * h_ and bx0_ > x:
                                hit = j; break
                        if hit is not None and merge_single:  # False = b2 behaviour (lone figure kept separate)
                            old = text_out.pop(hit); ob = boxes.pop(hit)
                            if place(old[0] if old[0].startswith(t) else t + old[0], x, min(y, ob[1]), ob[2], max(y + h_, ob[3])):
                                notes.append(f'merged {t!r} into {old[0]!r}')
                            continue
                        if place(t, x, y, x + w_, y + h_):
                            notes.append(f'single-char legend {t!r} ({sc:.2f})')
    if subst:
        text_out[:] = [(subst.get(t[0], t[0]),) + tuple(t[1:]) for t in text_out]
    # glyph mapping: the Schedule 17 stand-in (lettering.SHEET_CHARS) has no ',' or '?' etc.;
    # an unsupported character would fall back to a bar ('|' / '!'), so drop it here, once, for every face.
    ok = set(lettering.SHEET_CHARS) | {' '}
    mapped = []
    for t in text_out:
        s_ = ''.join(c for c in t[0] if c in ok)
        s_ = ' '.join(s_.split())
        if s_ != t[0]:
            notes.append(f'unsupported glyphs dropped: {t[0]!r} -> {s_!r}')
        if s_:
            mapped.append((s_,) + tuple(t[1:]))
    text_out[:] = mapped
    # ---- layers ----
    layers, paths = [], {}
    k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    if kind == 'plate':
        # silhouette in the colour of its boundary
        er = cv2.erode(sil, k3, iterations=2)
        edge = (sil > 0) & (er == 0)
        ev, ec = np.unique(lab[edge & (lab != 'none')], return_counts=True)
        sc = ev[np.argmax(ec)] if len(ev) else 'black'
        paths[f'{key}/0'] = trace(sil, xf, eps)
        layers.append((sc, f'{key}/0'))
        base = sc
    else:
        base = bg
    areas = {}
    for c in np.unique(lab[(region > 0) & (lab != 'none')]):
        if c == base:
            continue
        areas[c] = int(((lab == c) & (region > 0)).sum())
    order = sorted(areas, key=lambda c: -areas[c])
    n = len(layers)
    for c in order:
        if c in drop_layers:  # e.g. a traced ring duplicating the template ring (618.2)
            continue
        m = ((lab == c) & (region > 0)).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k3)
        if m.sum() < 20:
            continue
        m = cv2.dilate(m, k3)
        d = trace(m, xf, eps)
        if d:
            paths[f'{key}/{n}'] = d; layers.append((c, f'{key}/{n}')); n += 1
    # when plate background is under other layers, a 2nd pass of the base colour restores
    # thin details of the base colour (e.g. black symbols on a white plate with black border)
    if kind == 'plate':
        inner = cv2.erode(sil, k3, iterations=4)
        m = ((lab == base) & (inner > 0)).astype(np.uint8)
        # only if base colour areas lie on top of another layer colour region
        if order and m.sum() > 50:
            covered = np.zeros_like(m)
            for c in order[:1]:
                cm = cv2.morphologyEx(((lab == c) & (region > 0)).astype(np.uint8), cv2.MORPH_CLOSE,
                                      cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
                covered |= cm
            m2 = (m & covered).astype(np.uint8)
            if m2.sum() > 30:
                d = trace(m2, xf, eps)
                if d:
                    paths[f'{key}/{n}'] = d; layers.append((base, f'{key}/{n}')); n += 1
    # residual legend check: OCR the masked label image again
    if not no_ocr:
        rgbmap = {'white': (247, 247, 247), 'black': (20, 20, 20), 'grey': (140, 142, 148), 'red': (204, 26, 26), 'blue': (0, 92, 166),
                  'motorway': (0, 82, 158), 'yellow': (230, 194, 0), 'amber': (242, 158, 20), 'brown': (115, 69, 31), 'primary': (13, 115, 56),
                  'green': (30, 184, 56), 'none': (255, 255, 255)}
        img2 = np.zeros_like(sign)
        for c, v in rgbmap.items():
            img2[lab == c] = v
        for b, t, sc in ocr(img2):
            if sc > 0.5 and len(t.strip()) >= 1:
                notes.append(f'RESIDUAL TEXT {t!r} {sc:.2f} at {b[0]}')
    w = _num((bx1 - bx0) * s); h = _num((by1 - by0) * s)
    if kind == 'plate':
        field = [('rect', _num(-w / 2), _num(-h / 2), _num(w / 2), _num(h / 2))]
    elif kind == 'warn':
        field = []  # render.WARN_FIELD is set for these keys in render.py
    else:
        field = [FIELD[kind]]
    plate = {'w': w, 'h': h, 'rx': 0.0, 'plate': None, 'layers': layers, 'text': text_out,
             'over': [], 'fields': field if text_out else [], 'kind': kind}
    return paths, plate, notes


def detect_kind(sign, sil, family=''):
    ys, xs = np.where(sil > 0)
    bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    fr = sil.sum() / float(bw * bh)
    lab = classify(sign, family)
    k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edge = (sil > 0) & (cv2.erode(sil, k3, iterations=3) == 0)
    ev, ec = np.unique(lab[edge], return_counts=True)
    ecol = ev[np.argmax(ec)] if len(ev) else ''
    sq = 0.85 < bw / bh < 1.18
    if sq and 0.74 < fr < 0.83:
        if ecol == 'red':
            return 'proh'
        if ecol in ('blue', 'motorway'):
            return 'mand'
    # apex-up triangle: top rows narrow
    top = sil[ys.min():ys.min() + max(2, bh // 10)].sum(1).max() / bw
    if 0.42 < fr < 0.6 and top < 0.35 and ecol == 'red' and 1.0 < bw / bh < 1.25:
        return 'warn'
    return 'plate'

def isolate_frame(img):
    """Framed plate (thin border fails isolate()'s area test, e.g. 651): the largest
    component not touching the crop edge is the border; silhouette = its convex hull."""
    a = np.array(img.convert('RGB'))
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    ink = ((hsv[..., 2] < 200) | (hsv[..., 1] > 60)).astype(np.uint8)
    n, L, st, _ = cv2.connectedComponentsWithStats(ink, 8)
    cands = [i for i in range(1, n) if st[i, 0] > 0 and st[i, 1] > 0 and st[i, 0] + st[i, 2] < a.shape[1] and st[i, 1] + st[i, 3] < a.shape[0]]
    f = max(cands, key=lambda i: st[i, 2] * st[i, 3]); x, y, w, h = st[f, :4]
    cs, _ = cv2.findContours((L == f).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(max(cs, key=len))
    sil = np.zeros_like(ink); cv2.fillConvexPoly(sil, hull, 1)
    p = 2
    return a[y - p:y + h + p, x - p:x + w + p].copy(), sil[y - p:y + h + p, x - p:x + w + p]
