import argparse
import builtins
import copy
import importlib.util
import json
import os
from contextlib import contextmanager
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / '.agents/skills/image-production/scripts/inspect_artifacts.py'
spec = importlib.util.spec_from_file_location('artifacts', SCRIPT)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class ArtifactsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # Resolve macOS /var -> /private/var for the deliberate no-symlinks policy.
        self.root = Path(self.temp.name).resolve()
        self.image = self.root / 'wrong-extension.dat'
        im = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        im.putpixel((4, 4), (10, 20, 30, 255))
        im.save(self.image, format='PNG')
        self.prompt = self.root / 'prompt.txt'
        self.prompt.write_text('A blue mug; no logo', encoding='utf-8')
        self.brief = {'purpose': 'Test', 'audience': 'Reviewers', 'intended_use': 'Catalog',
                      'use_case': 'product-mockup', 'variants': 1, 'text': '',
                      'constraints': ['No logo'], 'acceptance': ['Transparent'],
                      'transparent': True, 'brand_kit': None, 'references': []}
        self.brief_file = self.root / 'brief.json'

    def prepare(self, **updates):
        self.brief.update(updates)
        self.brief_file.write_text(json.dumps(self.brief))
        result = a.prepare(argparse.Namespace(root=str(self.root / 'runs'),
                           brief=str(self.brief_file), surface='exec', cli_version='0.163.0'))
        return Path(result['run'])

    def collect(self, run, name='mug', source=None):
        return a.collect(argparse.Namespace(run=str(run), source=str(source or self.image),
                                           prompt=str(self.prompt), name=name))

    def review(self, run, asset='mug.png', changes=None):
        criteria = {key: {'score': 2, 'evidence': 'Synthetic test assertion, not visual QA'}
                    for key in a.CRITERIA}
        for key, value in (changes or {}).items():
            criteria[key] = value
        path = self.root / 'review.json'
        path.write_text(json.dumps({'reviewer': 'unit-test', 'criteria': criteria}))
        return a.review(argparse.Namespace(run=str(run), asset=asset, review=str(path)))

    def test_roundtrip_and_resume_without_source(self):
        run = self.prepare(references=[{'path': str(self.image), 'role': 'reference'}])
        self.collect(run)
        self.image.unlink()
        self.prompt.unlink()
        _, m = a.load(run)
        a.verify_manifest(run, m)
        self.assertEqual(self.review(run)['state'], 'approved')

    def test_actual_format_hash_and_no_overwrite(self):
        run = self.prepare()
        source_bytes = self.image.read_bytes()
        first = self.collect(run)
        second = self.collect(run)
        self.assertEqual((first['asset'], second['asset']), ('mug.png', 'mug-v2.png'))
        self.assertEqual((run / 'final/mug.png').read_bytes(), source_bytes)
        self.assertEqual(self.image.read_bytes(), source_bytes)
        self.assertEqual(first['metadata']['transparent_pixels'], 63)

    def test_opaque_and_all_transparent_rejected(self):
        run = self.prepare()
        for mode, color in [('RGB', 'blue'), ('RGBA', (0, 0, 0, 0))]:
            p = self.root / 'bad.png'
            Image.new(mode, (4, 4), color).save(p)
            with self.assertRaises(ValueError):
                self.collect(run, source=p)
        self.assertEqual(list((run / 'final').iterdir()), [])

    def test_corrupt_missing_and_animated_rejected(self):
        run = self.prepare()
        p = self.root / 'bad.png'
        p.write_bytes(b'not an image')
        for source in (p, self.root / 'missing.png'):
            with self.assertRaises((OSError, ValueError)):
                self.collect(run, source=source)
        frames = [Image.new('RGB', (4, 4), c) for c in ('red', 'blue')]
        frames[0].save(p, format='WEBP', save_all=True, append_images=frames[1:])
        with self.assertRaises(ValueError):
            self.collect(run, source=p)

    def test_confinement_errors_omit_paths_and_manifest_is_private(self):
        run = self.prepare()
        for relative in ('../escape', '', '/tmp/outside', 'final/../../outside'):
            with self.assertRaises(ValueError) as caught:
                a.inside(run, relative)
            message = str(caught.exception)
            self.assertNotIn(str(run), message)
            self.assertNotIn(str(self.root), message)
        self.collect(run)
        self.assertEqual(list(run.glob('.manifest-*')), [])
        self.assertEqual((run / 'manifest.json').stat().st_mode & 0o777, 0o600)

    def test_invalid_name_and_parent_traversal(self):
        run = self.prepare()
        for name in ('../escape', '/absolute', 'mug.png', 'a;touch nope'):
            with self.assertRaises(ValueError):
                self.collect(run, name=name)
        with self.assertRaises(ValueError):
            a.inside(run, '../escape')
        with self.assertRaises(ValueError):
            a.inside(run, '/absolute')

    def test_symlink_root_and_final_directory_rejected(self):
        run = self.prepare()
        link = self.root / 'link'
        link.symlink_to(self.root / 'runs', target_is_directory=True)
        with self.assertRaises(ValueError):
            a.safe_path(link / 'child')
        (run / 'final').rmdir()
        (run / 'final').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.collect(run)
        self.assertFalse((self.root / 'mug.png').exists())

    def test_symlink_manifest_cannot_overwrite_external_file(self):
        run = self.prepare()
        manifest_bytes = (run / 'manifest.json').read_bytes()
        outside = self.root / 'outside.json'
        outside.write_bytes(manifest_bytes)
        (run / 'manifest.json').unlink()
        (run / 'manifest.json').symlink_to(outside)
        with self.assertRaises(ValueError):
            a.status(argparse.Namespace(run=str(run), state='failed', reason='test'))
        self.assertEqual(outside.read_bytes(), manifest_bytes)

    def test_tamper_output_input_prompt(self):
        for target in ('output', 'input', 'prompt'):
            run = self.prepare(references=[{'path': str(self.image), 'role': 'reference'}])
            self.collect(run)
            _, m = a.load(run)
            rel = {'output': m['outputs'][0]['path'], 'input': m['inputs'][0]['path'],
                   'prompt': m['outputs'][0]['prompt_path']}[target]
            (run / rel).write_bytes(b'changed')
            with self.assertRaises((ValueError, OSError)):
                a.verify_manifest(run, m)

    def test_no_visual_approval_from_metadata_or_partial_score(self):
        run = self.prepare()
        self.collect(run)
        self.assertEqual(a.load(run)[1]['state'], 'generated')
        self.assertEqual(self.review(run, changes={'composition': {'score': 1, 'evidence': 'Crop uncertain'}})['state'], 'needs_revision')
        self.assertEqual(self.review(run)['state'], 'approved')
        self.assertEqual(len(a.load(run)[1]['outputs'][0]['review_history']), 1)
        self.collect(run)
        self.assertEqual(a.load(run)[1]['state'], 'generated')

    def test_required_gate_and_evidence_and_boolean_scores(self):
        run = self.prepare(text='Olá')
        self.collect(run)
        for key, entry in [('text_facts', {'score': 'na', 'evidence': 'not checked'}),
                           ('transparency', {'score': 'na', 'evidence': 'not checked'}),
                           ('objective', {'score': 2, 'evidence': ''}),
                           ('objective', {'score': True, 'evidence': 'invalid bool'})]:
            with self.assertRaises(ValueError):
                self.review(run, changes={key: entry})

    def test_variants_require_all_reviews(self):
        run = self.prepare(variants=2)
        self.collect(run)
        self.assertEqual(self.review(run)['state'], 'needs_revision')
        self.collect(run, name='mug-alt')
        self.assertEqual(self.review(run, asset='mug-alt.png')['state'], 'approved')

    def test_stored_empty_review_cannot_approve_another_variant(self):
        run = self.prepare(variants=2)
        self.collect(run)
        self.collect(run, name='mug-alt')
        path = run / 'manifest.json'
        manifest = json.loads(path.read_text())
        manifest['outputs'][0]['review'] = {'criteria': {}}
        path.write_text(json.dumps(manifest))
        before = path.read_bytes()
        with self.assertRaises(ValueError):
            self.review(run, asset='mug-alt.png')
        self.assertEqual(path.read_bytes(), before)

    def test_invalid_stored_reviews_fail_as_json_before_any_write(self):
        run = self.prepare()
        self.collect(run)
        self.review(run)
        self.review(run)
        path = run / 'manifest.json'
        valid = json.loads(path.read_text())
        cases = []
        for field, value in [('review', {'criteria': {}}), ('review_history', None),
                             ('review_history', [{'criteria': {}}])]:
            broken = copy.deepcopy(valid)
            broken['outputs'][0][field] = value
            cases.append(broken)
        for field in ('review', 'review_history'):
            broken = copy.deepcopy(valid)
            review = broken['outputs'][0][field]
            if isinstance(review, list):
                review = review[0]
            review['criteria']['transparency']['score'] = 'na'
            cases.append(broken)
        broken = copy.deepcopy(valid)
        broken['outputs'][0].update(review=None, review_history=[None])
        cases.append(broken)
        for case_index, broken in enumerate(cases):
            for command in (['verify'], ['status', '--state', 'failed', '--reason', 'test'],
                            ['review', '--asset', 'mug.png', '--review', str(self.root / 'review.json')]):
                with self.subTest(case=case_index, command=command[0]):
                    path.write_text(json.dumps(broken))
                    before = path.read_bytes()
                    result = subprocess.run([sys.executable, str(SCRIPT), *command,
                                             '--run', str(run)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(result.stdout, '')
                    self.assertEqual(list(json.loads(result.stderr)), ['error'])
                    self.assertEqual(path.read_bytes(), before)

    def test_manifest_temporary_is_private_from_creation(self):
        run = self.prepare()
        manifest = a.load(run)[1]
        real_open = Path.open
        real_builtin_open = builtins.open
        observed = []

        @contextmanager
        def inspect_open(path, *args, **kwargs):
            with real_open(path, *args, **kwargs) as stream:
                if path.name.startswith('.manifest-'):
                    observed.append(path.stat().st_mode & 0o777)
                yield stream

        @contextmanager
        def inspect_builtin_open(path, *args, **kwargs):
            with real_builtin_open(path, *args, **kwargs) as stream:
                if Path(path).name.startswith('.manifest-'):
                    observed.append(os.fstat(stream.fileno()).st_mode & 0o777)
                yield stream

        previous = os.umask(0o022)
        try:
            with patch.object(Path, 'open', inspect_open), patch.object(builtins, 'open', inspect_builtin_open):
                a.save(run, manifest)
        finally:
            os.umask(previous)
        self.assertEqual(observed, [0o600])
        self.assertEqual((run / 'manifest.json').stat().st_mode & 0o777, 0o600)
        self.assertEqual(list(run.glob('.manifest-*')), [])

    def test_brief_validation_and_brand_snapshot(self):
        for value in (0, True, 21, '1'):
            with self.assertRaises(ValueError):
                self.prepare(variants=value)
        self.brief['variants'] = 1
        brand = self.root / 'brand.md'
        brand.write_text('Blue ceramic; no logo')
        run = self.prepare(brand_kit=str(brand))
        self.assertEqual(a.load(run)[1]['inputs'][0]['role'], 'brand-kit')
        self.collect(run)
        with self.assertRaises(ValueError):
            self.review(run, changes={'brand_reference': {'score': 'na', 'evidence': 'ignored'}})

    def test_parser_errors_are_json_and_nonzero(self):
        cases = [
            (['collect', '--run', str(self.root)], '--source'),
            (['prepare', '--root', str(self.root), '--brief', str(self.brief_file),
              '--surface', 'nope'], 'invalid choice'),
            (['status', '--run', str(self.root), '--state', 'approved', '--reason', 'x'],
             'invalid choice'),
            (['nope'], 'invalid choice'),
            ([], 'command'),
            (['verify', '--run', str(self.root), '--extra', 'x'], 'unrecognized arguments'),
        ]
        for args, snippet in cases:
            result = subprocess.run([sys.executable, str(SCRIPT), *args],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, args)
            self.assertEqual(result.stdout, '', args)
            self.assertFalse(result.stderr.startswith('usage:'), args)
            self.assertEqual(result.stderr.count('\n'), 1, args)
            payload = json.loads(result.stderr)
            self.assertEqual(list(payload), ['error'], args)
            self.assertIn(snippet, payload['error'], args)

    def test_help_remains_plain_text(self):
        for args in (['--help'], ['prepare', '--help']):
            result = subprocess.run([sys.executable, str(SCRIPT), *args],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, args)
            self.assertIn('usage:', result.stdout, args)
            self.assertEqual(result.stderr, '', args)

    def test_cli_error_is_structured_and_nonzero(self):
        run = self.prepare()
        result = subprocess.run([sys.executable, str(SCRIPT), 'collect', '--run', str(run),
                                 '--source', str(self.root / 'missing.png'), '--prompt', str(self.prompt),
                                 '--name', 'missing'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('error', json.loads(result.stderr))
        self.assertEqual(result.stdout, '')
        self.assertEqual(a.load(run)[1]['outputs'], [])

    def test_approval_policy_does_not_touch_files(self):
        self.assertEqual(a.applicable_criteria({'text': 'Olá', 'transparent': True},
                                                [{'role': 'edit-target'}]), a.CRITERIA)
        self.assertEqual(a.applicable_criteria({'text': '', 'transparent': False}, []),
                         {'objective', 'composition', 'visual_integrity'})
        pending = [{'review': None}]
        self.assertEqual(a.approval_state(pending, 1), 'needs_revision')
        passing = [{'review': {'criteria': {'objective': {'score': 2}, 'text_facts': {'score': 'na'}}}}]
        self.assertEqual(a.approval_state(passing, 1), 'approved')
        self.assertEqual(a.approval_state(passing, 2), 'needs_revision')
        passing[0]['review']['criteria']['objective'] = {'score': 1}
        self.assertEqual(a.approval_state(passing, 1), 'needs_revision')
        with self.assertRaises(ValueError):
            a.checked_review({'reviewer': 'unit-test', 'criteria': {
                key: {'score': True, 'evidence': 'bool is not an int'} for key in a.CRITERIA
            }}, {'objective'})

    def test_malformed_manifest_fails_before_write(self):
        run = self.prepare()
        self.collect(run)
        path = run / 'manifest.json'
        manifest = json.loads(path.read_text(encoding='utf-8'))
        del manifest['outputs'][0]['prompt_path']
        path.write_text(json.dumps(manifest), encoding='utf-8')
        before = path.read_bytes()
        with self.assertRaises(ValueError) as caught:
            a.load(run)
        self.assertEqual(str(caught.exception), 'Malformed manifest')
        with self.assertRaises(ValueError):
            a.status(argparse.Namespace(run=str(run), state='failed', reason='must not write'))
        self.assertEqual(path.read_bytes(), before)

    def test_manifest_states_match_result_schema(self):
        schema = json.loads((SCRIPT.parents[1] / 'references' / 'result.schema.json').read_text(encoding='utf-8'))
        self.assertEqual(set(schema['properties']['state']['enum']), a.STATES)

    def test_verify_is_idempotent(self):
        run = self.prepare()
        self.collect(run)
        before = (run / 'manifest.json').read_bytes()
        args = argparse.Namespace(run=str(run))
        first = a.verify(args)
        second = a.verify(args)
        self.assertEqual(first, {'valid': True, 'state': 'generated', 'outputs': 1})
        self.assertEqual(second, first)
        self.assertEqual((run / 'manifest.json').read_bytes(), before)

    def test_blocked_status_cannot_force_approval(self):
        run = self.prepare()
        a.status(argparse.Namespace(run=str(run), state='blocked', reason='Tool unavailable'))
        self.assertEqual(a.load(run)[1]['state'], 'blocked')
        with self.assertRaises(ValueError):
            a.status(argparse.Namespace(run=str(run), state='approved', reason='bypass'))


if __name__ == '__main__':
    unittest.main()
