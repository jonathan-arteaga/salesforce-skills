"""Keep rhetorical framing in Persona and factual support in agent design."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ReadingBridgeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.guide = (
            SKILL_ROOT / "references" / "persona-handoff-guide-agentscript.md"
        ).read_text(encoding="utf-8")
        cls.template = (
            SKILL_ROOT / "templates" / "persona-template.md"
        ).read_text(encoding="utf-8")

    def test_reading_level_and_framing_preference_are_independent(self):
        self.assertIn("Bridge strength does not change", self.framework)
        self.assertIn("terminology density", self.framework)
        self.assertIn("Reading Level", self.framework)

    def test_persona_records_rhetorical_preference_only(self):
        for source in (self.framework, self.guide, self.template):
            self.assertIn("Stay in frame", source)
            self.assertIn("Selective bridge", source)
            self.assertIn("Pair routinely", source)
        self.assertIn("rhetorical", self.guide.lower())

    def test_agent_design_owns_factual_support(self):
        for source in (self.framework, self.guide, self.template):
            self.assertIn("agent-architecture", source)
            self.assertIn("agentforce-generate", source)
        self.assertIn("comparability", self.framework)
        self.assertIn("recommendation confidence", self.framework)


if __name__ == "__main__":
    unittest.main()
