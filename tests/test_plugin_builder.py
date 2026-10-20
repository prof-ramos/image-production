import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


BUILDER = Path(__file__).resolve().parents[1] / 'scripts/build_plugin.py'


class PluginBuilderTests(unittest.TestCase):
    def create_fixture(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'scripts').mkdir()
        shutil.copyfile(BUILDER, self.root / 'scripts/build_plugin.py')
        manifest = self.root / '.codex-plugin/plugin.json'
        manifest.parent.mkdir()
        manifest.write_text(json.dumps({'name': 'fixture', 'version': '0.1.0',
                                       'description': 'fixture', 'author': {'name': 'test'},
                                       'interface': {}}))
        self.source = self.root / '.agents/skills/image-production'
        self.source.mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('safe skill\n')
        self.destination = self.root / 'work/plugin-dist/image-production'

    def run_builder(self):
        return subprocess.run([sys.executable, str(self.root / 'scripts/build_plugin.py')],
                              capture_output=True, text=True)

    def test_valid_source_bootstraps_portable_plugin(self):
        self.create_fixture()
        result = self.run_builder()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.destination / 'skills/image-production/SKILL.md').read_text(),
                         'safe skill\n')
        overlay = json.loads((self.destination / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(overlay['skills'], './skills/')

    def test_source_symlinks_are_rejected_before_destination_changes(self):
        # Removing source validation would leak external bytes, follow directories,
        # or delete the old build before copytree fails on a dangling link.
        for kind in ('file', 'directory', 'dangling', 'root'):
            with self.subTest(kind=kind):
                self.create_fixture()
                result = self.run_builder()
                self.assertEqual(result.returncode, 0, result.stderr)
                (self.destination / 'skills/image-production/SKILL.md').write_text('previous build\n')
                before = {str(p.relative_to(self.destination)): p.read_bytes()
                          for p in self.destination.rglob('*') if p.is_file()}
                outside = self.root / 'outside'
                if kind == 'directory':
                    outside.mkdir()
                    (outside / 'private.txt').write_text('do not package')
                elif kind in ('file', 'root'):
                    outside.write_text('do not package')
                link = self.source / 'linked'
                if kind == 'root':
                    shutil.rmtree(self.source)
                    outside.unlink()
                    outside.mkdir()
                    (outside / 'SKILL.md').write_text('do not package')
                    link = self.source
                link.symlink_to(outside, target_is_directory=kind in ('directory', 'root'))
                result = self.run_builder()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('symlink', result.stderr.lower())
                after = {str(p.relative_to(self.destination)): p.read_bytes()
                         for p in self.destination.rglob('*') if p.is_file()}
                self.assertEqual(after, before)
                link.unlink()
                if kind == 'root':
                    self.source.mkdir()
                    (self.source / 'SKILL.md').write_text('safe skill\n')
                if outside.is_dir():
                    shutil.rmtree(outside)
                elif outside.exists():
                    outside.unlink()

    def test_rejected_source_does_not_create_destination(self):
        self.create_fixture()
        (self.source / 'missing').symlink_to(self.root / 'absent')
        result = self.run_builder()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main()
