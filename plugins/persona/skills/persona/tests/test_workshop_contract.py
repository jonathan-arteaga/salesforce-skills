"""Validate Persona-level technical framing and its agent-design boundary."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class TechnicalExplanationPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.policy = (
            SKILL_ROOT / "references" / "workshop-question-policy.md"
        ).read_text(encoding="utf-8")
        cls.seeds = (
            SKILL_ROOT / "references" / "workshop-scenario-seeds.md"
        ).read_text(encoding="utf-8")
        cls.template = (
            SKILL_ROOT / "templates" / "persona-template.md"
        ).read_text(encoding="utf-8")
        cls.guide = (
            SKILL_ROOT / "references" / "persona-handoff-guide-agentscript.md"
        ).read_text(encoding="utf-8")

    def test_policy_lives_under_phrasing_not_reading_level(self):
        policy_index = self.framework.index("## Technical Explanation Policy")
        lexicon_index = self.framework.index("## Lexicon")
        reference_index = self.framework.index("## Reference")
        self.assertGreater(policy_index, lexicon_index)
        self.assertLess(policy_index, reference_index)

    def test_three_framing_preferences_remain(self):
        for value in ("Stay in frame", "Selective bridge", "Pair routinely"):
            self.assertIn(value, self.framework)
            self.assertIn(value, self.template)
            self.assertIn(value, self.guide)

    def test_factual_support_is_handed_to_agent_design(self):
        for source in (self.framework, self.template, self.guide):
            self.assertIn("agent-architecture", source)
            self.assertIn("agentforce-generate", source)
        self.assertIn("comparability", self.framework)
        self.assertIn("recommendation confidence", self.framework)

    def test_workshop_question_remains_rhetorical(self):
        self.assertIn(
            "When answering a technical question, should the agent tie it back to outcomes, or stick to the technical details?",
            self.policy,
        )
        self.assertIn("Technical detail → outcome", self.seeds)
        self.assertIn("Outcome → technical evidence", self.seeds)


if __name__ == "__main__":
    unittest.main()
