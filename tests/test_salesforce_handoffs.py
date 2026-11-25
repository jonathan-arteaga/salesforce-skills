"""Validate explicit handoff contracts, routing coverage, and Antigravity/Codex catalog parity."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def skill(name):
    return ROOT / "plugins" / name / "skills" / name


class HandoffTests(unittest.TestCase):
    def test_handoff_targets_are_packaged_and_cover_catalog(self):
        catalog = {
            p["name"]
            for p in json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))["plugins"]
        }
        routes = json.loads((ROOT / "docs/salesforce/routes.json").read_text(encoding="utf-8"))
        self.assertEqual(set(routes), catalog)
        for owner, targets in routes.items():
            self.assertIn(owner, catalog)
            self.assertTrue((skill(owner) / "SKILL.md").is_file())
            self.assertEqual(len(targets), len(set(targets)))
            self.assertNotIn(owner, targets, f"{owner} should not route to itself")
            for target in targets:
                self.assertIn(target, catalog, (owner, target))
                self.assertTrue((skill(target) / "SKILL.md").is_file())

    def test_behavior_routing_fixture_covers_every_skill(self):
        catalog = {
            p["name"]
            for p in json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))["plugins"]
        }
        cases = json.loads((ROOT / "tests/skill_behavior_cases.json").read_text(encoding="utf-8"))["routing"]
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        covered = set()
        negatives = 0
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            if not case["expected_primary"]:
                negatives += 1
            for target in case["expected_primary"]:
                self.assertIn(target, catalog, target)
                covered.add(target)
        self.assertEqual(covered, catalog, f"Uncovered skills in skill_behavior_cases.json: {sorted(catalog - covered)}")
        self.assertGreaterEqual(negatives, 2, "Expected at least 2 negative boundary cases")

    def test_foundation_routing_fixture_targets_exist(self):
        cases = json.loads((ROOT / "tests/salesforce_foundation_cases.json").read_text(encoding="utf-8"))["routing"]
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            for target in case["expected_primary"]:
                self.assertTrue((skill(target) / "SKILL.md").exists(), target)


if __name__ == "__main__":
    unittest.main()
