import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('score_skill_routes', ROOT/'scripts/score_skill_routes.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class RoutingTests(unittest.TestCase):
    cases = [{'id': 'positive', 'expected_primary': ['write-as-me']}, {'id': 'negative', 'expected_primary': []}]

    def test_correct_and_negative_cases(self):
        result = module.score(self.cases, [{'id': 'positive', 'primary_skill': 'write-as-me'}, {'id': 'negative', 'primary_skill': None}])
        self.assertEqual(result['passed'], 2)

    def test_wrong_skill_and_overtrigger(self):
        result = module.score(self.cases, [{'id': 'positive', 'primary_skill': 'write-readme'}, {'id': 'negative', 'primary_skill': 'write-as-me'}])
        self.assertEqual(result['passed'], 0)
        self.assertEqual(len(result['failures']), 2)

    def test_missing_duplicate_and_unknown_results(self):
        for results in ([], [{'id': 'negative', 'primary_skill': None}]*2, [{'id': 'unknown', 'primary_skill': None}]):
            with self.subTest(results=results), self.assertRaises(ValueError):
                module.score(self.cases, results)

    def test_fixture_names_exist(self):
        cases = json.loads((ROOT/'tests/skill_behavior_cases.json').read_text())['routing']
        names = {p.parent.name for p in (ROOT/'plugins').glob('*/skills/*/SKILL.md')}
        self.assertEqual(len({c['id'] for c in cases}), len(cases))
        for case in cases:
            self.assertTrue(case['prompt'].strip())
            self.assertTrue(set(case['expected_primary']) <= names, case['id'])


if __name__ == '__main__':
    unittest.main()
