"""Malformed metadata must fail before it can reach the marketplace."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('validate_skills', Path(__file__).resolve().parents[1] / 'scripts/validate_skills.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

SKILL = '---\nname: demo\ndescription: Demonstrate one workflow.\n---\n\nProduce the requested output.\n'
UI = 'interface:\n  display_name: "Demo"\n  short_description: "Demonstrate one small workflow."\n  default_prompt: "Use $demo to demonstrate a workflow."\n'


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.skill = Path(self.tmp.name) / 'demo'
        (self.skill / 'agents').mkdir(parents=True)
        self.write(SKILL, UI)

    def write(self, skill=SKILL, ui=UI):
        (self.skill / 'SKILL.md').write_text(skill)
        (self.skill / 'agents/openai.yaml').write_text(ui)

    def test_valid_metadata(self):
        self.assertEqual(module.validate_skill(self.skill), [])

    def test_invalid_frontmatter(self):
        cases = [
            SKILL.replace('name: demo', 'name: ""'),
            SKILL.replace('name: demo', 'name: 123'),
            SKILL.replace('name: demo', 'name: Other'),
            SKILL.replace('name: demo', 'name: other'),
            SKILL.replace('name: demo', 'name: demo\nname: demo'),
            SKILL.replace('description: Demonstrate one workflow.', 'description: ""'),
            SKILL.replace('description: Demonstrate one workflow.', 'description: ['),
            SKILL.replace('description: Demonstrate one workflow.', 'description: '+ 'x'*1025),
            SKILL.replace('description: Demonstrate one workflow.', 'description: <instruction>'),
            SKILL.replace('name: demo', 'name: demo\nunexpected: true'),
            SKILL.replace('name: demo', 'name: demo\nmetadata: {version: 1}'),
            '---\n- demo\n---\nBody',
            '---\nname: demo\ndescription: test\n---\n',
            SKILL.lstrip('-'),
        ]
        for content in cases:
            with self.subTest(content=content):
                self.write(skill=content)
                self.assertTrue(module.validate_skill(self.skill))

    def test_invalid_ui(self):
        cases = [
            UI.replace('$demo', '$demo-other'),
            UI.replace('Demonstrate one small workflow.', 'Short'),
            UI + 'policy:\n  allow_implicit_invocation: "false"\n',
            UI + 'dependencies:\n  tools: wrong\n',
            UI + 'dependencies:\n  tools: [{type: http, value: github}]\n',
            UI + 'interface: {}\n',
            'interface: []\n',
            UI.replace('  display_name:', '  icon_small: "../../outside.svg"\n  display_name:'),
            UI.replace('  display_name:', '  icon_large: "./assets/missing.svg"\n  display_name:'),
        ]
        for content in cases:
            with self.subTest(content=content):
                self.write(ui=content)
                self.assertTrue(module.validate_skill(self.skill))

    def test_false_policy_is_valid(self):
        self.write(ui=UI+'policy:\n  allow_implicit_invocation: false\n')
        self.assertEqual(module.validate_skill(self.skill), [])

    def test_missing_ui_fails(self):
        (self.skill/'agents/openai.yaml').unlink()
        self.assertTrue(module.validate_skill(self.skill))

    def test_empty_repository_fails(self):
        from unittest.mock import patch
        with patch('sys.argv', ['validate_skills', '--root', self.tmp.name]):
            self.assertEqual(module.main(), 1)


if __name__ == '__main__':
    unittest.main()
