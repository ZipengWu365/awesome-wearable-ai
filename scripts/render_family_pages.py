#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict

from registry import ROOT, load_records, slugify

OUT = ROOT / "generated" / "families"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    grouped = defaultdict(list)
    for record in load_records():
        grouped[record["family"]].append(record)
    index = ["# Family index", "", "| Family | Count |", "|---|---:|"]
    for family, rows in sorted(grouped.items()):
        filename = slugify(family) + ".md"
        index.append(f"| [{family}]({filename}) | {len(rows)} |")
        lines = [f"# {family}", "", f"Accepted records: **{len(rows)}**", ""]
        for row in sorted(rows, key=lambda item: (-int(item["year"]), item["title"].lower())):
            lines.extend([
                f"## [{row['title']}]({row['primary_url']})",
                "",
                f"- **Year / source:** {row['year']} · {row['venue']} · `{row['venue_tier']}`",
                f"- **Type / stage:** `{row['record_type']}` · `{row['lifecycle_stage']}` · `{row['evidence_stage']}`",
                f"- **Contribution:** {row['contribution']}",
                f"- **Why it matters:** {row['why_it_matters']}",
                f"- **Limitations:** {row['limitations']}",
                f"- **Evidence boundary:** {row['evidence_boundary']}",
                f"- **Verification:** `{row['verification_status']}` on {row['verified_on']}",
                "",
            ])
        (OUT / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"Rendered {len(grouped)} family pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
