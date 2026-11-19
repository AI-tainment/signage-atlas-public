"""Minimal in-place patcher for tools/atlas/traced.py (keeps order/format)."""
import re, pathlib
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); import paths as _P
T = _P.TRACED

def _fmt_path(key, d):
    chunks = [d[i:i+100] for i in range(0, len(d), 100)]
    body = ''.join(f"        {c!r}\n" for c in chunks)
    return f"    {key!r}: (\n{body}    ),\n"

def _span(src, name):
    i = src.index(f"\n{name}: dict")
    j = src.index("\n}\n", i) + 1  # index of closing '}' line start
    return i, j

def set_path(src, key, d):
    i, j = _span(src, 'PATHS')
    new = _fmt_path(key, d)
    m = re.compile(r"    " + re.escape(repr(key)) + r": \(\n(?:        .*\n)*?    \),\n").search(src, i, j)
    if m: return src[:m.start()] + new + src[m.end():]
    return src[:j] + new + src[j:]

def set_source(src, key, s):
    i, j = _span(src, 'SOURCE')
    new = f"    {key!r}: {s!r},\n"
    m = re.compile(r"    " + re.escape(repr(key)) + r": .*\n").search(src, i, j)
    if m: return src[:m.start()] + new + src[m.end():]
    return src[:j] + new + src[j:]

def set_entries(paths: dict, sources: dict):
    src = T.read_text()
    for k, d in paths.items(): src = set_path(src, k, d)
    for k, s in sources.items(): src = set_source(src, k, s)
    T.write_text(src)

def del_paths(src, prefix):
    i, j = _span(src, 'PATHS')
    rx = re.compile(r"    '" + re.escape(prefix) + r"/\d+': \(\n(?:        .*\n)*?    \),\n")
    head, mid, tail = src[:i], src[i:j], src[j:]
    mid = rx.sub('', mid)
    return head + mid + tail
