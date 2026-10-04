import copy
import json
import unittest

from jsonschema import Draft202012Validator

from scripts.validate_technology_radar import SCHEMA_PATH, validate_radar


ROUTES = {"prediction", "intervention", "twin", "interface"}
REGISTRY_IDS = {"paper-one", "paper-two"}
UPDATE_TYPES = ["method", "data", "hardware", "performance", "product", "direction"]


def fixture() -> dict:
    signals = []
    for index, route in enumerate(("prediction", "intervention", "twin", "interface"), start=1):
        signals.append({
            "id": f"signal-{index}", "route": route, "secondary_routes": [],
            "types": ["method"], "publication_date": f"2026-09-{20 + index:02d}",
            "event_date": f"2026-09-{20 + index:02d}", "verified_on": "2026-10-04",
            "temporal_role": "baseline", "evidence_level": "peer_reviewed",
            "availability": "Published methods; availability of weights is not established.",
            "title": f"Fixture signal {index}", "before": "Previous method.",
            "after": "Reported technical change.", "evidence": "A primary-source report.",
            "limit": "This fixture makes no scientific claim.",
            "implication": "A potential enabling contribution, not an achieved research stage.",
            "sources": [{"title": "Primary source", "url": f"https://example.org/source-{index}"}],
            "registry_ids": ["paper-one"] if index == 1 else [],
            "keywords": ["Fixture keyword"],
        })
    signals[1]["secondary_routes"] = ["prediction"]
    return {
        "schema_version": 1, "reviewed_on": "2026-10-04",
        "window": {"start": "2026-09-28", "end": "2026-10-04"},
        "coverage_note": "Selective source review; not exhaustive frontier monitoring.",
        "update_types": [{"id": type_id, "label": type_id.title()} for type_id in UPDATE_TYPES],
        "assessments": [
            {"route": route, "kind": "assessment", "headline": f"{route.title()} assessment",
             "summary": "Current technical state.", "limit": "Editorial assessment, not a proven trend.",
             "signal_ids": [f"signal-{index}"]}
            for index, route in enumerate(("prediction", "intervention", "twin", "interface"), start=1)
        ],
        "signals": signals,
    }


class TechnologyRadarTests(unittest.TestCase):
    def assertInvalid(self, radar: dict):
        with self.assertRaises(ValueError):
            validate_radar(radar, REGISTRY_IDS, ROUTES)

    def test_schema_is_valid_and_validation_preserves_input(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
        radar = fixture()
        original = copy.deepcopy(radar)
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))
        self.assertEqual(original, radar)

    def test_no_recent_signal_is_required_or_fabricated(self):
        radar = fixture()
        self.assertTrue(all(signal["event_date"] < radar["window"]["start"] for signal in radar["signals"]))
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))
        radar["signals"] = []
        for assessment in radar["assessments"]:
            assessment["signal_ids"] = []
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))

    def test_version_missing_fields_and_unexpected_fields_fail(self):
        for version in (0, 2, True, "1"):
            radar = fixture()
            radar["schema_version"] = version
            self.assertInvalid(radar)
        radar = fixture()
        del radar["coverage_note"]
        self.assertInvalid(radar)
        radar = fixture()
        radar["signals"][0]["unreviewed_claim"] = "Unexpected content"
        self.assertInvalid(radar)

    def test_six_update_types_are_unique_and_complete(self):
        radar = fixture()
        radar["update_types"][0] = copy.deepcopy(radar["update_types"][1])
        self.assertInvalid(radar)
        radar = fixture()
        radar["update_types"].pop()
        self.assertInvalid(radar)
        radar = fixture()
        radar["signals"][0]["types"] = ["marketing"]
        self.assertInvalid(radar)
        radar = fixture()
        radar["signals"][0]["types"] = []
        self.assertInvalid(radar)

    def test_four_assessments_have_unique_valid_routes(self):
        radar = fixture()
        radar["assessments"][1]["route"] = "prediction"
        self.assertInvalid(radar)
        radar = fixture()
        radar["assessments"][0]["route"] = "unknown"
        self.assertInvalid(radar)
        with self.assertRaises(ValueError):
            validate_radar(fixture(), REGISTRY_IDS, {"prediction"})

    def test_duplicate_signal_ids_and_unknown_registry_ids_fail(self):
        radar = fixture()
        radar["signals"][1]["id"] = radar["signals"][0]["id"]
        self.assertInvalid(radar)
        radar = fixture()
        radar["signals"][0]["registry_ids"] = ["nonexistent-paper"]
        self.assertInvalid(radar)

    def test_invalid_primary_secondary_and_duplicate_routes_fail(self):
        for field, value in (("route", "unknown"), ("secondary_routes", ["unknown"]),
                             ("secondary_routes", ["prediction"]),
                             ("secondary_routes", ["twin", "twin"])):
            radar = fixture()
            radar["signals"][0][field] = value
            self.assertInvalid(radar)

    def test_assessment_signal_links_are_real_and_relevant(self):
        radar = fixture()
        radar["assessments"][0]["signal_ids"] = ["missing-signal"]
        self.assertInvalid(radar)
        radar = fixture()
        radar["assessments"][0]["signal_ids"] = ["signal-3"]
        self.assertInvalid(radar)
        radar = fixture()
        radar["assessments"][0]["signal_ids"] = ["signal-2"]
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))

    def test_emerging_pattern_requires_two_distinct_event_dates(self):
        radar = fixture()
        assessment = radar["assessments"][0]
        assessment["kind"] = "emerging_pattern"
        self.assertInvalid(radar)
        assessment["signal_ids"] = ["signal-1", "signal-2"]
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))
        radar["signals"][1]["event_date"] = radar["signals"][0]["event_date"]
        self.assertInvalid(radar)

    def test_date_shape_and_calendar_validity_fail(self):
        for value in ("2026-2-01", "2026-02-30", "not-a-date", None):
            radar = fixture()
            radar["signals"][0]["event_date"] = value
            self.assertInvalid(radar)

    def test_window_order_and_review_cutoff_are_validated(self):
        radar = fixture()
        radar["window"]["start"] = "2026-10-05"
        self.assertInvalid(radar)
        radar = fixture()
        radar["window"]["end"] = "2026-10-05"
        self.assertInvalid(radar)
        for field in ("publication_date", "event_date", "verified_on"):
            radar = fixture()
            radar["signals"][0][field] = "2026-10-05"
            self.assertInvalid(radar)

    def test_verification_cannot_precede_publication(self):
        radar = fixture()
        radar["signals"][0]["verified_on"] = "2026-09-20"
        self.assertInvalid(radar)

    def test_event_date_remains_separate_from_publication_date(self):
        radar = fixture()
        radar["signals"][0]["event_date"] = "2026-09-19"
        radar["signals"][1]["event_date"] = "2026-10-01"
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))

    def test_sources_require_https_host_and_no_credentials(self):
        for url in ("http://example.org/paper", "javascript:alert(1)", "/relative/paper",
                    "https:///missing-host", "https://user:secret@example.org/paper",
                    "https://user@example.org/paper", "https://example.org:invalid/paper",
                    "https://example.org/paper name", "https://example.org\\@other.org/paper"):
            radar = fixture()
            radar["signals"][0]["sources"][0]["url"] = url
            self.assertInvalid(radar)
        radar = fixture()
        radar["signals"][0]["sources"] = []
        self.assertInvalid(radar)

    def test_performance_needs_explicit_comparison_conditions(self):
        radar = fixture()
        radar["signals"][0]["types"] = ["performance"]
        self.assertInvalid(radar)
        radar["signals"][0]["comparison"] = {
            "baseline": "Prior method under the same task.",
            "result": "Source-reported result, not independently reproduced.",
            "conditions": "Same task, split and metric; compute cost not established.",
        }
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))
        radar["signals"][0]["comparison"]["conditions"] = "  "
        self.assertInvalid(radar)

    def test_availability_and_claim_boundaries_cannot_be_blank(self):
        for field in ("title", "before", "after", "evidence", "limit", "implication", "availability"):
            radar = fixture()
            radar["signals"][0][field] = "  "
            self.assertInvalid(radar)
        radar = fixture()
        radar["assessments"][0]["limit"] = "\n"
        self.assertInvalid(radar)

    def test_vendor_and_preprint_status_are_not_upgraded(self):
        radar = fixture()
        signal = radar["signals"][3]
        signal["types"] = ["hardware", "product"]
        signal["evidence_level"] = "vendor_announcement"
        signal["availability"] = "Announced prototype; no shipping availability established."
        signal["temporal_role"] = "update"
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))
        self.assertEqual("vendor_announcement", signal["evidence_level"])
        signal["evidence_level"] = "preprint"
        self.assertIs(radar, validate_radar(radar, REGISTRY_IDS, ROUTES))
        signal["evidence_level"] = "validated_clinical_system"
        self.assertInvalid(radar)


if __name__ == "__main__":
    unittest.main()
