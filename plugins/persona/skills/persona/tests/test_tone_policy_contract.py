import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class TonePolicyContractTests(unittest.TestCase):
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
        cls.builder_encoder = (
            SKILL_ROOT / "references" / "persona-encoding-guide-builder-legacy.md"
        ).read_text(encoding="utf-8")
        cls.draft = (SKILL_ROOT / "references" / "draft-phase.md").read_text(
            encoding="utf-8"
        )
        cls.scoring = (
            SKILL_ROOT / "references" / "scoring-rubric.md"
        ).read_text(encoding="utf-8")

    def test_tone_flex_has_observable_cues_and_reset_conditions(self):
        for source in (
            self.framework,
            self.template,
            self.checklist,
            self.encoder,
            self.builder_encoder,
            self.draft,
            self.scoring,
        ):
            self.assertIn("observable cue", source.lower())
            self.assertIn("reset condition", source.lower())
        self.assertIn("do not carry the prior tone", self.framework)

    def test_archetype_examples_include_cues_and_resets(self):
        header = (
            "| Trigger | Dimension | Shift + maximum | Observable cue | "
            "Reset condition | Hard Boundary |"
        )
        for path in sorted((SKILL_ROOT / "archetypes").glob("*-persona.md")):
            with self.subTest(path=path.name):
                self.assertIn(header, path.read_text(encoding="utf-8"))

    def test_tone_boundaries_constrain_specific_failure_modes(self):
        self.assertIn("Positive behavior sets the baseline", self.framework)
        self.assertIn("plausible drift", self.framework)
        self.assertIn("preferred behavior", self.template)


if __name__ == "__main__":
    unittest.main()
