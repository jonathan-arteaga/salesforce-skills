import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class RegisterContractTests(unittest.TestCase):
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

    def test_register_is_encoded_as_decision_ownership(self):
        self.assertIn("Register changes decision ownership, not just pronouns", self.framework)
        self.assertGreaterEqual(self.framework.count("Observable decision move:"), 4)
        self.assertIn("decision-ownership behavior", self.template)
        self.assertIn("decision-ownership behavior", self.checklist)

    def test_peer_advisor_overlap_is_explicit(self):
        self.assertIn("Peer and Advisor may converge", self.framework)
        self.assertIn("no genuine shared work", self.framework)
        self.assertIn("do not simulate collaboration", self.framework)

    def test_subordinate_and_coach_preserve_task_quality(self):
        self.assertIn("Subordinate never suppresses material evidence", self.framework)
        self.assertIn(
            "Coach asks at most one targeted question before useful output",
            self.framework,
        )


if __name__ == "__main__":
    unittest.main()
