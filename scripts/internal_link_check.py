#!/usr/bin/env python3
from __future__ import annotations

import re
import sys

from registry import ROOT

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP = ("http://", "https://", "mailto:", "#")


def main() -> int:
    errors: list[str] = []
    paths = list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md"))
    family_dir = ROOT / "generated" / "families"
    if family_dir.exists():
        paths += list(family_dir.glob("*.md"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(SKIP):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)} -> {target}")
    if errors:
        print("Internal link check FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Internal Markdown links OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
