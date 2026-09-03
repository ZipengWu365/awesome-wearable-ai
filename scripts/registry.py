#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
RECORD_DIR = ROOT / "data" / "records"
WATCHLIST = ROOT / "data" / "excluded" / "watchlist.yaml"

RECORD_FILES = (
    "models.yaml",
    "datasets.yaml",
    "methods.yaml",
    "interventions.yaml",
    "measures.yaml",
    "infrastructure.yaml",
)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(value: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in RECORD_FILES:
        path = RECORD_DIR / name
        data = load_yaml(path) or []
        if not isinstance(data, list):
            raise TypeError(f"{path} must contain a top-level list")
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(f"{path} contains a non-object record")
            item = dict(item)
            item["_source_file"] = str(path.relative_to(ROOT))
            records.append(item)
    return records


def load_watchlist() -> list[dict[str, Any]]:
    if not WATCHLIST.exists():
        return []
    data = load_yaml(WATCHLIST) or []
    if not isinstance(data, list):
        raise TypeError(f"{WATCHLIST} must contain a top-level list")
    return data


def load_venues() -> dict[str, dict[str, Any]]:
    rows = load_yaml(ROOT / "data" / "venues.yaml") or []
    return {row["name"]: row for row in rows}


def load_concepts() -> dict[str, Any]:
    return load_yaml(ROOT / "data" / "concepts.yaml") or {}


def public_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def record_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(record["record_type"] for record in records).items()))


def family_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(record["family"] for record in records).items()))


def venue_tier_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(record["venue_tier"] for record in records).items()))


def verification_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(record["verification_status"] for record in records).items()))


def evidence_depth_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(record["evidence_depth"] for record in records).items()))


def derive_relations(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    relations: list[dict[str, str]] = []
    relation_fields = {
        "modalities": "uses_modality",
        "clinical_domains": "targets_domain",
        "body_locations": "uses_body_location",
        "populations": "studies_population",
        "related_ids": "related_to",
    }
    for record in records:
        for field, predicate in relation_fields.items():
            for target in record.get(field, []) or []:
                relations.append({
                    "source_id": record["id"],
                    "predicate": predicate,
                    "target_id": str(target),
                    "provenance": "derived_from_record_metadata",
                })
    explicit = load_yaml(ROOT / "data" / "relations.yaml") or []
    relations.extend(explicit)
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict[str, str]] = []
    for relation in relations:
        key = (relation["source_id"], relation["predicate"], relation["target_id"])
        if key not in seen:
            seen.add(key)
            unique.append(relation)
    return sorted(unique, key=lambda row: (row["source_id"], row["predicate"], row["target_id"]))


def group_by(records: Iterable[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record.get(key, "unknown"))].append(record)
    return dict(grouped)
