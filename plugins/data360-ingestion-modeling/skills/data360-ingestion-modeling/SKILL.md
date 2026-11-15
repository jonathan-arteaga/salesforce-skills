---
name: data360-ingestion-modeling
description: "Build or troubleshoot Data Cloud / Data 360 ingestion, federation and DLO-to-DMO mapping workflows. Use for connector choices, keys, relationships, refresh, rejected records and source-to-target reconciliation. Not schema inventory alone, identity resolution, or audience activation."
---

# Data 360 Ingestion and Modeling

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Capture source system, owner, volume estimate, change pattern, latency target, deletion semantics, classification and intended consumers. Separate source ingestion, federation/zero-copy, transforms and DLO-to-DMO mapping; don't promise zero-copy for unsupported sources.
2. Discover existing connectors, streams, DLOs, DMOs, data spaces and relationships. Reuse data360-schema-get when available for schema evidence, not provisioning. Record exact names and types from the org. Route access failures to governance instead of switching to another data space.
3. Choose a supported connector or federation path using current docs. Document refresh/CDC behavior, credentials and failure/retry semantics. Treat connector availability, credits and source access as prerequisites, not capabilities guaranteed by the skill.
4. Define each source row's grain and durable key. Profile null/duplicate keys and source namespaces, including platform key qualifiers where present. Model event timestamps and category where required. Map fields and relationships with compatible types and explicit join cardinality. Keep identity matching separate from mapping; concatenating inconsistent source IDs is not identity resolution.
5. Draft connector/stream configuration and mapping artifacts. Use supported tools or APIs only after inspecting current schemas; otherwise provide a step-by-step Setup handoff. Never describe a generic JSON workbook as deployable metadata.
6. In an authorized sandbox, ingest or federate a small synthetic sample, wait for observable processing state, inspect rejects, and reconcile counts at each boundary. Check updates, late arrivals, deletion handling and repeat runs. Do not equate a successful job with complete or accurate data.
7. Deliver a reconciliation report and recovery/rollback plan. Stop promotion when mismatches are unexplained. Delegate policies to data360-governance and SQL validation to data360-query-insights. Describe unsupported operations honestly rather than inventing a Data Kit workflow.
