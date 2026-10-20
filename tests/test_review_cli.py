"""Exercise public CLIs with an isolated gh executable at the system boundary."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
STUB = ROOT / 'tests/fixtures/gh_stub.py'


class ReviewCliTests(unittest.TestCase):
    def run_cli(self, script, scenario, *args):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / 'gh'
            executable.write_text(f'#!{sys.executable}\n' + STUB.read_text())
            executable.chmod(0o755)
            fixture = root / 'scenario.json'
            fixture.write_text(json.dumps(scenario))
            state = root / 'state.json'
            env = dict(os.environ, PATH=str(root), FAKE_GH_SCENARIO=str(fixture),
                       FAKE_GH_STATE=str(state), GH_CONFIG_DIR=str(root / 'gh-config'))
            for name in ('GH_TOKEN', 'GITHUB_TOKEN', 'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN'):
                env.pop(name, None)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts' / script),
                                     *args, '--repo', 'test/repo'],
                                    env=env, cwd=root, capture_output=True, text=True, timeout=15)
            return result, json.loads(state.read_text()) if state.exists() else {}

    def scenario(self, **changes):
        return {'pr': {'state': 'open', 'draft': False, 'head': {'sha': 'abc'}}, **changes}

    def test_export_reads_all_pages_and_feedback_surfaces(self):
        def item(number):
            return {'id': number, 'user': {'login': 'coderabbitai[bot]'}, 'body': 'finding', 'commit_id': 'abc'}
        result, state = self.run_cli('export_coderabbit.py', self.scenario(
            comments_pages=[[item(1)], [item(2)]], reviews_pages=[[item(3)], [item(4)]],
            inline_pages=[[item(5)], [item(6)]]), '4')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([i['id'] for i in json.loads(result.stdout)['items']], [1, 2, 3, 4, 5, 6])
        self.assertEqual(state['posts'], [])

    def test_export_discards_report_if_head_changes(self):
        result, state = self.run_cli('export_coderabbit.py', self.scenario(
            later_pr={'head': {'sha': 'new'}}), '4')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertEqual(state['posts'], [])

    def test_export_failure_does_not_emit_partial_report(self):
        result, _ = self.run_cli('export_coderabbit.py', self.scenario(
            fail_endpoint='repos/test/repo/pulls/4/reviews?per_page=100'), '4')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_request_finds_existing_marker_on_later_page(self):
        comment = {'user': {'login': 'owner'}, 'body': '@coderabbitai full review\n\n<!-- image-production:coderabbit-request:abc -->'}
        result, state = self.run_cli('request_coderabbit.py', self.scenario(
            comments_pages=[[], [comment]]), '4')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['action'], 'skip')
        self.assertEqual(state['posts'], [])

    def test_request_aborts_before_post_when_head_changes(self):
        result, state = self.run_cli('request_coderabbit.py', self.scenario(
            later_pr={'head': {'sha': 'new'}, 'state': 'open', 'draft': False}), '4')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertEqual(state['posts'], [])

    def test_failed_post_is_not_reported_as_requested_or_retried(self):
        result, state = self.run_cli('request_coderabbit.py', self.scenario(post_exit=1), '4')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('uncertain', result.stderr)
        self.assertEqual(len(state['posts']), 1)

    def test_current_branch_pr_receives_saved_exact_comment(self):
        result, state = self.run_cli('request_coderabbit.py', self.scenario())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'requested')
        self.assertEqual(state['posts'], ['@coderabbitai full review\n\n<!-- image-production:coderabbit-request:abc -->\nHead: `abc`\n'])

    def test_dry_run_has_no_comment_side_effect(self):
        result, state = self.run_cli('request_coderabbit.py', self.scenario(), '4', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['action'], 'post')
        self.assertEqual(state['posts'], [])
