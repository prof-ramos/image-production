#!/usr/bin/env python3
"""Offline run bookkeeping and raster inspection; never generates images."""
import argparse
from copy import deepcopy
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
REVIEW_POLICY = 'independent-dual-role-v1'
ATTEMPT_POLICY = 'stable-asset-lineage-v1'
REVIEW_ROLES = {'technical', 'visual'}

ROLES = {'reference', 'edit-target', 'insert', 'brand-kit'}
USE_CASES = set('photorealistic-natural product-mockup ui-mockup infographic-diagram '
                'scientific-educational ads-marketing productivity-visual logo-brand '
                'illustration-story stylized-concept historical-scene text-localization '
                'identity-preserve precise-object-edit lighting-weather background-extraction '
                'style-transfer compositing sketch-to-render'.split())


def now():
    return datetime.now(timezone.utc).isoformat()


def safe_path(value):
    try:
        p = Path(value).expanduser()
    except RuntimeError as error:
        raise ValueError('Cannot resolve home directory') from error
    if '..' in p.parts:
        raise ValueError('Parent traversal is not allowed')
    p = p.absolute()
    for part in (p, *p.parents):
        if part.is_symlink():
            raise ValueError('Symlink paths are not allowed')
    return p


def relative_path(relative):
    """Validate manifest path syntax without requiring its artifact to exist."""
    relative = Path(relative)
    if relative.is_absolute():
        raise ValueError('Manifest paths must be relative')
    if not relative.parts:
        raise ValueError('Manifest paths must stay inside the run')
    if any(part == '..' for part in relative.parts):
        raise ValueError('Parent traversal is not allowed')
    if '\x00' in str(relative):
        raise ValueError('Manifest paths must not contain null bytes')
    return relative


def inside(root, relative):
    """Return one absolute path that is strictly inside a confined root."""
    root = safe_path(root)
    relative = relative_path(relative)
    result = safe_path(root / relative)
    if result == root or not result.is_relative_to(root):
        raise ValueError('Manifest paths must stay inside the run')
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    try:
        return json.loads(safe_path(path).read_text(encoding='utf-8'))
    except RecursionError as error:
        raise ValueError('JSON nesting is too deep') from error


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
    try:
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
    except (SyntaxError, EOFError) as error:
        raise ValueError('Image could not be decoded') from error


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


def atomic_json(path, payload):
    """Persist coordinator-owned lineage state with private, atomic replacement."""
    path = safe_path(path)
    temp = safe_path(path.parent / ('.lineage-' + uuid.uuid4().hex + '.tmp'))
    try:
        with open(temp, 'xb', opener=lambda name, flags: os.open(name, flags, 0o600)) as stream:
            stream.write(json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8'))
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


def lineage_path(root, key):
    return inside(root, '.lineages/' + digest(key.encode('utf-8')) + '.json')


def checked_asset_keys(keys, variants):
    if isinstance(keys, str):
        keys = [keys]
    if (not isinstance(keys, list) or len(keys) != variants
            or any(not isinstance(key, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', key)
                   for key in keys) or len(set(keys)) != len(keys)):
        raise ValueError('Provide one unique --asset-key per variant; reuse its lineage via --continue-from')
    return keys


class AssetReservations:
    """Root-owned attempt budget; disk failures deliberately never refund it.

    Commands select/check before inspecting a candidate, then consume before
    writing its files. Ledger details and continuation rules stay here.
    """

    def __init__(self, root):
        self.root = root

    def _read(self, key):
        ledger = read_json(lineage_path(self.root, key))
        if (not isinstance(ledger, dict) or ledger.get('asset_key') != key
                or not isinstance(ledger.get('attempts'), list) or not 1 <= len(ledger['attempts']) <= 3):
            raise ValueError('Malformed asset lineage')
        seen = set()
        for index, entry in enumerate(ledger['attempts']):
            if (not isinstance(entry, dict) or not isinstance(entry.get('run_id'), str)
                    or entry['run_id'] in seen or type(entry.get('ordinal')) is not int or entry['ordinal'] != index
                    or type(entry.get('collected')) is not bool):
                raise ValueError('Malformed asset lineage')
            seen.add(entry['run_id'])
        return ledger

    def reserve(self, variants, supplied=None, continuation=None):
        root = self.root
        previous = None
        if continuation:
            previous_run, previous = load(continuation)
            if previous_run.parent != root:
                raise ValueError('Continuation must use the same output root')
            verify_manifest(previous_run, previous)
            if previous.get('attempt_policy') != ATTEMPT_POLICY:
                raise ValueError('Legacy run has no stable asset lineage; audit its historical attempts before migration')
            inherited = [asset['asset_key'] for asset in previous['assets']]
            keys = checked_asset_keys(supplied if supplied is not None else inherited, variants)
            if any(key not in inherited for key in keys):
                raise ValueError('Continuation can only select existing asset keys; do not rename them')
        else:
            keys = checked_asset_keys(supplied, variants)
        root.mkdir(parents=True, exist_ok=True)
        ledgers = []
        for key in keys:
            path = lineage_path(root, key)
            if previous is None:
                if path.exists():
                    raise ValueError('Asset key already exists; use --continue-from to retain correction history')
                ledger = {'asset_key': key, 'attempts': []}
            else:
                ledger = self._read(key)
                if ledger['attempts'][-1]['run_id'] != previous['run_id']:
                    raise ValueError('Continue from the latest attempt, not an older run')
                if len(ledger['attempts']) >= 3:
                    raise ValueError('Asset correction limit reached: initial attempt plus two corrections')
            ledgers.append(ledger)
        run_id = str(uuid.uuid4())
        assets = [{'asset_key': key, 'attempt': len(ledger['attempts'])}
                  for key, ledger in zip(keys, ledgers)]
        # Reserve before returning permission to generate; failures never refund attempts.
        inside(root, '.lineages').mkdir(mode=0o700, exist_ok=True)
        for ledger in ledgers:
            ledger['attempts'].append({'run_id': run_id, 'ordinal': len(ledger['attempts']),
                                       'collected': False, 'reserved_at': now()})
            atomic_json(lineage_path(root, ledger['asset_key']), ledger)
        return run_id, assets

    def verify(self, manifest):
        if manifest.get('attempt_policy') != ATTEMPT_POLICY:
            return
        for asset in manifest['assets']:
            ledger = self._read(asset['asset_key'])
            reservation = next((entry for entry in ledger['attempts']
                                if entry['run_id'] == manifest['run_id']), None)
            if reservation is None or reservation['ordinal'] != asset['attempt']:
                raise ValueError('Missing or inconsistent asset reservation; preserve the output root lineage')
            outputs = [item for item in manifest['outputs'] if item['asset_key'] == asset['asset_key']]
            if outputs and (not reservation['collected'] or reservation.get('sha256') != outputs[0]['metadata']['sha256']):
                raise ValueError('Asset reservation does not match collected candidate')

    def _uncollected(self, manifest, key):
        if manifest.get('attempt_policy') != ATTEMPT_POLICY:
            raise ValueError('Legacy collection requires audited migration to a stable asset lineage')
        if key is None and len(manifest['assets']) == 1:
            key = manifest['assets'][0]['asset_key']
        if key not in [asset['asset_key'] for asset in manifest['assets']]:
            raise ValueError('Select a reserved --asset-key for this run')
        ledger = self._read(key)
        reservation = next(entry for entry in ledger['attempts'] if entry['run_id'] == manifest['run_id'])
        if reservation['collected']:
            raise ValueError('Asset reservation already collected; prepare a continuation before another generation')
        return key, ledger, reservation

    def select(self, manifest, key=None):
        return self._uncollected(manifest, key)[0]

    def consume(self, manifest, key, candidate_sha256):
        key, ledger, reservation = self._uncollected(manifest, key)
        reservation.update(collected=True, sha256=candidate_sha256)
        atomic_json(lineage_path(self.root, key), ledger)


def prepare(args):
    b = read_json(args.brief)
    refs = validate_brief(b)
    root = safe_path(args.root)
    run_id, assets = AssetReservations(root).reserve(
        b['variants'], getattr(args, 'asset_key', None), getattr(args, 'continue_from', None))
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
         'brief': b, 'inputs': inputs, 'outputs': [], 'state': 'prepared', 'error': None,
         'review_policy': REVIEW_POLICY, 'attempt_policy': ATTEMPT_POLICY, 'assets': assets}
    save(run, m)
    return {'run': str(run), 'manifest': str(run / 'manifest.json'), 'state': m['state'],
            'assets': assets, 'review_policy': REVIEW_POLICY}


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
    if (type(brief.get('transparent')) is not bool or type(brief.get('variants')) is not int
            or not 1 <= brief['variants'] <= 20):
        raise ValueError('Malformed manifest')
    if not isinstance(brief.get('text'), str):
        raise ValueError('Malformed manifest')
    for item in inputs:
        if not isinstance(item, dict) or item.get('role') not in ROLES:
            raise ValueError('Malformed manifest')
        if not isinstance(item.get('path'), str) or not isinstance(item.get('sha256'), str):
            raise ValueError('Malformed manifest')
        relative_path(item['path'])
    required = applicable_criteria(brief, inputs)
    policy = m.get('review_policy', 'legacy-single-review-historical')
    if policy not in {REVIEW_POLICY, 'legacy-single-review-historical'}:
        raise ValueError('Unsupported review policy')
    assets = m.get('assets')
    if 'attempt_policy' in m:
        if policy != REVIEW_POLICY:
            raise ValueError('Reserved runs require independent dual-role review policy')
        if m['attempt_policy'] != ATTEMPT_POLICY or not isinstance(assets, list):
            raise ValueError('Malformed asset reservations')
        if any(not isinstance(asset, dict) for asset in assets):
            raise ValueError('Malformed asset reservation')
        checked_asset_keys([asset.get('asset_key') for asset in assets], brief['variants'])
        if any(type(asset.get('attempt')) is not int or not 0 <= asset['attempt'] <= 2 for asset in assets):
            raise ValueError('Malformed asset reservation')
    output_paths = set()
    output_assets = set()
    for item in outputs:
        if not isinstance(item, dict) or not isinstance(item.get('metadata'), dict) or 'review' not in item:
            raise ValueError('Malformed manifest')
        for key in ('path', 'prompt_path', 'prompt_sha256'):
            if not isinstance(item.get(key), str):
                raise ValueError('Malformed manifest')
        path = relative_path(item['path'])
        relative_path(item['prompt_path'])
        if path in output_paths:
            raise ValueError('Duplicate output path in manifest')
        output_paths.add(path)
        if 'attempt_policy' in m:
            key = item.get('asset_key')
            if key not in [asset['asset_key'] for asset in assets] or key in output_assets:
                raise ValueError('Each asset reservation permits one collected candidate per run')
            output_assets.add(key)
        checked_candidate_reviews(item, required, policy)
    if m['state'] == 'approved' and approval_state(outputs, brief['variants'], policy) != 'approved':
        raise ValueError('Approved state requires all variants and passing reviews')
    return m


def load(run_value):
    run = safe_path(run_value)
    return run, validate_manifest(read_json(inside(run, 'manifest.json')))


def verify_manifest(run, m):
    AssetReservations(run.parent).verify(m)
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
    reservations = AssetReservations(run.parent)
    key = reservations.select(m, getattr(args, 'asset_key', None))
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', args.name):
        raise ValueError('Invalid asset name')
    source = safe_path(args.source)
    metadata = inspect(source, m['brief']['transparent'])
    data = source.read_bytes()
    if digest(data) != metadata['sha256']:
        raise ValueError('Source changed during inspection')
    encoded = safe_path(args.prompt).read_bytes()
    if not encoded.decode('utf-8').strip():
        raise ValueError('Submitted prompt must not be empty')
    reservations.consume(m, key, metadata['sha256'])
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
    write_new(inside(run, prompt_rel), encoded)
    m['outputs'].append({'path': 'final/' + name, 'metadata': metadata,
                         'prompt_path': prompt_rel, 'prompt_sha256': digest(encoded), 'review': None,
                         'reviews': {}, 'asset_key': key})
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
    return {'reviewer': payload['reviewer'].strip(), 'criteria': criteria}


def checked_role_review(payload, required, role, candidate_sha256):
    checked = checked_review(payload, required)
    if payload.get('role') != role or role not in REVIEW_ROLES:
        raise ValueError('Review role must be technical or visual')
    if payload.get('candidate_sha256') != candidate_sha256 or not isinstance(candidate_sha256, str):
        raise ValueError('Review must identify the current candidate SHA256')
    return {**checked, 'role': role, 'candidate_sha256': candidate_sha256}


def checked_candidate_reviews(item, required, policy):
    """One policy for persisted reports and proposed review replacements."""
    if policy == REVIEW_POLICY:
        reports = item.get('reviews', {})
        if not isinstance(reports, dict) or set(reports) - REVIEW_ROLES:
            raise ValueError('Malformed independent reviews')
        for role, report in reports.items():
            checked_role_review(report, required, role, item['metadata'].get('sha256'))
        if len(reports) == 2 and reports['technical']['reviewer'] == reports['visual']['reviewer']:
            raise ValueError('Independent review roles require distinct reviewers')
        if (reports and item['review'] is None) or (item['review'] is not None and item['review'] not in reports.values()):
            raise ValueError('Latest review must match a persisted role report')
    history = item.get('review_history', [])
    if not isinstance(history, list):
        raise ValueError('Malformed review history')
    if item['review'] is not None:
        checked_review(item['review'], required)
    for stored in history:
        checked_review(stored, required)


def approval_state(outputs, variants, policy=REVIEW_POLICY):
    """Separate passing technical and visual reports for every current candidate."""
    if policy == 'legacy-single-review-historical':
        passed = all(item['review'] is not None and all(
            entry['score'] in (2, 'na') for entry in item['review']['criteria'].values()) for item in outputs)
    else:
        passed = True
        for item in outputs:
            reports = item.get('reviews', {})
            if set(reports) != REVIEW_ROLES:
                passed = False
                break
            if reports['technical']['reviewer'] == reports['visual']['reviewer']:
                passed = False
                break
            if any(report.get('candidate_sha256') != item['metadata']['sha256'] or any(
                    entry['score'] not in (2, 'na') for entry in report['criteria'].values())
                   for report in reports.values()):
                passed = False
                break
    return 'approved' if passed and len(outputs) == variants else 'needs_revision'


def review_candidate(manifest, asset):
    """Validate the requested candidate before reading a submitted report."""
    if Path(asset).name != asset:
        raise ValueError('Review asset must be a filename')
    item = next((x for x in manifest['outputs'] if x['path'] == 'final/' + asset), None)
    if item is None:
        raise ValueError('Unknown asset')
    return item


def reviewed_manifest(manifest, asset, payload, reviewed_at):
    """Return a new review state from a validated manifest, without clock or disk I/O.

    Own migration, role replacement, history and approval together. The caller
    supplies the timestamp; accepted and rejected updates both leave inputs intact.
    """
    m = deepcopy(manifest)
    item = review_candidate(m, asset)
    if not isinstance(payload, dict):
        raise ValueError('Review must be an object')
    required = applicable_criteria(m['brief'], m['inputs'])
    checked = checked_role_review(deepcopy(payload), required,
                                  payload.get('role'), item['metadata']['sha256'])
    if m.get('review_policy') != REVIEW_POLICY:
        # Historical approvals remain readable, but a new review starts a new gate.
        for output in m['outputs']:
            if output['review'] is not None:
                output.setdefault('review_history', []).append(output['review'])
            output['review'], output['reviews'] = None, {}
        m['review_policy'] = REVIEW_POLICY
    reports = item.setdefault('reviews', {})
    if item['review'] is not None:
        item.setdefault('review_history', []).append(item['review'])
    item['review'] = {**checked, 'reviewed_at': reviewed_at}
    reports[checked['role']] = item['review']
    checked_candidate_reviews(item, required, REVIEW_POLICY)
    m['state'] = approval_state(m['outputs'], m['brief']['variants'])
    m['error'] = None
    return m


def review(args):
    run, m = load(args.run)
    verify_manifest(run, m)
    review_candidate(m, args.asset)
    m = reviewed_manifest(m, args.asset, read_json(args.review), now())
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
    result = {'valid': True, 'state': m['state'], 'outputs': len(m['outputs'])}
    if m.get('review_policy') != REVIEW_POLICY:
        result['review_policy'] = 'legacy-single-review-historical'
    return result


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
    p.add_argument('--asset-key', action='append', help='Stable logical asset key, once per variant')
    p.add_argument('--continue-from', help='Latest run in the same output root; inherits stable keys')
    for cmd in ('collect', 'review', 'verify', 'status'):
        p = sub.add_parser(cmd)
        p.add_argument('--run', required=True)
        if cmd == 'collect':
            p.add_argument('--asset-key')
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
    except (OSError, ValueError, KeyError, TypeError, RecursionError, Image.DecompressionBombError,
            Image.DecompressionBombWarning) as error:
        # Avoid dumping filesystem paths or arbitrary reference content into logs.
        message = str(error) if isinstance(error, ValueError) else type(error).__name__
        emit_error(message)
        return 2


if __name__ == '__main__':
    sys.exit(main())
