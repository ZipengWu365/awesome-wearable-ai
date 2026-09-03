#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

from jsonschema import Draft202012Validator

from registry import ROOT, RECORD_DIR, RECORD_FILES, WATCHLIST, load_yaml, load_records, load_watchlist, load_venues

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
SCIENTIFIC_BASES = {"peer_reviewed_publication", "big_tech_official_report"}
ALLOWED_SCIENTIFIC_TIERS = {"top_conference", "domain_leading_conference", "sci_journal", "big_tech_report"}


def validate_url(value: str, location: str, errors: list[str]) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append(f"{location}: invalid URL {value!r}")


def schema_errors(path: Path, schema: dict) -> list[str]:
    rows = load_yaml(path) or []
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    if not isinstance(rows, list):
        return [f"{path.relative_to(ROOT)}: top-level value must be a list"]
    for index, row in enumerate(rows):
        record_id = row.get("id", "no-id") if isinstance(row, dict) else "no-id"
        for error in sorted(validator.iter_errors(row), key=lambda err: list(err.path)):
            location = ".".join(str(x) for x in error.path) or "<root>"
            errors.append(f"{path.relative_to(ROOT)}[{index}] ({record_id}).{location}: {error.message}")
    return errors


def main() -> int:
    errors: list[str] = []
    schema = json.loads((ROOT / "schema" / "record.schema.json").read_text(encoding="utf-8"))
    for name in RECORD_FILES:
        errors.extend(schema_errors(RECORD_DIR / name, schema))
    errors.extend(schema_errors(WATCHLIST, json.loads((ROOT / "schema" / "watchlist.schema.json").read_text(encoding="utf-8"))))

    records = load_records()
    watchlist = load_watchlist()
    venues = load_venues()
    seen: dict[str, str] = {}
    seen_titles: dict[str, str] = {}
    accepted_ids = {record["id"] for record in records}

    for record in records:
        record_id = record["id"]
        source_file = record["_source_file"]
        if record_id in seen:
            errors.append(f"duplicate accepted id {record_id!r}: {seen[record_id]} and {source_file}")
        seen[record_id] = source_file
        normalized_title = re.sub(r"\s+", " ", record["title"].strip().lower())
        if normalized_title in seen_titles:
            errors.append(f"duplicate accepted title {record['title']!r}: {seen_titles[normalized_title]} and {record_id}")
        seen_titles[normalized_title] = record_id
        if not ID_PATTERN.fullmatch(record_id):
            errors.append(f"{record_id}: id must match {ID_PATTERN.pattern}")
        for field in ("primary_url", "code_url", "data_url", "project_url"):
            if record.get(field):
                validate_url(str(record[field]), f"{record_id}.{field}", errors)
        if record["inclusion_basis"] in SCIENTIFIC_BASES:
            if record["venue_tier"] not in ALLOWED_SCIENTIFIC_TIERS:
                errors.append(f"{record_id}: scientific record has disallowed venue_tier {record['venue_tier']!r}")
            if record["inclusion_basis"] == "peer_reviewed_publication":
                if record["venue"] not in venues:
                    errors.append(f"{record_id}: peer-reviewed venue {record['venue']!r} absent from data/venues.yaml")
                elif venues[record["venue"]]["tier"] != record["venue_tier"]:
                    errors.append(f"{record_id}: venue_tier {record['venue_tier']!r} disagrees with policy tier {venues[record['venue']]['tier']!r}")
        if record["inclusion_basis"] == "big_tech_official_report" and record["venue_tier"] != "big_tech_report":
            errors.append(f"{record_id}: big-tech report must use venue_tier=big_tech_report")
        if (record["inclusion_basis"] == "peer_reviewed_publication"
                and record["verification_status"] == "primary_source_checked"
                and urlparse(record["primary_url"]).netloc.lower().endswith("arxiv.org")):
            errors.append(f"{record_id}: arXiv-linked peer-reviewed record cannot be labelled primary_source_checked")
        for related_id in record.get("related_ids", []) or []:
            if related_id not in accepted_ids:
                errors.append(f"{record_id}: related_ids contains unknown accepted record {related_id!r}")

    accepted_titles = {re.sub(r"\s+", " ", record["title"].strip().lower()): record["id"] for record in records}
    for item in watchlist:
        record_id = item["id"]
        if record_id in accepted_ids:
            errors.append(f"watchlist id {record_id!r} duplicates an accepted record")
        normalized_watch_title = re.sub(r"\s+", " ", item["title"].strip().lower())
        if normalized_watch_title in accepted_titles:
            errors.append(f"watchlist title {item['title']!r} duplicates accepted record {accepted_titles[normalized_watch_title]}")
        if not ID_PATTERN.fullmatch(record_id):
            errors.append(f"watchlist {record_id}: invalid id")
        validate_url(item["primary_url"], f"watchlist.{record_id}.primary_url", errors)

    if errors:
        print("Registry validation FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(records)} accepted records, {len(watchlist)} watchlist records, "
        f"{len(venues)} venue-policy entries validated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
