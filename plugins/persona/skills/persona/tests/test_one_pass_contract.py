"""Protect bounded one-pass completion for headless and unavailable users."""

from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]


class OnePassContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.draft = (SKILL_ROOT / "references/draft-phase.md").read_text(
            encoding="utf-8"
        )
        cls.encode = (SKILL_ROOT / "references/encode-detail.md").read_text(
            encoding="utf-8"
        )
        cls.interaction = (
            SKILL_ROOT / "references/interaction-design-notes.md"
        ).read_text(encoding="utf-8")

    def test_dispatcher_declares_bounded_one_pass_mode(self):
        self.assertIn("bounded one-pass", self.skill.lower())
        self.assertIn("interactive practitioner", self.skill.lower())

    def test_one_pass_detection_and_checkpoint_bypass_are_explicit(self):
        for phrase in (
            "I won't be available for follow-up",
            "finish in one pass",
            "completion_mode = bounded_one_pass",
            "do not stop at the start-small checkpoint",
            "record assumptions",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.draft)

    def test_name_gate_has_safe_one_pass_fallback(self):
        self.assertIn("bounded one-pass", self.encode.lower())
        self.assertIn("functional placeholder", self.encode)
        self.assertIn("never invent a person-like name", self.encode)

    def test_artifacts_are_written_before_response_summary(self):
        for phrase in (
            "Write artifacts before composing the response",
            "artifact index",
            "do not echo every complete artifact",
            "never omit a requested artifact",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.interaction.lower())


if __name__ == "__main__":
    unittest.main()
