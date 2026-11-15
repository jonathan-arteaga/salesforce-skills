---
name: data360-governance
description: "Design or review Data Cloud / Data 360 data spaces, data access policies, masking, consent requirements and governed consumption paths. Use for policy matrices and allowed/denied access evidence. Not core CRM permission-set design, activation execution, or legal compliance certification."
---

# Data 360 Governance

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Identify data owner, classification, purpose, personas, data spaces and every consumption path: query, insight, dashboard/cache, agent retrieval, export and activation. Ask the owner for applicable retention and consent requirements; do not invent legal obligations or certify compliance.
2. Inventory available policies, object/field access, masking controls and consumption identities. Distinguish creating an asset from consuming its data. Metadata discoverability and a successful admin preview do not prove runtime access for other users.
3. Create a policy matrix by persona, object/field, record scope, purpose and channel. Specify deny behavior and masking expectations. Treat data spaces as part of the control model, not proof of isolation on their own. Verify each consumer's enforcement behavior in official docs and the org.
4. Map consent fields to the Privacy Data Model where appropriate, or document the custom model and provenance. Define opt-out, unknown, expired and revoked cases with the owner. Apply explicit segment filters for applicable consent preferences; do not assume a destination or an agent automatically honors every preference.
5. Draft supported policy/configuration changes and separate retention/deletion procedures. Account for caches, exports and downstream copies: a query-time control is not evidence that previously copied data was withdrawn. Avoid promising universal revocation or deletion propagation.
6. In an authorized sandbox, test allowed and denied identities on each actual consumption path. Include system-mode consumers requiring CRM safeguards, cached artifacts, masked fields and revoked consent. Do not relax controls or use a default data space after a denial.
7. Deliver the policy matrix, evidence, exceptions, owner decisions and rollback/verification steps. Route CRM permission grants to salesforce-access-design, data mapping to data360-ingestion-modeling and retrieval testing to agentforce-grounding. Missing platform features remain explicit gaps.
