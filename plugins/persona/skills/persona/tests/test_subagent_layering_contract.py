"""Subagent Persona calibration is semantic and architecture-grounded."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class SubagentLayeringContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.encode = (SKILL_ROOT / "references" / "encode-detail.md").read_text(
            encoding="utf-8"
        )
        cls.spokes = (SKILL_ROOT / "references" / "spokes.md").read_text(
            encoding="utf-8"
        )
        cls.scoring = (
            SKILL_ROOT / "references" / "scoring-rubric.md"
        ).read_text(encoding="utf-8")

    def test_global_persona_is_inherited(self):
        self.assertIn("Global Persona is inherited", self.framework)
        self.assertIn("global Persona is inherited", self.scoring)

    def test_local_calibration_requires_canonical_architecture_evidence(self):
        self.assertIn("canonical inspection", self.spokes)
        self.assertIn("does not inspect the DSL", self.spokes)
        self.assertIn("existing subagent", self.encode)
        self.assertIn("semantic Persona delta", self.encode)

    def test_canonical_owner_applies_local_delta(self):
        self.assertIn("canonical authoring owner", self.spokes)
        self.assertIn("agentforce-generate", self.encode)
        self.assertNotIn("reasoning.instructions", self.spokes)
        self.assertNotIn("progress_indicator_message", self.spokes)


if __name__ == "__main__":
    unittest.main()
