#!/usr/bin/env python3
"""Offline run bookkeeping and raster inspection; never generates images."""
import argparse
import hashlib
import json
import os
import re
import sys
import uuid
import warnings
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

CRITERIA = {'objective', 'text_facts', 'composition', 'brand_reference',
            'visual_integrity', 'preservation', 'transparency'}
STATES = {'prepared', 'generated', 'needs_revision', 'approved', 'blocked', 'failed'}
ROLES = {'reference', 'edit-target', 'insert', 'brand-kit'}
USE_CASES = set('photorealistic-natural product-mockup ui-mockup infographic-diagram '
                'scientific-educational ads-marketing productivity-visual logo-brand '
                'illustration-story stylized-concept historical-scene text-localization '
                'identity-preserve precise-object-edit lighting-weather background-extraction '
                'style-transfer compositing sketch-to-render'.split())


def now():
    return datetime.now(timezone.utc).isoformat()


def safe_path(value):
    p = Path(value).expanduser()
    if '..' in p.parts:
        raise ValueError('Parent traversal is not allowed')
    p = p.absolute()
    for part in (p, *p.parents):
        if part.is_symlink():
            raise ValueError('Symlink paths are not allowed')
    return p


def inside(root, relative):
    """Return one absolute path that is strictly inside a confined root."""
    root = safe_path(root)
    relative = Path(relative)
    if relative.is_absolute():
        raise ValueError('Manifest paths must be relative')
    if not relative.parts:
        raise ValueError('Manifest paths must stay inside the run')
    if any(part == '..' for part in relative.parts):
        raise ValueError('Parent traversal is not allowed')
    result = safe_path(root / relative)
    if result == root or not result.is_relative_to(root):
        raise ValueError('Manifest paths must stay inside the run')
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(safe_path(path).read_text(encoding='utf-8'))


def write_new(path, data):
    with safe_path(path).open('xb') as f:
        f.write(data)


def save(run, m):
    target = inside(run, 'manifest.json')
    m['updated_at'] = now()
    data = json.dumps(m, ensure_ascii=False, indent=2).encode('utf-8')
    # Same-directory replacement avoids a partially written manifest.
    temp = inside(run, '.manifest-' + uuid.uuid4().hex + '.tmp')
    try:
        # Set owner-only access at exclusive creation, before any brief bytes.
        with open(temp, 'xb', opener=lambda path, flags: os.open(path, flags, 0o600)) as f:
            f.write(data)
        temp.chmod(0o600)
        temp.replace(target)
    finally:
        if temp.exists():
            temp.unlink()


def inspect(path, transparent=False):
    path = safe_path(path)
    if not path.is_file():
        raise ValueError('Image source must be an existing regular file')
    data = path.read_bytes()
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(path) as im:
            if im.format not in {'PNG', 'JPEG', 'WEBP'}:
                raise ValueError('Only PNG, JPEG and WebP are supported')
            if getattr(im, 'n_frames', 1) != 1:
                raise ValueError('Animated images are not supported')
            im.load()
            rgba = im.convert('RGBA')
            histogram = rgba.getchannel('A').histogram()
            visible = sum(histogram[1:])
            if not visible:
                raise ValueError('Image is entirely transparent')
            has_alpha = 'A' in im.getbands() or 'transparency' in im.info
            if transparent and (not has_alpha or not histogram[0]):
                raise ValueError('Requested transparency requires actual transparent pixels')
            return {'format': im.format, 'width': im.width, 'height': im.height,
                    'bytes': len(data), 'sha256': digest(data), 'has_alpha': has_alpha,
                    'transparent_pixels': histogram[0], 'visible_pixels': visible}


def validate_brief(b):
    if not isinstance(b, dict):
        raise ValueError('Brief must be an object')
    for key in ('purpose', 'audience', 'intended_use'):
        if not isinstance(b.get(key), str) or not b[key].strip():
            raise ValueError('Missing brief field: ' + key)
    if b.get('use_case') not in USE_CASES:
        raise ValueError('Unknown imagegen use_case')
    if type(b.get('variants')) is not int or not 1 <= b['variants'] <= 20:
        raise ValueError('variants must be an integer from 1 to 20')
    if not isinstance(b.get('text'), str) or type(b.get('transparent')) is not bool:
        raise ValueError('text must be a string and transparent a boolean')
    for key in ('constraints', 'acceptance'):
        if not isinstance(b.get(key), list) or not b[key] or any(
                not isinstance(x, str) or not x.strip() for x in b[key]):
            raise ValueError(key + ' must contain nonempty strings')
    if 'brand_kit' not in b or (b['brand_kit'] is not None and not isinstance(b['brand_kit'], str)):
        raise ValueError('brand_kit must be a path or null')
    refs = b.get('references')
    if not isinstance(refs, list):
        raise ValueError('references must be an array')
    refs = list(refs)
    if b['brand_kit'] is not None:
        refs.append({'path': b['brand_kit'], 'role': 'brand-kit'})
    for ref in refs:
        if not isinstance(ref, dict) or ref.get('role') not in ROLES:
            raise ValueError('Every reference requires a supported role')
        if not isinstance(ref.get('path'), str) or not Path(ref['path']).is_absolute():
            raise ValueError('Reference paths must be absolute')
        p = safe_path(ref['path'])
        if not p.is_file():
            raise ValueError('Reference is not a regular file')
        if ref['role'] != 'brand-kit':
            inspect(p)
    return refs


def prepare(args):
    b = read_json(args.brief)
    refs = validate_brief(b)
    root = safe_path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    run = root / run_id
    run.mkdir()
    for folder in ('inputs', 'work', 'final'):
        (run / folder).mkdir()
    inputs = []
    for index, ref in enumerate(refs):
        source = safe_path(ref['path'])
        data = source.read_bytes()
        # Keep the useful extension; never use input basenames as output paths.
        suffix = source.suffix if re.fullmatch(r'\.[A-Za-z0-9]{1,10}', source.suffix) else '.bin'
        rel = f'inputs/ref-{index + 1}{suffix}'
        write_new(inside(run, rel), data)
        inputs.append({'path': rel, 'role': ref['role'], 'sha256': digest(data)})
    m = {'schema_version': 1, 'run_id': run_id, 'created_at': now(),
         'surface': args.surface, 'cli_version': args.cli_version, 'mode': 'built-in',
         'brief': b, 'inputs': inputs, 'outputs': [], 'state': 'prepared', 'error': None}
    save(run, m)
    return {'run': str(run), 'manifest': str(run / 'manifest.json'), 'state': m['state']}


def validate_manifest(m):
    """Check the shape commands read. Do not reopen original reference files."""
    if not isinstance(m, dict):
        raise ValueError('Manifest must be an object')
    if m.get('schema_version') != 1 or m.get('mode') != 'built-in':
        raise ValueError('Unsupported manifest')
    if m.get('state') not in STATES:
        raise ValueError('Malformed manifest')
    brief = m.get('brief')
    inputs = m.get('inputs')
    outputs = m.get('outputs')
    if not isinstance(brief, dict) or not isinstance(inputs, list) or not isinstance(outputs, list):
        raise ValueError('Malformed manifest')
    if type(brief.get('transparent')) is not bool or type(brief.get('variants')) is not int:
        raise ValueError('Malformed manifest')
    if not isinstance(brief.get('text'), str):
        raise ValueError('Malformed manifest')
    for item in inputs:
        if not isinstance(item, dict) or item.get('role') not in ROLES:
            raise ValueError('Malformed manifest')
        if not isinstance(item.get('path'), str) or not isinstance(item.get('sha256'), str):
            raise ValueError('Malformed manifest')
    required = applicable_criteria(brief, inputs)
    for item in outputs:
        if not isinstance(item, dict) or not isinstance(item.get('metadata'), dict) or 'review' not in item:
            raise ValueError('Malformed manifest')
        for key in ('path', 'prompt_path', 'prompt_sha256'):
            if not isinstance(item.get(key), str):
                raise ValueError('Malformed manifest')
        history = item.get('review_history', [])
        if not isinstance(history, list):
            raise ValueError('Malformed review history')
        if item['review'] is not None:
            checked_review(item['review'], required)
        for stored in history:
            checked_review(stored, required)
    return m


def load(run_value):
    run = safe_path(run_value)
    return run, validate_manifest(read_json(inside(run, 'manifest.json')))


def verify_manifest(run, m):
    for item in m['inputs']:
        if digest(inside(run, item['path']).read_bytes()) != item['sha256']:
            raise ValueError('Input snapshot hash mismatch')
    for item in m['outputs']:
        if inspect(inside(run, item['path']), m['brief']['transparent']) != item['metadata']:
            raise ValueError('Output metadata/hash mismatch')
        if digest(inside(run, item['prompt_path']).read_bytes()) != item['prompt_sha256']:
            raise ValueError('Prompt snapshot hash mismatch')


def collect(args):
    run, m = load(args.run)
    verify_manifest(run, m)
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', args.name):
        raise ValueError('Invalid asset name')
    source = safe_path(args.source)
    metadata = inspect(source, m['brief']['transparent'])
    data = source.read_bytes()
    if digest(data) != metadata['sha256']:
        raise ValueError('Source changed during inspection')
    prompt = safe_path(args.prompt).read_text(encoding='utf-8')
    if not prompt.strip():
        raise ValueError('Submitted prompt must not be empty')
    extension = {'PNG': '.png', 'JPEG': '.jpg', 'WEBP': '.webp'}[metadata['format']]
    # Exclusive creation preserves earlier outputs even on a name collision.
    version = 1
    while True:
        name = args.name + (f'-v{version}' if version > 1 else '') + extension
        target = inside(run, 'final/' + name)
        try:
            write_new(target, data)
            break
        except FileExistsError:
            version += 1
    prompt_rel = 'work/prompt-' + str(uuid.uuid4()) + '.txt'
    encoded = prompt.encode('utf-8')
    write_new(inside(run, prompt_rel), encoded)
    m['outputs'].append({'path': 'final/' + name, 'metadata': metadata,
                         'prompt_path': prompt_rel, 'prompt_sha256': digest(encoded), 'review': None})
    m['state'], m['error'] = 'generated', None
    save(run, m)
    return {'asset': name, 'state': m['state'], 'metadata': metadata}


def applicable_criteria(brief, inputs):
    """Criteria that cannot be na for this brief. Core three are always required."""
    required = {'objective', 'composition', 'visual_integrity'}
    if brief['text']:
        required.add('text_facts')
    if inputs:
        required.add('brand_reference')
    if any(item['role'] == 'edit-target' for item in inputs):
        required.add('preservation')
    if brief['transparent']:
        required.add('transparency')
    return required


def checked_review(payload, required):
    """Validate a review document. Does not read the clock or the filesystem."""
    if not isinstance(payload, dict) or not isinstance(payload.get('reviewer'), str) or not payload['reviewer'].strip():
        raise ValueError('Reviewer required')
    criteria = payload.get('criteria')
    if not isinstance(criteria, dict) or set(criteria) != CRITERIA:
        raise ValueError('Review must contain all seven rubric criteria')
    for key, entry in criteria.items():
        if not isinstance(entry, dict):
            raise ValueError('Invalid criterion')
        score = entry.get('score')
        if not ((type(score) is int and score in (0, 1, 2)) or score == 'na'):
            raise ValueError('Score must be 0, 1, 2 or na')
        if not isinstance(entry.get('evidence'), str) or not entry['evidence'].strip():
            raise ValueError('Evidence/reason required for every criterion')
        if key in required and score == 'na':
            raise ValueError('Applicable criterion cannot be na: ' + key)
    return {'reviewer': payload['reviewer'], 'criteria': criteria}


def approval_state(outputs, variants):
    """approved only when every collected output passes and the count matches."""
    passed = all(item['review'] is not None and all(
        entry['score'] in (2, 'na') for entry in item['review']['criteria'].values()) for item in outputs)
    return 'approved' if passed and len(outputs) == variants else 'needs_revision'


def review(args):
    run, m = load(args.run)
    verify_manifest(run, m)
    if Path(args.asset).name != args.asset:
        raise ValueError('Review asset must be a filename')
    item = next((x for x in m['outputs'] if x['path'] == 'final/' + args.asset), None)
    if item is None:
        raise ValueError('Unknown asset')
    checked = checked_review(read_json(args.review), applicable_criteria(m['brief'], m['inputs']))
    if item['review'] is not None:
        item.setdefault('review_history', []).append(item['review'])
    item['review'] = {**checked, 'reviewed_at': now()}
    m['state'] = approval_state(m['outputs'], m['brief']['variants'])
    m['error'] = None
    save(run, m)
    return {'state': m['state'], 'asset': args.asset}


def status(args):
    run, m = load(args.run)
    if args.state not in {'blocked', 'failed'}:
        raise ValueError('Status cannot force approval')
    if not args.reason.strip():
        raise ValueError('Reason required')
    m['state'], m['error'] = args.state, args.reason.strip()
    save(run, m)
    return {'state': m['state']}


def verify(args):
    run, m = load(args.run)
    verify_manifest(run, m)
    return {'valid': True, 'state': m['state'], 'outputs': len(m['outputs'])}


COMMANDS = {'prepare': prepare, 'collect': collect, 'review': review, 'verify': verify, 'status': status}


def emit_error(message):
    print(json.dumps({'error': message}), file=sys.stderr)


class JsonArgumentParser(argparse.ArgumentParser):
    """Parser failures use the same stderr JSON object and exit code as runtime failures."""

    def error(self, message):
        emit_error(message)
        self.exit(2)


def main():
    parser = JsonArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True, parser_class=JsonArgumentParser)
    p = sub.add_parser('prepare')
    p.add_argument('--root', required=True)
    p.add_argument('--brief', required=True)
    p.add_argument('--surface', choices=['desktop', 'exec'], required=True)
    p.add_argument('--cli-version', default=None)
    for cmd in ('collect', 'review', 'verify', 'status'):
        p = sub.add_parser(cmd)
        p.add_argument('--run', required=True)
        if cmd == 'collect':
            for arg in ('source', 'prompt', 'name'):
                p.add_argument('--' + arg, required=True)
        elif cmd == 'review':
            p.add_argument('--asset', required=True)
            p.add_argument('--review', required=True)
        elif cmd == 'status':
            p.add_argument('--state', choices=['blocked', 'failed'], required=True)
            p.add_argument('--reason', required=True)
    args = parser.parse_args()
    try:
        command = COMMANDS.get(args.command)
        if command is None:
            raise ValueError('Unknown command')
        result = command(args)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, Image.DecompressionBombError,
            Image.DecompressionBombWarning) as error:
        # Avoid dumping filesystem paths or arbitrary reference content into logs.
        message = str(error) if isinstance(error, ValueError) else type(error).__name__
        emit_error(message)
        return 2


if __name__ == '__main__':
    sys.exit(main())
