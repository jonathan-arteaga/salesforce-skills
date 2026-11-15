"""Validate Reading Level remains one axis with a companion Flex policy."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = SKILL_ROOT / "references/persona-framework.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
CHECKLIST = SKILL_ROOT / "templates/checklist-template.md"
PERSONA_TEMPLATE = SKILL_ROOT / "templates/persona-template.md"
SAMPLE_DIALOG_TEMPLATE = SKILL_ROOT / "templates/persona-calibration-template.md"
AGENTSCRIPT_GUIDE = SKILL_ROOT / "references/persona-handoff-guide-agentscript.md"
BUILDER_GUIDE = SKILL_ROOT / "references/persona-encoding-guide-builder-legacy.md"
ARCHETYPES = sorted((SKILL_ROOT / "archetypes").glob("*-persona.md"))
SCENARIOS = SKILL_ROOT / "tests/fixtures/reading-level-scenarios.md"
EXPECTED_CONTRAST = SKILL_ROOT / "tests/fixtures/reading-level-expected.md"
VALID_LEVELS = {"Plain Language", "Explained", "Technical"}


class ReadingLevelContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = FRAMEWORK.read_text(encoding="utf-8")
        cls.skill = SKILL_MD.read_text(encoding="utf-8")
        cls.checklist = CHECKLIST.read_text(encoding="utf-8")
        cls.persona_template = PERSONA_TEMPLATE.read_text(encoding="utf-8")
        cls.sample_dialog_template = SAMPLE_DIALOG_TEMPLATE.read_text(encoding="utf-8")
        cls.agentscript_guide = AGENTSCRIPT_GUIDE.read_text(encoding="utf-8")
        cls.builder_guide = BUILDER_GUIDE.read_text(encoding="utf-8")
        cls.scenarios = SCENARIOS.read_text(encoding="utf-8")
        cls.expected = EXPECTED_CONTRAST.read_text(encoding="utf-8")
        cls.reading_section = cls.framework.split("### Reading Level\n", 1)[1].split(
            "### Reading Level Flex", 1
        )[0]
        cls.flex_section = cls.framework.split("### Reading Level Flex", 1)[1].split(
            "\n---\n\n## Tone", 1
        )[0]
        cls.technical_policy_section = cls.framework.split(
            "## Technical Explanation Policy", 1
        )[1].split("\n---\n\n## Reference", 1)[0]

    def test_exact_definition(self):
        self.assertIn(
            "*How densely the agent uses domain terminology and specifications.*",
            self.reading_section,
        )

    def test_voice_boundary_declares_reading_level_as_the_sole_flex_exception(self):
        """The Voice section's own persistence claim must carry the Reading
        Level exception inline, not only three sections away under Tone --
        otherwise a Voice-only context load re-creates the 'Voice doesn't
        shift' contradiction with Reading Level Flex."""
        voice_boundary = self.framework.split('## Voice - "How do you talk?"', 1)[1].split(
            "### Formality", 1
        )[0]
        self.assertIn("persistent across all interactions", voice_boundary)
        self.assertIn("with one exception: Reading Level", voice_boundary)
        self.assertIn("Reading Level Flex", voice_boundary)
        self.assertIn("do not flex", voice_boundary)

    def test_authoritative_spectrum_has_exactly_three_positions(self):
        spectrum = re.search(r"◄─── (.+?) ───►", self.reading_section)
        self.assertIsNotNone(spectrum)
        positions = {part.strip() for part in spectrum.group(1).split("────")}
        self.assertEqual(positions, VALID_LEVELS)
        for legacy in ("Suppress", "Explain", "Match", "Advanced"):
            self.assertNotIn(f"**{legacy}**", self.reading_section)

    def test_flex_is_a_companion_not_a_dimension(self):
        self.assertIn("not a dimension", self.flex_section)
        self.assertIn("not a separate output artifact", self.flex_section)
        self.assertIn("**Baseline**", self.flex_section)
        self.assertIn("**Adaptation policy**", self.flex_section)
        self.assertIn("**Triggers**", self.flex_section)
        self.assertIn("**Shift rules**", self.flex_section)
        self.assertIn("**Flex range**", self.flex_section)
        self.assertIn("**Hard boundaries**", self.flex_section)
        self.assertIn("**14 dimensions**", self.skill)

    def test_archetypes_use_current_values_and_include_flex(self):
        for path in ARCHETYPES:
            text = path.read_text(encoding="utf-8")
            match = re.search(r"\| Voice \| Reading Level \| ([^|]+) \|", text)
            with self.subTest(file=path.name):
                self.assertIsNotNone(match)
                self.assertIn(match.group(1).strip(), VALID_LEVELS)
                self.assertIn("### Reading Level Flex", text)
                self.assertIn("**Baseline:**", text)
                self.assertIn("**Adaptation policy:**", text)
                self.assertIn("**Flex range:**", text)
                self.assertIn("**Hard boundaries:**", text)

    def test_checklist_uses_current_values_and_flex(self):
        self.assertIn("Plain Language / Explained / Technical", self.checklist)
        self.assertIn("**Reading Level Flex**", self.checklist)

    def test_compound_first_turn_signal_preserves_isolated_term_guard(self):
        self.assertIn("multiple mutually reinforcing", self.flex_section.lower())
        self.assertIn("one request", self.flex_section.lower())
        self.assertIn("at least two distinct terms", self.flex_section)
        self.assertIn("configured domain definitions", self.flex_section)
        self.assertIn("at most one position", self.flex_section)
        self.assertIn("for that turn", self.flex_section)
        self.assertIn("One isolated term is never enough", self.flex_section)

    def test_definition_request_is_term_local_by_default(self):
        self.assertIn("Define the requested term locally", self.flex_section)
        self.assertIn("broader simplification", self.flex_section)
        self.assertIn("broader misunderstanding", self.flex_section)

    def test_inferred_expertise_is_scoped_and_reset(self):
        self.assertIn("current domain or subagent", self.flex_section)
        self.assertIn("material topic change", self.flex_section)

    def test_reading_level_scope_boundary_is_explicit(self):
        boundary = (
            "does not establish technical-analysis quality, factual grounding, "
            "or product-suitability logic"
        )
        self.assertIn(boundary, self.flex_section)
        self.assertIn("Reading Level Flex changes presentation", self.skill)

    def test_factual_bridge_support_is_agent_design_owned(self):
        self.assertIn("Agent-design handoff", self.technical_policy_section)
        self.assertIn("agent-architecture", self.technical_policy_section)
        self.assertIn("agentforce-generate", self.technical_policy_section)
        self.assertIn("comparability", self.technical_policy_section)
        self.assertIn("recommendation confidence", self.technical_policy_section)

    def test_reading_flex_rules_live_in_persona_not_handoff_syntax(self):
        required = (
            "multiple mutually reinforcing",
            "requested term locally",
            "current domain or subagent",
            "technical-analysis quality",
        )
        normalized = re.sub(r"\s+", " ", self.persona_template).lower()
        for phrase in required:
            self.assertIn(phrase.lower(), normalized)
        self.assertIn("complete character contract", self.agentscript_guide)
        self.assertNotIn("```agentscript", self.agentscript_guide)

    def test_behavior_fixture_covers_reading_level_boundaries(self):
        for scenario in (
            "Compound first-turn expertise",
            "Term-local clarification",
            "Material domain change",
        ):
            self.assertIn(scenario, self.scenarios)
        self.assertIn("reading level flex", self.sample_dialog_template.lower())
        self.assertIn("controlled", self.sample_dialog_template.lower())

    def _expected_sections(self):
        sections = {}
        for level in VALID_LEVELS:
            sections[level] = self.expected.split(f"## {level}\n\n", 1)[1].split(
                "\n\n## ", 1
            )[0].replace("\n", " ")
        return sections

    def test_expected_contrast_is_grounded_and_single_axis(self):
        sections = self._expected_sections()
        for level in VALID_LEVELS:
            self.assertIn(f"## {level}", self.expected)
        self.assertIn("Denier is the yarn-weight measure", self.scenarios)
        self.assertIn("Hydrostatic head measures resistance to water pressure", self.scenarios)

        for level, response in sections.items():
            with self.subTest(level=level):
                self.assertRegex(response, r"(?:3-layer|three protective layers)")
                self.assertIn("75", response)
                self.assertIn("20,000", response)
                self.assertRegex(response.lower(), r"(?:pit|underarm).+zip")
                self.assertIn("sustained rain", response.lower())
                self.assertIn("alpine use", response.lower())
                numbers = set(re.findall(r"\b\d[\d,]*", response))
                self.assertLessEqual(numbers, {"3", "75", "20,000"})

        combined = " ".join(sections.values()).lower()
        for unsupported in (
            "breathability number", "price is", "weighs", "warranty",
            "guarantee", "rugged",
        ):
            self.assertNotIn(unsupported, combined)

        word_counts = [len(re.findall(r"\b[\w,.-]+\b", text)) for text in sections.values()]
        self.assertLessEqual(max(word_counts) - min(word_counts), max(word_counts) * 0.20)

        self.assertNotIn("hydrostatic", sections["Plain Language"].lower())
        self.assertIn("yarn-weight", sections["Explained"].lower())
        self.assertIn("water-pressure", sections["Explained"].lower())
        self.assertIn("75d", sections["Technical"].lower())
        self.assertIn("mechanical ventilation", sections["Technical"].lower())

    def test_archetypes_delegate_representative_scenarios(self):
        for path in ARCHETYPES:
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertIn("persona-calibration.md", text)
                self.assertIn("conversation-design", text)
                self.assertFalse(
                    path.with_name(path.name.replace("-persona.md", "-sample-dialog.md")).exists()
                )


if __name__ == "__main__":
    unittest.main()
