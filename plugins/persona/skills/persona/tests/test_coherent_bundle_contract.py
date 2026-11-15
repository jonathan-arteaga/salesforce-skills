"""Persona exports content-preservation criteria without claiming runtime proof."""

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class CoherentBundleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.calibration = (
            SKILL_ROOT / "templates" / "persona-calibration-template.md"
        ).read_text(encoding="utf-8")
        cls.refine = (
            SKILL_ROOT / "references" / "refinement-mappings.md"
        ).read_text(encoding="utf-8")
        cls.score = (
            SKILL_ROOT / "references" / "scoring-rubric.md"
        ).read_text(encoding="utf-8")
        cls.encode = (
            SKILL_ROOT / "references" / "encode-detail.md"
        ).read_text(encoding="utf-8")
        cls.handoff = (
            SKILL_ROOT / "templates" / "persona-handoff-template.md"
        ).read_text(encoding="utf-8")

    def test_persona_changes_expression_not_content(self):
        self.assertIn("Persona changes expression, not the content contract", self.framework)
        for required in (
            "explicit statuses",
            "dates",
            "uncertainty",
            "capability and action ownership",
            "permitted recommendations",
        ):
            self.assertIn(required, self.framework)

    def test_calibration_is_not_a_runtime_test_or_flow(self):
        self.assertIn("not a conversation flow", self.calibration.lower())
        self.assertIn("do not claim", self.calibration.lower())
        self.assertIn("controlled response", self.refine.lower())
        self.assertIn("conversation-design", self.refine)
        self.assertIn("agentforce-test", self.refine)

    def test_acceptance_criteria_are_handed_downstream(self):
        self.assertIn("downstream_acceptance", self.handoff)
        self.assertIn("conversation-design", self.handoff)
        self.assertIn("agentforce-test", self.handoff)
        self.assertIn("emits acceptance criteria, not runtime evidence", self.encode)
        self.assertIn("does not claim runtime proof", self.score)


if __name__ == "__main__":
    unittest.main()
