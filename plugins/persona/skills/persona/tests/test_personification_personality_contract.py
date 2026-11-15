import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class PersonificationPersonalityContractTests(unittest.TestCase):
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

    def test_personification_and_intensity_evidence_are_independent(self):
        self.assertIn(
            "Personification markers do not count as Personality Intensity evidence",
            self.framework,
        )
        self.assertIn("Not personal + Bold", self.framework)
        self.assertIn("Anthropomorphic + Reserved", self.framework)
        self.assertIn("task-response cue", self.framework)

    def test_intensity_cue_excludes_personification_markers(self):
        self.assertIn("task-response intensity cue", self.template.lower())
        self.assertIn("excluding names", self.checklist.lower())


if __name__ == "__main__":
    unittest.main()
