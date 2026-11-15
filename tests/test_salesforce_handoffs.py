"""Validate explicit handoff contracts and standalone reference ownership."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

def skill(name):
    return ROOT / "plugins" / name / "skills" / name

class HandoffTests(unittest.TestCase):
    def test_handoff_targets_are_packaged_and_consumers_exist(self):
        catalog = {p["name"] for p in json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())["plugins"]}
        for owner, targets in json.loads((ROOT / "docs/salesforce/routes.json").read_text()).items():
            self.assertIn(owner, catalog)
            self.assertTrue((skill(owner) / "SKILL.md").is_file())
            self.assertEqual(len(targets), len(set(targets)))
            for target in targets:
                self.assertIn(target, catalog, (owner, target))
                self.assertTrue((skill(target) / "SKILL.md").is_file())

    def test_grounding_standalone_copies_match_canonical_owner(self):
        owner = skill("agentforce-grounding") / "references"
        consumer = skill("agentforce-generate") / "references"
        expected = (owner / "data-library-reference.md").read_bytes().replace(b"(workflow.md)", b"(grounding-workflow.md)")
        self.assertEqual(expected, (consumer / "data-library-reference.md").read_bytes())
        self.assertEqual((owner / "workflow.md").read_bytes(), (consumer / "grounding-workflow.md").read_bytes())

    def test_wave_one_routing_fixture_targets_exist(self):
        cases = json.loads((ROOT / "tests/salesforce_foundation_cases.json").read_text())["routing"]
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            for target in case["expected_primary"]:
                self.assertTrue((skill(target) / "SKILL.md").exists(), target)

if __name__ == "__main__":
    unittest.main()
