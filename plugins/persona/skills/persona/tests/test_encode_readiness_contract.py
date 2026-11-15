"""Agent Script readiness belongs to the canonical authoring owner."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class EncodeReadinessContractTests(unittest.TestCase):
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
        cls.draft = (SKILL_ROOT / "references" / "draft-phase.md").read_text(
            encoding="utf-8"
        )

    def test_persona_does_not_resolve_schema_or_access_inputs(self):
        combined = self.skill + self.encode + self.guide + self.template
        for forbidden in (
            "AgentforceServiceAgent",
            "AgentforceEmployeeAgent",
            "default_agent_user",
            "developer_name",
            "start_agent",
        ):
            self.assertNotIn(forbidden, combined)
        self.assertIn("current agent-type, access, schema", self.guide)

    def test_handoff_readiness_is_not_agent_readiness(self):
        self.assertIn("Persona handoff ready", self.encode)
        self.assertIn("does not mean an Agent Script artifact", self.guide)
        self.assertIn("A generated handoff is not a compiled", self.template)

    def test_greenfield_voice_handoff_is_ordered_across_owners(self):
        sequence = "`persona` → `agentforce-generate` → `conversation-design`"
        self.assertIn(sequence, self.guide)
        self.assertIn("→ `voice-ux`", self.guide)

    def test_telephony_does_not_force_concise_brevity(self):
        self.assertNotIn("Telephony → Concise", self.draft)
        self.assertIn("intended text-density baseline", self.draft)
        self.assertIn("voice-ux", self.draft)


if __name__ == "__main__":
    unittest.main()
