"""Exercise interrupted attempts through the same CLI dispatch as normal runs."""
import contextlib
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import test_artifacts as fixtures


a = fixtures.a


class LineageLifecycleTest(unittest.TestCase):
    def setUp(self):
        # Reuse data setup by composition, without inheriting its test methods.
        self.fixture = fixtures.ArtifactsTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root / 'runs'
        self.fixture.brief_file.write_text(json.dumps(self.fixture.brief))

    def command(self, *arguments):
        out, err = io.StringIO(), io.StringIO()
        with patch('sys.argv', [str(fixtures.SCRIPT), *map(str, arguments)]), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = a.main()
        self.assertIn(code, (0, 2))
        self.assertEqual(err.getvalue() if code == 0 else out.getvalue(), '')
        return code, json.loads(out.getvalue() if code == 0 else err.getvalue())

    def prepare(self, *extra):
        return self.command('prepare', '--root', self.root, '--brief', self.fixture.brief_file,
                            '--surface', 'exec', *extra)

    def collect(self, run):
        return self.command('collect', '--run', run, '--source', self.fixture.image,
                            '--prompt', self.fixture.prompt, '--name', 'mug')

    def ledger(self, key):
        return json.loads(a.lineage_path(self.root, key).read_text())

    def test_prepare_manifest_failure_keeps_initial_reservation(self):
        with patch.object(a, 'save', side_effect=OSError('injected manifest failure')):
            code, error = self.prepare('--asset-key', 'hero')
        self.assertEqual((code, error), (2, {'error': 'OSError'}))
        attempts = self.ledger('hero')['attempts']
        self.assertEqual(len(attempts), 1)
        self.assertFalse(attempts[0]['collected'])
        self.assertFalse((self.root / attempts[0]['run_id'] / 'manifest.json').exists())
        before = a.lineage_path(self.root, 'hero').read_bytes()
        code, error = self.prepare('--asset-key', 'hero')
        self.assertEqual(code, 2)
        self.assertIn('already exists', error['error'])
        self.assertEqual(a.lineage_path(self.root, 'hero').read_bytes(), before)

    def test_partial_multi_asset_reservation_is_not_rolled_back(self):
        self.fixture.brief['variants'] = 2
        self.fixture.brief_file.write_text(json.dumps(self.fixture.brief))
        write = a.atomic_json
        def fail_second(path, payload):
            if payload['asset_key'] == 'detail':
                raise OSError('injected second ledger failure')
            return write(path, payload)
        with patch.object(a, 'atomic_json', side_effect=fail_second):
            code, _ = self.prepare('--asset-key', 'hero', '--asset-key', 'detail')
        self.assertEqual(code, 2)
        self.assertEqual(len(self.ledger('hero')['attempts']), 1)
        self.assertFalse(a.lineage_path(self.root, 'detail').exists())
        self.assertEqual(list(self.root.glob('*/manifest.json')), [])
        code, error = self.prepare('--asset-key', 'hero', '--asset-key', 'detail')
        self.assertEqual(code, 2)
        self.assertIn('already exists', error['error'])
        self.assertFalse(a.lineage_path(self.root, 'detail').exists())

    def test_interrupted_correction_prevents_reusing_older_parent(self):
        code, first = self.prepare('--asset-key', 'hero')
        self.assertEqual(code, 0)
        with patch.object(a, 'save', side_effect=OSError('injected child manifest failure')):
            code, _ = self.prepare('--continue-from', first['run'])
        self.assertEqual(code, 2)
        self.assertEqual([entry['ordinal'] for entry in self.ledger('hero')['attempts']], [0, 1])
        before = a.lineage_path(self.root, 'hero').read_bytes()
        code, error = self.prepare('--continue-from', first['run'])
        self.assertEqual(code, 2)
        self.assertIn('latest attempt', error['error'])
        self.assertEqual(a.lineage_path(self.root, 'hero').read_bytes(), before)

    def test_collect_file_and_manifest_failures_never_refund(self):
        for failure in ('candidate', 'prompt', 'manifest'):
            with self.subTest(failure=failure):
                code, prepared = self.prepare('--asset-key', failure)
                self.assertEqual(code, 0)
                run = Path(prepared['run'])
                before = (run / 'manifest.json').read_bytes()
                write = a.write_new
                def fail_write(path, data):
                    if (failure == 'candidate' and path.parent.name == 'final'
                            or failure == 'prompt' and path.parent.name == 'work'):
                        raise OSError('injected file failure')
                    return write(path, data)
                fault = (patch.object(a, 'save', side_effect=OSError('injected manifest failure'))
                         if failure == 'manifest' else patch.object(a, 'write_new', side_effect=fail_write))
                with fault:
                    code, _ = self.collect(run)
                self.assertEqual(code, 2)
                self.assertEqual((run / 'manifest.json').read_bytes(), before)
                attempt = self.ledger(failure)['attempts'][0]
                self.assertTrue(attempt['collected'])
                self.assertEqual(attempt['sha256'], a.digest(self.fixture.image.read_bytes()))
                self.assertEqual(len(list((run / 'final').iterdir())), int(failure != 'candidate'))
                self.assertEqual(len(list((run / 'work').iterdir())), int(failure == 'manifest'))
                persisted = {path: path.read_bytes() for path in run.rglob('*') if path.is_file()}
                code, error = self.collect(run)
                self.assertEqual(code, 2)
                self.assertIn('already collected', error['error'])
                self.assertEqual(persisted, {path: path.read_bytes() for path in run.rglob('*') if path.is_file()})
                code, child = self.prepare('--continue-from', run)
                self.assertEqual(code, 0)
                self.assertEqual(child['assets'], [{'asset_key': failure, 'attempt': 1}])

    def test_failed_consumption_write_preserves_reservation_before_candidate_writes(self):
        code, prepared = self.prepare('--asset-key', 'hero')
        self.assertEqual(code, 0)
        run = Path(prepared['run'])
        before = a.lineage_path(self.root, 'hero').read_bytes()
        with patch.object(a, 'atomic_json', side_effect=OSError('injected ledger failure')):
            code, _ = self.collect(run)
        self.assertEqual(code, 2)
        self.assertEqual(a.lineage_path(self.root, 'hero').read_bytes(), before)
        self.assertEqual(list((run / 'final').iterdir()), [])
        self.assertEqual(list((run / 'work').iterdir()), [])
        self.assertEqual(self.collect(run)[0], 0)
        self.assertEqual(len(self.ledger('hero')['attempts']), 1)
