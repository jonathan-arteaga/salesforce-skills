"""Keep the Persona to voice-ux handoff reciprocal and precedence-safe."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = SKILL_ROOT.parents[1]
PERSONA_ROOT = PLUGIN_ROOT.parent / "persona" / "skills" / "persona"
MOVED_MARKER = "Moved verbatim from this skill's `SKILL.md`"


def _skill_with_moved_sections(root: Path) -> str:
    """SKILL.md with each section that was split into references/ restored in place."""
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    for path in sorted((root / "references").glob("*.md")):
        ref = path.read_text(encoding="utf-8")
        if MOVED_MARKER not in ref:
            continue
        body = ref.split(MOVED_MARKER, 1)[1].split("\n", 1)[1].lstrip("\n")
        if body.startswith("## Contents\n"):
            body = body.split("\n\n", 2)[2]
        link = f"references/{path.name}"
        pointer = re.compile(
            rf"^(#+ [^\n]*)\n\n(?:\*\*Required:\*\* read|Read) \[`{re.escape(link)}`\]\({re.escape(link)}\)[^\n]*\n",
            re.M,
        )
        text = pointer.sub(lambda _: body, text, count=1)
    return text

class PersonaHandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = _skill_with_moved_sections(SKILL_ROOT)
        cls.rubric = (SKILL_ROOT / "references" / "audit-rubric.md").read_text(
            encoding="utf-8"
        )
        cls.principles = (
            SKILL_ROOT / "references" / "voice-ux-principles.md"
        ).read_text(encoding="utf-8")
        cls.a08 = (
            SKILL_ROOT / "references" / "patterns" / "A08-tone-tags-and-expressivity.md"
        ).read_text(encoding="utf-8")
        cls.telephony = (
            SKILL_ROOT / "references" / "telephony-patterns.md"
        ).read_text(encoding="utf-8")
        cls.bundle = (
            SKILL_ROOT / "templates" / "rewrite-bundle.md"
        ).read_text(encoding="utf-8")
        cls.review = (
            SKILL_ROOT / "templates" / "v1-review-checklist.md"
        ).read_text(encoding="utf-8")
        patterns = SKILL_ROOT / "references" / "patterns"
        cls.patterns = {
            p.name[:3]: p.read_text(encoding="utf-8")
            for p in patterns.glob("[A-Z][0-9][0-9]-*.md")
        }
        cls.brief_template = (
            SKILL_ROOT / "templates" / "vocal-identity-brief.md"
        ).read_text(encoding="utf-8")
        cls.persona_framework = (
            PERSONA_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")

    def test_current_persona_skill_name_is_used(self):
        self.assertIn("`persona`", self.skill)
        self.assertNotIn("sf-ai-agentforce-persona", self.skill)

    def test_completed_persona_is_optional_authoritative_input(self):
        self.assertIn("optional", self.skill.lower())
        self.assertIn("persona.md", self.skill)
        self.assertIn("authoritative character contract", self.skill)
        self.assertIn("persona_source_sha256", self.bundle)

    def test_character_constraints_have_explicit_precedence(self):
        for phrase in (
            "Never-Say",
            "immutable",
            "Lexicon",
            "Guardrails",
            "[review needed]",
        ):
            self.assertIn(phrase, self.skill)
        self.assertIn("Persona precedence", self.rubric)
        self.assertIn("Persona preservation", self.review)

    def test_layer_c_is_adaptation_not_persona_redesign(self):
        self.assertIn("derive these from Persona", self.skill)
        self.assertIn("2–4", self.skill)
        self.assertIn("4–6", self.skill)
        self.assertIn("character redesign", self.telephony.lower())

    def test_phrasebook_rule_is_consistent(self):
        # One rule everywhere: a 4–6 acknowledgment signature set, never the
        # same token in adjacent turns. The old 3–6 range must not come back.
        for name, text in (
            ("SKILL.md", self.skill),
            ("telephony-patterns.md", self.telephony),
            ("rewrite-bundle.md", self.bundle),
            ("audit-rubric.md", self.rubric),
            ("voice-ux-principles.md", self.principles),
        ):
            self.assertNotIn("3–6", text, name)
        self.assertIn("adjacent turns", self.telephony)
        self.assertIn("adjacent turns", self.bundle)

    def test_lexical_tone_flex_remains_in_persona(self):
        self.assertIn("### Tone Flex", self.persona_framework)
        self.assertIn("word choice", self.persona_framework)
        self.assertIn("Persona Tone Flex", self.principles)
        self.assertIn("Persona Tone Flex", self.a08)
        self.assertIn("does not redefine", self.a08)

    def test_positive_trigger_covers_spoken_configuration_requests(self):
        frontmatter = self.skill.split("---", 2)[1]
        for phrase in (
            "voice casting",
            "voice tuning",
            "prosody",
            "audio tags",
            "pronunciation",
            "STT bias",
            "`modality voice:`",
        ):
            self.assertIn(phrase, frontmatter)

    def test_external_setup_exclusion_preserves_in_script_scope(self):
        self.assertIn("external carrier", self.skill)
        self.assertIn("in-script `modality voice:`", self.skill)


    def test_boundary_statement_is_verbatim(self):
        self.assertIn(
            "`persona` decides who the agent is and what it would say. This skill "
            "decides what that character sounds like on a phone line and how it "
            "behaves in spoken time.",
            self.skill,
        )
        self.assertIn("never redefines the character", self.skill)

    def test_structured_handoff_is_consumed_and_hash_checked(self):
        self.assertIn("persona-handoff.json", self.skill)
        self.assertIn("source_persona.sha256", self.skill)
        self.assertIn("persona_handoff_status", self.skill)
        self.assertIn("persona_handoff_status", self.bundle)
        self.assertIn('owner: "voice-ux"', self.skill)

    def test_extraction_covers_voice_relevant_persona_fields(self):
        for field in (
            "Personification",
            "Negative Identity",
            "agent name",
            "radio-test",
            "Empathy",
            "Personality Intensity",
            "Humor",
            "Brevity intent",
            "Reading Level",
            "technical_explanation_framing",
        ):
            self.assertIn(field, self.skill, field)

    def test_vocal_identity_casting_and_impersonation_patterns_exist(self):
        for pid in ("H08", "H09", "Z05"):
            self.assertIn(pid, self.patterns, pid)
        self.assertIn("Phase 4b", self.skill)
        self.assertIn("deliberately ambiguous", self.patterns["H08"])
        self.assertIn("never infer it from the role", self.patterns["H08"])
        self.assertIn("Runner-up", self.brief_template)
        self.assertIn("Listener tier", self.brief_template)

    def test_audition_channel_is_a_recommendation_with_preview_caveat(self):
        h09 = self.patterns["H09"]
        self.assertIn("A real phone call is recommended", h09)
        self.assertIn("Preview is acceptable", h09)
        self.assertNotIn("Listen on a real phone call, not Builder Preview", h09)

    def test_v3_stability_default_is_point_five(self):
        h03 = self.patterns["H03"]
        self.assertIn("**v3: 0.5**", h03)
        self.assertIn("outbound_stability: 0.5", self.bundle)
        self.assertIn("one parameter at a time", h03)
        self.assertIn("`persona_id` is a voice, not a Persona", h03)

    def test_casting_is_in_scope(self):
        out_of_scope = self.skill.split("## What this skill does NOT do", 1)[1]
        out_of_scope = out_of_scope.split("## Verification", 1)[0]
        self.assertNotIn("TTS voice casting", self.skill)
        self.assertIn("Casting the agent voice is in scope", out_of_scope)

    def test_no_unlabeled_hardcoded_register(self):
        # Warm-clinical survives only as a labeled illustration, never as a default.
        for pid, text in self.patterns.items():
            self.assertNotIn("Warm-clinical", text, pid)
            self.assertNotIn("warm-clinical", text, pid)
        self.assertNotIn("Warm-clinical", self.telephony)
        self.assertNotIn("warm-clinical", self.bundle)

    def test_voice_floors_flag_rather_than_override(self):
        a10 = self.patterns["A10"]
        self.assertIn("voice floor", a10)
        self.assertIn("Anthropomorphic", a10)
        self.assertIn("[review needed]", a10)
        self.assertIn("Voice floors the Persona can't lower", self.skill)


if __name__ == "__main__":
    unittest.main()
