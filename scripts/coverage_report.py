#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import json

from registry import ROOT, load_records, load_watchlist


def main() -> int:
    records = load_records()
    watchlist = load_watchlist()
    dimensions = {
        "record_type": Counter(record["record_type"] for record in records),
        "family": Counter(record["family"] for record in records),
        "modality": Counter(item for record in records for item in record.get("modalities", [])),
        "clinical_domain": Counter(item for record in records for item in record.get("clinical_domains", [])),
        "evidence_stage": Counter(record["evidence_stage"] for record in records),
        "causal_status": Counter(record["causal_status"] for record in records),
        "verification_status": Counter(record["verification_status"] for record in records),
    }
    payload = {key: dict(sorted(counter.items())) for key, counter in dimensions.items()}
    payload["accepted_total"] = len(records)
    payload["watchlist_total"] = len(watchlist)
    (ROOT / "generated" / "coverage.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Coverage report",
        "",
        "> Generated from the accepted registry. Counts describe coverage, not scientific importance.",
        "",
        f"- Accepted records: **{len(records)}**",
        f"- Watchlist records: **{len(watchlist)}**",
        "",
    ]
    for name, counter in dimensions.items():
        lines += [f"## {name.replace('_', ' ').title()}", "", "| Value | Count |", "|---|---:|"]
        for value, count in counter.most_common():
            lines.append(f"| {value} | {count} |")
        lines.append("")
    lines += [
        "## Interpretation limits",
        "",
        "- A large count can reflect mature infrastructure or a broad source family; it does not imply stronger evidence.",
        "- Dataset and standard records enter through canonical-resource rules rather than publication-venue rules.",
        "- Watchlist items are deliberately excluded from headline counts until venue, publication status, or source metadata is resolved.",
    ]
    (ROOT / "generated" / "coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Coverage report generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
