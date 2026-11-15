"""Protect the reconstructed Degree of Personification contract."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
NEW_LEVELS = ("Not personal", "Individuated", "Anthropomorphic")
LEGACY_LEVELS = ("Talking System", "Familiar Thing", "Personal Assistant")


class PersonificationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.framework = (SKILL_ROOT / "references/persona-framework.md").read_text(
            encoding="utf-8"
        )
        cls.draft = (SKILL_ROOT / "references/draft-phase.md").read_text(
            encoding="utf-8"
        )
        cls.spokes = (SKILL_ROOT / "references/spokes.md").read_text(
            encoding="utf-8"
        )
        cls.scoring = (SKILL_ROOT / "references/scoring-rubric.md").read_text(
            encoding="utf-8"
        )
        cls.template = (SKILL_ROOT / "templates/persona-template.md").read_text(
            encoding="utf-8"
        )
        cls.checklist = (SKILL_ROOT / "templates/checklist-template.md").read_text(
            encoding="utf-8"
        )
        cls.migration = (
            SKILL_ROOT / "references/personification-migration.md"
        ).read_text(encoding="utf-8")

    def test_all_authoritative_surfaces_use_reconstructed_levels(self):
        surfaces = (
            self.skill,
            self.framework,
            self.draft,
            self.spokes,
            self.scoring,
            self.template,
            self.checklist,
        )
        for level in NEW_LEVELS:
            with self.subTest(level=level):
                self.assertTrue(all(level in surface for surface in surfaces))

    def test_legacy_levels_exist_only_in_migration_reference(self):
        for path in SKILL_ROOT.rglob("*.md"):
            if "tests" in path.parts or path.name == "personification-migration.md":
                continue
            text = path.read_text(encoding="utf-8")
            for legacy in LEGACY_LEVELS:
                with self.subTest(path=str(path), legacy=legacy):
                    self.assertNotIn(legacy, text)
        for legacy, current in zip(LEGACY_LEVELS, NEW_LEVELS):
            self.assertIn(f"`{legacy}` → `{current}`", self.migration)

    def test_framework_defines_observable_personification_boundaries(self):
        required = (
            "How strongly the agent presents itself as a distinct, person-like entity",
            "Proper Name",
            "singular self-reference",
            "Personal opinions",
            "Organizational “we”",
            "Human experiences or feelings",
            "does not determine how much character comes through",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.framework)

    def test_archetypes_use_deliberate_reconstructed_degrees(self):
        expected = {
            "drover-persona.md": "Anthropomorphic",
            "yt-persona.md": "Anthropomorphic",
            "steady-hand-persona.md": "Individuated",
            "concierge-persona.md": "Individuated",
        }
        for filename, level in expected.items():
            text = (SKILL_ROOT / "archetypes" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn(f"| **Personification** | {level} |", text)

    def test_personification_is_not_personality_intensity(self):
        self.assertIn(
            "Personification does not determine Personality Intensity", self.framework
        )
        self.assertIn(
            "A highly personified agent can be Reserved", self.framework
        )


if __name__ == "__main__":
    unittest.main()
