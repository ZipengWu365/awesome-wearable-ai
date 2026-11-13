"""November reading additions: provenance, full coverage and unchanged originals."""
import copy
from datetime import date
import json
from pathlib import Path
import re
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'website'
additions = json.loads((SITE / 'literature-updates.json').read_text())
original = json.loads((ROOT / 'assets/research-map/technology-radar.json').read_text())
merge = runpy.run_path(str(SITE / 'research_updates.py'))['merge_updates']
payload = json.loads(re.search(r'<script id="research-data" type="application/json">(.*?)</script>',
                              (SITE / 'research-map.html').read_text(), re.S)[1])


class LiteratureUpdateTests(unittest.TestCase):
    def test_old_notes_and_registry_are_preserved(self):
        before = copy.deepcopy(original)
        combined = merge(original, additions)
        self.assertEqual(original, before)
        self.assertEqual(combined['signals'][:len(original['signals'])], original['signals'])
        self.assertEqual(combined, payload['radar'])
        registry = json.loads((ROOT / 'generated/registry.json').read_text())
        self.assertEqual(len(payload['records']), 441)
        by_id = {r['id']:r for r in payload['records']}
        for r in registry['records'] + registry['watchlist']:
            self.assertEqual(r, {key:by_id[r['id']][key] for key in r})

    def test_new_papers_have_publication_status_dates_and_landing_links(self):
        self.assertEqual(additions['reviewed_on'], '2026-11-13')
        self.assertEqual(len(additions['signals']), 16)
        self.assertEqual(sum(not s['registry_ids'] for s in additions['signals']), 15)
        venues = {s['venue'] for s in additions['signals']}
        self.assertTrue({'Nature','Nature Communications','NeurIPS 2026','ICML 2026','ICLR 2026'} <= venues)
        for s in additions['signals']:
            for key in ('short_name','title','venue','publication_status','article_type','resource_type'):
                self.assertTrue(s[key])
            for key in ('publication_date','event_date','verified_on','added_on'):
                self.assertLessEqual(date.fromisoformat(s[key]), date(2026,11,13))
            for link in s['sources']:
                self.assertTrue(link['url'].startswith('https://'))
                self.assertNotRegex(link['url'], r'/pdf/|\.pdf(?:[?#]|$)')

    def test_every_added_work_reaches_each_relevant_tree(self):
        for s in additions['signals']:
            for route in [s['route'], *s['secondary_routes']]:
                nodes = payload['tree']['columns'][route]['nodes']
                linked = set(s['registry_ids']) & {n['id'] for n in nodes}
                matches = [n for n in nodes if n['id'] == 'signal-' + s['id']]
                self.assertEqual(len(matches), 0 if linked else 1, (route,s['id']))
                if matches:
                    self.assertEqual(matches[0]['related'], route != s['route'])
                    period = payload['tree']['periods'][matches[0]['period']]
                    year = int(s['event_date'][:4])
                    self.assertLessEqual(period['start'], year)
                    self.assertGreaterEqual(period['end'], year)

    def test_existing_glucofm_has_one_tree_node_with_a_linked_review(self):
        s = next(s for s in additions['signals'] if s['id']=='glucofm-neurips-review-2026')
        self.assertEqual(s['registry_ids'], ['model-glucofm-2026'])
        nodes = payload['tree']['columns']['prediction']['nodes']
        self.assertEqual(sum(n['id']=='model-glucofm-2026' for n in nodes), 1)
        self.assertFalse(any(n['id']=='signal-'+s['id'] for n in nodes))

    def test_duplicate_reading_notes_are_rejected(self):
        changed = copy.deepcopy(additions)
        changed['signals'].append(changed['signals'][0])
        with self.assertRaises(AssertionError): merge(original, changed)

    def test_new_editorial_copy_uses_direct_language(self):
        fields = ('before','after','evidence','limit','implication')
        for s in additions['signals']:
            for key in fields:
                self.assertNotRegex(s[key], r'[→↗↓↑—–]|(?i:not just|we do not claim|groundbreaking|game.changing)')


if __name__ == '__main__':
    unittest.main()
