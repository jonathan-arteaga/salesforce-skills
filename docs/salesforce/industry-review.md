# Cross-industry design review — 2026-11-15

Added a reusable industry/role playbook to persona and packaged it with six consuming workflows: architecture, conversation design, generation, testing, workshops, and voice. Twelve industry contexts and seven roles are starting hypotheses, not Salesforce-certified personalities or deployable templates. Product anchors and design synthesis are explicitly separated.

Research used official Salesforce persona guidance, industry Help catalogs, current setup pages, use-case pages, and customer examples. Several industry URLs were absent from the Docs MCP index; official web documentation supplied the fallback. Marketing/customer-story sources support inspiration, not availability or outcome guarantees. The source register is in the playbook.

Two independent offline exercises covered retail/admissions personality alternatives and hotel/manufacturing first-release designs. Outputs preserved the distinction between tone and permission, proposed bounded workflows, handled uncertain outcomes, and honestly marked runtime checks NOT RUN. These are design checks, not live agent evaluations.

Validation: 43 skill metadata checks; package generation/link checks; 29 root, 164 persona, 604 architecture, and 407 Data 360 tests passed (1,204 total). No org deployment or live model evaluation occurred.

## Public-export review

The owner explicitly authorized public publication. Automated approval review initially rejected one upload batch because its exact private-origin contents had not been screened. Before retrying, all 1,202 tracked export files were scanned for credential assignments, private keys, GitHub/AWS token shapes, Salesforce session-token shapes, JWT shapes, org IDs, Salesforce hosts, email addresses, and internal host patterns. Candidate assignments were reviewed: they were runtime variables, placeholders, or synthetic test tokens. No live credentials were identified by these checks; pattern scans are not a guarantee that all sensitive data can be detected.

Four example files were sanitized to replace person-specific email addresses, a demo org ID, and a demo site with reserved example values:

- Escalation generator metadata/requirements reference
- Escalation generator dashboard template
- Data 360 schema skill example
- Voice summary/readback example

The public export excludes personal packages and the private writing profile. Third-party license files are preserved. Per-file migration checksums describe the original extraction baseline, not these later edits. Current Git content hashes are the authority for the published revision.

The owner subsequently explicitly approved publishing the reviewed library, including synthetic test identifiers and configuration examples. Publication proceeds with the sanitized export.
