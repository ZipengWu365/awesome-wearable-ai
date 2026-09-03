#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import csv
import json

from registry import (
    ROOT,
    derive_relations,
    family_counts,
    flatten,
    load_concepts,
    load_records,
    load_venues,
    load_watchlist,
    public_record,
    record_counts,
    verification_counts,
    evidence_depth_counts,
    venue_tier_counts,
)

OUT = ROOT / "generated"
OUT.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict]) -> None:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: flatten(row.get(key)) for key in keys})


def main() -> int:
    records = [public_record(record) for record in load_records()]
    watchlist = load_watchlist()
    relations = derive_relations(records)
    statistics = {
        "accepted_total": len(records),
        "watchlist_total": len(watchlist),
        "relation_total": len(relations),
        "by_record_type": record_counts(records),
        "by_family": family_counts(records),
        "by_venue_tier": venue_tier_counts(records),
        "by_verification_status": verification_counts(records),
        "by_evidence_depth": evidence_depth_counts(records),
        "by_year": dict(sorted(Counter(str(record["year"]) for record in records).items())),
    }
    registry = {
        "version": "0.3.0",
        "generated_on": "2026-09-02",
        "records": records,
        "watchlist": watchlist,
        "relations": relations,
        "statistics": statistics,
        "concepts": load_concepts(),
        "venues": list(load_venues().values()),
    }
    (OUT / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "statistics.json").write_text(json.dumps(statistics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(OUT / "catalog.csv", records)
    write_csv(OUT / "watchlist.csv", watchlist)
    write_csv(OUT / "relations.csv", relations)
    print(f"Exported {len(records)} accepted records, {len(watchlist)} watchlist records, {len(relations)} relations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
