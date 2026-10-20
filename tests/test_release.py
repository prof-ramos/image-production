import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        for name in ('scripts', '.agents/skills', '.agents/plugins', '.codex-plugin', '.codex'):
            shutil.copytree(ROOT / name, self.root / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.base_version = json.loads((self.root / '.codex-plugin/plugin.json').read_text())['version']
        self.git('init', '-b', 'main')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'Test')
        self.git('add', '.')
        self.git('commit', '-m', 'source')
        self.sha = self.git('rev-parse', 'HEAD').strip()
        self.output = Path(self.temp.name) / 'release'

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True,
                                       stderr=subprocess.PIPE)

    def run_release(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/release_plugin.py'),
                               '--repo', str(self.root), *map(str, args)],
                              text=True, capture_output=True)

    def test_prepare_exports_exact_committed_skill_and_unique_version(self):
        skill = self.root / '.agents/skills/image-production/SKILL.md'
        committed = skill.read_bytes()
        skill.write_text('uncommitted bytes must not ship')
        result = self.run_release('prepare', '--sha', self.sha, '--output', self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = self.output / 'plugins/image-production'
        self.assertEqual((payload / 'skills/image-production/SKILL.md').read_bytes(), committed)
        release = json.loads((self.output / 'release.json').read_text())
        self.assertEqual(release['source_sha'], self.sha)
        manifest = json.loads((payload / 'plugin.json').read_text())
        self.assertEqual(manifest['version'], self.base_version + '-main.g' + self.sha)
        self.assertTrue((self.output / 'agent-bundle/agents/chief_of_staff.toml').is_file())
        for name, digest in release['files'].items():
            self.assertEqual(hashlib.sha256((self.output / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(self.run_release('verify', '--path', self.output).returncode, 0)

    def test_verify_rejects_missing_extra_and_modified_files(self):
        result = self.run_release('prepare', '--sha', self.sha, '--output', self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        skill = self.output / 'plugins/image-production/skills/image-production/SKILL.md'
        original = skill.read_bytes()
        for failure in ('missing', 'modified', 'extra'):
            with self.subTest(failure=failure):
                if failure == 'missing':
                    skill.unlink()
                elif failure == 'modified':
                    skill.write_bytes(b'tampered')
                else:
                    (self.output / 'extra').write_text('unexpected')
                self.assertNotEqual(self.run_release('verify', '--path', self.output).returncode, 0)
                skill.write_bytes(original)
                (self.output / 'extra').unlink(missing_ok=True)

    def test_publish_creates_installable_snapshot_and_rerun_is_noop(self):
        remote = Path(self.temp.name) / 'remote.git'
        subprocess.check_call(['git', 'init', '--bare', str(remote)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', 'origin', 'main')
        result = self.run_release('publish', '--sha', self.sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        tip = subprocess.check_output(['git', '--git-dir', str(remote), 'rev-parse', 'plugin-release'], text=True)
        clone = Path(self.temp.name) / 'consumer'
        subprocess.check_call(['git', 'clone', '--branch', 'plugin-release', str(remote), str(clone)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        catalog = json.loads((clone / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(catalog['name'], 'image-production-local')
        source = catalog['plugins'][0]['source']
        self.assertEqual(source['source'], 'git-subdir')
        self.assertEqual(source['sha'], subprocess.check_output(
            ['git', '-C', str(clone), 'rev-parse', 'HEAD^'], text=True).strip())
        self.assertTrue((clone / 'plugins/image-production/skills/image-production/SKILL.md').is_file())
        self.assertEqual(self.run_release('verify', '--path', clone).returncode, 0)
        again = self.run_release('publish', '--sha', self.sha)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn('already published', again.stdout)
        self.assertEqual(subprocess.check_output(
            ['git', '--git-dir', str(remote), 'rev-parse', 'plugin-release'], text=True), tip)

    def test_stale_source_does_not_publish(self):
        remote = Path(self.temp.name) / 'remote.git'
        subprocess.check_call(['git', 'init', '--bare', str(remote)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.git('remote', 'add', 'origin', str(remote))
        self.git('commit', '--allow-empty', '-m', 'new main')
        self.git('push', 'origin', 'main')
        result = self.run_release('publish', '--sha', self.sha)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('main', result.stderr)
        refs = subprocess.check_output(['git', '--git-dir', str(remote), 'for-each-ref'], text=True)
        self.assertNotIn('plugin-release', refs)

    def test_rejected_push_preserves_published_branch(self):
        remote = Path(self.temp.name) / 'remote.git'
        subprocess.check_call(['git', 'init', '--bare', str(remote)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', 'origin', 'main')
        self.assertEqual(self.run_release('publish', '--sha', self.sha).returncode, 0)
        previous = subprocess.check_output(['git', '--git-dir', str(remote), 'rev-parse',
                                             'plugin-release'], text=True)
        self.git('commit', '--allow-empty', '-m', 'next main')
        self.git('push', 'origin', 'main')
        sha = self.git('rev-parse', 'HEAD').strip()
        hook = remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        self.assertNotEqual(self.run_release('publish', '--sha', sha).returncode, 0)
        self.assertEqual(subprocess.check_output(['git', '--git-dir', str(remote), 'rev-parse',
                                                 'plugin-release'], text=True), previous)
        self.assertEqual(self.git('rev-parse', 'HEAD').strip(), sha)
        self.assertEqual(self.git('status', '--porcelain'), '')

    @unittest.skipUnless(shutil.which('codex'), 'Codex CLI is an optional local integration check')
    def test_native_codex_migrates_local_marketplace_and_updates_verified_plugin(self):
        remote = Path(self.temp.name) / 'remote.git'
        subprocess.check_call(['git', 'init', '--bare', str(remote)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', 'origin', 'main')
        self.assertEqual(self.run_release('publish', '--sha', self.sha).returncode, 0)
        local = Path(self.temp.name) / 'old-local-marketplace'
        subprocess.check_call(['git', 'clone', '--branch', 'plugin-release', str(remote), str(local)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        home = Path(self.temp.name) / 'codex-home'
        home.mkdir()
        env = {**os.environ, 'CODEX_HOME': str(home), 'GIT_CONFIG_COUNT': '1',
               'GIT_CONFIG_KEY_0': 'url.' + str(remote) + '.insteadOf',
               'GIT_CONFIG_VALUE_0': 'https://github.com/prof-ramos/image-production.git'}
        subprocess.run(['codex', 'plugin', 'marketplace', 'add', str(local), '--json'],
                       cwd=self.temp.name, env=env, capture_output=True, check=True)
        updater = [sys.executable, str(ROOT / 'scripts/update_plugin.py')]
        first = subprocess.run(updater, cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn(self.base_version + '-main.g' + self.sha, first.stdout)
        source = self.root / '.agents/skills/image-production/SKILL.md'
        source.write_text(source.read_text() + '\nA new revision.\n')
        self.git('add', '.')
        self.git('commit', '-m', 'new skill')
        self.git('push', 'origin', 'main')
        next_sha = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(self.run_release('publish', '--sha', next_sha).returncode, 0)
        second = subprocess.run(updater, cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn(self.base_version + '-main.g' + next_sha, second.stdout)
        self.assertTrue((home / 'plugins/cache/image-production-local/image-production' /
                         (self.base_version + '-main.g' + next_sha) / 'skills/image-production/SKILL.md').is_file())

    def test_main_advancing_during_preparation_does_not_promote(self):
        remote = Path(self.temp.name) / 'remote.git'
        subprocess.check_call(['git', 'init', '--bare', str(remote)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', 'origin', 'main')
        bin_path = Path(self.temp.name) / 'bin'
        bin_path.mkdir()
        wrapper = bin_path / 'git'
        real_git = shutil.which('git')
        count_file = Path(self.temp.name) / 'lookups'
        wrapper.write_text('#!' + sys.executable + '\n' +
            'import pathlib, subprocess, sys\n' +
            'args = sys.argv[1:]\n' +
            'if "ls-remote" in args and "refs/heads/main" in args:\n' +
            '    count = pathlib.Path(' + repr(str(count_file)) + ')\n' +
            '    if count.exists():\n' +
            '        subprocess.run([' + repr(real_git) + ', "-C", ' + repr(str(self.root)) +
            ', "commit", "--allow-empty", "-m", "main advanced"], check=True, capture_output=True)\n' +
            '        subprocess.run([' + repr(real_git) + ', "-C", ' + repr(str(self.root)) +
            ', "push", "origin", "main"], check=True, capture_output=True)\n' +
            '    count.write_text("seen")\n' +
            'sys.exit(subprocess.call([' + repr(real_git) + '] + args))\n')
        wrapper.chmod(0o755)
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/release_plugin.py'),
                                 '--repo', str(self.root), 'publish', '--sha', self.sha],
                                env={**os.environ, 'PATH': str(bin_path) + os.pathsep + os.environ['PATH']},
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('main advanced', result.stderr)
        refs = subprocess.check_output([real_git, '--git-dir', str(remote), 'for-each-ref'], text=True)
        self.assertNotIn('plugin-release', refs)

    def test_committed_symlinks_and_invalid_skill_do_not_prepare_release(self):
        linked = self.root / '.agents/skills/image-production/external'
        linked.symlink_to('/private/secret')
        self.git('add', '.')
        self.git('commit', '-m', 'unsafe input')
        result = self.run_release('prepare', '--sha', 'HEAD', '--output', self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('regular Git files', result.stderr)
        self.assertFalse(self.output.exists())
        linked.unlink()
        (self.root / '.agents/skills/image-production/SKILL.md').write_text('missing frontmatter')
        self.git('add', '.')
        self.git('commit', '-m', 'invalid skill')
        result = self.run_release('prepare', '--sha', 'HEAD', '--output', self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('frontmatter', result.stderr)
        self.assertFalse(self.output.exists())

    def test_same_source_with_damaged_remote_payload_does_not_claim_success(self):
        remote = Path(self.temp.name) / 'remote.git'
        subprocess.check_call(['git', 'init', '--bare', str(remote)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', 'origin', 'main')
        self.assertEqual(self.run_release('publish', '--sha', self.sha).returncode, 0)
        consumer = Path(self.temp.name) / 'damaged'
        subprocess.check_call(['git', 'clone', '--branch', 'plugin-release', str(remote), str(consumer)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (consumer / 'plugins/image-production/skills/image-production/SKILL.md').write_text('damaged')
        for args in [('config', 'user.email', 'test@example.com'), ('config', 'user.name', 'Test'),
                     ('add', '.'), ('commit', '-m', 'damage'), ('push', 'origin', 'plugin-release')]:
            subprocess.run(['git', '-C', str(consumer), *args], capture_output=True, check=True)
        result = self.run_release('publish', '--sha', self.sha)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('already published', result.stdout)
