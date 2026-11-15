"""Validate skill metadata across the marketplace; no model or live-service calls."""

import argparse
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
    """Return diagnostics for a skill folder (including packaged bundle copies)."""
    directory = Path(directory)
    errors = []
    try:
        content = (directory / 'SKILL.md').read_text(encoding='utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', content, re.S)
        if not match:
            raise ValueError('Missing or malformed frontmatter delimiters')
        data = read_mapping(match[1])
        allowed = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
        if set(data) - allowed:
            raise ValueError(f'Unknown frontmatter fields: {sorted(set(data) - allowed)}')
        name = required_string(data, 'name')
        if len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ValueError('name must be hyphen-case and at most 64 characters')
        if name != directory.name:
            raise ValueError(f'name {name!r} does not match directory {directory.name!r}')
        description = required_string(data, 'description')
        if len(description) > 1024 or '<' in description or '>' in description:
            raise ValueError('description must be at most 1024 characters without angle brackets')
        if not content[match.end():].strip():
            raise ValueError('Skill instructions are empty')
        if 'metadata' in data and (not isinstance(data['metadata'], dict) or
                                  any(not isinstance(v, str) for v in data['metadata'].values())):
            raise ValueError('metadata must map strings to strings')
        for field in ('license', 'compatibility', 'allowed-tools'):
            if field in data:
                required_string(data, field)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f'SKILL.md: {exc}')
        return errors

    # These fields are optional in the platform, but required by this marketplace.
    try:
        ui = read_mapping((directory / 'agents/openai.yaml').read_text(encoding='utf-8'))
        interface = ui.get('interface')
        if not isinstance(interface, dict):
            raise ValueError('interface must be a mapping')
        required_string(interface, 'display_name')
        short = required_string(interface, 'short_description')
        if not 25 <= len(short) <= 64:
            raise ValueError('short_description must contain 25–64 characters')
        prompt = required_string(interface, 'default_prompt')
        if not re.search(r'\$' + re.escape(name) + r'(?![a-zA-Z0-9_-])', prompt):
            raise ValueError('default_prompt must invoke the exact $skill-name')
        policy = ui.get('policy', {})
        if not isinstance(policy, dict):
            raise ValueError('policy must be a mapping')
        if 'allow_implicit_invocation' in policy and type(policy['allow_implicit_invocation']) is not bool:
            raise ValueError('allow_implicit_invocation must be a YAML boolean')
        for field in ('icon_small', 'icon_large'):
            if field in interface:
                asset = (directory / required_string(interface, field)).resolve()
                if not asset.is_relative_to(directory.resolve()) or not asset.is_file():
                    raise ValueError(f'{field} must reference a file inside the skill')
        if 'brand_color' in interface and not re.fullmatch(r'#[0-9A-Fa-f]{6}', str(interface['brand_color'])):
            raise ValueError('brand_color must be a six-digit hex color')
        dependencies = ui.get('dependencies', {})
        if not isinstance(dependencies, dict):
            raise ValueError('dependencies must be a mapping')
        tools = dependencies.get('tools', [])
        if not isinstance(tools, list):
            raise ValueError('dependencies.tools must be a list')
        for tool in tools:
            if not isinstance(tool, dict) or tool.get('type') != 'mcp':
                raise ValueError('Each tool dependency must be an MCP mapping')
            required_string(tool, 'value')
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f'agents/openai.yaml: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    skills = sorted((args.root / 'plugins').glob('*/skills/*/SKILL.md'))
    if not skills:
        print('No skills found', file=sys.stderr)
        return 1
    errors = [(p, error) for p in skills for error in validate_skill(p.parent)]
    for path, error in errors:
        print(f'{path.relative_to(args.root)}: {error}', file=sys.stderr)
    if errors:
        return 1
    unique = len({p.parent.name for p in skills})
    print(f'Validated metadata for {len(skills)} packaged skills ({unique} unique names).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
