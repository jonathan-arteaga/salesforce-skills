"""Validate target handoffs are isolated and selected before loading."""

import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SELECTOR = SKILL_ROOT / "references/persona-encoding-guide.md"
ENCODE_DETAIL = SKILL_ROOT / "references/encode-detail.md"
AGENT_GUIDE = SKILL_ROOT / "references/persona-handoff-guide-agentscript.md"
BUILDER_GUIDE = SKILL_ROOT / "references/persona-encoding-guide-builder-legacy.md"
AGENT_TEMPLATE = SKILL_ROOT / "templates/persona-handoff-template.md"
BUILDER_TEMPLATE = SKILL_ROOT / "templates/persona-encoding-template-builder-legacy.md"
CASES = SKILL_ROOT / "tests/fixtures/encoder-selection-cases.json"


class EncodingSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selector = SELECTOR.read_text(encoding="utf-8")
        cls.encode = ENCODE_DETAIL.read_text(encoding="utf-8")
        cls.agent_guide = AGENT_GUIDE.read_text(encoding="utf-8")
        cls.builder_guide = BUILDER_GUIDE.read_text(encoding="utf-8")
        cls.agent_template = AGENT_TEMPLATE.read_text(encoding="utf-8")
        cls.builder_template = BUILDER_TEMPLATE.read_text(encoding="utf-8")
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))

    def test_selector_loads_exactly_one_target_path(self):
        self.assertIn("Never load both paths", self.selector)
        for path in (AGENT_GUIDE, BUILDER_GUIDE, AGENT_TEMPLATE, BUILDER_TEMPLATE):
            self.assertTrue(path.is_file(), path)
            self.assertIn(path.name, self.selector)

    def test_agent_script_path_is_semantic_handoff_only(self):
        combined = self.agent_guide + self.agent_template
        self.assertIn("persona-handoff.json", combined)
        self.assertIn("agentforce-generate", combined)
        for forbidden in (
            "```agentscript",
            "start_agent",
            "default_agent_user",
            "AgentforceServiceAgent",
            "@utils.transition",
        ):
            self.assertNotIn(forbidden, combined)

    def test_legacy_builder_path_is_provisional_brownfield_only(self):
        for text in (self.selector, self.encode, self.builder_guide):
            self.assertIn("provisional", text.lower())
            self.assertIn("brownfield", text.lower())
        self.assertIn("cannot create new legacy Builder agents", self.selector)
        self.assertNotIn("```agentscript", self.builder_template)

    def test_voice_routes_through_canonical_authoring_then_voice_ux(self):
        self.assertIn("agentforce-generate", self.selector)
        self.assertIn("conversation-design", self.selector)
        self.assertIn("voice-ux", self.selector)
        self.assertFalse((SKILL_ROOT / "references/persona-encoding-guide-voice.md").exists())
        self.assertFalse((SKILL_ROOT / "templates/persona-encoding-template-voice.md").exists())

    @staticmethod
    def _resolve_case(case):
        source = case["source"] or ""
        explicit_base = case.get("explicit_base")
        redirected = explicit_base == "legacy-builder" and case["mode"] == "greenfield"
        if explicit_base == "agent-script" or redirected:
            base = "references/persona-handoff-guide-agentscript.md"
            template = "templates/persona-handoff-template.md"
        elif explicit_base == "legacy-builder":
            base = "references/persona-encoding-guide-builder-legacy.md"
            template = "templates/persona-encoding-template-builder-legacy.md"
        elif source.endswith(".agent") or case["mode"] == "greenfield":
            base = "references/persona-handoff-guide-agentscript.md"
            template = "templates/persona-handoff-template.md"
        else:
            base = "references/persona-encoding-guide-builder-legacy.md"
            template = "templates/persona-encoding-template-builder-legacy.md"
        return base, template, case["channel"] in {"telephony", "multimodal-with-audio"}, redirected

    def test_selection_cases(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                base, template, voice, redirected = self._resolve_case(case)
                self.assertEqual(case["expected_base"], base)
                self.assertEqual(case["expected_template"], template)
                self.assertEqual(case["voice_handoff"], voice)
                self.assertEqual(case.get("legacy_builder_redirected", False), redirected)


if __name__ == "__main__":
    unittest.main()
