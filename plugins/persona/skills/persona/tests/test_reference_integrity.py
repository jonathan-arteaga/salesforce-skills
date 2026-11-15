"""Validate Persona reference and template paths resolve."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DOCS = ("SKILL.md", "README.md")


class ReferenceIntegrityTests(unittest.TestCase):
    def test_backticked_local_paths_exist(self):
        pattern = re.compile(r"`((?:references|templates)/[^`]+)`")
        for source_name in SOURCE_DOCS:
            text = (SKILL_ROOT / source_name).read_text(encoding="utf-8")
            for rel_path in sorted(set(pattern.findall(text))):
                with self.subTest(source=source_name, path=rel_path):
                    self.assertTrue(
                        (SKILL_ROOT / rel_path).is_file(),
                        f"{source_name} references missing file: {rel_path}",
                    )

    def test_core_persona_files_exist(self):
        expected = (
            "SKILL.md",
            "README.md",
            "RELATED-READING.md",
            "references/attributions.md",
            "references/draft-phase.md",
            "references/refinement-mappings.md",
            "references/scoring-rubric.md",
            "references/encode-detail.md",
            "references/spokes.md",
            "references/interaction-design-notes.md",
            "references/persona-framework.md",
            "references/framework-manifest.json",
            "references/personification-migration.md",
            "references/persona-encoding-guide.md",
            "references/persona-handoff-guide-agentscript.md",
            "references/persona-encoding-guide-builder-legacy.md",
            "templates/persona-template.md",
            "templates/persona-calibration-template.md",
            "templates/persona-handoff-template.md",
            "templates/persona-encoding-template-builder-legacy.md",
        )
        for rel_path in expected:
            with self.subTest(path=rel_path):
                self.assertTrue((SKILL_ROOT / rel_path).is_file())

    def test_out_of_scope_agent_script_assets_are_absent(self):
        for rel_path in (
            "scripts/parse_agent_yaml.py",
            "scripts/verify_persona_patch.py",
            "scripts/lint_static_strings.py",
            "references/persona-encoding-guide-agentscript.md",
            "templates/persona-encoding-template-agentscript.md",
            "templates/sample-dialog-template.md",
        ):
            with self.subTest(path=rel_path):
                self.assertFalse((SKILL_ROOT / rel_path).exists())


if __name__ == "__main__":
    unittest.main()
