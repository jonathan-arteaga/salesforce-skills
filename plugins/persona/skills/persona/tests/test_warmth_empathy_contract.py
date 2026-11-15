import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class WarmthEmpathyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.template = (SKILL_ROOT / "templates" / "persona-template.md").read_text(
            encoding="utf-8"
        )
        cls.checklist = (
            SKILL_ROOT / "templates" / "checklist-template.md"
        ).read_text(encoding="utf-8")

    def test_warmth_is_visible_outside_empathy_moments(self):
        self.assertIn("low-emotion routine sample", self.framework)
        self.assertIn("Cool + Attuned", self.framework)
        self.assertIn("Warm + Minimal", self.framework)
        self.assertIn("routine warmth cue", self.template.lower())

    def test_warmth_does_not_invent_service_capability_or_length(self):
        self.assertIn("unsupported availability or follow-up", self.framework)
        self.assertIn("Warmth does not require more words", self.framework)
        self.assertIn("Brevity stays fixed", self.checklist)

    def test_empathy_names_impact_without_forcing_affiliation(self):
        self.assertIn("impact without first-person affiliation", self.framework)
        self.assertIn("empathy cue", self.template.lower())


if __name__ == "__main__":
    unittest.main()
