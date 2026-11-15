"""Brownfield Persona work emits semantic deltas for the canonical owner."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class BrownfieldDeltaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.encode = (SKILL_ROOT / "references" / "encode-detail.md").read_text(
            encoding="utf-8"
        )
        cls.guide = (
            SKILL_ROOT / "references" / "persona-handoff-guide-agentscript.md"
        ).read_text(encoding="utf-8")
        cls.template = (
            SKILL_ROOT / "templates" / "persona-handoff-template.md"
        ).read_text(encoding="utf-8")

    def test_brownfield_delta_is_semantic_and_no_op_is_valid(self):
        for source in (self.skill, self.encode, self.guide):
            self.assertIn("semantic Persona delta", source)
            self.assertIn("no-op is valid", source.lower())
        self.assertIn("semantic_deltas", self.template)

    def test_canonical_owner_inspects_applies_and_verifies(self):
        for source in (self.skill, self.encode, self.guide):
            self.assertIn("agentforce-generate", source)
        self.assertIn("canonical Agent Script owner", self.guide)
        self.assertIn("structural mutation", self.guide)
        self.assertIn("candidate verification", self.guide)

    def test_persona_does_not_ship_a_dsl_parser_or_patch_verifier(self):
        for relative in (
            "scripts/parse_agent_yaml.py",
            "scripts/verify_persona_patch.py",
            "scripts/lint_static_strings.py",
        ):
            self.assertFalse((SKILL_ROOT / relative).exists(), relative)
        combined = self.skill + self.encode + self.guide
        self.assertIn("does not parse", combined.lower())
        self.assertIn("do not produce a source patch", combined.lower())

    def test_handoff_excludes_agent_script_mechanics(self):
        for forbidden in (
            "start_agent",
            "default_agent_user",
            "AgentforceServiceAgent",
            "@utils.transition",
            "```agentscript",
        ):
            self.assertNotIn(forbidden, self.template)
        self.assertEqual("persona-handoff.json", Path("persona-handoff.json").name)


if __name__ == "__main__":
    unittest.main()
