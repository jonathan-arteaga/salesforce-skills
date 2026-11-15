"""Protect evidence-backed Chatting Style encoding specificity."""

from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ChattingStyleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = (SKILL_ROOT / "references/persona-framework.md").read_text(
            encoding="utf-8"
        )
        cls.template = (SKILL_ROOT / "templates/persona-template.md").read_text(
            encoding="utf-8"
        )
        cls.checklist = (SKILL_ROOT / "templates/checklist-template.md").read_text(
            encoding="utf-8"
        )

    def test_emoji_requires_vocabulary_and_cadence_when_enabled(self):
        self.assertIn("**Emoji vocabulary:**", self.framework)
        self.assertIn("**Emoji cadence:**", self.framework)
        self.assertIn("approved emoji vocabulary", self.template.lower())
        self.assertIn("Emoji cadence", self.template)
        self.assertIn("Emoji vocabulary + cadence", self.checklist)

    def test_expressive_punctuation_requires_observable_pattern(self):
        self.assertIn("**Punctuation pattern:**", self.framework)
        self.assertIn("em dash, ellipsis, or exclamation point", self.framework)
        self.assertIn("Punctuation pattern / cadence", self.template)
        self.assertIn("Punctuation pattern", self.checklist)

    def test_casual_capitalization_preserves_proper_and_immutable_terms(self):
        phrase = "Never lowercase proper nouns, product names, acronyms, units, or immutable terms"
        self.assertIn(phrase, self.framework)
        self.assertIn("Never reorder a sentence or add filler merely to force a lowercase opening", self.framework)
        self.assertIn("Capitalization exceptions", self.template)
        self.assertIn("Capitalization exceptions", self.checklist)


if __name__ == "__main__":
    unittest.main()
