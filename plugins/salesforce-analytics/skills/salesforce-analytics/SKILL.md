---
name: salesforce-analytics
description: "Build and govern Tableau Next semantic models, visualizations, and dashboards via MCP, or author CRM Analytics Wave recipes, datasets, SAQL, and dashboards. Use data360-data-pipeline for DLO/DMO modeling, data360-activation-governance for Data 360 SQL, or salesforce-lwc for custom UI."
---

# Salesforce Analytics

Build, query, style, and govern **Tableau Next** semantic data models (SDMs), visualizations, and dashboards via `tableau-next-*` MCP tools, or author **CRM Analytics (Wave)** R3 recipes, datasets, SAQL, and dashboards via SFDX and REST APIs.

## Mode Routing

Select the platform and mode matching the request and load only its references:

| Mode | Trigger | Reference |
| --- | --- | --- |
| Tableau Next SDM & Query | Profile data, create/edit SDM, enrich metrics/calcs, AI readiness, `run_semantic_query` | [Tableau Next Semantic Models](references/tableau-next-semantic-models.md) |
| Tableau Next Viz & Lifecycle | Charts, dashboards, `edit_dashboard`, sharing, promotion/reuse, alerts, destructive ops | [Tableau Next Viz & Lifecycle](references/tableau-next-viz-lifecycle.md) |
| CRM Analytics (Wave) | `.wdpr` R3 recipes, `.wdash` dashboards, SAQL bindings, `InsightsExternalData`, XMD hygiene | [CRM Analytics Wave](references/crm-analytics-wave.md) |
| Governance & Row Security | Dataset row-level security, sharing inheritance, predicates, Tableau Next 3-layer access, metric checks | [Analytics Governance & Security](references/analytics-governance-security.md) |

## Core 2026 Invariants

- **CRMA default all-row access**: CRM Analytics dataset access grants ALL dataset rows by default unless sharing inheritance and/or security predicates are configured. Dashboard filters are NEVER row-level security.
- **Tableau Next multi-layer governance**: Access spans three independent layers — licenses/permission sets, Data 360 policies/Data Spaces, and asset sharing. Sharing a dashboard or SDM never proves correct underlying data access.
- **Data presence & metric correctness**: Never build on empty objects (`SELECT COUNT(*) > 0` required on discovered sources). Verify metric grain, aggregation, joins, filters, refresh state, and null handling against source evidence before publishing.
- **Tableau Next MCP discipline**: Require a live `tableau-next-*` MCP server before executing tool actions; never invent `apiName` values (always `list_*`), never leave island objects, and never auto-call `save_dashboard` without explicit user confirmation of the draft.
- **CRMA API integrity**: Pair every `.wdpr`/`.wdash`/`.wapp` with its `-meta.xml`, POST/PATCH recipes as R3 JSON at `?format=R3` (never multipart), run jobs with `targetDataflowId` (`02K`), and ALWAYS HTML-decode (`decodeAll`) every `state.steps[*].query` before PATCHing a dashboard.

## Hard Org & Safety Gates

- **MCP disconnect stop**: For Tableau Next authoring/querying, if no `mcp__tableau-next-*` tool is connected, STOP and ask the user to connect one (or provide an explicit offline plan without fabricating calls/IDs).
- **Destructive & share confirmations**: Obtain explicit confirmation before deleting assets, saving dashboard drafts, changing asset shares, promoting packages, or provisioning roles (`upsert_user`).
- **Explicit target org & token hygiene**: Verify CRMA target org alias via `sf org list`; never print raw `sf org display --json` tokens.

## Bundled Scripts (Black-Box Execution)

Run the bundled CRM Analytics Node/Bash scripts directly via CLI relative to this skill directory rather than reading script source into context (every script takes `<org_alias>` as arg 1):

- App & recipe lifecycle: `node ./scripts/create_app.js`, `deploy_and_run_recipe.js`, `probe_recipe.js`, `bash ./scripts/check_connector_error.sh`
- Datasets & synthetic tests: `node ./scripts/fetch_dataset_xmd.js`, `gen_synthetic_dataset.js`, `upload_dataset.js`, `verify_synthetic_dataset.js`
- Dashboard verification & hygiene: `node ./scripts/verify_dashboard_steps.js`, `patch_t_oppo_view.js`, `find_unused_dataset_fields.js`

## Verification Integrity & Output Contract

- Validate restricted-user row visibility and totals against source queries before publishing or changing sharing.
- Report draft plans, sandbox queries/uploads, and browser render checks separately; do not declare CRMA dashboards done until SAQL steps return 200 + rows and widgets render cleanly.
- Structure final deliverables clearly:
  1. **Platform & Target**: Tableau Next MCP server or CRMA org alias + API version.
  2. **Assets / Queries**: Created IDs, SFDX file pairs (`.wdpr`/`.wdash` + `-meta.xml`), or semantic query output.
  3. **Governance & Accuracy Evidence**: Row-security checks, grain/total comparisons, and refresh status.
  4. **Pending User Actions**: Draft save confirmations, UI similarity scans, or browser render verification.

## Handoffs

- Data 360 DLO/DMO schema, ingestion, Zero Copy, or Identity Resolution -> `data360-data-pipeline`
- Data 360 Data Spaces, policies, SQL, or Calculated Insights -> `data360-activation-governance`
- Custom LWC analytics wrappers -> `salesforce-lwc`
- SFDX metadata deployment orchestration -> `salesforce-devops-deploy`
