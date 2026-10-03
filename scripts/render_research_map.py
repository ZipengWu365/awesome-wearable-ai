#!/usr/bin/env python3
"""Render the full registry map and its reproducible coverage manifest."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "research-map"
REGISTRY_PATH = ROOT / "generated" / "registry.json"
PLACEHOLDER = "__RESEARCH_DATA__"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_issues() -> dict:
    """Keep existing source warnings separate from the unmodified registry."""
    return read_json(ASSETS / "milestones.json").get("known_source_issues", {})


def build_bins(years: list) -> list:
    if not years or any(type(year) is not int or year < 1 for year in years):
        raise ValueError("Every record must have a valid integer publication year")
    earliest = min(1980, min(years))
    latest = max(2026, max(years))
    bins = [
        {"id": "pre2010", "label": f"{earliest}\u20132009", "start": earliest, "end": 2009},
        {"id": "2010-2014", "label": "2010\u20132014", "start": 2010, "end": 2014},
    ]
    bins.extend(
        {"id": str(year), "label": str(year), "start": year, "end": year}
        for year in range(2015, latest + 1)
    )
    return bins


def bin_for_year(year: int, bins: list) -> str:
    matches = [item["id"] for item in bins if item["start"] <= year <= item["end"]]
    if len(matches) != 1:
        raise ValueError(f"Publication year {year} must map to exactly one time bin")
    return matches[0]


def build_payload(registry: dict = None, issues: dict = None) -> dict:
    """Retain every original field and add only map-specific classification."""
    if registry is None:
        registry = read_json(REGISTRY_PATH)
    if issues is None:
        issues = load_issues()
    taxonomy = read_json(ASSETS / "taxonomy.json")
    branches = copy.deepcopy(taxonomy["branches"])
    accepted_types = {branch["id"] for branch in branches if branch["id"] != "watchlist"}
    originals = list(registry["records"]) + list(registry["watchlist"])
    ids = [record["id"] for record in originals]
    if any(not isinstance(record_id, str) or not record_id for record_id in ids):
        raise ValueError("Every registry record must have a nonempty string ID")
    if len(ids) != len(set(ids)):
        raise ValueError("Registry IDs must be unique across accepted records and watchlist")
    bins = build_bins([record["year"] for record in originals])
    mapped = []
    for status, original_records in (("accepted", registry["records"]), ("watchlist", registry["watchlist"])):
        for original in original_records:
            branch = original["record_type"] if status == "accepted" else "watchlist"
            if status == "accepted" and branch not in accepted_types:
                raise ValueError(f"Unknown accepted record type {branch!r} for {original['id']}")
            family = original.get("family") or original.get("proposed_family")
            if not isinstance(family, str) or not family:
                raise ValueError(f"Missing research family for {original['id']}")
            additions = {
                "catalog_status": status,
                "branch": branch,
                "family": family,
                "bin": bin_for_year(original["year"], bins),
            }
            if original["id"] in issues:
                additions["source_issue"] = issues[original["id"]]
                additions["link_withheld"] = True
            for key, value in additions.items():
                if key in original and original[key] != value:
                    raise ValueError(f"Map metadata would overwrite original field {key!r} for {original['id']}")
            record = copy.deepcopy(original)
            record.update(additions)
            mapped.append(record)
    return {
        "cutoff": registry["generated_on"],
        "version": registry["version"],
        "branches": branches,
        "bins": bins,
        "records": mapped,
        "counts": {
            "accepted": len(registry["records"]),
            "watchlist": len(registry["watchlist"]),
            "by_type": {
                branch["id"]: sum(record["record_type"] == branch["id"] for record in registry["records"])
                for branch in branches if branch["id"] != "watchlist"
            },
        },
    }


def build_coverage(registry: dict, payload: dict) -> dict:
    """Produce an ID-by-ID assignment ledger, failing instead of omitting rows."""
    accepted_ids = sorted(record["id"] for record in registry["records"])
    watchlist_ids = sorted(record["id"] for record in registry["watchlist"])
    expected = accepted_ids + watchlist_ids
    original_by_id = {record["id"]: record for record in registry["records"] + registry["watchlist"]}
    if len(expected) != len(original_by_id):
        raise ValueError("Source registry IDs must be unique")
    assigned = [record["id"] for record in payload["records"]]
    duplicates = sorted(record_id for record_id, count in Counter(assigned).items() if count > 1)
    omitted = sorted(set(expected) - set(assigned))
    unexpected = sorted(set(assigned) - set(expected))
    if duplicates or omitted or unexpected:
        raise ValueError("Coverage must contain every registry ID exactly once")
    expected_counts = {
        "accepted": len(accepted_ids),
        "watchlist": len(watchlist_ids),
        "by_type": {
            branch["id"]: sum(record["record_type"] == branch["id"] for record in registry["records"])
            for branch in payload["branches"] if branch["id"] != "watchlist"
        },
    }
    if payload["counts"] != expected_counts:
        raise ValueError("Coverage counts must equal source registry counts")
    if payload["cutoff"] != registry["generated_on"] or payload["version"] != registry["version"]:
        raise ValueError("Coverage version and cutoff must match the source registry")
    mappings = []
    for record in sorted(payload["records"], key=lambda item: item["id"]):
        original = original_by_id[record["id"]]
        for field, value in original.items():
            if record.get(field) != value:
                raise ValueError(f"Original metadata changed for {record['id']}: {field}")
        if record["branch"] not in {branch["id"] for branch in payload["branches"]}:
            raise ValueError(f"Unassigned branch for {record['id']}")
        if record["bin"] != bin_for_year(record["year"], payload["bins"]):
            raise ValueError(f"Incorrect time bin for {record['id']}")
        expected_status = "accepted" if record["id"] in accepted_ids else "watchlist"
        if record["catalog_status"] != expected_status:
            raise ValueError(f"Incorrect catalog status for {record['id']}")
        expected_branch = original["record_type"] if expected_status == "accepted" else "watchlist"
        expected_family = original.get("family") or original.get("proposed_family")
        if record["branch"] != expected_branch or record["family"] != expected_family:
            raise ValueError(f"Incorrect native classification for {record['id']}")
        mapping = {key: record[key] for key in ("id", "branch", "year", "bin", "family", "catalog_status")}
        if record.get("source_issue"):
            mapping.update(source_issue=record["source_issue"], link_withheld=record["link_withheld"])
        mappings.append(mapping)
    canonical_source = json.dumps(registry, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return {
        "status": "complete registry coverage",
        "source_registry": "../../generated/registry.json",
        "source_sha256": hashlib.sha256(canonical_source.encode("utf-8")).hexdigest(),
        "cutoff": payload["cutoff"],
        "version": payload["version"],
        "counts": copy.deepcopy(payload["counts"]),
        "mapped_total": len(mappings),
        "unassigned_ids": [],
        "omitted_ids": omitted,
        "unexpected_ids": unexpected,
        "duplicate_ids": duplicates,
        "accepted_ids": accepted_ids,
        "watchlist_ids": watchlist_ids,
        "branches": copy.deepcopy(payload["branches"]),
        "bins": copy.deepcopy(payload["bins"]),
        "records": mappings,
    }


def render_template(template: str, payload: dict) -> str:
    if template.count(PLACEHOLDER) != 1:
        raise ValueError("Expected exactly one research-data placeholder")
    encoded = json.dumps(payload, ensure_ascii=True).replace("<", "\\u003c")
    return template.replace(PLACEHOLDER, encoded)


def main() -> int:
    registry = read_json(REGISTRY_PATH)
    payload = build_payload(registry)
    coverage = build_coverage(registry, payload)
    template = (ASSETS / "compact-map-source.html").read_text(encoding="utf-8")
    output = render_template(template, payload)
    (ROOT / "site" / "research-map.html").write_text(output, encoding="utf-8")
    (ASSETS / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = payload["counts"]
    print(f"Research map rendered: {counts['accepted']} accepted + {counts['watchlist']} watchlist records; no omissions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
