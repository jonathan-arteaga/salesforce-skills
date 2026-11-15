"""Require coding-agent workflow references to route through versioned artifact templates."""
from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class VersionedArtifactContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.draft = (SKILL_ROOT / "references" / "draft-phase.md").read_text(encoding="utf-8")
        cls.refine = (SKILL_ROOT / "references" / "refinement-mappings.md").read_text(encoding="utf-8")
        cls.score = (SKILL_ROOT / "references" / "scoring-rubric.md").read_text(encoding="utf-8")

    def test_draft_routes_to_canonical_persona_template(self):
        self.assertIn("templates/persona-template.md", self.draft)
        self.assertIn("version and date frontmatter", self.draft)

    def test_refine_routes_to_canonical_sample_template(self):
        self.assertIn("templates/persona-calibration-template.md", self.refine)
        self.assertIn("version and date frontmatter", self.refine)

    def test_score_requires_versioned_evaluation_artifact(self):
        self.assertIn("version and date frontmatter", self.score)
        self.assertIn("evaluation.md", self.score)

    def test_generated_artifacts_use_current_date_not_template_revision_date(self):
        for label, text in (
            ("skill", self.skill),
            ("draft", self.draft),
            ("refine", self.refine),
            ("score", self.score),
        ):
            with self.subTest(label=label):
                self.assertIn("current local date", text)
                self.assertIn("template revision date", text)

    def test_always_loaded_dispatcher_preserves_artifact_invariant(self):
        self.assertIn("Every generated Markdown artifact", self.skill)
        self.assertIn("version and date frontmatter", self.skill)


if __name__ == "__main__":
    unittest.main()
