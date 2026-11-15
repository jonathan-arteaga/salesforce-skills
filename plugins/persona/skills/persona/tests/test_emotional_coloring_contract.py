import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class EmotionalColoringContractTests(unittest.TestCase):
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

    def test_non_neutral_coloring_has_an_observable_cue(self):
        self.assertIn("Neutral may remain linguistically unmarked", self.framework)
        self.assertIn("observable cue", self.framework.lower())
        self.assertIn("observable cue", self.template.lower())
        self.assertIn("observable cue", self.checklist.lower())

    def test_coloring_preserves_adjacent_dimensions_and_facts(self):
        self.assertIn("Brevity remains separate", self.framework)
        self.assertIn("must not remove task-required content", self.framework)
        self.assertIn("does not create epistemic rules", self.framework)

    def test_positive_coloring_uses_only_supplied_progress(self):
        self.assertIn("supplied confirmed progress/success", self.framework)
        self.assertIn("Persona does not invent progress", self.framework)


if __name__ == "__main__":
    unittest.main()
