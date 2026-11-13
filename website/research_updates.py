"""Add dated website reading notes without rewriting registry records."""
import copy
from datetime import date


def merge_updates(radar, additions):
    result = copy.deepcopy(radar)
    reviewed = date.fromisoformat(additions['reviewed_on'])
    assert reviewed >= date.fromisoformat(radar['reviewed_on'])
    prior_ids = {item['id'] for item in radar['signals']}
    new_ids = [item['id'] for item in additions['signals']]
    assert len(new_ids) == len(set(new_ids)), 'Duplicate new paper ID'
    assert not prior_ids.intersection(new_ids), 'A reading note already exists'
    for item in additions['signals']:
        assert item['added_on'] == additions['reviewed_on']
        assert item['venue'] and item['publication_status'] and item['short_name']
    result.update({key:copy.deepcopy(additions[key]) for key in
                   ('reviewed_on', 'window', 'coverage_note', 'assessments')})
    result['signals'].extend(copy.deepcopy(additions['signals']))
    return result
