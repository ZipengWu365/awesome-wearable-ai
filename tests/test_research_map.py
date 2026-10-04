import copy
import json
import unittest

from scripts.render_research_map import (
    ASSETS,
    REGISTRY_PATH,
    bin_for_year,
    build_coverage,
    build_payload,
    matches_keyword,
    read_json,
    render_template,
)


class ResearchMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = read_json(REGISTRY_PATH)
        cls.payload = build_payload(cls.registry)

    def test_exact_accepted_and_watchlist_coverage(self):
        for status, source_key in (("accepted", "records"), ("watchlist", "watchlist")):
            expected = {record["id"] for record in self.registry[source_key]}
            mapped = [record["id"] for record in self.payload["records"] if record["catalog_status"] == status]
            self.assertEqual(expected, set(mapped))
            self.assertEqual(len(expected), len(mapped))
            self.assertEqual(len(expected), self.payload["counts"][status])
        ids = [record["id"] for record in self.payload["records"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_four_user_themes_cover_every_record_with_honest_roles(self):
        self.assertEqual(["prediction", "intervention", "twin", "interface"], [r["id"] for r in self.payload["routes"]])
        for record in self.payload["records"]:
            self.assertIn(record["primary_route"], {r["id"] for r in self.payload["routes"]})
            self.assertIn(record["route_role"], {"direct", "support", "framework", "adjacent"})
            self.assertTrue(record["classification_reason"])
            self.assertNotIn(record["primary_route"], record["secondary_routes"])
        for status in ("accepted", "watchlist"):
            self.assertEqual(self.payload["counts"][status], sum(row["total"] for row in self.payload["route_counts"][status].values()))
        twins = {r["id"]: r for r in self.payload["records"] if r["primary_route"] == "twin"}
        self.assertEqual({"method-causal-digital-twins-2026", "intervention-aid-digital-twin-coadaptation-2025"}, set(twins))
        self.assertEqual("framework", twins["method-causal-digital-twins-2026"]["route_role"])

    def test_coverage_rejects_tampered_editorial_assignment(self):
        for field, value in (("primary_route", "twin"), ("secondary_routes", ["twin"]), ("route_role", "direct"), ("classification_reason", "Unverified claim")):
            payload = copy.deepcopy(self.payload)
            record = next(r for r in payload["records"] if r["id"] == "dataset-mitbih-arrhythmia")
            record[field] = value
            with self.assertRaises(ValueError):
                build_coverage(self.registry, payload)

    def test_keywords_have_real_matches_and_explicit_selectors(self):
        source_ids = {r["id"] for r in self.payload["records"]}
        for route in self.payload["routes"]:
            self.assertEqual(3, len(route["keywords"]))
            self.assertEqual(3, len({keyword["id"] for keyword in route["keywords"]}))
            for keyword in route["keywords"]:
                self.assertTrue(set(keyword.get("ids", [])) <= source_ids, keyword["id"])
                self.assertTrue(any(matches_keyword(r, route, keyword) for r in self.payload["records"]), keyword["id"])
        mapped = {r["id"]: r for r in self.payload["records"]}
        self.assertIn("Smart glasses", mapped["model-sing-wearables-2025"]["topic_keywords"])
        self.assertIn("Personalization", mapped["model-ph-llm-2025"]["topic_keywords"])
        self.assertEqual("prediction", mapped["model-ph-llm-2025"]["primary_route"])
        self.assertNotIn("Personalization", mapped["dataset-mitbih-arrhythmia"]["topic_keywords"])

    def test_coverage_rejects_invented_keywords(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][0]["topic_keywords"] = ["Invented evidence"]
        with self.assertRaises(ValueError):
            build_coverage(self.registry, payload)

    def test_original_metadata_and_source_are_unchanged(self):
        before = copy.deepcopy(self.registry)
        payload = build_payload(self.registry)
        mapped = {record["id"]: record for record in payload["records"]}
        for original in self.registry["records"] + self.registry["watchlist"]:
            for field, value in original.items():
                self.assertEqual(value, mapped[original["id"]][field], (original["id"], field))
            if "proposed_family" in original:
                self.assertEqual(original["proposed_family"], mapped[original["id"]]["family"])
        self.assertEqual(before, self.registry)

    def test_every_record_has_one_native_branch_and_time_bin(self):
        expected_types = ["model", "measure", "method", "intervention", "dataset", "infrastructure", "watchlist"]
        self.assertEqual(expected_types, [branch["id"] for branch in self.payload["branches"]])
        for record in self.payload["records"]:
            expected_branch = record["record_type"] if record["catalog_status"] == "accepted" else "watchlist"
            self.assertEqual(expected_branch, record["branch"])
            matches = [item for item in self.payload["bins"] if item["start"] <= record["year"] <= item["end"]]
            self.assertEqual(1, len(matches), record["id"])
            self.assertEqual(matches[0]["id"], record["bin"])
        bins = self.payload["bins"]
        self.assertEqual(["pre2010", "2010-2014"], [item["id"] for item in bins[:2]])
        self.assertEqual("1980–2009", bins[0]["label"])
        for left, right in zip(bins, bins[1:]):
            self.assertEqual(left["end"] + 1, right["start"])

    def test_oldest_dataset_and_infrastructure_guidelines_are_retained(self):
        mapped = {record["id"]: record for record in self.payload["records"]}
        oldest = mapped["dataset-mitbih-arrhythmia"]
        self.assertEqual(1980, oldest["year"])
        self.assertEqual("pre2010", oldest["bin"])
        for original in self.registry["records"]:
            if original["record_type"] == "infrastructure" and original["family"] in ("reporting-guidelines", "regulatory-guidance"):
                self.assertEqual("infrastructure", mapped[original["id"]]["branch"])
                self.assertEqual(original, {field: mapped[original["id"]][field] for field in original})
        self.assertIn("infra-consort-ai-2020", mapped)
        self.assertIn("infra-stard-ai-2025", mapped)

    def test_known_bad_links_are_withheld_without_losing_records(self):
        mapped = {record["id"]: record for record in self.payload["records"]}
        for record_id in ("model-eeg-to-text-2022", "method-v-learning-2015"):
            self.assertTrue(mapped[record_id]["link_withheld"])
            self.assertTrue(mapped[record_id]["source_issue"])
            original = next(record for record in self.registry["records"] if record["id"] == record_id)
            self.assertEqual(original["primary_url"], mapped[record_id]["primary_url"])
        self.assertEqual(2, sum(bool(record.get("link_withheld")) for record in self.payload["records"]))

    def test_coverage_manifest_proves_exact_id_sets(self):
        coverage = build_coverage(self.registry, self.payload)
        self.assertEqual(sorted(record["id"] for record in self.registry["records"]), coverage["accepted_ids"])
        self.assertEqual(sorted(record["id"] for record in self.registry["watchlist"]), coverage["watchlist_ids"])
        self.assertEqual(len(self.payload["records"]), coverage["mapped_total"])
        for field in ("unassigned_ids", "omitted_ids", "unexpected_ids", "duplicate_ids"):
            self.assertEqual([], coverage[field])
        mapped = {record["id"]: record for record in self.payload["records"]}
        for row in coverage["records"]:
            self.assertEqual(row, {key: mapped[row["id"]][key] for key in row})
        stored = read_json(ASSETS / "coverage.json")
        self.assertEqual(coverage, stored)

    def test_coverage_rejects_an_omitted_or_duplicate_record(self):
        omitted = copy.deepcopy(self.payload)
        omitted["records"].pop()
        with self.assertRaises(ValueError):
            build_coverage(self.registry, omitted)
        duplicated = copy.deepcopy(self.payload)
        duplicated["records"].append(duplicated["records"][0])
        with self.assertRaises(ValueError):
            build_coverage(self.registry, duplicated)

    def test_coverage_rejects_changed_classification_counts_or_metadata(self):
        for field, value in (("branch", "dataset"), ("family", "invented-family"), ("title", "Changed title"), ("year", 2025)):
            payload = copy.deepcopy(self.payload)
            payload["records"][0][field] = value
            if field == "year":
                payload["records"][0]["bin"] = "2025"
            with self.assertRaises(ValueError):
                build_coverage(self.registry, payload)
        payload = copy.deepcopy(self.payload)
        payload["counts"]["accepted"] -= 1
        with self.assertRaises(ValueError):
            build_coverage(self.registry, payload)

    def test_future_or_earlier_years_are_not_silently_dropped(self):
        registry = copy.deepcopy(self.registry)
        registry["records"][0]["year"] = 2027
        registry["records"][1]["year"] = 1970
        payload = build_payload(registry)
        self.assertEqual(1970, payload["bins"][0]["start"])
        self.assertEqual(2027, payload["bins"][-1]["end"])
        self.assertEqual("2027", bin_for_year(2027, payload["bins"]))
        self.assertEqual("pre2010", bin_for_year(1970, payload["bins"]))
        self.assertEqual(len(self.payload["records"]), len(payload["records"]))

    def test_invalid_year_type_branch_or_duplicate_id_fails(self):
        for year in (None, "2026", 2026.0, True, 0):
            registry = copy.deepcopy(self.registry)
            registry["records"][0]["year"] = year
            with self.assertRaises(ValueError):
                build_payload(registry)
        registry = copy.deepcopy(self.registry)
        registry["records"][0]["record_type"] = "unknown"
        with self.assertRaises(ValueError):
            build_payload(registry)
        registry = copy.deepcopy(self.registry)
        registry["watchlist"][0]["id"] = registry["records"][0]["id"]
        with self.assertRaises(ValueError):
            build_payload(registry)

    def test_template_requires_one_placeholder_and_escapes_script_close(self):
        payload = {"title": "</script><script>alert(1)</script>"}
        output = render_template("const data = __RESEARCH_DATA__;", payload)
        self.assertNotIn("</script>", output)
        self.assertIn("\\u003c/script>", output)
        encoded = output.removeprefix("const data = ").removesuffix(";")
        self.assertEqual(payload, json.loads(encoded))
        for template in ("no placeholder", "__RESEARCH_DATA__ __RESEARCH_DATA__"):
            with self.assertRaises(ValueError):
                render_template(template, payload)


if __name__ == "__main__":
    unittest.main()
