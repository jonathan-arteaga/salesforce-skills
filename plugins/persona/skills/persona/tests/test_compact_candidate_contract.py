"""Persona handoff stays compact and delegates implementation."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class CompactCandidateContractTests(unittest.TestCase):
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

    def test_persona_emits_handoff_not_agent_script(self):
        for source in (self.skill, self.encode, self.guide):
            self.assertIn("persona-handoff.json", source)
            self.assertIn("agentforce-generate", source)
        self.assertNotIn("```agentscript", self.template)

    def test_requested_use_case_is_not_implementation_evidence(self):
        self.assertIn("no guessed action", self.guide.lower())
        self.assertIn("adjacent_constraints", self.template)
        self.assertIn("agent-architecture", self.encode)

    def test_completion_claim_is_bounded(self):
        self.assertIn("Persona handoff ready", self.encode)
        for forbidden in ("agent is generated", "preview-ready", "published", "active"):
            self.assertIn(forbidden, self.encode)


if __name__ == "__main__":
    unittest.main()
