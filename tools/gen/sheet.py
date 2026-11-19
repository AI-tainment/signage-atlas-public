"""Contact sheet via one headless-chrome screenshot.
usage: sheet.py out.png title rows.json   rows: [[label, [img paths...]], ...]  (svg or png)"""
import sys, json, subprocess, tempfile, os, html
out, title, rows = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
cell = int(os.environ.get('CELL', 150))
ncol = max(len(r[1]) for r in rows)
per = int(os.environ.get('PER', 1))  # rows of entries side by side
H = ["<html><body style='margin:0;background:#fff;font:12px sans-serif'>",
     f"<div style='padding:4px;font-weight:bold'>{html.escape(title)}</div><div style='display:flex;flex-wrap:wrap'>"]
for lab, imgs in rows:
    H.append(f"<div style='display:flex;align-items:center;border:1px solid #ccc;margin:2px'><div style='width:70px;padding:2px'>{html.escape(lab)}</div>")
    for p in imgs:
        if p: H.append(f"<img src='file://{os.path.abspath(p)}' style='width:{cell}px;height:{cell}px;object-fit:contain;background:#ddd;margin:2px'>")
        else: H.append(f"<div style='width:{cell}px;height:{cell}px;margin:2px'></div>")
    H.append("</div>")
H.append("</div></body></html>")
w = per * (80 + ncol * (cell + 6)) + 20
n = (len(rows) + per - 1) // per
h = 30 + n * (cell + 8) + 20
f = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False); f.write(''.join(H)); f.close()
subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                f'--window-size={w},{h}', f'--screenshot={os.path.abspath(out)}', 'file://' + f.name],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.unlink(f.name); print(out, w, h)
