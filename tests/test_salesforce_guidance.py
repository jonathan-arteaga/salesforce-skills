"""Keep Salesforce packages aligned with documented Release 264+ factual sources and API 67+ safety."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class SalesforceGuidanceTests(unittest.TestCase):
    def test_every_salesforce_package_has_documented_source_coverage(self):
        catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))["plugins"]
        expected = {entry["name"] for entry in catalog}
        manifest = json.loads((ROOT / "docs/salesforce/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(expected, set(manifest["skills"]))
        for name, domains in manifest["skills"].items():
            skill = ROOT / "plugins" / name / "skills" / name
            self.assertTrue((skill / "SKILL.md").is_file(), name)
            self.assertTrue(domains, name)
            for domain in domains:
                self.assertTrue((ROOT / "docs/salesforce" / f"{domain}.md").exists(), domain)
                for source in manifest["sources"][domain]:
                    self.assertIn(
                        urlsplit(source["url"]).hostname,
                        ("help.salesforce.com", "developer.salesforce.com", "architect.salesforce.com"),
                    )
                    self.assertTrue(source["document_path"])

    def test_reusable_apex_files_avoid_retired_query_clause(self):
        for path in (ROOT / "plugins").rglob("*.cls"):
            code = re.sub(r"//[^\n]*|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
            self.assertNotIn("WITH SECURITY_ENFORCED", code, str(path))


if __name__ == "__main__":
    unittest.main()
