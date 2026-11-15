---
name: data360-segmentation-activation
description: "Create or troubleshoot Data Cloud / Data 360 segments and activation mappings, contact-point selection, audience counts and destination delivery. Use for audience preview, consent exclusion and authorized publishing. Not identity matching, core CRM campaigns, or general governance design."
---

# Data 360 Segmentation and Activation

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Establish audience purpose, membership entity/grain, target/channel, owner, refresh/freshness requirement and authorization scope. Distinguish a preview from creating an activation that may publish on its next schedule. Inspect existing target schedules and linked flows before saving anything live.
2. Inspect modeled relationships, identity requirements, calculated insights, data space and supported target/type compatibility. Reuse current schemas; do not guess object names or force identity resolution when source-level membership is sufficient.
3. Express inclusion and exclusion logic explicitly, including applicable opt-in/opt-out, unknown/expired/revoked consent, contact-point availability and owner-approved suppression rules. Verify consent provenance and precedence with data360-governance. Never assume all destinations enforce these rules automatically.
4. Preview synthetic membership and compare expected counts and individual inclusions/exclusions. Check nulls, duplicates, time windows, identity splits/merges and insight freshness. Separate member count from output-row count when multiple attributes/contact points expand the output.
5. Define activation membership DMO, contact-point selection and priority, attribute mappings and target identifiers. Verify supported related-attribute relationship paths and target-specific limits in current docs. Do not copy a Data 360 target workflow unchanged to every external target.
6. Prepare a configuration draft and payload samples. Treat saving/enabling an activation as potentially consequential because scheduled publishing and linked flows can deliver data. Execute only within authorization for the intended audience, fields, target and schedule; do not send a real audience as a validation shortcut.
7. In an authorized sandbox/test destination, observe publication and destination receipt, rejected rows and reconciliation. A successful save or queued publish is not proof of delivery. Bound retries and verify destination deduplication before resending.
8. Deliver segment logic, consent tests, mappings, run evidence and stop/rollback plan. Explain removal/consent-revocation propagation and retained downstream copies as target-specific unknowns until verified. Pausing future runs does not retract data already delivered.
