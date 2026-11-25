# Analytics Governance, Row-Level Security & Metric Verification

Enforce data-access boundaries and analytical accuracy across CRM Analytics and Tableau Next before publishing dashboards or changing asset shares.

## CRM Analytics Row-Level Security Invariants

- **Default open-row hazard**: Granting app/dataset access in CRM Analytics exposes **ALL rows** in that dataset by default unless row-level security is explicitly configured.
- **Dashboard filters are NOT security**: Global filters, listselectors, and SAQL filter steps can be bypassed through exploration, API queries, or lens editing and never enforce row-level security.
- **Sharing inheritance + security predicates**:
  1. Enable **Sharing Inheritance** where the source sObject is supported and within platform sharing-descriptor row limits, AND always configure a fallback **Security Predicate** for rows exceeding inheritance limits or non-inherited records:

```text
'OwnerId' == "$User.Id" || 'Account.OwnerId' == "$User.Id"
```

  2. Never rely on admin previews to verify predicates — admins with broad permissions bypass typical user restrictions.
  3. Re-validate security predicates whenever recipe joins rename or drop owner, territory, or hierarchy key columns.

## Tableau Next Multi-Layer Governance Model

Tableau Next enforces access across **three independent layers** — all three must align for safe consumption:

| Layer | Controls | What It Does NOT Prove |
| --- | --- | --- |
| 1. Licenses & Permission Sets | Tableau Next seats, role (`upsert_user`), feature access | Does not restrict which Data 360 rows a user can query |
| 2. Data 360 Governance Policies | Data Spaces, row/column access policies, field masking | Does not grant visibility to a specific dashboard or workspace |
| 3. Asset Sharing | Workspace, SDM, visualization, and dashboard `accessType` | Sharing a dashboard or SDM does NOT prove correct underlying Data 360 row access |

- Coordinate Data 360 policy and Data Space design with `data360-activation-governance` and core CRM permission sets/sharing rules with `salesforce-security-access`.
- When sharing an asset or modifying workspace membership, verify whether cached visuals or semantic previews reflect recent policy changes.

## Restricted-User Verification Matrix

Test totals and row visibility against source evidence before publishing or expanding shares:

| Test Persona | Expected Scope | Verification Check | Pass Criteria |
| --- | --- | --- | --- |
| Full-access reviewer | All authorized rows in org/space | Compare dashboard KPI against source SOQL / Data 360 SQL | Exact total match at agreed grain & timezone |
| Restricted territory/rep user | Owned / shared rows only | Run same dashboard, exploration lens, and direct query | Zero out-of-scope rows; masked columns stay masked |
| Unassigned / no-space user | Denied | Attempt dashboard open and underlying semantic/dataset query | Explicit access denial; no cached leak or silent fallback |

## Six Pre-Publish Metric Correctness Checks

1. **Metric grain**: Confirm one row represents the intended business entity and time period (preventing join fan-out or snapshot double-counting).
2. **Aggregation & additivity**: Verify semi-additive balances, ratios (`SUM(a)/SUM(b)` vs. `AVG(a/b)`), and KPI totals (`group q by all` in SAQL).
3. **Join cardinality**: Confirm left vs. inner joins do not silently drop expected rows or multiply measures.
4. **Filter scope**: Verify WHERE vs. HAVING placement, timezone boundaries, and active/deleted record exclusions.
5. **Refresh & materialization state**: Confirm recipes completed (`Success`), `InsightsExternalData` reached `Completed`, and Data 360 DMOs/caches are current.
6. **Null handling**: Check how nulls affect counts, averages, and groupings across both full-access and restricted-user test personas before sign-off.
