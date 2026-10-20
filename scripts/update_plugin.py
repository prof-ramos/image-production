#!/usr/bin/env python3
"""Install the latest published plugin through Codex and verify the installed bytes."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from release_plugin import BRANCH, MARKETPLACE, REPOSITORY, git, regular_files, verify, verify_catalog

URL = 'https://github.com/' + REPOSITORY + '.git'
PLUGIN = 'image-production@' + MARKETPLACE


def codex(*args, cwd):
    result = subprocess.run(['codex', 'plugin', *args, '--json'], capture_output=True, text=True,
                            check=True, cwd=cwd)
    return json.loads(result.stdout)


def update():
    with tempfile.TemporaryDirectory(prefix='image-update-') as temporary:
        snapshot = Path(temporary) / 'snapshot'
        subprocess.run(['git', 'clone', '--single-branch', '--branch', BRANCH,
                        URL, str(snapshot)], check=True, capture_output=True)
        expected = verify(snapshot)
        payload = git(snapshot, 'rev-parse', 'HEAD^').decode().strip()
        verify_catalog(snapshot, payload)
        # Run outside the checkout so its development marketplace cannot shadow Git.
        # Codex owns migration from the local marketplace, config writes and its cache.
        added = codex('marketplace', 'add', URL, '--ref', BRANCH, cwd=temporary)
        if added.get('marketplaceName') != MARKETPLACE:
            raise ValueError('Codex returned an unexpected marketplace')
        codex('marketplace', 'upgrade', MARKETPLACE, cwd=temporary)
        installed = codex('add', PLUGIN, cwd=temporary)
        if installed.get('pluginId') != PLUGIN or installed.get('version') != expected['version']:
            raise ValueError('Installed version differs from verified snapshot; rerun after publication settles')
        path = Path(installed['installedPath'])
        prefix = 'plugins/image-production/'
        hashes = {name[len(prefix):]: digest for name, digest in expected['files'].items()
                  if name.startswith(prefix)}
        if not hashes or regular_files(path) != hashes:
            raise ValueError('Installed plugin does not match published file hashes')
        print(json.dumps({'plugin': PLUGIN, 'version': expected['version'],
                          'source_sha': expected['source_sha'], 'installed_path': str(path),
                          'verified': True}, indent=2))
        print('Start a new Codex session to verify skill discovery. Agent configuration remains separate.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        update()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        # Do not print git/codex stderr, which can include credential-bearing URLs.
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
