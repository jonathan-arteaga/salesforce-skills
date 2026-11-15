import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ReadingBrevityContractTests(unittest.TestCase):
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

    def test_reading_level_and_brevity_are_orthogonal(self):
        self.assertIn("Brevity must not change glossing policy", self.framework)
        self.assertIn("Reading Level must not set response length", self.framework)
        self.assertIn("Terse + Plain Language", self.framework)
        self.assertIn("Expansive + Technical", self.framework)

    def test_identifiers_do_not_raise_reading_level(self):
        self.assertIn("Required identifiers", self.framework)
        self.assertIn("terminology-density cue", self.template.lower())
        self.assertIn("required identifiers", self.checklist.lower())


if __name__ == "__main__":
    unittest.main()
