#!/usr/bin/env python3
"""Validate skill metadata, manifest parity, and Markdown hygiene across the marketplace."""

import argparse
import json
from pathlib import Path
import re
import sys

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently retaining the last value."""


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)

RAW_HTML_PATTERN = re.compile(r"</?(?:br|b|i|quote)\b[^>]*>", re.IGNORECASE)
MULTILINE_FIELD_PATTERN = re.compile(
    r"^(name|description)\s*:\s*(?:[|>][-+]?\s*$|\s*$)", re.MULTILINE
)


def read_mapping(text):
    result = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(result, dict):
        raise ValueError("Expected a YAML mapping")
    return result


def required_string(data, key):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a nonempty string")
    return value


def validate_skill(directory):
    """Return diagnostics for a skill folder (including standalone plugin parity)."""
    directory = Path(directory)
    errors = []
    name = None
    description = None

    try:
        content = (directory / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.S)
        if not match:
            raise ValueError("Missing or malformed frontmatter delimiters")
        fm_raw = match[1]
        if MULTILINE_FIELD_PATTERN.search(fm_raw):
            raise ValueError("Frontmatter name and description must be single-line YAML fields")
        data = read_mapping(fm_raw)
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        if set(data) - allowed:
            raise ValueError(f"Unknown frontmatter fields: {sorted(set(data) - allowed)}")
        name = required_string(data, "name")
        if "\n" in name or "\r" in name:
            raise ValueError("name must be single-line")
        if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("name must be hyphen-case and at most 64 characters")
        if name != directory.name:
            raise ValueError(f"name {name!r} does not match directory {directory.name!r}")
        description = required_string(data, "description")
        if "\n" in description or "\r" in description:
            raise ValueError("description must be single-line")
        if len(description) > 1024 or "<" in description or ">" in description:
            raise ValueError("description must be at most 1024 characters without angle brackets")
        body = content[match.end():]
        if not body.strip():
            raise ValueError("Skill instructions are empty")
        if RAW_HTML_PATTERN.search(body):
            raise ValueError("SKILL.md must not contain raw HTML tags (<br>, <b>, <i>, <quote>)")
        if r"\|" in body:
            raise ValueError(r"SKILL.md must not contain escaped-pipe tables (\|)")
        if "metadata" in data and (
            not isinstance(data["metadata"], dict)
            or any(not isinstance(v, str) for v in data["metadata"].values())
        ):
            raise ValueError("metadata must map strings to strings")
        for field in ("license", "compatibility", "allowed-tools"):
            if field in data:
                required_string(data, field)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"SKILL.md: {exc}")
        return errors

    # Required LICENSE file inside every standalone skill package.
    license_path = directory / "LICENSE"
    if not license_path.is_file() or not license_path.read_text(encoding="utf-8").strip():
        errors.append("LICENSE: missing or empty LICENSE file")

    # Exact plugin.json <-> SKILL.md parity when inside plugins/<name>/skills/<name>.
    if len(directory.parents) >= 2 and directory.parent.name == "skills":
        plugin_json = directory.parents[1] / "plugin.json"
        if not plugin_json.is_file():
            errors.append("plugin.json: missing package manifest")
        else:
            try:
                manifest = json.loads(plugin_json.read_text(encoding="utf-8"))
                if manifest.get("name") != name:
                    errors.append(
                        f"plugin.json: name {manifest.get('name')!r} does not match {name!r}"
                    )
                if manifest.get("description") != description:
                    errors.append(
                        "plugin.json: description does not match SKILL.md frontmatter verbatim"
                    )
            except (OSError, ValueError) as exc:
                errors.append(f"plugin.json: {exc}")

    # Required Codex / host UI metadata + explicit invocation policy.
    try:
        ui = read_mapping((directory / "agents/openai.yaml").read_text(encoding="utf-8"))
        interface = ui.get("interface")
        if not isinstance(interface, dict):
            raise ValueError("interface must be a mapping")
        required_string(interface, "display_name")
        short = required_string(interface, "short_description")
        if not 25 <= len(short) <= 64:
            raise ValueError("short_description must contain 25-64 characters")
        prompt = required_string(interface, "default_prompt")
        if not re.search(r"\$" + re.escape(name) + r"(?![a-zA-Z0-9_-])", prompt):
            raise ValueError("default_prompt must invoke the exact $skill-name")
        policy = ui.get("policy")
        if not isinstance(policy, dict) or "allow_implicit_invocation" not in policy:
            raise ValueError("policy.allow_implicit_invocation is required")
        if type(policy["allow_implicit_invocation"]) is not bool:
            raise ValueError("allow_implicit_invocation must be a YAML boolean")
        for field in ("icon_small", "icon_large"):
            if field in interface:
                asset = (directory / required_string(interface, field)).resolve()
                if not asset.is_relative_to(directory.resolve()) or not asset.is_file():
                    raise ValueError(f"{field} must reference a file inside the skill")
        if "brand_color" in interface and not re.fullmatch(
            r"#[0-9A-Fa-f]{6}", str(interface["brand_color"])
        ):
            raise ValueError("brand_color must be a six-digit hex color")
        dependencies = ui.get("dependencies", {})
        if not isinstance(dependencies, dict):
            raise ValueError("dependencies must be a mapping")
        tools = dependencies.get("tools", [])
        if not isinstance(tools, list):
            raise ValueError("dependencies.tools must be a list")
        for tool in tools:
            if not isinstance(tool, dict) or tool.get("type") != "mcp":
                raise ValueError("Each tool dependency must be an MCP mapping")
            required_string(tool, "value")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"agents/openai.yaml: {exc}")

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    skills = sorted((args.root / "plugins").glob("*/skills/*/SKILL.md"))
    if not skills:
        print("No skills found", file=sys.stderr)
        return 1
    errors = [(p, error) for p in skills for error in validate_skill(p.parent)]
    for path, error in errors:
        print(f"{path.relative_to(args.root)}: {error}", file=sys.stderr)
    if errors:
        return 1
    unique = len({p.parent.name for p in skills})
    print(f"Validated metadata for {len(skills)} packaged skills ({unique} unique names).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
