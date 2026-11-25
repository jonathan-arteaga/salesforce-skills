#!/usr/bin/env python3
"""Sync or check Codex + Google Antigravity manifests, links, and zero orphaned references."""

import argparse
from collections import deque
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ANTIGRAVITY_SCHEMA = "https://antigravity.dev/schemas/plugin/v1.json"
DEFAULT_CATEGORY_MAP = {
    "salesforce-discovery": "Discover & Enable",
    "salesforce-tutorial-builder": "Discover & Enable",
    "data360-data-pipeline": "Data 360, Core Data & Analytics",
    "data360-activation-governance": "Data 360, Core Data & Analytics",
    "salesforce-schema-data": "Data 360, Core Data & Analytics",
    "salesforce-analytics": "Data 360, Core Data & Analytics",
    "salesforce-apex": "Core Platform & Integrations",
    "salesforce-flow": "Core Platform & Integrations",
    "salesforce-lwc": "Core Platform & Integrations",
    "salesforce-integrations": "Core Platform & Integrations",
    "agentforce-design": "Agentforce Design, Build & QA",
    "agentforce-build": "Agentforce Design, Build & QA",
    "agentforce-review": "Agentforce Design, Build & QA",
    "agentforce-test": "Agentforce Design, Build & QA",
    "salesforce-security-access": "Security, DevOps & Production Ops",
    "salesforce-devops-deploy": "Security, DevOps & Production Ops",
    "agentforce-observe": "Security, DevOps & Production Ops",
}
SUGGESTED_PROMPTS = [
    "Run brownfield discovery for our Salesforce Service Cloud org before proposing an Agentforce build.",
    "Design a Data 360 DLO-to-DMO pipeline and identity resolution ruleset for customer profiles.",
    "Implement and unit-test a bulkified Apex service using explicit WITH USER_MODE and Apex Cursors.",
    "Audit our Agentforce agent configuration for regulated-industry controls without mutating the org.",
    "Trace a failing Agentforce session in Data 360 and identify latency or tool-call bottlenecks.",
    "Validate our deployment package against a sandbox with RunSpecifiedTests before release.",
]

LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IGNORED_PARTS = {".DS_Store", "__pycache__", ".pytest_cache"}


def discover_packages(root: Path) -> list[dict]:
    """Return sorted package descriptors from plugins/*/plugin.json."""
    plugins_dir = root / "plugins"
    packages = []
    for manifest_path in sorted(plugins_dir.glob("*/plugin.json")):
        plugin_dir = manifest_path.parent
        name = plugin_dir.name
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if data.get("name") != name:
            raise ValueError(f"plugin.json name mismatch in {manifest_path.relative_to(root)}")
        discovered = {p.parent.name for p in plugin_dir.glob("skills/*/SKILL.md")}
        if discovered != {name}:
            raise ValueError(f"Expected single skill entrypoint {name!r} in {plugin_dir.relative_to(root)}")
        category = data.get("category") or DEFAULT_CATEGORY_MAP.get(name, "Salesforce Platform")
        packages.append({
            "name": name,
            "category": category,
            "description": data.get("description", ""),
            "plugin_rel": f"./plugins/{name}",
            "skill_rel": f"./plugins/{name}/skills/{name}",
        })
    if not packages:
        raise ValueError(f"No packaged plugins found under {plugins_dir}")
    return packages


def build_codex_marketplace(packages: list[dict]) -> dict:
    """Build .agents/plugins/marketplace.json payload."""
    return {
        "name": "salesforce-skills",
        "interface": {
            "displayName": "Salesforce Skills",
        },
        "plugins": [
            {
                "name": pkg["name"],
                "source": {
                    "source": "local",
                    "path": pkg["plugin_rel"],
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": pkg["category"],
            }
            for pkg in packages
        ],
    }


def build_antigravity_manifest(packages: list[dict]) -> dict:
    """Build .antigravity-plugin/plugin.json payload."""
    return {
        "$schema": ANTIGRAVITY_SCHEMA,
        "name": "salesforce-skills",
        "displayName": "Salesforce Skills",
        "version": "2.0.0",
        "description": (
            f"Domain-owning Salesforce, Data 360, and Agentforce skill library ({len(packages)} skills) "
            "engineered for Gemini 4 / Google Antigravity progressive disclosure and strict org safety gates."
        ),
        "author": {
            "name": "Jonathan Arteaga",
            "url": "https://github.com/jonathan-arteaga",
        },
        "license": "Apache-2.0",
        "repository": "https://github.com/jonathan-arteaga/salesforce-skills",
        "keywords": [
            "salesforce",
            "agentforce",
            "data-360",
            "apex",
            "lwc",
            "flow",
            "sf-cli",
            "antigravity",
        ],
        "skills": [pkg["skill_rel"] for pkg in packages],
        "suggestedPrompts": SUGGESTED_PROMPTS,
    }


def sync_or_check_json(path: Path, payload: dict, check: bool, root: Path, stale: list[str]) -> None:
    expected = json.dumps(payload, indent=2) + "\n"
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == expected:
        return
    if check:
        stale.append(str(path.relative_to(root)))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8")


def check_links_and_orphans(root: Path) -> None:
    """Verify every relative Markdown link resolves inside its plugin and zero references/ files are orphaned."""
    plugins_dir = root / "plugins"
    errors: list[str] = []

    for skill_md in sorted(plugins_dir.glob("*/skills/*/SKILL.md")):
        skill_dir = skill_md.parent
        package_dir = skill_dir.parents[1]

        # 1. Validate all relative links in every Markdown file inside the skill.
        for md_file in sorted(skill_dir.rglob("*.md")):
            if any(part in IGNORED_PARTS for part in md_file.parts):
                continue
            for href in LINK_RE.findall(md_file.read_text(encoding="utf-8")):
                target = unquote(href.strip("<>")).split("#", 1)[0]
                if not target:
                    continue
                if re.fullmatch(r"http://[\w.-]+\.md", target, re.IGNORECASE):
                    errors.append(f"{md_file.relative_to(root)}: invalid filename URL {href}")
                    continue
                if urlsplit(target).scheme:
                    continue
                resolved = (md_file.parent / target).resolve()
                if not resolved.is_relative_to(package_dir.resolve()) or not resolved.exists():
                    errors.append(f"{md_file.relative_to(root)}: missing packaged reference {href}")

        # 2. Enforce zero orphaned files in references/ via reachability from SKILL.md.
        refs_dir = skill_dir / "references"
        if refs_dir.is_dir():
            all_refs = {
                p.resolve()
                for p in refs_dir.rglob("*")
                if p.is_file() and not any(part in IGNORED_PARTS for part in p.parts)
            }
            visited_md: set[Path] = set()
            reachable: set[Path] = set()
            queue: deque[Path] = deque([skill_md.resolve()])
            while queue:
                current = queue.popleft()
                if current in visited_md or not current.is_file():
                    continue
                visited_md.add(current)
                for href in LINK_RE.findall(current.read_text(encoding="utf-8")):
                    target = unquote(href.strip("<>")).split("#", 1)[0]
                    if not target or urlsplit(target).scheme:
                        continue
                    resolved = (current.parent / target).resolve()
                    if resolved.is_relative_to(skill_dir.resolve()) and resolved.is_file():
                        reachable.add(resolved)
                        if resolved.suffix.lower() == ".md" and resolved not in visited_md:
                            queue.append(resolved)
            for orphan in sorted(all_refs - reachable):
                errors.append(f"{orphan.relative_to(root)}: orphaned reference file (not linked from SKILL.md)")

    if errors:
        raise ValueError("\n".join(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true", help="Verify manifests without rewriting files.")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    try:
        packages = discover_packages(root)
        stale: list[str] = []
        sync_or_check_json(
            root / ".agents" / "plugins" / "marketplace.json",
            build_codex_marketplace(packages),
            args.check,
            root,
            stale,
        )
        sync_or_check_json(
            root / ".antigravity-plugin" / "plugin.json",
            build_antigravity_manifest(packages),
            args.check,
            root,
            stale,
        )
        if stale:
            print("Regenerate stale manifests:\n" + "\n".join(stale), file=sys.stderr)
            return 1
        check_links_and_orphans(root)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    action = "Checked" if args.check else "Synced and checked"
    print(
        f"{action} {len(packages)} packaged skills across Codex + Antigravity manifests, "
        "links, and zero orphaned references."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
