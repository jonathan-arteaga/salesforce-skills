"""Keep character design in Persona and spoken realization in voice-ux."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = SKILL_ROOT.parents[1]
VOICE_UX_ROOT = PLUGIN_ROOT.parent / "voice-ux" / "skills" / "voice-ux"
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

class VoiceScopeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shipping_markdown = {
            path: path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*.md")
            if "tests" not in path.parts
        }
        cls.combined = "\n".join(cls.shipping_markdown.values())
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.framework = (
            SKILL_ROOT / "references" / "persona-framework.md"
        ).read_text(encoding="utf-8")
        cls.encode = (SKILL_ROOT / "references" / "encode-detail.md").read_text(
            encoding="utf-8"
        )
        cls.draft = (SKILL_ROOT / "references" / "draft-phase.md").read_text(
            encoding="utf-8"
        )
        cls.voice_ux = _skill_with_moved_sections(VOICE_UX_ROOT)

    def test_static_catalog_and_voice_overlay_are_absent(self):
        for relative_path in (
            "references/voice-catalog.json",
            "references/persona-encoding-guide-voice.md",
            "templates/persona-encoding-template-voice.md",
        ):
            with self.subTest(relative_path=relative_path):
                self.assertFalse((SKILL_ROOT / relative_path).exists())

    def test_persona_does_not_select_or_tune_a_voice(self):
        forbidden = (
            "voice-catalog.json",
            "persona-encoding-guide-voice.md",
            "persona-encoding-template-voice.md",
            "## Voice Selection",
            "Fine-Tuning Starting Points",
            "recommend at least 3 voices",
            "recommend a voice by name",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), self.combined.lower())

    def test_persona_keeps_lexical_situational_tone_flex(self):
        self.assertIn("### Tone Flex", self.framework)
        self.assertIn("word choice", self.framework)
        self.assertIn("lexical", self.framework.lower())
        self.assertIn("Observable cue", self.framework)
        self.assertIn("Reset condition", self.framework)
        self.assertIn("Tone Flex", self.draft)

    def test_voice_ux_owns_prosodic_realization_not_tone_policy(self):
        self.assertIn("situational prosody", self.framework.lower())
        self.assertIn("voice-ux", self.framework)
        self.assertIn("Persona Tone Flex", self.voice_ux)
        self.assertIn("prosod", self.voice_ux.lower())
        self.assertIn("[review needed]", self.voice_ux)

    def test_reciprocal_ownership_is_explicit(self):
        normalized = " ".join(self.encode.split())
        self.assertIn("`voice-ux`", normalized)
        self.assertIn("Persona retains situational Tone Flex", normalized)
        self.assertIn("prosodic realization", normalized)
        self.assertIn("existing `voice-ux` implementation scope is unchanged", normalized.lower())

    def test_ambiguous_warmth_request_is_disambiguated(self):
        for source in (self.skill, self.voice_ux):
            self.assertIn("make it warmer", source)
            self.assertIn("words/stance", source)
            self.assertIn("audible delivery", source)

    def test_persona_trigger_excludes_spoken_delivery_configuration(self):
        frontmatter = self.skill.split("---", 2)[1]
        for phrase in (
            "voice casting",
            "prosody",
            "audio tags",
            "pronunciation",
            "STT bias",
            "`modality voice:`",
            "use `voice-ux`",
        ):
            self.assertIn(phrase, frontmatter)

    def test_readme_documents_voice_handoff_not_voice_assets(self):
        readme = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Persona owns situational Tone Flex", readme)
        self.assertIn("`voice-ux`", readme)
        self.assertNotIn("Static voice catalog", readme)

    def test_voice_requirements_route_to_voice_ux_verbatim(self):
        template = (SKILL_ROOT / "templates" / "persona-handoff-template.md").read_text(
            encoding="utf-8"
        )
        guide = (
            SKILL_ROOT / "references" / "persona-handoff-guide-agentscript.md"
        ).read_text(encoding="utf-8")
        framework = (SKILL_ROOT / "references" / "persona-framework.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("agent-architecture | agentforce-generate | voice-ux", template)
        self.assertIn('owner: "voice-ux"', guide)
        self.assertIn("does not design or cast the voice", guide)
        self.assertIn("persona-handoff.json", guide)
        self.assertIn("Vocal Identity brief, casting, and light tuning", framework)
        self.assertNotIn("voice casting/tuning guidance", framework)


if __name__ == "__main__":
    unittest.main()
