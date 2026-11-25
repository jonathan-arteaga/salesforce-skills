"""Verify Antigravity installer, skill scaffolder, manifest lockstep, SVGs, and README invariants."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


packager = load_script("package_marketplace")
installer = load_script("install_antigravity")
scaffolder = load_script("new_skill")
validator = load_script("validate_skills")


def github_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = slug.replace(" ", "-")
    return slug


class PackagingAndToolingTests(unittest.TestCase):
    def test_antigravity_and_codex_manifests_in_lockstep(self):
        codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        agy = json.loads((ROOT / ".antigravity-plugin/plugin.json").read_text(encoding="utf-8"))
        codex_names = [p["name"] for p in codex["plugins"]]
        agy_names = [Path(s).name for s in agy["skills"]]
        self.assertEqual(codex_names, agy_names)
        self.assertEqual(len(codex_names), 17)
        self.assertTrue(agy.get("$schema"))
        self.assertTrue(agy.get("suggestedPrompts"))

    def test_install_antigravity_sync_and_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills"
            dry = installer.sync_skills(target_dir=target, selected=["salesforce-apex"], dry_run=True)
            self.assertEqual(list(dry["installed"]), ["salesforce-apex"])
            self.assertFalse(target.exists())

            full = installer.sync_skills(target_dir=target)
            self.assertEqual(len(full["installed"]), 17)
            self.assertTrue((target / "salesforce-apex" / "SKILL.md").is_file())
            self.assertTrue((target / "agentforce-review" / "LICENSE").is_file())

            cleaned = installer.sync_skills(target_dir=target, selected=["salesforce-apex"], clean=True)
            self.assertEqual(list(cleaned["installed"]), ["salesforce-apex"])
            self.assertEqual(len(cleaned["removed"]), 16)
            self.assertFalse((target / "agentforce-review").exists())

    def test_new_skill_scaffolds_compliant_skill_and_detects_orphans(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            plugin_dir = scaffolder.scaffold_skill(
                name="salesforce-sample",
                display_name="Salesforce Sample",
                description="Handle a sample Salesforce workflow cleanly. Use salesforce-apex for Apex.",
                short_description="Handle a sample Salesforce workflow cleanly.",
                category="Core Platform & Integrations",
                root=tmp_root,
                sync_manifests=False,
            )
            skill_dir = plugin_dir / "skills" / "salesforce-sample"
            self.assertEqual(validator.validate_skill(skill_dir), [])
            self.assertEqual(packager.main(["--root", str(tmp_root)]), 0)
            self.assertEqual(packager.main(["--root", str(tmp_root), "--check"]), 0)

            # Adding an unlinked reference file must fail the zero-orphan check.
            (skill_dir / "references" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                packager.check_links_and_orphans(tmp_root)

    def test_adaptive_svgs_are_valid_xml(self):
        expected = [
            "hero-dark.svg",
            "hero-light.svg",
            "architecture-dark.svg",
            "architecture-light.svg",
        ]
        for filename in expected:
            svg_path = ROOT / "assets" / filename
            self.assertTrue(svg_path.is_file(), filename)
            ET.fromstring(svg_path.read_text(encoding="utf-8"))

    def test_readme_links_anchors_and_html_blocks(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        headings = {github_slug(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.+)$", readme, re.M)}

        # Check markdown and HTML links + #anchors
        hrefs = re.findall(r'href="([^"]+)"', readme) + re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)\)", readme)
        self.assertTrue(hrefs)
        for href in hrefs:
            if href.startswith("#"):
                self.assertIn(href[1:], headings, f"Broken README anchor {href}")
                continue
            if urlsplit(href).scheme:
                continue
            target = (ROOT / href.split("#", 1)[0]).resolve()
            self.assertTrue(target.exists(), f"Missing README link target {href}")

        # Verify every skill SKILL.md is linked in README.md
        for skill_md in sorted((ROOT / "plugins").glob("*/skills/*/SKILL.md")):
            rel = str(skill_md.relative_to(ROOT))
            self.assertIn(rel, readme, f"README missing skill link {rel}")

        # Verify zero blank lines or fenced code blocks inside HTML <table> or <details> blocks
        for tag in ("table", "details"):
            for block in re.findall(rf"<{tag}\b.*?</{tag}>", readme, re.S):
                self.assertNotIn("\n\n", block, f"Blank line inside <{tag}> breaks GitHub GFM HTML parsing")
                self.assertNotIn("```", block, f"Fenced code block inside <{tag}> breaks GitHub GFM HTML parsing")


if __name__ == "__main__":
    unittest.main()
