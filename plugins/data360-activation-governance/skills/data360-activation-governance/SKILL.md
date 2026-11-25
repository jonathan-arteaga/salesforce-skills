---
name: data360-activation-governance
description: "Govern Data 360 data spaces and policies, write Data 360 SQL or calculated insights, and build consent-aware segments and activations. Use data360-data-pipeline for schemas, ingestion, or IR, salesforce-security-access for core CRM RBAC, or salesforce-schema-data for SOQL."
---

# Data 360 Activation & Governance

Design and validate Data 360 (Data Cloud) Data Spaces, data governance policies, masking, Data 360 SQL, calculated insights, consent-aware segmentation, and authorized audience activations.

## Mode Routing

Select the mode matching the user request and load only its reference:

| Mode | Trigger | Reference |
| --- | --- | --- |
| Data Spaces & Governance | Data Space boundaries, policy matrices, masking, consent provenance, allowed/denied consumer testing | [Data Spaces & Governance](references/data-spaces-governance.md) |
| Query & Calculated Insights | Data 360 SQL, Legacy SQL vs Data 360 SQL, Query V2 pagination vs newer query API, grain, joins, CIOs | [Query SQL & Calculated Insights](references/query-sql-insights.md) |
| Segmentation & Activation | Segment logic, consent exclusion, contact-point priority, activation payloads, destination reconciliation | [Segmentation & Activation](references/segmentation-activation.md) |

## Core 2026 Invariants

- **Strict Data Space boundary**: Resolve the intended org and Data Space from explicit evidence. An access error (HTTP 403 or missing space grant) MUST fail closed and NEVER trigger a silent fallback to the `default` Data Space or a broad permission grant just to make a query pass.
- **Separate governance checks**: Data Space association, permission-set feature rights, governance policies/masking, and CRM safeguards are distinct layers. Metadata discoverability or an admin preview never proves runtime access for restricted users.
- **API family & pagination discipline**: Do not mix dialects or pagination contracts. Core SOQL (`nextRecordsUrl`) and Data 360 SQL are not interchangeable; SSOT metadata uses `nextPageUrl`/`limit`/`offset`, while Query V2 uses `done` and `nextBatchId`. Check current Salesforce docs for Query V2's newer successor before starting new query implementations.
- **SQL grain & engine honesty**: Identify whether an insight uses Data 360 SQL or Legacy SQL before authoring. Define output grain in one sentence, join on Fully Qualified Keys (`KQ_*` + ID), and aggregate before joining to prevent fan-out — never hide inflated totals with `DISTINCT`.
- **Consent-first segmentation**: Express opt-in/opt-out, unknown, expired, and revoked consent rules explicitly in segment filters and Privacy Data Model mappings. Never assume external destinations or agents automatically honor consent preferences.

## Hard Org & Safety Gates

- **Authorization before Save/Enable**: Treat saving or enabling an activation as consequential — Data 360 targets can publish on the next scheduled run and fire linked activation-triggered flows. Keep local drafts until the user authorizes target, audience, fields, and schedule; never publish a real audience as a validation shortcut.
- **No compliance certification claims**: Capture owner-approved retention, consent, and masking rules and document platform gaps honestly; never claim legal or regulatory compliance certification.
- **Consumption & run-plan discipline**: For large queries, frequent CIO schedules, or broad activations, record expected row volume, bounded synthetic sample size, and explicit stop conditions — never reuse obsolete pricing estimates.
- **Auth & data hygiene**: Never print access tokens or raw `sf org display --json` output. Use synthetic fixtures for allowed/denied policy tests, SQL golden rows, and segment previews.
- **CLI / script execution**: Execute org inspection helpers (such as `data360-data-pipeline` schema scripts) or `sf` CLI commands directly via CLI without reading script internals into context.

## Verification Integrity & Output Contract

- Report static drafts, offline arithmetic checks, sandbox executions, and untested production behavior separately — a generic SQL parser or SQLite test does not prove Data 360 SQL compilation.
- Distinguish three failure causes explicitly: empty matching rows, denied access (HTTP 403 / policy), and execution error. Never collapse them into "no data".
- For Query V2 runs, fetch batches until `done: true` within API time limits (under 1 hour total, under 3 minutes between batches) and report truncated results honestly.
- Separate five delivery states: segment membership, eligible consented contact points, activation export, destination acceptance, and audience visibility. Report `exported; destination unverified` whenever destination receipt is unobserved.
- Structure final deliverables clearly:
  1. **Target Scope**: Org alias, Data Space, API family/engine, and executing identity.
  2. **Design / Artifact**: Policy matrix, SQL/CIO definition, or segment + activation payload draft.
  3. **Validation Evidence**: Synthetic fixtures, allowed/denied results, batch pagination state, and counts.
  4. **Rollback & Gaps**: Stop/pause steps, cache/downstream copy caveats, and unverified platform limits.
- Verify release-sensitive behavior via Salesforce Docs MCP (`admin/data`, `developer/data-cloud`) or official documentation and cite real URLs.

## Handoffs

- DLO/DMO schema inspection, ingestion, Zero Copy federation, or Identity Resolution -> `data360-data-pipeline`
- Core CRM permission sets, sharing rules, or RBAC -> `salesforce-security-access`
- Core CRM SOQL, CustomObject/CustomField XML, or `sf data` -> `salesforce-schema-data`
- Agentforce retriever/grounding testing -> `agentforce-test`
- Tableau Next or CRM Analytics dashboards -> `salesforce-analytics`
