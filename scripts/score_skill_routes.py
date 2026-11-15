"""Score independently collected routing decisions; does not invoke a model."""
import argparse
import json
from pathlib import Path
import sys


def score(cases, decisions):
    expected = {c['id']: set(c['expected_primary']) for c in cases}
    if len(expected) != len(cases):
        raise ValueError('Duplicate case IDs')
    observed = {}
    for row in decisions:
        if row['id'] in observed:
            raise ValueError(f'Duplicate result: {row["id"]}')
        if row['id'] not in expected:
            raise ValueError(f'Unknown result: {row["id"]}')
        observed[row['id']] = row['primary_skill']
    if expected.keys() != observed.keys():
        raise ValueError(f'Missing results: {sorted(expected.keys() - observed.keys())}')
    failures = []
    for case_id, names in expected.items():
        actual = observed[case_id]
        matches = actual in names if names else actual is None
        if not matches:
            failures.append({'id': case_id, 'expected': sorted(names), 'actual': actual})
    return {'passed': len(cases) - len(failures), 'total': len(cases), 'failures': failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path)
    parser.add_argument('--cases', type=Path, default=Path(__file__).resolve().parents[1] / 'tests/skill_behavior_cases.json')
    args = parser.parse_args()
    try:
        result = score(json.loads(args.cases.read_text())['routing'], json.loads(args.results.read_text()))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return int(bool(result['failures']))


if __name__ == '__main__':
    sys.exit(main())
