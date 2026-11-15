"""Protect canonical subagent terminology in Persona source files."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


class TerminologyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = [
            path
            for path in SKILL_ROOT.rglob("*.md")
            if "tests/fixtures" not in path.as_posix()
        ]

    def test_deprecated_architecture_phrases_are_absent(self):
        """Deprecated topic-architecture phrases may appear only inside an
        explicit migration note (nearby 'legacy' or 'pre-refactor' context),
        mirroring the Topic Instructions carve-out below."""
        banned = ("per-topic", "Per-Topic", "Topic lexicon", "within each topic")
        for path in self.files:
            lines = path.read_text(encoding="utf-8").splitlines()
            for line_number, line in enumerate(lines, 1):
                for phrase in banned:
                    if phrase not in line:
                        continue
                    with self.subTest(file=path.name, phrase=phrase, line=line_number):
                        context = " ".join(lines[max(0, line_number - 2):line_number + 1]).lower()
                        self.assertTrue(
                            "legacy" in context or "pre-refactor" in context,
                            f"{path.name}:{line_number} uses deprecated phrase {phrase!r} "
                            "outside an explicit legacy/pre-refactor migration note",
                        )

    def test_no_deprecated_agent_script_topic_declarations(self):
        pattern = re.compile(r"^\s*topic\s+[A-Za-z][A-Za-z0-9_]*\s*:", re.MULTILINE)
        for path in self.files:
            with self.subTest(file=path.name):
                self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")))

    def test_topic_instructions_are_explicitly_legacy_ui_labels(self):
        for path in self.files:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "Topic Instructions" not in line:
                    continue
                with self.subTest(file=path.name, line=line_number):
                    context = " ".join(
                        path.read_text(encoding="utf-8").splitlines()[max(0, line_number - 2):line_number + 1]
                    ).lower()
                    self.assertIn("legacy", context)


if __name__ == "__main__":
    unittest.main()
