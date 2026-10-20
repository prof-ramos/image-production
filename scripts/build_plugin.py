#!/usr/bin/env python3
"""Build the local plugin from the canonical skill, without repository artifacts."""
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "work/plugin-dist/image-production"


def build(*, root=None, version=None):
    root = Path(root) if root is not None else ROOT
    destination = root / "work/plugin-dist/image-production"
    # Check lexical ancestors before traversal or writes can follow a parent link.
    for path in (destination, *(root / part for part in destination.relative_to(root).parents)):
        if path.is_symlink():
            raise ValueError("Generated plugin path must not contain a symlink")
    source = root / ".agents/skills/image-production"
    # Validate the entire canonical source before touching the previous build.
    # copytree otherwise dereferences file and directory symlinks by default.
    for path in source.relative_to(root).parents:
        if (root / path).is_symlink():
            raise ValueError("Canonical skill path must not contain a symlink")
    if source.is_symlink():
        raise ValueError("Canonical skill directory must not be a symlink")
    if not source.is_dir():
        raise ValueError("Canonical skill source must be an existing directory")
    for path in source.rglob("*"):
        if path.is_symlink():
            relative = path.relative_to(source).as_posix()
            raise ValueError(f"Unexpected symlink in canonical skill: {relative}")
    if not (source / "SKILL.md").is_file():
        raise ValueError("Canonical skill requires a regular SKILL.md")
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
    if version is not None:
        manifest["version"] = version
    manifest["skills"] = "./skills/"
    if destination.is_symlink():
        raise ValueError("Generated plugin directory must not be a symlink")
    if destination.exists() and not destination.is_dir():
        raise ValueError("Generated plugin destination must be a directory")
    for path in destination.rglob("*"):
        relative = path.relative_to(destination).as_posix()
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink in generated plugin: {relative}")
        if path.is_file() and relative not in ("plugin.json", ".codex-plugin/plugin.json"):
            if not relative.startswith("skills/image-production/"):
                raise ValueError(f"Unexpected file in generated plugin: {relative}")
    # Render and copy everything before moving a usable previous package.
    overlay_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    portable = {key: manifest[key] for key in ("name", "version", "description", "author")}
    portable["$schema"] = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    portable["extensions"] = {"com.openai": {"interface": manifest["interface"]}}
    portable_text = json.dumps(portable, ensure_ascii=False, indent=2) + "\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".image-production-", dir=destination.parent))
    backup = stage.with_name(stage.name + ".previous")
    try:
        shutil.copytree(source, stage / "skills/image-production",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        overlay = stage / ".codex-plugin/plugin.json"
        overlay.parent.mkdir()
        overlay.write_text(overlay_text)
        (stage / "plugin.json").write_text(portable_text)
        if destination.exists():
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup.exists():
                backup.rename(destination)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    if backup.exists():
        shutil.rmtree(backup)
    print(destination)
    return destination


if __name__ == "__main__":
    build()
