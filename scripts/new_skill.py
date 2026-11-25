#!/usr/bin/env python3
"""Scaffold a compliant Salesforce skill and register it in Antigravity + Codex manifests."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
VALID_CATEGORIES = (
    "Discover & Enable",
    "Data 360, Core Data & Analytics",
    "Core Platform & Integrations",
    "Agentforce Design, Build & QA",
    "Security, DevOps & Production Ops",
)


def default_license_text(root: Path = ROOT) -> str:
    """Reuse canonical Apache-2.0 text from an existing packaged skill."""
    for candidate in sorted((root / "plugins").glob("*/skills/*/LICENSE")):
        return candidate.read_text(encoding="utf-8")
    return (
        "Apache License, Version 2.0\n\n"
        "Licensed under the Apache License, Version 2.0 (the \"License\");\n"
        "you may not use this file except in compliance with the License.\n"
        "You may obtain a copy of the License at\n\n"
        "    http://www.apache.org/licenses/LICENSE-2.0\n"
    )


def validate_inputs(name: str, description: str, short_description: str) -> None:
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("name must be hyphen-case (a-z, 0-9, -) and at most 64 characters")
    if "\n" in description or "\r" in description or not description.strip():
        raise ValueError("description must be a non-empty single line")
    if len(description) > 1024 or "<" in description or ">" in description:
        raise ValueError("description must be <= 1024 chars and contain no < or >")
    if not 25 <= len(short_description) <= 64:
        raise ValueError("short_description must be 25-64 characters")


def scaffold_skill(
    name: str,
    display_name: str,
    description: str,
    short_description: str,
    category: str,
    allow_implicit: bool = True,
    root: Path = ROOT,
    sync_manifests: bool = True,
) -> Path:
    """Create plugins/<name> with compliant SKILL.md, plugin.json, LICENSE, openai.yaml, and reference."""
    validate_inputs(name, description, short_description)
    plugin_dir = root / "plugins" / name
    if plugin_dir.exists():
        raise FileExistsError(f"Plugin already exists: {plugin_dir}")

    skill_dir = plugin_dir / "skills" / name
    (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)

    plugin_manifest = {
        "$schema": PLUGIN_SCHEMA,
        "name": name,
        "version": "2.0.0",
        "category": category,
        "description": description,
    }
    (plugin_dir / "plugin.json").write_text(
        json.dumps(plugin_manifest, indent=2) + "\n", encoding="utf-8"
    )

    escaped_desc = description.replace("\\", "\\\\").replace('"', '\\"')
    skill_md = f"""---
name: {name}
description: "{escaped_desc}"
---

# {display_name}

Route to the active workflow reference first; skip unrelated modes.

## Mode Routing

| Request Type | Read Reference | Output |
| --- | --- | --- |
| Primary workflow | [references/workflow.md](references/workflow.md) | Scoped design, artifact, or evidence report |

## Core Invariants

1. Verify target org API version, edition, licenses, and schema before writing metadata or code.
2. Encode platform invariants and negative failure modes rather than generic syntax tutorials.
3. Preserve explicit sibling handoffs; do not absorb work owned by adjacent skills.

## Safety & Org Gates

- Read-only inspection and planning never mutate org metadata or records.
- Require explicit user approval and pinned `--target-org` identity before any deployment, permission change, destructive data write, or live agent publication.

## Verification Integrity

- Distinguish static inspection, executed `sf` CLI checks, org readback, and `Not verified` gaps.
- Never claim a command, test, or org change succeeded without observed output.
"""
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    ref_md = f"""# {display_name} — Workflow & Invariants

## Inputs & Pre-Flight

- Confirm explicit scope, target org/environment identity, and read-only vs authorized write intent.
- Verify relevant object, field, permission, or metadata definitions against the target release.

## Execution Checklist

1. Inspect existing artifacts and dependencies before proposing changes.
2. Apply release-accurate Salesforce patterns and least-privilege access controls.
3. Produce reproducible validation commands and record observed vs unverified checks.

## Failure Modes to Guard Against

- Assuming sandbox or documentation parity with the target org.
- Conflating missing data with denied permissions or failed tool calls.
"""
    (skill_dir / "references" / "workflow.md").write_text(ref_md, encoding="utf-8")

    (skill_dir / "LICENSE").write_text(default_license_text(root), encoding="utf-8")

    escaped_display = display_name.replace('"', '\\"')
    escaped_short = short_description.replace('"', '\\"')
    allow_str = "true" if allow_implicit else "false"
    openai_yaml = f"""interface:
  display_name: "{escaped_display}"
  short_description: "{escaped_short}"
  default_prompt: "Use ${name} to handle this Salesforce workflow with strict org safety gates."
policy:
  allow_implicit_invocation: {allow_str}
"""
    (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml, encoding="utf-8")

    if sync_manifests:
        packager = root / "scripts" / "package_marketplace.py"
        if packager.exists():
            subprocess.run([sys.executable, str(packager), "--root", str(root)], check=True)

    return plugin_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Hyphen-case skill name (e.g. salesforce-experience-site).")
    parser.add_argument("--display-name", required=True, help="Human-readable skill title.")
    parser.add_argument(
        "--description",
        required=True,
        help="Single-line description with positive triggers and explicit negative handoffs.",
    )
    parser.add_argument(
        "--short-description",
        required=True,
        help="Catalog card summary (25-64 characters).",
    )
    parser.add_argument(
        "--category",
        default="Core Platform & Integrations",
        choices=VALID_CATEGORIES,
        help="Lifecycle stage category.",
    )
    parser.add_argument(
        "--no-implicit",
        action="store_true",
        help="Set policy.allow_implicit_invocation to false.",
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="Skip running scripts/package_marketplace.py after scaffolding.",
    )
    args = parser.parse_args(argv)

    try:
        plugin_dir = scaffold_skill(
            name=args.name,
            display_name=args.display_name,
            description=args.description,
            short_description=args.short_description,
            category=args.category,
            allow_implicit=not args.no_implicit,
            sync_manifests=not args.no_sync,
        )
    except (ValueError, FileExistsError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Scaffolded compliant skill at {plugin_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
