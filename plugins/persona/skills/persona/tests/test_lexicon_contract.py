"""Validate every Persona lexicon carries definitions."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = SKILL_ROOT / "references/persona-framework.md"
AGENT_GUIDE = SKILL_ROOT / "references/persona-handoff-guide-agentscript.md"
BUILDER_GUIDE = SKILL_ROOT / "references/persona-encoding-guide-builder-legacy.md"
PERSONA_TEMPLATE = SKILL_ROOT / "templates/persona-template.md"
ARCHETYPES = sorted((SKILL_ROOT / "archetypes").glob("*-persona.md"))


def _global_lexicon_table(text: str) -> list[list[str]]:
    section = text.split("**Global Lexicon:**", 1)[1].split("### Adaptation Notes", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or re.match(r"^\|[-|]+\|$", line.replace(" ", "")):
            continue
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


class LexiconContractTests(unittest.TestCase):
    def test_framework_requires_term_and_definition(self):
        text = FRAMEWORK.read_text(encoding="utf-8")
        self.assertIn("**Term** | Yes", text)
        self.assertIn("**Definition** | Yes", text)
        self.assertIn("Definitions are required at every Reading Level", text)

    def test_authoritative_guides_reject_bare_term_lists(self):
        for path in (AGENT_GUIDE, BUILDER_GUIDE):
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertNotIn("Legacy term list", text)
                self.assertNotIn("term-only", text)
                self.assertIn("term and definition", text)

    def test_persona_template_uses_definition_columns_for_both_scopes(self):
        text = PERSONA_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("| Term | Definition | Usage / preferred contrast | Immutable? |", text)
        self.assertIn(
            "| Subagent | Term | Definition | Usage / preferred contrast | Immutable? |",
            text,
        )

    def test_every_archetype_lexicon_row_has_a_definition(self):
        self.assertGreater(len(ARCHETYPES), 0)
        for path in ARCHETYPES:
            rows = _global_lexicon_table(path.read_text(encoding="utf-8"))
            with self.subTest(file=path.name):
                self.assertGreaterEqual(len(rows), 2, "Missing lexicon header or entries")
                self.assertEqual(rows[0][:2], ["Term", "Definition"])
                for row in rows[1:]:
                    self.assertGreaterEqual(len(row), 4, f"Malformed lexicon row: {row}")
                    self.assertTrue(row[0], f"Missing term: {row}")
                    self.assertTrue(row[1], f"Missing definition: {row}")


if __name__ == "__main__":
    unittest.main()
