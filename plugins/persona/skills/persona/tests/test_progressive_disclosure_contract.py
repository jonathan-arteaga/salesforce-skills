"""Keep Persona's dispatcher compact without dropping behavioral contracts."""

from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]


class ProgressiveDisclosureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.draft_path = SKILL_DIR / "references" / "draft-phase.md"
        cls.spokes_path = SKILL_DIR / "references" / "spokes.md"
        cls.encode_path = SKILL_DIR / "references" / "encode-detail.md"

    def test_dispatcher_points_to_all_detailed_references(self):
        for relative_path in (
            "references/draft-phase.md",
            "references/refinement-mappings.md",
            "references/scoring-rubric.md",
            "references/encode-detail.md",
            "references/spokes.md",
            "references/interaction-design-notes.md",
        ):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, self.skill)
                self.assertTrue((SKILL_DIR / relative_path).is_file())

    def test_dispatcher_does_not_duplicate_extracted_procedures(self):
        self.assertNotIn("### Step 1: Input", self.skill)
        self.assertNotIn("### ⊙ NAME", self.skill)
        self.assertNotIn("### Decision Tree", self.skill)
        self.assertNotIn("### 100-Point Rubric", self.skill)
        self.assertLess(len(self.skill.splitlines()), 500)

    def test_draft_reference_keeps_current_reading_level_contract(self):
        draft = self.draft_path.read_text(encoding="utf-8")
        self.assertIn("Reading Level Flex", draft)
        self.assertIn("multiple mutually reinforcing relevant domain terms", draft)
        self.assertIn("Define a requested term locally", draft)
        self.assertIn("Technical Explanation Policy", draft)
        self.assertIn("rhetorical preference", draft)
        self.assertIn("agent-architecture", draft)

    def test_spokes_reference_keeps_lexicon_and_handoff_contract(self):
        spokes = self.spokes_path.read_text(encoding="utf-8")
        self.assertIn("Technical Explanation framing preference", spokes)
        self.assertIn("Term + Definition", spokes)
        self.assertIn("Semantic Persona calibration", spokes)
        self.assertIn("canonical authoring owner", spokes)

    def test_refinement_and_score_references_keep_current_contracts(self):
        refinement = (SKILL_DIR / "references" / "refinement-mappings.md").read_text(
            encoding="utf-8"
        )
        scoring = (SKILL_DIR / "references" / "scoring-rubric.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("controlled Persona calibration", refinement)
        self.assertIn("Technical Explanation Policy", refinement)
        self.assertIn("100-Point Rubric", scoring)
        self.assertIn("Existing local calibration review", scoring)
        self.assertIn("A term without a definition is an explicit gap", scoring)
        self.assertIn("agentforce-test", scoring)

    def test_interaction_reference_keeps_batching_and_confidence_rules(self):
        interaction = (
            SKILL_DIR / "references" / "interaction-design-notes.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Output before questions", interaction)
        self.assertIn("Batch independent questions", interaction)
        self.assertIn("Confidence callouts", interaction)

    def test_encode_reference_keeps_target_handoff_isolation(self):
        encode = self.encode_path.read_text(encoding="utf-8")
        self.assertIn("Choose one target", encode)
        self.assertIn("persona-handoff-guide-agentscript.md", encode)
        self.assertIn("persona-encoding-guide-builder-legacy.md", encode)
        self.assertIn("Do not load both target guides", encode)
        self.assertIn("contains no Agent Script syntax", encode)


if __name__ == "__main__":
    unittest.main()
