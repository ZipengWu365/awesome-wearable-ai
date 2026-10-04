import copy
import json
import unittest

from scripts.classify_research_routes import (
    OUTPUT_PATH,
    REGISTRY_PATH,
    ROLES,
    ROUTES,
    build_classification,
    classify_record,
)


class RouteClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.document = build_classification(cls.registry)
        cls.rows = {row["id"]: row for row in cls.document["records"]}

    def test_every_id_is_present_once(self):
        expected = self.registry["records"] + self.registry["watchlist"]
        actual = self.document["records"]
        self.assertEqual({row["id"] for row in expected}, set(self.rows))
        self.assertEqual(len(expected), len(actual))
        self.assertEqual(len(actual), len(self.rows))
        for key, status in (("records", "accepted"), ("watchlist", "watchlist")):
            self.assertEqual(
                {row["id"] for row in self.registry[key]},
                {row["id"] for row in actual if row["catalog_status"] == status},
            )

    def test_one_primary_and_valid_secondary_routes(self):
        for row in self.document["records"]:
            self.assertIn(row["primary_route"], ROUTES)
            self.assertIn(row["route_role"], ROLES)
            self.assertNotIn(row["primary_route"], row["secondary_routes"])
            self.assertEqual(len(row["secondary_routes"]), len(set(row["secondary_routes"])))
            self.assertTrue(set(row["secondary_routes"]).issubset(ROUTES))
            for field in ("subtopic", "classification_reason", "classification_basis"):
                self.assertTrue(row[field].strip(), (row["id"], field))

    def test_counts_and_stored_document_are_reproducible(self):
        self.assertEqual(self.document, json.loads(OUTPUT_PATH.read_text(encoding="utf-8")))
        self.assertEqual(len(self.rows), sum(value["total"] for value in self.document["counts"].values()))
        for route, count in self.document["counts"].items():
            rows = [row for row in self.rows.values() if row["primary_route"] == route]
            self.assertEqual(len(rows), count["accepted"] + count["watchlist"])
            self.assertEqual(len(rows), sum(count["by_role"].values()))

    def test_does_not_modify_canonical_metadata(self):
        before = copy.deepcopy(self.registry)
        build_classification(self.registry)
        self.assertEqual(before, self.registry)

    def test_twin_route_does_not_absorb_every_personalized_model(self):
        primary_twins = {row["id"] for row in self.rows.values() if row["primary_route"] == "twin"}
        self.assertEqual({"method-causal-digital-twins-2026", "intervention-aid-digital-twin-coadaptation-2025"}, primary_twins)
        self.assertEqual("framework", self.rows["method-causal-digital-twins-2026"]["route_role"])
        self.assertEqual("direct", self.rows["intervention-aid-digital-twin-coadaptation-2025"]["route_role"])
        for record_id in ("model-personal-health-insights-agent-2026", "model-ph-llm-2025", "model-personalized-physio-adaptation-2025"):
            self.assertEqual("prediction", self.rows[record_id]["primary_route"])
            self.assertEqual("support", self.rows[record_id]["route_role"])
            self.assertIn("twin", self.rows[record_id]["secondary_routes"])

    def test_subpopulation_and_synthetic_twins_are_not_individual_twins(self):
        for record_id in ("watch-jitai-diffusion-twins-2026", "method-synctwin-2021"):
            self.assertEqual("intervention", self.rows[record_id]["primary_route"])
            self.assertIn("twin", self.rows[record_id]["secondary_routes"])
        self.assertIn("subpopulation", self.rows["watch-jitai-diffusion-twins-2026"]["classification_reason"])
        self.assertIn("synthetic", self.rows["method-synctwin-2021"]["classification_reason"])

    def test_vr_trials_and_adjacent_interfaces_preserve_contribution_boundaries(self):
        for record_id in ("intervention-reverie-vr-sports-2025", "intervention-vr-chronic-pain-2025"):
            self.assertEqual("intervention", self.rows[record_id]["primary_route"])
            self.assertIn("interface", self.rows[record_id]["secondary_routes"])
        for record_id in ("model-generic-neuromotor-interface-2025", "model-sing-wearables-2025", "model-full-body-haptic-network-2025"):
            self.assertEqual("interface", self.rows[record_id]["primary_route"])
            self.assertEqual("adjacent", self.rows[record_id]["route_role"])
        self.assertEqual("support", self.rows["dataset-ego4d"]["route_role"])

    def test_watchlist_status_is_not_promoted_and_reviews_are_explicit(self):
        for row in self.registry["watchlist"]:
            mapped = self.rows[row["id"]]
            self.assertEqual("watchlist", mapped["catalog_status"])
            self.assertTrue(mapped["needs_review"])
            self.assertIn("Provisional watchlist", mapped["review_note"])
        self.assertTrue(self.rows["model-ph-llm-2025"]["needs_review"])

    def test_rules_do_not_use_boilerplate_or_twin_keyword_alone(self):
        source = copy.deepcopy(self.registry["records"][0])
        baseline = classify_record(source)
        source["limitations"] = "A mixed-reality personal digital twin intervention causal metaverse system."
        source["evidence_boundary"] = source["limitations"]
        source["title"] = "Personalized Twin Foundation Model"
        self.assertEqual(baseline["primary_route"], classify_record(source)["primary_route"])

    def test_unknown_family_and_duplicate_ids_fail_instead_of_silent_assignment(self):
        source = copy.deepcopy(self.registry["records"][0])
        source["id"] = "new-unreviewed-record"
        source["family"] = "new-unreviewed-family"
        with self.assertRaises(ValueError):
            classify_record(source)
        registry = copy.deepcopy(self.registry)
        registry["watchlist"][0]["id"] = registry["records"][0]["id"]
        with self.assertRaises(ValueError):
            build_classification(registry)


if __name__ == "__main__":
    unittest.main()
