"""Keep the pre-refactor contract available as migration evidence."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
LEGACY_FIXTURE = SKILL_ROOT / "tests/fixtures/legacy-contract.json"
SELECTOR = SKILL_ROOT / "references/persona-encoding-guide.md"
FRAMEWORK = SKILL_ROOT / "references/persona-framework.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
SCORING_RUBRIC = SKILL_ROOT / "references/scoring-rubric.md"


class MigrationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.legacy = json.loads(LEGACY_FIXTURE.read_text(encoding="utf-8"))
        cls.selector = SELECTOR.read_text(encoding="utf-8")
        cls.framework = FRAMEWORK.read_text(encoding="utf-8")
        cls.skill = SKILL_MD.read_text(encoding="utf-8")
        cls.scoring = SCORING_RUBRIC.read_text(encoding="utf-8")

    def test_legacy_reading_level_values_remain_recorded(self):
        self.assertEqual(
            self.legacy["reading_level"]["positions"],
            ["Suppress", "Explain", "Match", "Advanced"],
        )

    def test_legacy_combined_paths_remain_recorded(self):
        self.assertEqual(
            self.legacy["encoding"]["combined_guide"],
            "references/persona-encoding-guide.md",
        )
        self.assertEqual(
            self.legacy["encoding"]["combined_template"],
            "templates/persona-encoding-template.md",
        )

    def test_current_selector_records_the_handoff_migration(self):
        self.assertTrue(SELECTOR.is_file())
        self.assertIn("Persona target selector", self.selector)
        self.assertIn("persona-handoff-guide-agentscript.md", self.selector)
        self.assertNotIn("persona-encoding-guide-agentscript.md", self.selector)

    def test_legacy_reading_values_have_explicit_migrations(self):
        expected = {
            "Suppress": "Plain Language",
            "Explain": "Explained",
            "Advanced": "Technical",
        }
        for old, new in expected.items():
            with self.subTest(old=old, new=new):
                self.assertIn(f"`{old}` → `{new}`", self.framework)
        self.assertIn("references/scoring-rubric.md", self.skill)
        self.assertIn("`Match` requires a deliberate baseline", self.scoring)

    def test_legacy_lexicon_scope_and_bare_lists_have_explicit_migration(self):
        self.assertTrue(self.legacy["lexicon"]["term_only_lists_allowed"])
        self.assertIn("per-topic", self.legacy["lexicon"]["scopes"])
        self.assertIn(
            'A pre-refactor "Per-Topic Lexicon" scope maps to Per-Subagent Lexicon',
            self.framework,
        )
        self.assertIn(
            "A pre-refactor term-only list (terms with no Definition column) is not a valid lexicon",
            self.framework,
        )
        self.assertIn("never invent one", self.framework)

    def test_legacy_topic_instructions_label_migration_is_scoped_to_builder_ui(self):
        self.assertEqual(
            self.legacy["terminology"]["legacy_builder_ui_label"], "Topic Instructions"
        )
        self.assertIn(
            'Only the legacy Builder UI\'s literal field label ("Topic Instructions") stays as written',
            self.framework,
        )
        self.assertEqual(self.legacy["terminology"]["agent_script_canonical"], "subagent")


if __name__ == "__main__":
    unittest.main()
