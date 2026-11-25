---
name: data360-data-pipeline
description: "Inspect Data 360 DLO/DMO schemas, design ingestion or Zero Copy federation, map DLOs to DMOs, and configure identity resolution rulesets. Use data360-activation-governance for SQL, policies, or segments, salesforce-schema-data for core CRM metadata, or salesforce-analytics for BI."
---

# Data 360 Data Pipeline

Inspect Data 360 (Data Cloud) schemas, architect physical ingestion or Zero Copy federation (including Data Cloud One multi-org topologies), map DLOs to DMOs, and configure identity resolution rulesets.

## Mode Routing

Select the mode that matches the user intent and load only its reference:

| Mode | Trigger | Reference |
| --- | --- | --- |
| Schema Inspection | Enumerate DLOs/DMOs, inspect field types, primary keys, or system fields | [Schema Inspection](references/schema-inspection.md) |
| Ingestion & Modeling | Connectors, Zero Copy federation, Data Cloud One companion orgs, DLO-to-DMO mapping, FQK joins | [Ingestion, Zero Copy & Modeling](references/ingestion-zero-copy-modeling.md) |
| Identity Resolution | Rulesets, match criteria, field reconciliation, false merges/splits, unified profiles | [Identity Resolution](references/identity-resolution.md) |

## Core 2026 Invariants

- **Naming fidelity**: Data 360 is the current product name, while `Data Cloud`, `ssot`, `__dll`, and `__dlm` remain in APIs, permissions, and metadata. Always preserve actual API identifiers returned by metadata rather than assuming suffixes.
- **Stage separation**: Treat DLO ingestion/federation, DMO harmonization, unified DMOs from identity resolution, and downstream consumers as distinct boundaries. Object existence does not prove successful mapping, identity resolution, or Agentforce grounding readiness.
- **Zero Copy vs. Ingestion**: Zero Copy federation (Snowflake, Databricks, BigQuery, Redshift, Iceberg) avoids bulk duplication but is not universally free, instantaneous, or trigger-equivalent. Verify supported operations, freshness windows, and credit consumption against current docs.
- **Data Cloud One multi-org**: Distinguish home orgs from companion orgs when designing cross-org ingestion, Data Space sharing, and companion metadata visibility.
- **Fully Qualified Keys (FQK)**: Join across sources using both record ID and platform key-qualifier columns (`KQ_*`). Never concatenate arbitrary strings to simulate FQK or repair broken ingestion keys inside identity resolution.
- **Entity grain before matching**: Separate individual, household, legal entity, and storefront/location grain before authoring match rules. Separate grouping (match rules) from value selection (reconciliation); reconciliation never overwrites source records.

## Hard Org & Safety Gates

- **Explicit target org & Data Space**: Run `sf org list` and confirm the intended org alias and Data Space before querying or mutating. Never silently pick the first connected org, and never fall back to `default` Data Space after an access error; route permission gaps to `data360-activation-governance`.
- **Token & PII hygiene**: Never print raw `sf org display --json` output or access tokens. Use synthetic records for sample ingestion, mapping tests, and labeled identity pairs.
- **Mutation authorization**: Reviews, inventories, and local drafts require read-only access only. Creating streams, editing mappings, or running rulesets requires explicit authorization for the target sandbox or scoped org, plus a documented rollback plan.
- **No fabricated Data Kit claims**: Describe unsupported Metadata API or Data Kit deployment paths honestly rather than inventing deployable JSON workbooks.

## Bundled Scripts (Black-Box Execution)

Run the bundled Python scripts directly via CLI relative to this skill directory rather than reading script source into context:

- List DLOs or inspect one DLO: `python3 ./scripts/get_dlo_schema.py <org_alias> [dlo_name] [--api-version v64.0]`
- List DMOs or inspect one DMO: `python3 ./scripts/get_dmo_schema.py <org_alias> [dmo_name] [--api-version v64.0]`

Scripts use `schema_client.py` (Python stdlib, `sf` CLI auth capture without leaking tokens, SSOT pagination). Default API version is `v64.0`; pass `--api-version vNN.0` when targeting a verified newer API release.

## Verification Integrity

- Report static design drafts, executed sandbox runs, and untested production behavior separately.
- Reconcile row counts, rejects, duplicates, and null keys at every pipeline boundary; never discard unexplained rows to force counts to match.
- For identity resolution, evaluate labeled synthetic pairs and multi-record clusters with counts and denominators; a higher unification rate is not automatically better.
- Verify release-sensitive claims via Salesforce Docs MCP (`developer/data-cloud`, `admin/data`) or official Salesforce documentation and cite actual URLs.

## Handoffs

- Data Space policies, Data 360 SQL, calculated insights, segments, or activations -> `data360-activation-governance`
- Core CRM CustomObject/CustomField XML, SOQL, or `sf data` -> `salesforce-schema-data`
- Tableau Next semantic models or CRM Analytics recipes/dashboards -> `salesforce-analytics`
- Metadata deployment orchestration -> `salesforce-devops-deploy`
