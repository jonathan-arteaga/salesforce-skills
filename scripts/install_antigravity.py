#!/usr/bin/env python3
"""Direct installer to sync Salesforce Skills into Google Antigravity (~/.gemini/config/skills/)."""

import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / "plugins"
ANTIGRAVITY_MANIFEST = ROOT / ".antigravity-plugin" / "plugin.json"
DEFAULT_TARGET = Path.home() / ".gemini" / "config" / "skills"
IGNORED_PARTS = {".DS_Store", "__pycache__", ".pytest_cache"}


def discover_skills(root: Path = ROOT) -> list[tuple[str, Path]]:
    """Return sorted (skill_name, skill_dir) tuples from plugins/."""
    plugins = root / "plugins"
    skills: list[tuple[str, Path]] = []
    for skill_md in sorted(plugins.glob("*/skills/*/SKILL.md")):
        skill_dir = skill_md.parent
        skills.append((skill_dir.name, skill_dir))
    return skills


def copy_skill(src: Path, dest: Path, dry_run: bool = False) -> int:
    """Copy a single skill folder cleanly, excluding cache/bytecode artifacts."""
    copied = 0
    if not dry_run:
        if dest.exists() or dest.is_symlink():
            if dest.is_symlink() or dest.is_file():
                dest.unlink()
            else:
                shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.rglob("*")):
        if not item.is_file():
            continue
        rel = item.relative_to(src)
        if any(part in IGNORED_PARTS for part in rel.parts):
            continue
        if not dry_run:
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
        copied += 1
    return copied


def sync_skills(
    target_dir: Path = DEFAULT_TARGET,
    selected: list[str] | None = None,
    clean: bool = False,
    dry_run: bool = False,
    root: Path = ROOT,
) -> dict:
    """Sync all (or selected) skills into target_dir without requiring the agy CLI."""
    all_skills = dict(discover_skills(root))
    if not all_skills:
        raise RuntimeError(f"No skills found under {root / 'plugins'}")

    names = sorted(all_skills)
    if selected:
        unknown = sorted(set(selected) - set(all_skills))
        if unknown:
            raise ValueError(f"Unknown skill(s): {', '.join(unknown)}")
        names = sorted(selected)

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    removed: list[str] = []
    if clean and target_dir.exists():
        manifest_file = root / ".antigravity-plugin" / "plugin.json"
        managed = set(all_skills)
        if manifest_file.exists():
            try:
                manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                for entry in manifest.get("skills", []):
                    managed.add(Path(entry).name)
            except (OSError, ValueError):
                pass
        for name in sorted(managed - set(names)):
            stale = target_dir / name
            if stale.exists() or stale.is_symlink():
                if not dry_run:
                    if stale.is_symlink() or stale.is_file():
                        stale.unlink()
                    else:
                        shutil.rmtree(stale)
                removed.append(name)

    installed: dict[str, int] = {}
    for name in names:
        installed[name] = copy_skill(all_skills[name], target_dir / name, dry_run=dry_run)

    return {
        "target": str(target_dir),
        "installed": installed,
        "removed": removed,
        "dry_run": dry_run,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sync-skills",
        action="store_true",
        help="Sync skills directly into ~/.gemini/config/skills/ (or --target).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all discoverable skills in this repository.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Install only specific skill name(s); repeatable.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"Target Antigravity skills directory (default: {DEFAULT_TARGET}).",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove deselected skills from this repo in the target directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without modifying the filesystem.",
    )
    args = parser.parse_args(argv)

    if args.list:
        for name, path in discover_skills():
            print(f"{name}\t{path.relative_to(ROOT)}")
        return 0

    if not args.sync_skills:
        parser.print_help()
        print("\nTip: run with --sync-skills to install into ~/.gemini/config/skills/", file=sys.stderr)
        return 1

    try:
        result = sync_skills(
            target_dir=args.target.expanduser(),
            selected=args.skills,
            clean=args.clean,
            dry_run=args.dry_run,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    prefix = "[dry-run] " if result["dry_run"] else ""
    total_files = sum(result["installed"].values())
    print(
        f"{prefix}Synced {len(result['installed'])} Salesforce skill(s) "
        f"({total_files} files) -> {result['target']}"
    )
    if result["removed"]:
        print(f"{prefix}Removed: {', '.join(result['removed'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
