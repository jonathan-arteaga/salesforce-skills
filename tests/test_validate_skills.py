"""Malformed metadata, manifest drift, or Markdown hygiene issues must fail CI."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "validate_skills", Path(__file__).resolve().parents[1] / "scripts/validate_skills.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

SKILL = '---\nname: demo\ndescription: "Demonstrate one workflow."\n---\n\nProduce the requested output.\n'
UI = (
    'interface:\n'
    '  display_name: "Demo"\n'
    '  short_description: "Demonstrate one small workflow."\n'
    '  default_prompt: "Use $demo to demonstrate a workflow."\n'
    'policy:\n'
    '  allow_implicit_invocation: true\n'
)
PLUGIN = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": "demo",
    "version": "2.0.0",
    "description": "Demonstrate one workflow.",
}


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.plugin = Path(self.tmp.name) / "plugins" / "demo"
        self.skill = self.plugin / "skills" / "demo"
        (self.skill / "agents").mkdir(parents=True)
        self.write(SKILL, UI, PLUGIN, "Apache License 2.0\n")

    def write(self, skill=SKILL, ui=UI, plugin=PLUGIN, lic="Apache License 2.0\n"):
        (self.skill / "SKILL.md").write_text(skill, encoding="utf-8")
        (self.skill / "agents/openai.yaml").write_text(ui, encoding="utf-8")
        (self.plugin / "plugin.json").write_text(json.dumps(plugin, indent=2) + "\n", encoding="utf-8")
        (self.skill / "LICENSE").write_text(lic, encoding="utf-8")

    def test_valid_metadata(self):
        self.assertEqual(module.validate_skill(self.skill), [])

    def test_invalid_frontmatter_and_markdown_hygiene(self):
        cases = [
            SKILL.replace("name: demo", 'name: ""'),
            SKILL.replace("name: demo", "name: 123"),
            SKILL.replace("name: demo", "name: Other"),
            SKILL.replace("name: demo", "name: other"),
            SKILL.replace("name: demo", "name: demo\nname: demo"),
            SKILL.replace('description: "Demonstrate one workflow."', 'description: ""'),
            SKILL.replace('description: "Demonstrate one workflow."', "description: |-\n  Multiline description."),
            SKILL.replace('description: "Demonstrate one workflow."', "description: ["),
            SKILL.replace('description: "Demonstrate one workflow."', 'description: "' + "x" * 1025 + '"'),
            SKILL.replace('description: "Demonstrate one workflow."', 'description: "<instruction>"'),
            SKILL.replace("name: demo", "name: demo\nunexpected: true"),
            SKILL.replace("name: demo", "name: demo\nmetadata: {version: 1}"),
            "---\n- demo\n---\nBody",
            '---\nname: demo\ndescription: "test"\n---\n',
            SKILL.lstrip("-"),
            SKILL + "\nLine with <br> tag.\n",
            SKILL + "\nLine with <b>bold</b> tag.\n",
            SKILL + "\nLine with <i>italic</i> tag.\n",
            SKILL + "\n| Col |\n| --- |\n| A \\| B |\n",
        ]
        for content in cases:
            with self.subTest(content=content):
                self.write(skill=content)
                self.assertTrue(module.validate_skill(self.skill))

    def test_plugin_json_parity_and_license(self):
        bad_plugin = dict(PLUGIN, description="Different description.")
        self.write(plugin=bad_plugin)
        self.assertTrue(module.validate_skill(self.skill))

        self.write(plugin=PLUGIN, lic="")
        self.assertTrue(module.validate_skill(self.skill))

        (self.skill / "LICENSE").unlink()
        self.assertTrue(module.validate_skill(self.skill))

    def test_invalid_ui(self):
        no_policy = "\n".join(UI.splitlines()[:4]) + "\n"
        cases = [
            no_policy,
            UI.replace("$demo", "$demo-other"),
            UI.replace("Demonstrate one small workflow.", "Short"),
            UI.replace("allow_implicit_invocation: true", 'allow_implicit_invocation: "false"'),
            UI + "dependencies:\n  tools: wrong\n",
            UI + "dependencies:\n  tools: [{type: http, value: github}]\n",
            UI + "interface: {}\n",
            "interface: []\n",
            UI.replace("  display_name:", '  icon_small: "../../outside.svg"\n  display_name:'),
            UI.replace("  display_name:", '  icon_large: "./assets/missing.svg"\n  display_name:'),
        ]
        for content in cases:
            with self.subTest(content=content):
                self.write(ui=content)
                self.assertTrue(module.validate_skill(self.skill))

    def test_false_policy_is_valid(self):
        self.write(ui=UI.replace("allow_implicit_invocation: true", "allow_implicit_invocation: false"))
        self.assertEqual(module.validate_skill(self.skill), [])

    def test_missing_ui_fails(self):
        (self.skill / "agents/openai.yaml").unlink()
        self.assertTrue(module.validate_skill(self.skill))

    def test_empty_repository_fails(self):
        from unittest.mock import patch

        empty_dir = tempfile.TemporaryDirectory()
        self.addCleanup(empty_dir.cleanup)
        with patch("sys.argv", ["validate_skills", "--root", empty_dir.name]):
            self.assertEqual(module.main(), 1)


if __name__ == "__main__":
    unittest.main()
