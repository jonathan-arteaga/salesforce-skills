---
name: data360-identity-resolution
description: "Design, configure or troubleshoot Data Cloud / Data 360 identity resolution rulesets, match rules and field reconciliation. Use for false merges, split profiles, source lineage and ruleset evaluation. Not ingestion-key repair, CRM record merging, or schema inventory."
---

# Data 360 Identity Resolution

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Capture the entity being unified (for example individual versus account), business purpose, acceptable false-merge/split trade-off, source ownership, update timing and downstream consumers. Do not assume one ruleset fits every entity or a shared email proves one person.
2. Inspect mapped DMOs, fully qualified keys, source profiles and existing ruleset results with read-only tools. Route bad keys/mappings to data360-ingestion-modeling. Matching cannot repair unknown source provenance. Record data space, release and supported scheduled/real-time behavior.
3. Draft match criteria separately from reconciliation rules. Match rules decide which profiles group together; reconciliation selects values for unified fields. Explain which criteria must all match within each rule, and verify how multiple rules interact in the current product. Do not equate reconciliation with overwriting source records.
4. Create labeled synthetic pairs/clusters covering exact identifiers, shared households/emails, missing values, recycled identifiers and conflicting source values. Get business-owner truth labels and threshold decisions. Keep consent and account authorization separate from an inferred unified identity.
5. Draft supported ruleset configuration or a precise Setup handoff. Compare existing versus proposed grouping on a bounded sample. Capture false merges, false splits, unification rates and source lineage; a higher unification rate is not automatically better.
6. Run only in an authorized sandbox or explicitly scoped environment. Wait for actual processing completion, inspect latest-run and history semantics, and verify unified objects plus source records. Check downstream audience/retrieval effects before promoting a ruleset change.
7. Deliver rules, reconciliation precedence, test evidence, unresolved labels and a versioned rollback/reprocessing plan. Preserve previous rules/results and explain that returning to old rules may require reruns; do not promise instantaneous restoration or source-system writeback.
