"""Offline checks for the bounded, first-party deployment verifier."""
from pathlib import Path
import runpy
import unittest

checker = runpy.run_path(str(Path(__file__).resolve().parents[2] / 'scripts/check_website_availability.py'))
base = 'https://zipengwu.me/awesome-wearable-ai/'


class AvailabilityTests(unittest.TestCase):
    def test_relative_assets_keep_project_base(self):
        self.assertEqual(checker['first_party'](base, base + 'index.html', 'app.js?v=1'), base + 'app.js?v=1')

    def test_does_not_check_other_domains_or_insecure_urls(self):
        for target in ('https://fonts.googleapis.com/a.css', 'http://zipengwu.me/a.js', 'data:image/png;base64,abc'):
            self.assertIsNone(checker['first_party'](base, base, target))

    def test_does_not_request_personal_homepage_assets(self):
        self.assertIsNone(checker['first_party'](base, base, '../portrait.png'))

    def test_nested_css_assets_stay_in_scope(self):
        self.assertEqual(checker['first_party'](base, base + 'assets/styles/main.css', '../images/a.png'), base + 'assets/images/a.png')

    def test_only_static_asset_tags_are_collected(self):
        parsed = checker['Assets']('<script src="app.js"></script><img src="a.png"><link rel="stylesheet" href="a.css"><a href="https://example.com">Paper</a>')
        self.assertEqual(parsed.targets, ['app.js', 'a.png', 'a.css'])


if __name__ == '__main__':
    unittest.main()
