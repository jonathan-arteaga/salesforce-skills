"""Protect the Persona SCORE rubric's 100-point contract."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCORING_RUBRIC = SKILL_ROOT / "references" / "scoring-rubric.md"


class ScoringContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = SCORING_RUBRIC.read_text(encoding="utf-8")
        cls.rubric = text.split("### 100-Point Rubric", 1)[1].split(
            "### Per-Subagent and Per-Action Sub-Scoring", 1
        )[0]

    def test_rubric_totals_one_hundred(self):
        points = [int(value) for value in re.findall(r"\|\s*/(\d+)\s*\|", self.rubric)]
        self.assertGreater(len(points), 0, "No rubric point values found")
        self.assertEqual(sum(points), 100, f"Rubric totals {sum(points)}, not 100")

    def test_rubric_has_no_duplicate_category_names(self):
        names = re.findall(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*/\d+", self.rubric, re.MULTILINE)
        self.assertEqual(len(names), len(set(names)), "Duplicate SCORE categories found")


if __name__ == "__main__":
    unittest.main()
