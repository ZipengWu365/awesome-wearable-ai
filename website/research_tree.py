"""Presentation branches from the repository's existing family and route fields."""
import copy


def build_tree(payload, config):
    start = config['annual_from_year']
    assert isinstance(start, int) and start > 1
    latest = max([start] + [r['year'] for r in payload['records']] +
                 [int(s['event_date'][:4]) for s in payload['radar']['signals']])
    periods = [{'start':1, 'end':start-1, 'label':f'Before {start}'}] + [
        {'start':year, 'end':year, 'label':str(year)} for year in range(start, latest + 1)]
    assert all(a['end'] < b['start'] for a, b in zip(periods, periods[1:]))
    known_ids = {r['id'] for r in payload['records']}
    labels = config.get('display_labels', {})
    assert set(labels) <= known_ids, 'Display label refers to an unknown resource'
    result = {'periods': copy.deepcopy(periods), 'columns': {}, 'display_labels':copy.deepcopy(labels),
              'default_start_year':start, 'latest_year':latest}
    for theme, settings in config['columns'].items():
        branches = copy.deepcopy(settings['branches'])
        families = {}
        for branch in branches:
            for family in branch['families'].split():
                assert family not in families, f'Duplicate tree family: {theme} {family}'
                families[family] = branch['id']
            del branch['families']
        branches.append({'id':'related','label':'Related methods & resources','color':'#6c7d8e','summary':'Studies linked from another column, using the repository’s existing classifications.'})
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
            primary = signal['route'] == theme
            if (not primary and theme not in signal['secondary_routes']) or any(id in present for id in signal['registry_ids']):
                continue
            branch = settings['signal_branches'].get(signal['id']) if primary else 'related'
            assert branch in ids, f'Unmapped source update: {theme} {signal["id"]}'
            year = int(signal['event_date'][:4])
            period = next(i for i, p in enumerate(periods) if p['start'] <= year <= p['end'])
            nodes.append({'id':'signal-' + signal['id'], 'branch':branch, 'period':period, 'related':not primary, 'featured':True})
        assert len(nodes) == len({n['id'] for n in nodes})
        expected = {r['id'] for r in payload['records'] if r['primary_route'] == theme}
        assert {n['id'] for n in nodes if not n['related'] and not n['id'].startswith('signal-')} == expected
        assert set(settings['lanes']) == {'top', 'bottom'}
        result['columns'][theme] = {'branches':branches, 'nodes':nodes, 'lanes':copy.deepcopy(settings['lanes'])}
    return result
