"""Presentation-only evidence checks; never change the scientific registry."""
import copy
import json
from pathlib import Path
import re
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]
validate = runpy.run_path(str(ROOT / 'build_pages.py'))['validate_editorial']
briefs = json.loads((ROOT / 'editorial-briefs.json').read_text())
page = (ROOT / 'research-map.html').read_text()
payload = json.loads(re.search(r'<script id="research-data" type="application/json">(.*?)</script>', page, re.S)[1])


class EditorialBriefTests(unittest.TestCase):
    def test_complete_evidence_fields(self):
        validate(briefs, payload)

    def test_unknown_source_fails(self):
        changed = copy.deepcopy(briefs)
        changed['columns']['prediction']['ids'].append('invented-paper')
        with self.assertRaises(AssertionError):
            validate(changed, payload)

    def test_missing_comparison_fails(self):
        changed = copy.deepcopy(briefs)
        changed['columns']['prediction']['stories'][0]['before'] = ''
        with self.assertRaises(AssertionError):
            validate(changed, payload)

    def test_future_check_date_fails(self):
        changed = copy.deepcopy(briefs)
        changed['columns']['prediction']['stories'][0]['checked_on'] = '2099-01-01'
        with self.assertRaises(AssertionError):
            validate(changed, payload)

    def test_history_requires_dated_evidence_and_explanation(self):
        for brief in briefs['columns'].values():
            for stage in brief['evolution']:
                self.assertTrue(stage['meaning'])
                self.assertTrue(stage['limit'])
                self.assertNotRegex(stage['headline'], '[→↗↓↑]')
        changed = copy.deepcopy(briefs)
        changed['columns']['prediction']['evolution'][0]['ids'] = ['model-sensorfm-2026']
        with self.assertRaises(AssertionError):
            validate(changed, payload)

    def test_history_periods_cannot_overlap(self):
        changed = copy.deepcopy(briefs)
        changed['columns']['prediction']['evolution'][1]['start'] = 2000
        with self.assertRaises(AssertionError):
            validate(changed, payload)

    def test_embedded_briefs_match_source_on_every_column(self):
        for name in ('research-map','prediction','intervention','digital-twins','mixed-reality'):
            text = (ROOT / (name + '.html')).read_text()
            embedded = json.loads(re.search(r'<script id="editorial-data" type="application/json">(.*?)</script>', text, re.S)[1])
            self.assertEqual(embedded, briefs)

    def test_existing_coverage_is_preserved(self):
        self.assertEqual(len(payload['records']), 441)
        self.assertEqual(len({r['id'] for r in payload['records']}), 441)
        self.assertEqual(sum(r['catalog_status']=='accepted' for r in payload['records']), 396)

    def test_result_conditions_are_not_missing(self):
        for brief in briefs['columns'].values():
            self.assertTrue(brief['status'].startswith(('Our ', 'A research direction')))
            for story in brief['stories']:
                self.assertTrue(story['condition'])
                self.assertTrue(story['locator'])
                self.assertNotRegex(story['headline'], '[→↗↓↑]')


if __name__ == '__main__':
    unittest.main()
