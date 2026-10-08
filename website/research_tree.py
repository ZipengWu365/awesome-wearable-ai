"""Presentation branches from the repository's existing family and route fields."""
import copy


def build_tree(payload, config):
    periods = config['periods']
    assert all(a['end'] < b['start'] for a, b in zip(periods, periods[1:]))
    result = {'periods': copy.deepcopy(periods), 'columns': {}}
    for theme, settings in config['columns'].items():
        branches = copy.deepcopy(settings['branches'])
        families = {}
        for branch in branches:
            for family in branch['families'].split():
                assert family not in families, f'Duplicate tree family: {theme} {family}'
                families[family] = branch['id']
            del branch['families']
        branches.append({'id':'related','label':'Related methods & resources','color':'#6c7d8e','summary':'Existing cross-links from the other columns. These provide parts or methods, rather than a demonstrated complete system.'})
        ids = {b['id'] for b in branches}
        nodes = []
        for record in payload['records']:
            primary = record['primary_route'] == theme
            if not primary and theme not in record['secondary_routes']:
                continue
            if primary:
                assert record['family'] in families, f'Unmapped tree family: {theme} {record["family"]}'
            period = next((i for i, p in enumerate(periods) if p['start'] <= record['year'] <= p['end']), None)
            assert period is not None, f'Unmapped tree year: {record["id"]}'
            nodes.append({'id':record['id'], 'branch':families[record['family']] if primary else 'related', 'period':period, 'related':not primary, 'featured':record['id'] in settings['featured']})
        # Source reviews attached to a collected record enrich that node. They
        # never count the same paper twice. Standalone updates have their own badge.
        present = {n['id'] for n in nodes}
        for signal in payload['radar']['signals']:
            if signal['route'] != theme or any(id in present for id in signal['registry_ids']):
                continue
            branch = settings['signal_branches'].get(signal['id'])
            assert branch in ids, f'Unmapped source update: {theme} {signal["id"]}'
            year = int(signal['event_date'][:4])
            period = next(i for i, p in enumerate(periods) if p['start'] <= year <= p['end'])
            nodes.append({'id':'signal-' + signal['id'], 'branch':branch, 'period':period, 'related':False, 'featured':True})
        assert len(nodes) == len({n['id'] for n in nodes})
        expected = {r['id'] for r in payload['records'] if r['primary_route'] == theme}
        assert {n['id'] for n in nodes if not n['related'] and not n['id'].startswith('signal-')} == expected
        result['columns'][theme] = {'branches':branches, 'nodes':nodes}
    return result
