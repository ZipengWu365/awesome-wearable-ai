import json
import unittest
from collections import Counter

from scripts.registry import ROOT, derive_relations, load_records, load_watchlist


class RegistryTests(unittest.TestCase):
    def test_headline_scale(self):
        records = load_records()
        counts = Counter(record["record_type"] for record in records)
        self.assertGreaterEqual(len(records), 390)
        self.assertGreaterEqual(counts["model"], 100)
        self.assertGreaterEqual(counts["dataset"], 100)
        self.assertGreaterEqual(counts["method"], 50)
        self.assertGreaterEqual(counts["intervention"], 40)
        self.assertGreaterEqual(counts["measure"], 30)
        self.assertGreaterEqual(counts["infrastructure"], 40)
        self.assertGreaterEqual(len(load_watchlist()), 40)

    def test_unique_ids_and_titles(self):
        records = load_records()
        ids = [record["id"] for record in records]
        titles = [" ".join(record["title"].lower().split()) for record in records]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(titles), len(set(titles)))

    def test_evidence_records_are_not_link_only(self):
        for record in load_records():
            self.assertGreaterEqual(len(record["contribution"]), 24)
            self.assertGreaterEqual(len(record["why_it_matters"]), 24)
            self.assertGreaterEqual(len(record["limitations"]), 24)
            self.assertGreaterEqual(len(record["evidence_boundary"]), 24)

    def test_intervention_outcome_transparency(self):
        interventions = [record for record in load_records() if record["record_type"] == "intervention"]
        self.assertGreaterEqual(sum(bool(r.get("negative_or_null_result")) for r in interventions), 10)
        for record in interventions:
            self.assertIn("outcome_status", record)
            self.assertGreaterEqual(len(record["outcome_status"]), 24)

    def test_registry_export(self):
        path = ROOT / "generated" / "registry.json"
        self.assertTrue(path.exists())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["statistics"]["accepted_total"], len(load_records()))
        self.assertEqual(payload["statistics"]["watchlist_total"], len(load_watchlist()))

    def test_relations(self):
        self.assertGreater(len(derive_relations(load_records())), 4 * len(load_records()))


if __name__ == "__main__":
    unittest.main()
