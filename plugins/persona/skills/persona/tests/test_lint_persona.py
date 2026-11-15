import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "lint_persona.py"

VALID = '''---
version: "1.0.0"
date: 2026-09-03
---
# Agent Persona: Compass
## Context
| **Agent Name** | Compass |
| **Personification** | Individuated |
| **Organizational “we”** | No |
## Identity
- **Calm** — States pressure without escalating it.
- **Candid** — Names uncertainty before reassurance.
- **Decisive** — Gives one supported next step.
### What You're Not
- Not a cheerleader — keeps praise proportional.
- Not an oracle — never turns unknowns into facts.
### Degree of Personification: Individuated
- **Separate identity:** descriptive label.
- **Singular self-reference:** functional only.
- **Personal opinions:** No.
- **Organizational “we”:** No.
## Persona Profile
| Category | Dimension | Value | Signal |
|---|---|---|---|
| Register | Register | Advisor | strong |
| Voice | Formality | Professional | strong |
| Voice | Warmth | Neutral | strong |
| Voice | Personality Intensity | Moderate | strong |
| Voice | Reading Level | Explained | strong |
| Tone | Emotional Coloring | Neutral | strong |
| Tone | Empathy Level | Understated | strong |
| Delivery | Brevity | Concise | strong |
| Delivery | Humor | None | strong |
| Chatting Style | Emoji | None | strong |
| Chatting Style | Formatting | Selective | strong |
| Chatting Style | Punctuation | Standard | strong |
| Chatting Style | Capitalization | Standard | strong |
### Tone Flex
| Trigger | Dimension | Shift + maximum | Observable cue | Reset condition | Hard Boundary |
|---|---|---|---|---|---|
| Frustration | Empathy | Understated → Moderate; one clause | “That repeat miss is frustrating.” | Next routine topic | Never mirror panic |
## Expression
### Never-Say List
- “Great question!”
- “I’d be happy to help.”
- “Hope this helps.”
- “Let me think.”
- “Absolutely!”
## Phrasing
### Phrase Book
A palette, not a script. Do not reuse the same phrase stem within one response or adjacent turns.
| Situation | Example Phrase(s) |
|---|---|
| Acknowledgment | “Got it.” / “Noted.” |
| Recommendation | “Next, …” / “The supported move is …” |
### Lexicon
| Term | Definition | Usage / preferred contrast | Immutable? |
|---|---|---|---|
| Gate | A required approval before release. | Use only for formal approval. | No |
'''


class LintPersonaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("lint_persona", SCRIPT)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load {SCRIPT}")
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.module
        spec.loader.exec_module(cls.module)

    def test_valid_persona_has_no_errors(self):
        diagnostics = self.module.lint_text(VALID)
        self.assertEqual([], [d for d in diagnostics if d["severity"] == "error"])

    def test_reports_actionable_contract_failures(self):
        broken = (
            VALID.replace(" | Observable cue | Reset condition", "")
            .replace("“Got it.” / “Noted.”", "“Got it.”")
            .replace("A palette, not a script. Do not reuse the same phrase stem within one response or adjacent turns.\n", "")
            .replace("| Gate | A required approval before release. |", "| Gate |  |")
            .replace("- “Absolutely!”\n", "")
        )
        codes = {d["code"] for d in self.module.lint_text(broken)}
        self.assertTrue(
            {"tone-flex-contract", "phrase-book-variety", "phrase-book-repetition", "lexicon-definition", "never-say-count"}.issubset(codes)
        )

    def test_reports_immutable_and_lexicon_conflicts(self):
        broken = VALID.replace(
            "- “Absolutely!”\n",
            "- “Absolutely!”\n- “Gate”\n",
        )
        broken += """\n### Immutable Content\n- “Required wording.”\n"""
        codes = {d["code"] for d in self.module.lint_text(broken)}
        self.assertIn("lexicon-never-say-conflict", codes)
        self.assertIn("immutable-precedence", codes)
        self.assertIn("immutable-shape", codes)

    def test_rejects_voice_configuration_but_only_warns_on_unusual_pairing(self):
        candidate = VALID.replace(
            "| Voice | Formality | Professional |",
            "| Voice | Formality | Formal |",
        )
        candidate = candidate.replace(
            "| Chatting Style | Punctuation | Standard |",
            "| Chatting Style | Punctuation | Expressive |",
        )
        candidate += (
            "\nPunctuation pattern: exclamation marks used sparingly."
            "\nmodality voice:\n    voice_id: forbidden\n"
        )
        diagnostics = self.module.lint_text(candidate)
        codes = {d["code"] for d in diagnostics}
        self.assertIn("dimension-pairing-warning", codes)
        self.assertIn("voice-scope", codes)
        self.assertFalse(
            any(
                d["severity"] == "error"
                and d["code"] == "dimension-pairing-warning"
                for d in diagnostics
            )
        )

    def test_formal_theatrical_persona_is_not_blocked(self):
        candidate = VALID.replace(
            "| Voice | Formality | Professional |",
            "| Voice | Formality | Formal |",
        ).replace(
            "| Chatting Style | Punctuation | Standard |",
            "| Chatting Style | Punctuation | Expressive |",
        )
        candidate += "\nPunctuation pattern: exclamation marks used sparingly.\n"
        diagnostics = self.module.lint_text(candidate)
        self.assertTrue(
            any(
                d["severity"] == "warning"
                and d["code"] == "dimension-pairing-warning"
                for d in diagnostics
            )
        )
        self.assertFalse(
            any(d["severity"] == "error" for d in diagnostics), diagnostics
        )

    def test_warns_on_clinical_playful_directional_risk(self):
        candidate = VALID.replace(
            "| Tone | Emotional Coloring | Neutral |",
            "| Tone | Emotional Coloring | Clinical |",
        ).replace("| Delivery | Humor | None |", "| Delivery | Humor | Playful |")
        diagnostics = self.module.lint_text(candidate)
        risks = [d for d in diagnostics if d["code"] == "dimension-interaction-risk"]
        self.assertTrue(risks)
        self.assertTrue(all(d["severity"] == "warning" for d in risks))
        self.assertTrue(any("Clinical" in d["message"] and "Playful" in d["message"] for d in risks))
        self.assertTrue(all("two fixtures" in d["message"] for d in risks))
        self.assertTrue(all("content-contract omission" in d["message"] for d in risks))
        self.assertTrue(all("not a universal contradiction" in d["message"] for d in risks))
        self.assertTrue(all("final combined" in d["message"] for d in risks))
        self.assertFalse(
            any(d["severity"] == "error" and "Clinical" in d["message"] for d in diagnostics)
        )

    def test_skill_runs_lint_at_complete_artifact_boundaries(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("allowed-tools:", skill.split("\n---\n", 1)[0])
        self.assertGreaterEqual(skill.count("scripts/lint_persona.py"), 2)
        self.assertIn("completed Persona document", skill)

    def test_shipping_archetypes_have_no_lint_errors(self):
        for path in sorted((SKILL_ROOT / "archetypes").glob("*-persona.md")):
            with self.subTest(path=path.name):
                errors = [
                    item
                    for item in self.module.lint_text(path.read_text(encoding="utf-8"))
                    if item["severity"] == "error"
                ]
                self.assertEqual([], errors)

    def test_cli_json_is_machine_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "persona.md"
            path.write_text(VALID, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--json", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(str(path), payload["path"])


if __name__ == "__main__":
    unittest.main()
