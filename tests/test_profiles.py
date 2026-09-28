import copy
import unittest
from scripts.registry import load_records,load_watchlist
from scripts.profiles import validate_profiles,public_profiles

class ProfileTests(unittest.TestCase):
    def test_migration_and_sources_valid(self):
        self.assertEqual(validate_profiles(load_records(),load_watchlist()),[])

    def test_original_record_deletion_rejected(self):
        records=load_records()[1:]
        self.assertTrue(any('preservation' in x for x in validate_profiles(records,load_watchlist())))

    def test_undocumented_original_change_rejected(self):
        records=copy.deepcopy(load_records());records[0]['title']='Accidental overwrite'
        self.assertTrue(any('preservation' in x for x in validate_profiles(records,load_watchlist())))

    def test_unimts_regression_rejected(self):
        records=load_records();next(r for r in records if r['id']=='model-unimts-2024')['open_weights']=False
        self.assertTrue(any('preservation' in x for x in validate_profiles(records,load_watchlist())))

    def test_profiles_never_promote_candidates(self):
        records=load_records();watch=load_watchlist();allowed={r['id'] for r in records+watch}
        profiles=public_profiles(records,watch)
        for name in ['resources','causal','digital_twin']:
            self.assertTrue(all(p['record_id'] in allowed for p in profiles[name]))
        self.assertEqual(len(records),408)
        self.assertEqual(len(profiles['digital_twin']),22)

    def test_formal_publication_preserved(self):
        records={r['id']:r for r in load_records()}
        for id in ['model-sensorlm-2025','model-unimts-2024']:
            self.assertEqual(records[id]['venue'],'NeurIPS')
