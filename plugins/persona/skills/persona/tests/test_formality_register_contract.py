import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class FormalityRegisterContractTests(unittest.TestCase):
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

    def test_formality_and_register_are_orthogonal(self):
        self.assertIn("Formality must not add deference", self.framework)
        self.assertIn("Register must not change contractions", self.framework)
        self.assertIn("Formal + Advisor", self.framework)
        self.assertIn("Casual + Subordinate", self.framework)

    def test_formality_does_not_amplify_certainty(self):
        self.assertIn("must not amplify certainty", self.framework)
        self.assertIn("confidence invariant", self.template.lower())
        self.assertIn("confidence stays fixed", self.checklist.lower())


if __name__ == "__main__":
    unittest.main()
