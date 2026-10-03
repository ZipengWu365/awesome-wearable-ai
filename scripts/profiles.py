"""Additive source-linked profiles; imported candidates never enter accepted counts."""
from pathlib import Path
import hashlib
import json
from jsonschema import Draft202012Validator
from .registry import ROOT

def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def load_profiles(root=ROOT):
    base=root/'data/profiles'
    return {name:load_json(base/f'{name}.json') for name in ('resources','sources','causal','digital_twin')}

def record_hash(row):
    public={k:v for k,v in row.items() if not k.startswith('_')}
    return hashlib.sha256(json.dumps(public,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def validate_profiles(records, watchlist, root=ROOT):
    errors=[]
    profiles=load_profiles(root)
    candidates=load_json(root/'data/imports/local_candidates.json')
    accepted={r['id']:r for r in records}
    targets=set(accepted)|{r['id'] for r in watchlist}
    pending={r['record_id'] for r in candidates}
    if targets & pending: errors.append('import candidates overlap accepted/watchlist IDs')
    sources={s['id']:s for s in profiles['sources']}
    if len(sources)!=len(profiles['sources']): errors.append('duplicate profile source ID')
    source_schema=load_json(root/'schema/profiles/sources.schema.json')
    errors.extend(f'sources: {e.message}' for e in Draft202012Validator(source_schema).iter_errors(profiles['sources']))
    for name in ('causal','digital_twin'):
        rows=profiles[name]
        clean=[{k:v for k,v in r.items() if k not in ('local_record_id','imported_from')} for r in rows]
        schema=load_json(root/f'schema/profiles/{name}_profiles.schema.json')
        errors.extend(f'{name}: {e.message}' for e in Draft202012Validator(schema).iter_errors(clean))
        for row in rows:
            if row['record_id'] not in targets|pending: errors.append(f'{name}: missing target {row["record_id"]}')
            if set(row['source_ids'])-sources.keys(): errors.append(f'{name}: missing source for {row["record_id"]}')
        local_ids=[r['local_record_id'] for r in rows]
        if len(local_ids)!=len(set(local_ids)): errors.append(f'{name}: duplicate local profile ID')
    imported=profiles['resources']+candidates
    if len({r['local_id'] for r in imported})!=len(imported): errors.append('duplicate imported resource')
    validators={k:Draft202012Validator(load_json(root/f'schema/profiles/{k}.schema.json')) for k in ('datasets','models','papers','biomarkers','benchmarks','tools','devices','surveys')}
    for row in imported:
        if row['record_id'] not in targets|pending: errors.append(f'missing resource target {row["record_id"]}')
        m=row['metadata'];kind=m['local_kind'];clean={k:v for k,v in m.items() if k!='local_kind'}
        errors.extend(f'{row["local_id"]}: {e.message}' for e in validators[kind].iter_errors([clean]))
        if set(m['source_ids'])-sources.keys(): errors.append(f'{row["local_id"]}: missing sources')
        for field,ids in m['field_sources'].items():
            if not ids or set(ids)-set(m['source_ids']):errors.append(f'{row["local_id"]}: invalid field sources for {field}')
    manifest=load_json(root/'data/imports/migration.json')
    for id,expected in manifest['original_record_hashes'].items():
        expected=manifest['allowed_existing_changes'].get(id,{}).get('expected_hash',expected)
        if id not in accepted or record_hash(accepted[id])!=expected:
            errors.append(f'preservation: original record changed without documented migration: {id}')
    watch_by_id={r['id']:r for r in watchlist}
    for id,expected in manifest['original_watchlist_hashes'].items():
        if id not in watch_by_id or record_hash(watch_by_id[id])!=expected:
            errors.append(f'preservation: original watchlist changed: {id}')
    return errors

def public_profiles(records, watchlist):
    data=load_profiles()
    visible={r['id'] for r in records+watchlist}
    for key in ('resources','causal','digital_twin'):
        data[key]=[r for r in data[key] if r['record_id'] in visible]
    data['statistics']={
        'digital_twin_profiles':len(data['digital_twin']),
        'causal_profiles':len(data['causal']),
        'resource_profiles':len(data['resources']),
        'pending_import_resources':len(load_json(ROOT/'data/imports/local_candidates.json')),
    }
    return data
