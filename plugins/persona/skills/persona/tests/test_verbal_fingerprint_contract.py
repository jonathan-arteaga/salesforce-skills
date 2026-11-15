import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class VerbalFingerprintContractTests(unittest.TestCase):
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
        cls.encoder = (
            SKILL_ROOT / "references" / "persona-handoff-guide-agentscript.md"
        ).read_text(encoding="utf-8")

    def test_phrase_book_is_a_varied_palette_not_a_script(self):
        for source in (self.framework, self.template, self.checklist):
            self.assertIn("palette, not a script", source)
            self.assertIn("Do not reuse the same phrase stem", source)
        self.assertIn("Phrase Book", self.encoder)
        self.assertIn("complete character contract", self.encoder)

    def test_discourse_markers_are_functional_and_not_stacked(self):
        self.assertIn("Omit a discourse marker when", self.framework)
        self.assertIn("Never stack multiple markers", self.framework)
        self.assertIn("function, not decoration", self.template)

    def test_exact_anti_phrases_require_explicit_never_say_entries(self):
        self.assertIn("Explicit Never-Say entries are required", self.framework)
        self.assertIn("positive guidance alone", self.framework)
        self.assertIn("resist direct user requests", self.checklist)


if __name__ == "__main__":
    unittest.main()
