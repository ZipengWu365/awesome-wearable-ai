#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
import re
import subprocess

from registry import ROOT, derive_relations, load_records, load_watchlist


def normalize_output(output: str) -> str:
    output = re.sub(r"Ran (\d+) tests in [0-9.]+s", r"Ran \1 tests", output)
    output = re.sub(
        r"(?m)^(test\w+) \(([^()\n]+)\.\1\)( \.\.\. .*)$",
        r"\1 (\2)\3",
        output,
    )
    return output.strip()


def run(command: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", capture_output=True)
    return proc.returncode == 0, normalize_output(proc.stdout + proc.stderr)


def duplicates(records: list[dict], field: str) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for record in records:
        value = record.get(field)
        if not value:
            continue
        key = " ".join(str(value).lower().strip().rstrip("/").split())
        grouped[key].append(record["id"])
    return {key: ids for key, ids in grouped.items() if len(ids) > 1}


def main() -> int:
    records = load_records()
    watchlist = load_watchlist()
    relations = derive_relations(records)
    checks = []
    for name, command in (
        ("registry validation", ["python", "scripts/validate_registry.py"]),
        ("unit tests", ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("internal links", ["python", "scripts/internal_link_check.py"]),
    ):
        ok, output = run(command)
        checks.append((name, ok, output))
    decision = "PASS" if all(ok for _, ok, _ in checks) else "FAIL"
    type_counts = Counter(record["record_type"] for record in records)
    verification = Counter(record["verification_status"] for record in records)
    depth_counts = Counter(record["evidence_depth"] for record in records)
    tier_counts = Counter(record["venue_tier"] for record in records)
    model_families = Counter(record["family"] for record in records if record["record_type"] == "model")
    negative_interventions = sum(
        bool(record.get("negative_or_null_result"))
        for record in records if record["record_type"] == "intervention"
    )
    title_dupes = duplicates(records, "title")
    url_dupes = duplicates(records, "primary_url")
    lines = [
        "# Awesome Wearable AI current repository audit",
        "",
        f"**Decision: {decision}**",
        "",
        "## Inventory",
        "",
        f"- Accepted records: **{len(records)}**",
        f"- Watchlist records: **{len(watchlist)}**",
        f"- Derived and explicit relations: **{len(relations)}**",
        f"- Negative, null or materially mixed intervention records: **{negative_interventions}**",
        f"- Exact duplicate accepted titles: **{len(title_dupes)}**",
        f"- Reused primary URLs: **{len(url_dupes)}** (permitted for parent/subset resources; listed below)",
        "",
        "### Accepted records by type",
        "",
    ]
    for key, value in sorted(type_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Model families", ""])
    for key, value in sorted(model_families.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Venue/source tiers", ""])
    for key, value in sorted(tier_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Verification levels", ""])
    for key, value in sorted(verification.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Evidence-depth levels", ""])
    for key, value in sorted(depth_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Reused primary URLs", ""])
    if not url_dupes:
        lines.append("- None")
    else:
        for url, ids in sorted(url_dupes.items()):
            lines.append(f"- `{url}`: {', '.join(ids)}")
    lines.extend(["", "## Automated checks", ""])
    for name, ok, output in checks:
        lines.extend([f"### {'PASS' if ok else 'FAIL'} — {name}", "", "```text", output or "(no output)", "```", ""])
    lines.extend([
        "## Scientific limitations",
        "",
        "- The atlas is a quality-screened scoping registry, not a PRISMA systematic review and not an exhaustive census.",
        "- Venue/source screening removes many weak or unresolved items but does not substitute for study-level risk-of-bias assessment.",
        "- `venue_verified` records are bibliography-grade index entries; their full methods and results have not been independently appraised in this release.",
        "- `metadata_verified` records have checked core metadata but may still lack effect-size, subgroup, calibration or transportability extraction.",
        "- Dataset, standard and tool entries enter through canonical-resource criteria rather than publication prestige.",
        "- Protocols are labelled as protocols and do not count as effectiveness evidence.",
        "- Predictive counterfactual explanations are separated from causal treatment effects and policy-value evidence.",
        "- A model's inclusion does not imply that its weights, training data or commercial use rights are open.",
        "- Original catalogue snapshot: 2026-09-02. The 2026-09-28 local integration retains per-source review dates; see LOCAL_SYNC.md.",
    ])
    report = "\n".join(lines) + "\n"
    path = ROOT / "docs" / "RELEASE_AUDIT.md"
    path.write_text(report, encoding="utf-8")
    print(f"Audit written to {path.relative_to(ROOT)}: {decision}")
    return 0 if decision == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
