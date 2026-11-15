"""Enforce required attribution and separation from colleague recognition."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RELATED = SKILL_ROOT / "RELATED-READING.md"
ATTRIBUTIONS = SKILL_ROOT / "references" / "attributions.md"
CREDITS = SKILL_ROOT / "CREDITS.md"
README = SKILL_ROOT / "README.md"
ATTRIBUTION = (
    "**Required attribution:** This skill includes adapted material from "
    "[conversation-design-library-v2]"
    "(https://github.com/phil-haenggi/conversation-design-library-v2) by "
    "Philipp Haenggi, licensed under "
    "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
    "Changes were made. No endorsement by the licensor is implied."
)
ATTRIBUTION_SHA256 = "11d9490a3d5917bb0c91962579527febdba4fe7e033eea32a148c60dc637119a"


class ProvenanceContractTests(unittest.TestCase):
    def test_required_attribution_is_exact_and_single(self):
        attribution = ATTRIBUTIONS.read_text(encoding="utf-8")
        self.assertIn(ATTRIBUTION, attribution)
        actual_hash = hashlib.sha256((ATTRIBUTION + "\n").encode("utf-8")).hexdigest()
        self.assertEqual(ATTRIBUTION_SHA256, actual_hash)

        occurrences = 0
        for path in SKILL_ROOT.rglob("*.md"):
            if "tests" in path.parts:
                continue
            occurrences += path.read_text(encoding="utf-8").count("CC BY 4.0")
        self.assertEqual(1, occurrences, "CC attribution must appear exactly once")

    def test_further_reading_is_neutral_and_drops_google_item(self):
        related = RELATED.read_text(encoding="utf-8")
        self.assertIn("## Further Reading", related)
        further_reading = related.split("## Further Reading", 1)[1]
        self.assertNotRegex(further_reading, r"(?i)\breferences?\b")
        self.assertNotIn("draws on", related.lower())
        self.assertNotIn("Google Conversation Design", related)

    def test_colleague_credits_are_separate_and_placeholder_free(self):
        credits = CREDITS.read_text(encoding="utf-8")
        self.assertNotIn("## Sources", credits)
        self.assertNotIn("{{URL", credits)
        self.assertNotIn("CC BY 4.0", credits)
        self.assertNotIn("reading references", credits.lower())

    def test_readme_is_portable_and_routes_required_attribution(self):
        readme = README.read_text(encoding="utf-8")
        self.assertIn("references/attributions.md", readme)
        self.assertIn("RELATED-READING.md", readme)
        for source_only_path in ("CREDITS.md", "ROADMAP.md", "templates/", "archetypes/"):
            self.assertNotIn(source_only_path, readme)
        self.assertIn("stakeholder-worksheet.md", readme)

    def test_source_shaped_phrases_are_absent_from_behavioral_assets(self):
        behavioral_paths = [
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "references" / "persona-framework.md",
            SKILL_ROOT / "templates" / "persona-template.md",
            SKILL_ROOT / "archetypes" / "drover-persona.md",
            SKILL_ROOT / "archetypes" / "steady-hand-persona.md",
            SKILL_ROOT / "archetypes" / "concierge-persona.md",
            SKILL_ROOT / "archetypes" / "yt-persona.md",
            SKILL_ROOT / "references" / "spokes.md",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in behavioral_paths)
        for phrase in ("One Breath Test", "### Backstory"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, combined)

    def test_radio_test_remains_and_repeat_turn_progression_is_delegated(self):
        framework = (SKILL_ROOT / "references" / "persona-framework.md").read_text(
            encoding="utf-8"
        )
        spokes = (SKILL_ROOT / "references" / "spokes.md").read_text(
            encoding="utf-8"
        )
        template = (SKILL_ROOT / "templates" / "persona-template.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("radio test", framework)
        self.assertIn("hears the name once", framework)
        self.assertIn("repeat it unambiguously", framework)
        self.assertIn("radio test", spokes)
        self.assertIn("pronounce, repeat, distinguish, and find", spokes)
        self.assertNotIn("**Tapering:**", framework)
        self.assertNotIn("tapering behavior", template)
        self.assertIn("conversation progression", framework.lower())
        self.assertIn("`conversation-design`", framework)


if __name__ == "__main__":
    unittest.main()
