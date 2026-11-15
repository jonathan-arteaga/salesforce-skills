#!/usr/bin/env python3
"""Validate Persona's machine-readable framework manifest against source docs."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = SKILL_ROOT / "references" / "framework-manifest.json"
FRAMEWORK_PATH = SKILL_ROOT / "references" / "persona-framework.md"
SKILL_PATH = SKILL_ROOT / "SKILL.md"

_COMPONENT_TOKENS = {
    "CMP-IDENTITY": "Identity Traits",
    "CMP-NEGATIVE-IDENTITY": "Negative Identity",
    "CMP-VALUES": "Values",
    "CMP-NAMING": "Naming Your Agent",
    "CMP-RADIO-TEST": "radio test",
    "CMP-ORG-WE": "Organizational “we”",
    "CMP-HUMAN-EXPERIENCE": "Human experiences or feelings",
    "CMP-TONE-BOUNDARIES": "Tone Boundaries",
    "CMP-TONE-FLEX": "Tone Flex",
    "CMP-READING-FLEX": "Reading Level Flex",
    "CMP-TAPERING": "Conversation progression boundary",
    "CMP-PHRASE-BOOK": "Phrase Book",
    "CMP-DISCOURSE-MARKERS": "Discourse Markers",
    "CMP-NEVER-SAY": "Never-Say List",
    "CMP-LEXICON": "Lexicon",
    "CMP-TECH-EXPLANATION": "Technical Explanation Policy",
    "CMP-IMMUTABLE": "Immutable",
    "CMP-GUARDRAILS": "Guardrails",
    "CMP-STATIC-MESSAGES": "Static-copy candidates",
    "CMP-SUBAGENT-CALIBRATION": "subagent",
    "CMP-ACTION-PROGRESS": "action progress wording candidate",
}


def validate(skill_root: Path = SKILL_ROOT) -> list[str]:
    """Return deterministic validation errors; an empty list is success."""
    errors: list[str] = []
    manifest_path = skill_root / "references" / "framework-manifest.json"
    framework_path = skill_root / "references" / "persona-framework.md"
    skill_path = skill_root / "SKILL.md"

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"manifest unreadable: {error}"]

    framework = framework_path.read_text(encoding="utf-8")
    skill = skill_path.read_text(encoding="utf-8")
    source_documents = [
        path
        for path in skill_root.rglob("*.md")
        if "tests" not in path.parts
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(source_documents)
    )

    dimensions = manifest.get("dimensions", [])
    if len(dimensions) != 14:
        errors.append(f"expected 14 dimensions, found {len(dimensions)}")

    dimension_ids = [item.get("id") for item in dimensions]
    dimension_names = [item.get("name") for item in dimensions]
    if len(dimension_ids) != len(set(dimension_ids)):
        errors.append("dimension IDs are not unique")
    if len(dimension_names) != len(set(dimension_names)):
        errors.append("dimension names are not unique")

    for dimension in dimensions:
        name = dimension.get("name")
        positions = dimension.get("positions", [])
        if not name or name not in combined:
            errors.append(f"dimension missing from source: {name!r}")
        if len(positions) < 2:
            errors.append(f"dimension has fewer than two positions: {name!r}")
        for position in positions:
            if position not in framework:
                errors.append(f"position missing from framework: {name} / {position}")

    components = manifest.get("components", [])
    component_ids = [item.get("id") for item in components]
    if len(component_ids) != len(set(component_ids)):
        errors.append("component IDs are not unique")
    for component_id in component_ids:
        token = _COMPONENT_TOKENS.get(component_id)
        if token is None:
            errors.append(f"component has no validation token: {component_id}")
        elif token not in combined:
            errors.append(f"component token missing: {component_id} / {token}")

    workflow = manifest.get("workflow", {})
    for phase in workflow.get("phases", []):
        if f"PHASE" not in skill or phase not in skill:
            errors.append(f"phase missing from dispatcher: {phase}")
    for spoke in workflow.get("spokes", []):
        if spoke not in skill:
            errors.append(f"spoke missing from dispatcher: {spoke}")

    retired_assets = (
        "references/voice-catalog.json",
        "references/persona-encoding-guide-voice.md",
        "templates/persona-encoding-template-voice.md",
        "scripts/parse_agent_yaml.py",
        "scripts/verify_persona_patch.py",
        "scripts/lint_static_strings.py",
        "references/persona-encoding-guide-agentscript.md",
        "templates/persona-encoding-template-agentscript.md",
        "templates/sample-dialog-template.md",
    )
    for relative_path in retired_assets:
        if (skill_root / relative_path).exists():
            errors.append(f"retired out-of-scope asset still exists: {relative_path}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Persona framework manifest OK: 14 dimensions and component contracts verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
