"""Behavior proofs for agentforce-generate dependency resolution."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = SKILL_ROOT.parents[1]
SKILL_TEXT = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
MIGRATION_TEXT = (
    SKILL_ROOT / "references" / "sf-skills-migration.md"
).read_text(encoding="utf-8")
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

CONVERSATION_TEXT = _skill_with_moved_sections(
    PLUGIN_ROOT.parent / "conversation-design" / "skills" / "conversation-design"
)
MANAGED_RELATIVE = Path(
    ".pi/agent/sf-skills/effective/skills/agentforce-generate/SKILL.md"
)


def _probe_from(text: str) -> str:
    match = re.search(
        r"```bash\n(# agentforce-generate-resolver-v1\n.*?)\n```",
        text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("No versioned agentforce-generate resolver found")
    return match.group(1)


class DependencyResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.voice_probe = _probe_from(SKILL_TEXT)

    def _run_probe(self, candidates: tuple[str, ...]):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / "home"
            project = root / "project"
            home.mkdir()
            project.mkdir()
            for candidate in candidates:
                path = Path(
                    candidate.replace("$HOME", str(home)).replace(
                        "$PWD", str(project)
                    )
                )
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "---\nname: agentforce-generate\n---\n", encoding="utf-8"
                )
            env = os.environ.copy()
            env["HOME"] = str(home)
            env["VOICE_UX_SKILL_DIR"] = str(project / "skills" / "voice-ux")
            (project / "skills" / "voice-ux").mkdir(parents=True)
            result = subprocess.run(
                ["bash", "-c", self.voice_probe],
                cwd=project,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            return result, home, project

    def test_managed_effective_tree_alone_satisfies_voice_ux_gate(self):
        candidate = "$HOME/" + str(MANAGED_RELATIVE)
        result, home, _project = self._run_probe((candidate,))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(str(home / MANAGED_RELATIVE), result.stdout.strip())

    def test_managed_effective_tree_is_preferred_over_generic_copy(self):
        managed = "$HOME/" + str(MANAGED_RELATIVE)
        generic = "$HOME/.agents/skills/agentforce-generate/SKILL.md"
        result, home, _project = self._run_probe((managed, generic))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(str(home / MANAGED_RELATIVE), result.stdout.strip())

    def test_existing_generic_and_project_paths_still_resolve(self):
        cases = (
            "$PWD/skills/agentforce-generate/SKILL.md",
            "$HOME/.agents/skills/agentforce-generate/SKILL.md",
            "$PWD/.agents/skills/agentforce-generate/SKILL.md",
        )
        for candidate in cases:
            with self.subTest(candidate=candidate):
                result, home, project = self._run_probe((candidate,))
                expected = candidate.replace("$HOME", str(home)).replace(
                    "$PWD", str(project)
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(
                    Path(expected).resolve(), Path(result.stdout.strip()).resolve()
                )

    def test_missing_dependency_returns_nonzero(self):
        result, _home, _project = self._run_probe(())
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)

    def test_conversation_design_delegates_instead_of_copying_resolver(self):
        self.assertNotIn("# agentforce-generate-resolver-v1", CONVERSATION_TEXT)
        self.assertNotIn(str(MANAGED_RELATIVE), CONVERSATION_TEXT)
        self.assertIn(
            "`voice-ux` owns and runs its own Phase 0 dependency gate",
            CONVERSATION_TEXT,
        )
        self.assertIn(
            "Do not cache or reinterpret the dependency result",
            CONVERSATION_TEXT,
        )

    def test_conversation_design_does_not_add_bash_for_dependency_probe(self):
        frontmatter = CONVERSATION_TEXT.removeprefix("---\n").split(
            "\n---\n", 1
        )[0]
        self.assertNotIn("allowed-tools:", frontmatter)

    def test_docs_treat_manual_only_copy_as_installed_without_reinstall(self):
        managed = "~/.pi/agent/sf-skills/effective/skills/agentforce-generate/SKILL.md"
        for source in (SKILL_TEXT, MIGRATION_TEXT):
            self.assertIn(managed, source)
        self.assertIn("manual-only", SKILL_TEXT)
        self.assertIn("do not install a duplicate", MIGRATION_TEXT.lower())

    def test_effective_tree_is_authoritative_not_pristine_source_clone(self):
        self.assertIn("over the source checkout", SKILL_TEXT)
        self.assertIn("not a replacement", MIGRATION_TEXT)


if __name__ == "__main__":
    unittest.main()
