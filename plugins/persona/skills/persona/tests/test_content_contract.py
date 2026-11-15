"""Persona owns expression constraints and hands agent-design constraints onward."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ContentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.template = (SKILL_ROOT / "templates" / "persona-template.md").read_text(
            encoding="utf-8"
        )
        cls.checklist = (
            SKILL_ROOT / "templates" / "checklist-template.md"
        ).read_text(encoding="utf-8")
        cls.handoff = (
            SKILL_ROOT / "templates" / "persona-handoff-template.md"
        ).read_text(encoding="utf-8")

    def test_guardrails_cannot_be_replaced_by_never_say(self):
        self.assertIn("Never-Say cannot substitute for a Guardrail", self.framework)
        self.assertIn("topic, claim, advice, or action boundary", self.framework)

    def test_immutable_content_has_precedence_and_shape_boundary(self):
        for source in (self.framework, self.template, self.checklist):
            self.assertIn("overrides Persona and user style requests", " ".join(source.split()))
        self.assertIn(
            "Immutability protects the exact string, not its surrounding response shape",
            self.framework,
        )
        self.assertIn("immutable_content", self.handoff)

    def test_lexicon_requires_meaning_not_bare_terms(self):
        self.assertIn("Bare term lists invite invented definitions", self.framework)
        self.assertIn("lexicon", self.handoff.lower())
        self.assertIn("terms, definitions", self.handoff)

    def test_guardrails_are_verbatim_adjacent_handoff_only(self):
        self.assertIn("agent-design-adjacent", self.framework.lower())
        self.assertIn("not a Persona component", self.framework)
        self.assertIn("not a Persona component", self.checklist)
        self.assertIn("guardrail design", self.skill.lower())
        self.assertIn("adjacent_constraints", self.handoff)
        self.assertIn("verbatim_reference", self.handoff)
        self.assertIn("agent-architecture", self.skill)


if __name__ == "__main__":
    unittest.main()
