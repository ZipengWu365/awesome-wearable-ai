#!/usr/bin/env python3
"""Validate the editorial radar without changing the underlying registry.

These checks enforce a reviewable data contract, not scientific truth. Two dated
signals are a minimum requirement for an emerging pattern, not proof of a trend.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "research-map"
SCHEMA_PATH = ASSETS / "technology-radar.schema.json"
RADAR_PATH = ASSETS / "technology-radar.json"
UPDATE_TYPES = {"method", "data", "hardware", "performance", "product", "direction"}


def _nonblank_strings(value: object, path: str = "radar") -> None:
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{path} must not be blank")
    if isinstance(value, dict):
        for key, child in value.items():
            _nonblank_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _nonblank_strings(child, f"{path}[{index}]")


def _source_url(url: str, signal_id: str) -> None:
    if any(char.isspace() or ord(char) < 32 for char in url) or "\\" in url:
        raise ValueError(f"Signal {signal_id}: source URL must not contain whitespace or backslashes")
    try:
        parts = urlsplit(url)
        valid = (
            parts.scheme == "https"
            and bool(parts.hostname)
            and parts.username is None
            and parts.password is None
        )
        # Accessing port also rejects malformed ports and invalid URL brackets.
        parts.port
    except ValueError as error:
        raise ValueError(f"Signal {signal_id}: invalid source URL") from error
    if not valid:
        raise ValueError(f"Signal {signal_id}: source URLs must use HTTPS without credentials")


def validate_radar(radar: dict, registry_ids: set[str], route_ids: set[str]) -> dict:
    """Return the same object when valid; raise ValueError for invalid data."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    error = next(validator.iter_errors(radar), None)
    if error is not None:
        path = ".".join(str(part) for part in error.absolute_path) or "radar"
        raise ValueError(f"Technology radar schema error at {path}: {error.message}")
    _nonblank_strings(radar)
    if len(route_ids) != 4:
        raise ValueError("Technology radar requires exactly four research routes")
    type_ids = [row["id"] for row in radar["update_types"]]
    if len(type_ids) != len(set(type_ids)) or set(type_ids) != UPDATE_TYPES:
        raise ValueError("Technology radar must define each of the six update types exactly once")
    assessed_routes = [row["route"] for row in radar["assessments"]]
    if len(assessed_routes) != len(set(assessed_routes)) or set(assessed_routes) != route_ids:
        raise ValueError("Technology radar must assess each research route exactly once")

    reviewed = date.fromisoformat(radar["reviewed_on"])
    start = date.fromisoformat(radar["window"]["start"])
    end = date.fromisoformat(radar["window"]["end"])
    if start > end or end > reviewed:
        raise ValueError("Technology radar window must be ordered and not exceed reviewed_on")

    signal_ids = [signal["id"] for signal in radar["signals"]]
    if len(signal_ids) != len(set(signal_ids)):
        raise ValueError("Technology radar signal IDs must be unique")
    by_id = {signal["id"]: signal for signal in radar["signals"]}
    for signal in radar["signals"]:
        signal_id = signal["id"]
        if signal["route"] not in route_ids:
            raise ValueError(f"Signal {signal_id}: unknown primary research route")
        if set(signal["secondary_routes"]) - route_ids or signal["route"] in signal["secondary_routes"]:
            raise ValueError(f"Signal {signal_id}: invalid secondary research routes")
        missing = set(signal["registry_ids"]) - registry_ids
        if missing:
            raise ValueError(f"Signal {signal_id}: unknown registry IDs: {', '.join(sorted(missing))}")
        publication = date.fromisoformat(signal["publication_date"])
        event = date.fromisoformat(signal["event_date"])
        verified = date.fromisoformat(signal["verified_on"])
        if publication > reviewed or event > reviewed or verified > reviewed:
            raise ValueError(f"Signal {signal_id}: dates must not exceed reviewed_on")
        if verified < publication:
            raise ValueError(f"Signal {signal_id}: verified_on must not precede publication_date")
        for source in signal["sources"]:
            _source_url(source["url"], signal_id)

    for assessment in radar["assessments"]:
        route = assessment["route"]
        missing = set(assessment["signal_ids"]) - set(by_id)
        if missing:
            raise ValueError(f"Assessment {route}: unknown signal IDs: {', '.join(sorted(missing))}")
        linked = [by_id[signal_id] for signal_id in assessment["signal_ids"]]
        if any(route != signal["route"] and route not in signal["secondary_routes"] for signal in linked):
            raise ValueError(f"Assessment {route}: linked signals must belong to this primary or secondary route")
        if assessment["kind"] == "emerging_pattern":
            if len(linked) < 2 or len({signal["event_date"] for signal in linked}) < 2:
                raise ValueError(f"Assessment {route}: an emerging pattern needs at least two signals at distinct event dates")
    return radar


def main() -> int:
    radar = json.loads(RADAR_PATH.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "generated" / "registry.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((ASSETS / "taxonomy.json").read_text(encoding="utf-8"))
    registry_ids = {record["id"] for record in registry["records"] + registry["watchlist"]}
    route_ids = {route["id"] for route in taxonomy["routes"]}
    validate_radar(radar, registry_ids, route_ids)
    print(f"Technology radar validated: {len(radar['signals'])} signals, four theme assessments; reviewed {radar['reviewed_on']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
