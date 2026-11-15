"""Regression contract for pre-DRAFT, stakeholder-specific persona input."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8")


class StakeholderInputContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = source("SKILL.md")
        cls.spokes = source("references/spokes.md")
        cls.policy = source("references/stakeholder-question-policy.md")
        cls.worksheet = source("templates/stakeholder-worksheet-template.md")
        cls.workshop = source("templates/workshop-outline-template.md")
        cls.framework = source("references/persona-framework.md")
        cls.question_policy = source("references/workshop-question-policy.md")

    def test_explicit_worksheet_routes_before_draft_even_inline(self):
        for phrase in (
            "Route on the requested deliverable before running any phase",
            "before any draft",
            "do not substitute a general persona draft",
            "deliver the full questions inline",
            "never require or silently create one",
        ):
            self.assertIn(phrase, self.skill)
        self.assertIn("Only write `persona/[agent-name]/stakeholder-worksheet.md` when a file is requested", self.spokes)

    def test_standalone_input_does_not_need_hub_or_recorded_decisions(self):
        for phrase in (
            "independently of the Agentic Experience Hub",
            "without a decision log",
            "not the Agentic Experience Hub",
            "do not search for or demand a recorded decision",
        ):
            self.assertIn(phrase, self.skill)
        for phrase in (
            "standalone outputs from any folder",
            "no required format or repository file",
            "need not be tracked anywhere",
            "do not require a DRAFT phase",
        ):
            self.assertIn(phrase, self.policy)
        self.assertIn("No decision tracker or prior persona draft is needed", self.workshop)
        self.assertIn("Do not treat an industry stereotype as a settled persona decision", self.question_policy)

    def test_worksheet_and_workshop_are_distinct_greenfield_outputs(self):
        self.assertIn("WORKSHEET and WORKSHOP may run independently before DRAFT", self.spokes)
        self.assertIn("answer independently", self.spokes)
        self.assertIn("facilitator's plan", self.spokes)
        self.assertIn("Answer:", self.worksheet)
        for phrase in ("Board layout", "Facilitator action", "Converge and assign"):
            self.assertIn(phrase, self.workshop)
        self.assertIn("The content should not merely be the worksheet questions", self.policy)

    def test_legal_worksheet_invites_review_not_invented_requirements(self):
        for phrase in (
            "risk", "responsible-AI", "personification", "anthropomorphization",
            "humane", "approval", "do not write legal advice",
        ):
            self.assertIn(phrase, self.spokes)
        self.assertIn("Do not claim a specific disclosure is mandatory", self.policy)
        self.assertIn("or assume Legal alone decides product behavior", self.policy)
        self.assertIn("Do not add a brand stakeholder when the user excludes Brand", self.policy)

    def test_high_stakes_legal_example_is_optional_and_deidentified(self):
        for phrase in (
            "Optional example: high-stakes human-agent assistance",
            "illustration, not a worksheet template",
            "supplied decisions, session input, and accessible repository evidence",
            "Do not copy its sections, length, options, or question count",
            "human remains responsible for decisions",
            "Legal-only questions when Legal is a reviewer",
        ):
            self.assertIn(phrase, self.policy)

    def test_high_stakes_comparisons_and_legal_ownership(self):
        for phrase in (
            "same facts and permitted action",
            "write-your-own option",
            "missed step without blaming",
            "word-for-word wording", "prohibited language",
            "specify whether it applies to the assistant's words",
            "record where and when it applies",
            "review evidence", "revisit approved wording",
            "adjacent-constraint handoff",
        ):
            self.assertIn(phrase, self.policy)

    def test_workshop_exercises_do_not_override_framework(self):
        for phrase in (
            "Explore identity individually or in pairs",
            "Test difficult moments",
            "write their own",
            "shared dimension scales",
            "11 × 17-inch",
            "facts, safety language, capability, and permitted recommendation constant",
        ):
            self.assertIn(phrase, self.workshop)
        self.assertIn("Dot placement maps positions; it is not automatically a vote or approval", self.workshop)
        self.assertIn("Use positions and definitions from `references/persona-framework.md`", self.question_policy)
        self.assertIn("Empathy Level is not Brevity", self.policy)
        self.assertIn("Personification does not determine Personality Intensity", self.framework)
        self.assertIn("### Empathy Level\n\n*How much emotional validation", self.framework)
        self.assertIn("### Brevity\n\n*Response length", self.framework)

    def test_workshop_can_produce_a_board_ready_plan_from_customer_examples(self):
        for phrase in (
            "opening contrast", "good and bad", "participant input spaces",
            "scenario moments", "same facts",
        ):
            self.assertIn(phrase, self.workshop.lower())
        self.assertIn("decision status", self.spokes.lower())
        for phrase in (
            "## Board or room setup", "What felt right for", "What would feel wrong for",
            "Park workflow", "Candidate / approved / open",
        ):
            self.assertIn(phrase, self.workshop)
        self.assertIn("If capabilities are unknown, compare words and stance", self.workshop)
        self.assertIn("Do not copy a source board's dimension count", self.policy)
        self.assertIn("do not silently expand a Persona workshop into full conversation design", self.policy)

    def test_delivery_boundary_and_customer_facing_format(self):
        self.assertIn("document encoding to Google Docs or .docx belongs to the delivery surface", self.skill)
        self.assertIn("Remove author-only dimension/style labels", self.policy)
        self.assertIn("A draft or calibration file is an optional source", self.skill)


if __name__ == "__main__":
    unittest.main()
