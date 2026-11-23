#!/usr/bin/env python3
"""Publish-time attribution check for EPS-derived (Crown copyright) artwork (r12, Reviewer r1 F8).

usage: python3 tools/eps/deploy_guard.py <dir-about-to-be-published>

The owner ruled (r12) that faces converted from the GOV.UK EPS may be published with attribution and an
OGL v3.0 citation. This check fails (exit 1) when any SVG converted from EPS (data-source="eps") in the
tree lacks the embedded Crown copyright / OGL v3.0 <desc> (tools/eps/convert.py ATTRIBUTION), or when
a site/faces-eps/ folder is published without its README.txt notice. It does not block publishing.
"""
from __future__ import annotations

import sys
from pathlib import Path


def scan(root: Path) -> tuple[list[str], list[str]]:
    eps, bare = [], []
    for p in sorted(root.rglob("*")):
        if p.is_dir() and p.name == "faces-eps":
            eps.append(str(p.relative_to(root)) + "/")
        elif p.suffix.lower() == ".svg" and p.is_file():
            b = p.read_bytes()
            if b'data-source="eps"' in b:
                eps.append(str(p.relative_to(root)))
                if b"<desc>Crown copyright" not in b:
                    bare.append(str(p.relative_to(root)))
    return eps, bare


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    root = Path(argv[0])
    eps, bare = scan(root)
    dirs = [root / e for e in eps if e.endswith("/")]
    no_readme = [str(d.relative_to(root)) for d in dirs if not any(d.rglob("README.txt"))]
    if bare or no_readme:
        print(f"deploy-guard: FAIL: {len(bare)} EPS SVG(s) without the Crown copyright / OGL v3.0 notice"
              f"{', e.g. ' + str(bare[:3]) if bare else ''}; {len(no_readme)} faces-eps folder(s) without README.txt")
        return 1
    print(f"deploy-guard: ok ({len(eps) - len(dirs)} EPS SVG(s), all attributed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
