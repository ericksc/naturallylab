"""Check the proposal's example package, without executing notebook code."""
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1] / 'docs/proposals/examples'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load(path):
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    require(isinstance(data, dict), f'{path}: expected a mapping')
    require(type(data.get('schema_version')) is int and data['schema_version'] == 1,
            f'{path}: unsupported schema_version')
    require(isinstance(data.get('id'), str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', data['id']),
            f'{path}: invalid id')
    require(isinstance(data.get('version'), str) and re.fullmatch(r'\d+\.\d+\.\d+', data['version']),
            f'{path}: version must be a semantic-version string')
    return data

def file_ref(base, name):
    require(isinstance(name, str), 'file reference must be text')
    relative = Path(name)
    require(not relative.is_absolute() and '..' not in relative.parts, f'unsafe path: {name}')
    path = base / relative
    require(not any(p.is_symlink() for p in [path, *path.parents] if p != base.parent),
            f'symlink reference: {name}')
    require(path.resolve().is_relative_to(base.resolve()) and path.is_file(), f'missing or unsafe file: {name}')
    return path

course = load(ROOT / 'course.yaml')
session = load(ROOT / 'session.yaml')
require(course['sessions'] == [{'id': session['id'], 'version': session['version']}],
        'course session ID/version does not resolve')
require(session['estimated_minutes'] == sum(a['estimated_minutes'] for a in session['activities']),
        'session activity durations do not add up')
activity_ids = [a['id'] for a in session['activities']]
require(len(activity_ids) == len(set(activity_ids)), 'duplicate activity ID')
for activity in session['activities']:
    if activity['type'] == 'reading':
        file_ref(ROOT, activity['content'])
    elif activity['type'] == 'lab':
        ref = activity['lab']
        require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ref['id']), 'unsafe lab ID')
        base = ROOT / 'labs' / ref['id']
        lab = load(base / 'lab.yaml')
        require(lab['id'] == ref['id'] and lab['version'] == ref['version'], 'lab version does not resolve')
        ids = [s['id'] for s in lab['steps']]
        require(len(ids) == len(set(ids)), 'duplicate step ID')
        for step in lab['steps']:
            file_ref(base, step['instructions'])
        notebook = json.loads(file_ref(base, lab['workspace']['notebook']).read_text())
        require(notebook['nbformat'] == 4 and isinstance(notebook['cells'], list), 'invalid notebook structure')
        require(all(not c.get('outputs') and c.get('execution_count') is None
                    for c in notebook['cells'] if c['cell_type'] == 'code'), 'starter notebook contains outputs')
    else:
        raise ValueError('unknown activity type')
print('PASS: course/session/lab versions, durations, unique IDs, safe paths, Markdown references and starter notebook.')
print('Scope: illustrative package only; no production publisher or Docker infrastructure tested.')
