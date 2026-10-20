#!/usr/bin/env python3
"""Build the local plugin from the canonical skill, without repository artifacts."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "work/plugin-dist/image-production"


def build():
    source = ROOT / ".agents/skills/image-production"
    # Validate the entire canonical source before touching the previous build.
    # copytree otherwise dereferences file and directory symlinks by default.
    for path in source.relative_to(ROOT).parents:
        if (ROOT / path).is_symlink():
            raise ValueError("Canonical skill path must not contain a symlink")
    if source.is_symlink():
        raise ValueError("Canonical skill directory must not be a symlink")
    for path in source.rglob("*"):
        if path.is_symlink():
            relative = path.relative_to(source).as_posix()
            raise ValueError(f"Unexpected symlink in canonical skill: {relative}")
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    manifest["skills"] = "./skills/"
    if DESTINATION.is_symlink():
        raise ValueError("Generated plugin directory must not be a symlink")
    for path in DESTINATION.rglob("*"):
        relative = path.relative_to(DESTINATION).as_posix()
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink in generated plugin: {relative}")
        if path.is_file() and relative not in ("plugin.json", ".codex-plugin/plugin.json"):
            if not relative.startswith("skills/image-production/"):
                raise ValueError(f"Unexpected file in generated plugin: {relative}")
    DESTINATION.mkdir(parents=True, exist_ok=True)
    # Only replace this builder's generated skill, never the canonical source.
    target = DESTINATION / "skills/image-production"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    overlay = DESTINATION / ".codex-plugin/plugin.json"
    overlay.parent.mkdir(exist_ok=True)
    overlay.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    portable = {key: manifest[key] for key in ("name", "version", "description", "author")}
    portable["$schema"] = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    portable["extensions"] = {"com.openai": {"interface": manifest["interface"]}}
    (DESTINATION / "plugin.json").write_text(json.dumps(portable, ensure_ascii=False, indent=2) + "\n")
    print(DESTINATION)


if __name__ == "__main__":
    build()
