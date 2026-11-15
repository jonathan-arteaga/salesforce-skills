"""Opt-in protected instructions remain separate from response copy and policy design."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProtectedInstructionContractTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_opt_in_intake_does_not_infer_legal_approval(self):
        text = self.read("references/draft-phase.md")
        self.assertIn("Protected instruction text", text)
        self.assertIn("explicit opt-in", text)
        self.assertIn("Do not infer protection or approval", text)
        self.assertIn("instructions, responses, or both", text)

    def test_attachment_is_optional_and_not_a_persona_dimension(self):
        text = self.read("templates/persona-template.md")
        self.assertIn("### Protected Instruction Text", text)
        self.assertIn("not a Persona dimension", text)
        self.assertIn("Omit this section when no protected instruction text is supplied", text)
        self.assertIn("Do not recite these instructions", text)

    def test_handoff_reuses_adjacent_constraints(self):
        text = self.read("templates/persona-handoff-template.md")
        payload = json.loads(text.split("```json\n", 1)[1].split("```", 1)[0])
        block = payload["adjacent_constraints"][0]
        self.assertEqual(block["preservation"], "exact")
        self.assertEqual(block["text_role"], "agent_instruction")
        for field in ("intended_scope", "approval_authority", "source_reference", "verbatim_reference"):
            self.assertIn(field, block)
        self.assertIn("omit these optional preservation fields", text)

    def test_exactness_and_conflict_rules_apply_to_handoff(self):
        text = self.read("references/persona-handoff-guide-agentscript.md")
        self.assertIn("shorten, paraphrase, merge, recase, or repunctuate", text)
        self.assertIn("surface the conflict", text)
        self.assertIn("unresolved", text)
        self.assertIn("does not grant higher runtime authority", text)

    def test_legacy_payload_is_prepared_not_applied(self):
        text = self.read("templates/persona-encoding-template-builder-legacy.md")
        self.assertIn("## Protected Instruction Text", text)
        self.assertIn("prepared, not applied", text)
        self.assertIn("Do not trim a protected block to fit", text)
        self.assertIn("unresolved", text)

    def test_legal_questions_distinguish_instruction_from_response(self):
        text = self.read("references/stakeholder-question-policy.md")
        self.assertIn("agent instructions, customer-facing responses, or both", text)
        self.assertIn("who approves", text)


if __name__ == "__main__":
    unittest.main()
