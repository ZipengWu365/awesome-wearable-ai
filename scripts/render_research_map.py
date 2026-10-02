#!/usr/bin/env python3
"""Rebuild the selected research overview without changing the full registry."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "research-map"


def main() -> int:
    source = json.loads((ASSETS / "milestones.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((ASSETS / "taxonomy.json").read_text(encoding="utf-8"))
    records = {record["id"]: record for record in source["milestones"]}
    data = []
    for role in taxonomy["roles"]:
        for route in role["routes"]:
            for entry in route["web_records"]:
                record = records[entry["id"]]
                if record["branch"] != route["id"]:
                    raise ValueError(f"Route mismatch for {entry['id']}")
                data.append({
                    "id": record["id"], "name": entry["label"],
                    "branch": record["branch"], "year": record["year"],
                    "caption": record["caption"], "venue": record["venue"],
                    "url": record["url"],
                })
    if len(data) != taxonomy["web_milestone_count"] or len({r["id"] for r in data}) != len(data):
        raise ValueError("Web selection count or uniqueness mismatch")
    if any(len(record["name"]) > 19 for record in data):
        raise ValueError("Compact labels must contain at most 19 characters")
    template = (ASSETS / "compact-map-source.html").read_text(encoding="utf-8")
    if template.count("__RESEARCH_DATA__") != 1:
        raise ValueError("Expected exactly one research-data placeholder")
    encoded = json.dumps(data, ensure_ascii=True).replace("<", "\\u003c")
    output = template.replace("__RESEARCH_DATA__", encoded)
    (ROOT / "site" / "research-map.html").write_text(output, encoding="utf-8")
    print(f"Research overview rendered: {len(data)} selected milestones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
