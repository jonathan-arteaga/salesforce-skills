"""Keep standalone Salesforce packages covered as the marketplace evolves."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]


class SalesforceGuidanceTests(unittest.TestCase):
    def test_every_salesforce_package_has_reachable_guidance(self):
        catalog=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())['plugins']
        expected={e['name'] for e in catalog if e['category'] in ('Agentforce','Salesforce Platform and Analytics')}
        manifest=json.loads((ROOT/'docs/salesforce/manifest.json').read_text())
        self.assertEqual(expected,set(manifest['skills']))
        for name,domains in manifest['skills'].items():
            skill=ROOT/'plugins'/name/'skills'/name
            self.assertIn('(references/current-salesforce/guide.md)',(skill/'SKILL.md').read_text())
            self.assertTrue(domains)
            for domain in domains:
                self.assertTrue((ROOT/'docs/salesforce'/(domain+'.md')).exists())
                for source in manifest['sources'][domain]:
                    self.assertIn(urlsplit(source['url']).hostname,('help.salesforce.com','developer.salesforce.com','architect.salesforce.com'))
                    self.assertTrue(source['document_path'])

    def test_reusable_apex_templates_avoid_retired_query_clause(self):
        for package in ['platform-soql-query','experience-lwc-generate']:
            for path in (ROOT/'plugins'/package/'skills'/package/'assets').rglob('*.cls'):
                code=re.sub(r'//[^\n]*|/\*.*?\*/','',path.read_text(),flags=re.S)
                self.assertNotIn('WITH SECURITY_ENFORCED',code,str(path))


if __name__=='__main__':unittest.main()
