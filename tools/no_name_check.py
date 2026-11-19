#!/usr/bin/env python3
"""Fail if the owner's personal name (any tracked file, path or content) or an absolute
machine path (tracked text files; justified allow-list) appears.

    python3 tools/no_name_check.py

Case-insensitive search over every file from `git ls-files` (falls back to walking the
tree when not in a git checkout). Matches are printed masked, so the output never
repeats the name. ALLOW lists genuine non-name words, each with a justification.
"""
from __future__ import annotations
import os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAT = re.compile(("p" "hil") + "|" + ("rob" "inson"), re.I)
ALLOW: dict[str, str] = {}  # word -> justification; empty: nothing needed

# Absolute machine paths (build-box working folders, scratch, home directories).
PATH_PAT = re.compile(r"(?<![\w.~-])/(?:" + "work" + "space|" + "tm" + "p|" + "ho" + "me" + r")(?:/|\b)")
# Files allowed to keep such paths, with the reason. Only historical QA working notes:
# they record where past rounds ran, are not used by any tool, and are left out of the
# public snapshot (see SNAPSHOT.md there).
PATH_ALLOW_FILES: dict[str, str] = {
    f: "historical QA working note (process record; excluded from the public snapshot)"
    for f in ("qa/HANDOFF-b1.md", "qa/HANDOFF-b3.md", "qa/HANDOFF-fix-622.8.md", "qa/HANDOFF-fix-b2b3.md",
              "qa/HANDOFF-r1.md", "qa/HANDOFF-r2.md", "qa/HANDOFF-r3.md", "qa/HANDOFF-r6.md",
              "qa/HANDOFF-r7.md", "qa/HANDOFF-r8.md", "qa/RESUME-THURSDAY.md", "qa/ROTATION-AUDIT.md")
}


def files() -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
        fs = [f for f in out.decode().split("\0") if f]
        if fs:
            return sorted(fs)
    except (OSError, subprocess.CalledProcessError):
        pass
    return sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts)


def scan() -> tuple[int, list[tuple[str, str]]]:
    hits, fs = [], files()
    for f in fs:
        if PAT.search(f):
            hits.append((PAT.sub("***", f), "path"))
        p = ROOT / f
        if not p.is_file():
            continue
        t = p.read_bytes().decode("latin-1")
        for m in PAT.finditer(t):
            w = re.search(r"\w*$", t[: m.start()]).group(0) + m.group(0) + re.match(r"\w*", t[m.end():]).group(0)
            if w.lower() not in ALLOW:
                hits.append((f, w[:1] + "*" * (len(w) - 1)))
    return len(fs), hits


def scan_paths() -> tuple[int, list[tuple[str, str]], int]:
    """Absolute machine paths in tracked text files (binary files are skipped)."""
    hits, fs, allowed = [], files(), 0
    for f in fs:
        p = ROOT / f
        if not p.is_file():
            continue
        b = p.read_bytes()
        if b"\0" in b[:8192]:
            continue
        t = b.decode("utf-8", "replace")
        found = [t[m.start(): m.start() + 24].split()[0] for m in PATH_PAT.finditer(t)]
        if not found:
            continue
        if f in PATH_ALLOW_FILES:
            allowed += 1
            continue
        hits += [(f, x) for x in found]
    return len(fs), hits, allowed


def main() -> int:
    n, hits = scan()
    print("no-name: %d tracked files scanned, %d matches%s; allow-list %s"
          % (n, len(hits), (" " + repr(hits[:10])) if hits else "", sorted(ALLOW) or "empty"))
    n2, phits, allowed = scan_paths()
    present = sum(1 for f in PATH_ALLOW_FILES if (ROOT / f).is_file())
    print("abs-paths: %d tracked files scanned, %d matches%s; %d allow-listed files present (of %d listed), %d of them contain paths"
          % (n2, len(phits), (" " + repr(phits[:10])) if phits else "", present, len(PATH_ALLOW_FILES), allowed))
    return 1 if hits or phits else 0


if __name__ == "__main__":
    sys.exit(main())
