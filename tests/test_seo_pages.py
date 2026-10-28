import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from scripts.render_research_map import build_payload
from scripts.validate_technology_radar import validate_radar
from website.seo import (
    BASE_URL, SOURCE_FILENAME, canonical_url, page_head,
    render_sources, render_sitemap, write_discovery_pages,
)


ROOT = Path(__file__).resolve().parents[1]


class ParsedHTML(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.metas, self.links, self.anchors, self.record_ids, self.record_statuses = [], [], [], [], []
        self.assessments, self.signals, self.ids, self.tags, self.jsonld = [], [], [], [], []
        self.title, self.h1, self.text = [], [], []
        self._title = self._h1 = self._jsonld = self._in_head = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.tags.append(tag)
        if tag == "meta": self.metas.append(data)
        if tag == "link": self.links.append(data)
        if tag == "a": self.anchors.append(data)
        if data.get("id"): self.ids.append(data["id"])
        if data.get("data-record-id"):
            self.record_ids.append(data["data-record-id"])
            self.record_statuses.append(data["data-catalog-status"])
        if data.get("data-assessment-route"): self.assessments.append(data["data-assessment-route"])
        if data.get("data-signal-id"): self.signals.append(data["data-signal-id"])
        if tag == "head": self._in_head = True
        if tag == "title" and self._in_head: self._title = True
        if tag == "h1": self._h1 = True
        if tag == "script" and data.get("type") == "application/ld+json": self._jsonld = True

    def handle_endtag(self, tag):
        if tag == "head": self._in_head = False
        if tag == "title": self._title = False
        if tag == "h1": self._h1 = False
        if tag == "script": self._jsonld = False

    def handle_data(self, data):
        self.text.append(data)
        if self._title: self.title.append(data)
        if self._h1: self.h1.append(data)
        if self._jsonld: self.jsonld.append(data)


def payload():
    data = build_payload()
    data["radar"] = validate_radar(
        json.loads((ROOT / "assets/research-map/technology-radar.json").read_text()),
        {record["id"] for record in data["records"]},
        {route["id"] for route in data["routes"]},
    )
    return data


class SEOPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = payload()
        cls.directory = render_sources(cls.data)
        cls.parsed = ParsedHTML(cls.directory)

    def test_canonical_urls_use_the_final_project_domain(self):
        self.assertEqual("https://zipengwu.me/awesome-wearable-ai/", BASE_URL)
        self.assertEqual(BASE_URL, canonical_url("index.html"))
        self.assertEqual(BASE_URL + "library.html", canonical_url("library.html"))
        for filename in ("../library.html", "library.html?view=map", "library.html#one", "https://other.org/", "file.js", "", "nested/page.html"):
            with self.assertRaises(ValueError): canonical_url(filename)

    def test_head_replaces_legacy_metadata_without_removing_assets(self):
        head = '''<head><meta charset="utf-8"><title>Old</title>
        <meta content='old description' name='description'><link href='https://old.example/' rel='canonical'>
        <meta property='og:title' content='old'><meta name='twitter:card' content='old'>
        <script type="application/ld+json">{"old":true}</script>
        <link rel="stylesheet" href="styles.css"><script src="keep.js"></script></head>'''
        rendered = page_head(head, "library.html", "Research library", "A clear description.", "CollectionPage")
        parsed = ParsedHTML(rendered)
        self.assertEqual([BASE_URL + "library.html"], [row["href"] for row in parsed.links if row.get("rel") == "canonical"])
        self.assertEqual(1, len([row for row in parsed.metas if row.get("name") == "description"]))
        self.assertEqual(1, len(parsed.title))
        self.assertIn("Research library", "".join(parsed.title))
        self.assertIn('href="styles.css"', rendered)
        self.assertIn('src="keep.js"', rendered)
        schema = json.loads("".join(parsed.jsonld))
        self.assertEqual("CollectionPage", schema["@type"])
        self.assertEqual(BASE_URL + "library.html", schema["url"])
        self.assertNotIn("old.example", rendered)
        self.assertNotIn('"old":true', rendered)
        self.assertEqual(rendered, page_head(rendered, "library.html", "Research library", "A clear description.", "CollectionPage"))

    def test_head_escapes_user_text_and_rejects_unsupported_inputs(self):
        title = '</title><script>alert("title")</script>'
        description = '"><img src=x onerror=alert(1)> & details'
        rendered = page_head("<head></head>", "sources.html", title, description)
        parsed = ParsedHTML(rendered)
        self.assertNotIn("img", parsed.tags)
        self.assertEqual(1, parsed.tags.count("script"))
        self.assertIn(title, json.loads("".join(parsed.jsonld))["name"])
        self.assertNotIn("</title><script>", rendered)
        for args in (("incomplete", "sources.html", "Title", "Description"), ("<head></head>", "sources.html", "", "Description")):
            with self.assertRaises(ValueError): page_head(*args)
        with self.assertRaises(ValueError): page_head("<head></head>", "sources.html", "Title", "Description", "MedicalStudy")

    def test_parser_keeps_svg_accessibility_titles_out_of_document_title(self):
        parsed = ParsedHTML('<html><head><title>Page title</title></head><body><svg><title>Accessible figure title</title></svg></body></html>')
        self.assertEqual(["Page title"], parsed.title)
        self.assertIn("Accessible figure title", parsed.text)

    def test_head_cleanup_removes_trailing_whitespace_from_retained_lines(self):
        head = '<head>\n  <meta name="description" content="Inherited">  \n  <link rel="stylesheet" href="styles.css">  \n</head>'
        rendered = page_head(head, "sources.html", "Sources", "Readable source directory.")
        self.assertFalse(any(line != line.rstrip() for line in rendered.splitlines()))
        self.assertIn('href="styles.css"', rendered)

    def test_every_real_record_has_one_static_primary_assignment_and_status(self):
        expected = {record["id"] for record in self.data["records"]}
        self.assertEqual(441, len(expected))
        self.assertEqual(expected, set(self.parsed.record_ids))
        self.assertEqual(len(expected), len(self.parsed.record_ids))
        self.assertEqual(396, self.parsed.record_statuses.count("accepted"))
        self.assertEqual(45, self.parsed.record_statuses.count("watchlist"))
        self.assertEqual(len(self.parsed.ids), len(set(self.parsed.ids)))
        self.assertEqual(1, len(self.parsed.h1))
        for record in self.data["records"]:
            self.assertIn(record["title"], "".join(self.parsed.text))

    def test_directory_preserves_metadata_and_claim_boundaries_without_mutation(self):
        data = copy.deepcopy(self.data)
        source = render_sources(data)
        self.assertEqual(self.data, data)
        text = "".join(ParsedHTML(source).text)
        for record in data["records"]:
            for field in ("contribution", "limitations", "evidence_boundary", "reason", "review_action", "review_note"):
                if record.get(field): self.assertIn(record[field], text)
        self.assertIn("Catalog cutoff: " + data["cutoff"], text)
        self.assertIn("Watchlist candidate — not accepted", text)
        self.assertIn("Complete repository coverage does not mean a complete frontier survey", text)

    def test_known_bad_links_are_retained_as_inert_metadata_not_clickable_sources(self):
        hrefs = {row.get("href") for row in self.parsed.anchors}
        withheld = [record for record in self.data["records"] if record.get("link_withheld")]
        self.assertEqual(2, len(withheld))
        for record in withheld:
            self.assertNotIn(record["primary_url"], hrefs)
            self.assertIn(record["primary_url"], "".join(self.parsed.text))
            self.assertIn(record["id"], self.parsed.record_ids)
        self.assertIn("Source link withheld", self.directory)

    def test_static_assessments_and_signals_retain_evidence_dates_and_limits(self):
        radar = self.data["radar"]
        self.assertEqual({row["route"] for row in radar["assessments"]}, set(self.parsed.assessments))
        self.assertEqual({row["id"] for row in radar["signals"]}, set(self.parsed.signals))
        self.assertEqual(len(radar["signals"]), len(self.parsed.signals))
        text = "".join(self.parsed.text)
        for signal in radar["signals"]:
            for field in ("before", "after", "evidence", "limit", "implication", "availability", "publication_date", "event_date", "verified_on"):
                self.assertIn(signal[field], text)
            for value in signal.get("comparison", {}).values(): self.assertIn(value, text)
        self.assertIn("Vendor announcement", text)
        self.assertIn("Preprint", text)
        self.assertIn("Dated intelligence snapshot", text)

    def test_directory_is_readable_without_script_and_has_normal_navigation(self):
        self.assertEqual(1, self.parsed.tags.count("script"))  # JSON-LD only.
        hrefs = {row.get("href") for row in self.parsed.anchors}
        self.assertTrue({"index.html", "columns.html", "library.html", "research-map.html", "sources.html"} <= hrefs)
        self.assertTrue({"prediction.html", "intervention.html", "digital-twins.html", "mixed-reality.html"} <= hrefs)
        schema = json.loads("".join(self.parsed.jsonld))
        self.assertEqual("CollectionPage", schema["@type"])
        self.assertEqual(BASE_URL + SOURCE_FILENAME, schema["url"])
        self.assertEqual(1, len([link for link in self.parsed.links if link.get("rel") == "canonical"]))
        meta = {row.get("property") or row.get("name"): row.get("content") for row in self.parsed.metas}
        self.assertEqual(BASE_URL + SOURCE_FILENAME, meta["og:url"])
        self.assertEqual("summary_large_image", meta["twitter:card"])
        self.assertNotIn("noindex", self.directory)

    def test_directory_escapes_html_and_unsafe_links(self):
        data = copy.deepcopy(self.data)
        row = data["records"][0]
        row["title"] = '<img src=x onerror=alert(1)> Injected'
        row["contribution"] = '</details><script>alert("unsafe")</script>'
        row["primary_url"] = "javascript:alert(1)"
        row["code_url"] = "https://user:secret@example.org/code"
        parsed = ParsedHTML(render_sources(data))
        self.assertNotIn("img", parsed.tags)
        self.assertEqual(1, parsed.tags.count("script"))
        self.assertIn(row["title"], "".join(parsed.text))
        hrefs = {anchor.get("href", "") for anchor in parsed.anchors}
        self.assertFalse(any(href.startswith("javascript:") or "user:secret@" in href for href in hrefs))

    def test_missing_duplicate_or_invalid_record_mapping_is_rejected(self):
        for edit in (lambda data: data["records"].pop(), lambda data: data["records"].append(data["records"][0]), lambda data: data["records"][0].update(primary_route="unknown"), lambda data: data["records"][0].update(catalog_status="published")):
            data = copy.deepcopy(self.data)
            edit(data)
            with self.assertRaises(ValueError): render_sources(data)

    def test_sitemap_contains_only_unique_canonical_pages_without_fake_dates(self):
        filenames = {"index.html", "columns.html", "library.html", "research-map.html", SOURCE_FILENAME}
        source = render_sitemap(filenames)
        tree = ET.fromstring(source)
        locations = [node.text for node in tree.findall("{*}url/{*}loc")]
        self.assertEqual({canonical_url(name) for name in filenames}, set(locations))
        self.assertEqual(len(filenames), len(locations))
        self.assertFalse(tree.findall(".//{*}lastmod"))
        self.assertTrue(all(not urlsplit(url).query and not urlsplit(url).fragment for url in locations))
        self.assertEqual(source, render_sitemap(reversed(sorted(filenames))))
        with self.assertRaises(ValueError): render_sitemap({"library.html"})

    def test_discovery_writer_only_writes_two_outputs_and_checks_page_existence(self):
        with tempfile.TemporaryDirectory() as name:
            target = Path(name)
            pages = {filename: {"title": filename, "description": "Fixture page."} for filename in ("index.html", "library.html", "research-map.html")}
            for filename in pages: (target / filename).write_text("Existing page", encoding="utf-8")
            write_discovery_pages(self.data, pages, target)
            self.assertEqual(set(pages) | {SOURCE_FILENAME, "sitemap.xml"}, {path.name for path in target.iterdir()})
            self.assertEqual(self.directory, (target / SOURCE_FILENAME).read_text())
            for filename in pages: self.assertEqual("Existing page", (target / filename).read_text())
            before = (target / "sitemap.xml").read_bytes()
            write_discovery_pages(self.data, pages, target)
            self.assertEqual(before, (target / "sitemap.xml").read_bytes())
            with self.assertRaises(ValueError): write_discovery_pages(self.data, {**pages, "missing.html": {}}, target)

    def test_deployed_sitemap_targets_have_page_specific_metadata_and_exist(self):
        target = ROOT / "website"
        expected = {
            "index.html", "columns.html", "guide.html", "story.html", "models.html",
            "history.html", "evidence.html", "library.html", "compare.html",
            "prediction.html", "intervention.html", "digital-twins.html", "mixed-reality.html",
            "research-map.html", "sources.html",
        }
        sitemap = ET.fromstring((target / "sitemap.xml").read_text())
        locations = [node.text for node in sitemap.findall("{*}url/{*}loc")]
        self.assertEqual({canonical_url(filename) for filename in expected}, set(locations))
        self.assertEqual(len(expected), len(locations))
        self.assertFalse(sitemap.findall(".//{*}lastmod"))
        titles, descriptions = [], []
        for filename in expected:
            self.assertTrue((target / filename).is_file(), filename)
            parsed = ParsedHTML((target / filename).read_text())
            canonical = [row["href"] for row in parsed.links if row.get("rel") == "canonical"]
            self.assertEqual([canonical_url(filename)], canonical, filename)
            self.assertEqual(1, len(parsed.title), filename)
            titles.append("".join(parsed.title))
            description = [row["content"] for row in parsed.metas if row.get("name") == "description"]
            self.assertEqual(1, len(description), filename)
            descriptions.extend(description)
            meta = {row.get("property") or row.get("name"): row.get("content") for row in parsed.metas}
            self.assertEqual(canonical_url(filename), meta["og:url"], filename)
            self.assertEqual("summary_large_image", meta["twitter:card"], filename)
            schema = json.loads("".join(parsed.jsonld))
            self.assertEqual(canonical_url(filename), schema["url"], filename)
            self.assertIn(schema["@type"], {"WebPage", "CollectionPage"}, filename)
        self.assertEqual(len(titles), len(set(titles)), "Page titles must be distinct")
        self.assertEqual(len(descriptions), len(set(descriptions)), "Page descriptions must be distinct")


if __name__ == "__main__":
    unittest.main()
