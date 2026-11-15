---
name: data360-query-insights
description: "Create or debug Data Cloud / Data 360 SQL queries and calculated insights with explicit grain, joins, measures and dimensions. Use for aggregate discrepancies, result validation and query execution planning. Not core CRM SOQL, CRM Analytics SAQL, or dashboard design."
---

# Data 360 Query and Insights

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Identify whether the task needs ad hoc Data 360 SQL or a reusable calculated insight. Route core CRM SOQL to platform-soql-query and CRM Analytics work to crm-analytics-wave-generate. Do not mix query dialects or API endpoints.
2. Inspect actual DLO/DMO/CIO schemas, keys, data space, execution identity and relationships; use data360-schema-get when available. Define the expected output grain and a small worked example before writing SQL. Distinguish no data from denied access and failed execution.
3. Specify measures, dimensions, time zone/window, null treatment and duplicate handling. Inspect fully qualified keys and include both ID and key qualifier where the schema requires them; an ID alone can collide across sources. Classify every join as one-to-one, many-to-one or many-to-many; aggregate before joining where required to prevent fan-out. Do not use DISTINCT as an unexplained repair for inflated totals.
4. Draft SQL in the current supported dialect. For calculated insights, verify supported functions, required aggregation/grouping and whether the intended segmentation use needs the segmented table's primary key. Do not substitute streaming insights semantics for calculated insights. Quote identifiers and bind parameters only as the target API supports; do not interpolate untrusted values.
5. Validate with golden rows and expected totals. Check empty inputs, duplicate keys, null measures, boundaries and one-to-many joins. A generic SQL parser or SQLite execution is not proof of Salesforce dialect compatibility; mark offline arithmetic separately from target compilation.
6. Use discovered query tools/APIs in an authorized environment. Apply supported timeout, result limits and pagination; do not infer completeness from the first page. Capture query/job identifiers and execution errors without secrets. For a saved insight, distinguish definition saved, processing complete and results validated.
7. Deliver SQL, the grain/measure contract, fixture results and freshness/cost observations if measured. Keep insight activation/scheduling within scope. Delegate access policy to data360-governance and activation to an available workflow; don't claim an uninstalled skill exists.
