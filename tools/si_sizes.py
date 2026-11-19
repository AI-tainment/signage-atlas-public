#!/usr/bin/env python3
"""D1: pull permitted sign sizes out of the SI 2016/362 (TSRGD 2016) XML.

Only two sign tables in the regulations carry a size column:
  Sch 3 Pt 2 col 4 "Sign diameter" and Sch 9 Pt 2 col 4 "Permitted sizes".
Every other sign table has no size column, so those diagrams are recorded
as not tabulated rather than given a guessed size.

usage: tools/si_sizes.py SI_XML  > countries/uk/sources/si2016_sizes.json
"""
import json, re, sys
import xml.etree.ElementTree as ET

NS = "{http://www.legislation.gov.uk/namespaces/legislation}"


def paras(el):
    out = []
    for p in el.iter(NS + "Para"):
        t = re.sub(r"\s+", " ", "".join(p.itertext())).strip()
        if t:
            out.append(t)
    if not out:
        t = re.sub(r"\s+", " ", "".join(el.itertext())).strip()
        if t:
            out.append(t)
    return out


def caption_before(xml_text: str, table_pos: int) -> str:
    pre = re.sub(r"<[^>]+>", " ", xml_text[max(0, table_pos - 4000):table_pos])
    m = re.findall(r"Sign table\s*[—–-]\s*Schedule (\d+), Part (\d+)", pre)
    return f"Sch {m[-1][0]} Pt {m[-1][1]}" if m else "?"


def main(path: str) -> dict:
    text = open(path, encoding="utf8").read()
    root = ET.fromstring(text)
    theads = [m.start() for m in re.finditer(r"<(?:\w+:)?thead\b", text)]
    out = {}
    for ti, thead in enumerate(t for t in root.iter() if t.tag.endswith("thead")):
        tbl = next(t for t in root.iter() if t.tag.endswith("table") and thead in list(t.iter()))
        heads = [" ".join(paras(th)) for th in thead.iter() if th.tag.endswith("th")]
        col = next((i for i, h in enumerate(heads) if "Sign diameter" in h or "Permitted sizes" in h), None)
        if col is None:
            continue
        ref = caption_before(text, theads[ti]) + f" col {col + 1}"
        for tr in tbl.iter():
            if not tr.tag.endswith("tr"):
                continue
            tds = [c for c in tr if c.tag.endswith("td")]
            if len(tds) <= col:
                continue
            dp = [t for t in paras(tds[1]) if re.match(r"Diagrams? ", t)]
            if not dp:
                continue
            ids = re.findall(r"\d+(?:\.\d+)?[A-Z]?", dp[0].split("(")[0])
            cell = paras(tds[col])
            nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", cell[-1])]
            label = " ".join(cell[:-1]).rstrip(":").strip().lower()
            dim = "diameter" if "diameter" in heads[col].lower() else (label or "size")
            for d in ids:
                e = {"dim": dim, "mm": [int(n) if n.is_integer() else n for n in nums],
                     "ref": ref, "item": paras(tds[0])[0], "cell": " / ".join(cell)}
                if d in out and out[d]["mm"] != e["mm"]:
                    raise SystemExit(f"{d}: two different size rows")
                out.setdefault(d, e)
    return {
        "_meta": {
            "source": "The Traffic Signs Regulations and General Directions 2016 (SI 2016/362), "
                      "revised XML, legislation.gov.uk",
            "tables_with_size_column": sorted({v["ref"] for v in out.values()}),
            "note": "No other sign table in SI 2016 has a size column; diagrams absent here are "
                    "'not tabulated' (sizes, if any, are only in the diagram drawings).",
        },
        "sizes": dict(sorted(out.items())),
    }


if __name__ == "__main__":
    json.dump(main(sys.argv[1]), sys.stdout, indent=1, sort_keys=False, ensure_ascii=False)
    sys.stdout.write("\n")
