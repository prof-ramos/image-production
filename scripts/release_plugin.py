#!/usr/bin/env python3
"""Build and publish an immutable plugin snapshot; never edit installed caches."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile


from build_plugin import build

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'prof-ramos/image-production'
BRANCH = 'plugin-release'
MARKETPLACE = 'image-production-local'
CATALOG = '.agents/plugins/marketplace.json'


def git(repo, *args, input=None):
    return subprocess.check_output(['git', '-C', str(repo), *args], input=input,
                                   stderr=subprocess.PIPE)


def resolve(repo, ref):
    return git(repo, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def regular_files(root):
    files = {}
    for path in root.rglob('*'):
        if path.relative_to(root).parts[0] == '.git':
            continue
        if path.is_symlink():
            raise ValueError('Release contains a symlink')
        if path.is_file():
            files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def export_source(repo, sha, destination):
    """Read only Git blobs, rejecting links before constructing a temporary tree."""
    selected = ('.agents/skills/image-production/', '.codex-plugin/plugin.json',
                '.codex/agents/', '.codex/config.toml')
    entries = git(repo, 'ls-tree', '-rz', sha, '--', *selected).split(b'\0')
    for entry in filter(None, entries):
        header, name = entry.split(b'\t', 1)
        mode, kind, oid = header.split()
        relative = name.decode('utf-8')
        path = PurePosixPath(relative)
        if mode not in (b'100644', b'100755') or kind != b'blob':
            raise ValueError('Source release inputs must be regular Git files')
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Invalid source path')
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git(repo, 'cat-file', 'blob', oid.decode()))
        target.chmod(0o755 if mode == b'100755' else 0o644)


def prepare(repo, sha, output):
    import yaml  # Required only for authoring validation, not installation or verification.
    sha = resolve(repo, sha)
    if output.exists() or output.is_symlink():
        raise ValueError('Output must be a new directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='image-release-') as temporary:
        source = Path(temporary) / 'source'
        source.mkdir()
        export_source(repo, sha, source)
        skill = source / '.agents/skills/image-production'
        frontmatter = (skill / 'SKILL.md').read_text().split('---', 2)
        if len(frontmatter) != 3 or frontmatter[0].strip():
            raise ValueError('Skill requires YAML frontmatter')
        try:
            definition = yaml.safe_load(frontmatter[1])
        except yaml.YAMLError as error:
            raise ValueError('Skill frontmatter is invalid YAML') from error
        if (not isinstance(definition, dict) or definition.get('name') != 'image-production'
                or not isinstance(definition.get('description'), str)
                or not definition['description'].strip()):
            raise ValueError('Skill name and description are required')
        manifest = json.loads((source / '.codex-plugin/plugin.json').read_text())
        base = manifest['version']
        if not re.fullmatch(r'(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)', base):
            raise ValueError('Source manifest requires a stable numeric SemVer base')
        version = base + '-main.g' + sha
        payload = build(root=source, version=version)
        expected_skill = {name: digest for name, digest in regular_files(skill).items()
                          if '__pycache__' not in PurePosixPath(name).parts and not name.endswith('.pyc')}
        if regular_files(payload / 'skills/image-production') != expected_skill:
            raise ValueError('Packaged skill differs from canonical source')
        stage = Path(temporary) / 'release'
        shutil.copytree(payload, stage / 'plugins/image-production')
        shutil.copytree(source / '.codex/agents', stage / 'agent-bundle/agents')
        shutil.copyfile(source / '.codex/config.toml', stage / 'agent-bundle/config.example.toml')
        (stage / 'agent-bundle/README.md').write_text(
            '# Project agents\n\nSource: https://github.com/' + REPOSITORY + '/tree/' + sha + '\n\n'
            'Copy only missing role files. Manually reconcile agent sections from '
            'config.example.toml; preserve models, credentials, security settings, comments '
            'and local concurrency limits. Installing the plugin does not install these roles. '
            'Start a new trusted project session and verify discovery.\n')
        write_json(stage / 'release.json', {'schema_version': 1, 'repository': REPOSITORY,
                   'source_sha': sha, 'version': version, 'files': regular_files(stage)})
        verify(stage)
        shutil.copytree(stage, output)
    return sha


def verify(path):
    metadata = json.loads((path / 'release.json').read_text())
    if metadata.get('schema_version') != 1 or metadata.get('repository') != REPOSITORY:
        raise ValueError('Unsupported release provenance')
    sha = metadata.get('source_sha', '')
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('Invalid release source SHA')
    expected = metadata.get('files')
    if not isinstance(expected, dict) or not expected:
        raise ValueError('Release requires file hashes')
    actual = regular_files(path)
    actual.pop('release.json', None)
    actual.pop(CATALOG, None)  # Catalog pins the earlier payload commit.
    if actual != expected:
        raise ValueError('Release file hashes or inventory do not match')
    plugin = path / 'plugins/image-production'
    portable = json.loads((plugin / 'plugin.json').read_text())
    overlay = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
    for manifest in (portable, overlay):
        if manifest.get('name') != 'image-production' or manifest.get('version') != metadata.get('version'):
            raise ValueError('Release manifests disagree with provenance')
    if not metadata['version'].endswith('-main.g' + sha):
        raise ValueError('Release version does not identify source commit')
    if overlay.get('skills') != './skills/':
        raise ValueError('Release skill path is invalid')
    if not (plugin / 'skills/image-production/SKILL.md').is_file():
        raise ValueError('Release is missing its skill')
    return metadata


def verify_catalog(path, payload_commit):
    catalog = json.loads((path / CATALOG).read_text())
    expected = {'name': MARKETPLACE, 'plugins': [{
        'name': 'image-production', 'source': {'source': 'git-subdir',
        'url': 'https://github.com/' + REPOSITORY + '.git',
        'path': './plugins/image-production', 'sha': payload_commit},
        'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_USE'},
        'category': 'Creativity'}]}
    if catalog != expected:
        raise ValueError('Published marketplace does not pin the verified payload')
    return catalog


def remote_ref(repo, remote, ref):
    output = git(repo, 'ls-remote', '--exit-code', remote, ref).decode().split()
    return output[0]


def publish(repo, sha, remote='origin'):
    sha = resolve(repo, sha)
    if remote_ref(repo, remote, 'refs/heads/main') != sha:
        raise ValueError('Source commit no longer matches remote main; nothing published')
    previous = None
    try:
        previous = remote_ref(repo, remote, 'refs/heads/' + BRANCH)
    except subprocess.CalledProcessError as error:
        if error.returncode != 2:  # ls-remote --exit-code: missing branch
            raise
    if previous:
        git(repo, 'fetch', '--no-tags', remote, 'refs/heads/' + BRANCH)
    with tempfile.TemporaryDirectory(prefix='image-publish-') as temporary:
        stage = Path(temporary) / 'snapshot'
        prepare(repo, sha, stage)
        checkout = Path(temporary) / 'git'
        checkout.mkdir()
        git(checkout, 'init', '-b', BRANCH)
        git(checkout, 'config', 'user.name', 'github-actions[bot]')
        git(checkout, 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
        if previous:
            git(checkout, 'fetch', '--no-tags', str(repo.resolve()), previous)
            git(checkout, 'checkout', '--detach', previous)
            recorded = verify(checkout)
            verify_catalog(checkout, resolve(checkout, 'HEAD^'))
            if recorded['source_sha'] == sha:
                print('Source commit already published: ' + sha)
                return previous
            for child in checkout.iterdir():
                if child.name == '.git':
                    continue
                if child.is_dir() and not child.is_symlink():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        shutil.copytree(stage, checkout, dirs_exist_ok=True)
        git(checkout, 'add', '--all')
        git(checkout, 'commit', '-m', 'Publish payload from ' + sha)
        payload_commit = resolve(checkout, 'HEAD')
        write_json(checkout / CATALOG, {'name': MARKETPLACE, 'plugins': [{
            'name': 'image-production', 'source': {'source': 'git-subdir',
            'url': 'https://github.com/' + REPOSITORY + '.git',
            'path': './plugins/image-production', 'sha': payload_commit},
            'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_USE'},
            'category': 'Creativity'}]})
        verify(checkout)
        verify_catalog(checkout, payload_commit)
        git(checkout, 'add', CATALOG)
        git(checkout, 'commit', '-m', 'Promote marketplace for ' + sha)
        published = resolve(checkout, 'HEAD')
        # Import objects only; checkout, branch and user configuration remain unchanged.
        git(repo, 'fetch', '--no-tags', str(checkout), published)
        if remote_ref(repo, remote, 'refs/heads/main') != sha:
            raise ValueError('Remote main advanced during preparation; nothing published')
        # A concurrent promotion rejects this normal push rather than replacing history.
        git(repo, 'push', remote, published + ':refs/heads/' + BRANCH)
        print('Published ' + sha + ' as ' + published)
        return published


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('prepare')
    command.add_argument('--sha', required=True)
    command.add_argument('--output', required=True, type=Path)
    command = sub.add_parser('verify')
    command.add_argument('--path', required=True, type=Path)
    command = sub.add_parser('publish')
    command.add_argument('--sha', required=True)
    command.add_argument('--remote', default='origin')
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            prepare(args.repo, args.sha, args.output)
        elif args.command == 'verify':
            metadata = verify(args.path)
            if (args.path / CATALOG).exists():
                verify_catalog(args.path, resolve(args.path, 'HEAD^'))
            print(json.dumps(metadata, sort_keys=True))
        else:
            publish(args.repo, args.sha, args.remote)
    except (ValueError, OSError, KeyError, ImportError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
