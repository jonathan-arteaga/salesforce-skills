# Data 360 Data Spaces & Governance

Design, review, and test Data Spaces, data access policies, masking, and consent provenance across every Data 360 consumption path.

## Strict Data Space Error Boundaries

1. **Resolve explicitly**: Confirm target org alias, Data Space API name, and effective execution identity from org evidence before running any query or policy change.
2. **Fail closed**: If a query or metadata request returns HTTP 403, missing object access, or a Data Space scoping error, STOP and report the denial. Never silently fall back to the `default` Data Space and never grant broad system-level permissions merely to make a query pass.
3. **Separate permission layers**: Data Space association (`Associate a Permission Set with a Data Space`), feature/admin permissions, governance policies (row/column masking and tag-based access), and CRM sharing are independent controls. A visible DMO in Setup or an admin preview does not establish bounded query access for end users or elevated service identities.

## Multi-Path Governance Matrix

Verify enforcement behavior for every actual consumer in current docs and in an authorized sandbox:

| Consumption Path | Governance Question to Prove |
| --- | --- |
| Interactive SQL query | Does the executing identity receive only authorized rows and unmasked columns? |
| Saved Calculated Insight | Are insight creation permissions and insight consumption permissions evaluated separately? |
| Dashboard / semantic cache | When a policy or mask changes, when do cached dashboard or semantic results refresh? |
| Agentforce / retriever | Which principal executes retrieval, and where is customer-level authorization enforced? |
| Activation / external export | Which consent filters apply, and what happens to data already copied to the destination? |
| Core CRM / system context | Which CRM FLS/sharing safeguards are required alongside Data 360 policies? |

## Policy Specification Matrix

Capture owner-approved access rules before implementing policies in an org:

| Persona / Identity | Data Space | Object / Field | Row Scope | Masking / Redaction | Expected Deny Behavior |
| --- | --- | --- | --- | --- | --- |
| Regional Analyst | `EMEA_Space` | `Individual__dlm.Email` | `Region = 'EMEA'` | Partial email mask | 0 rows outside EMEA |
| Restricted User | `EMEA_Space` | `UnifiedIndividual__dlm` | Denied | N/A | Explicit HTTP 403 / empty denied error |
| Elevated Service | `EMEA_Space` | Grounding chunks | Scoped tag | None on public docs | No restricted chunks or citations leaked |

## Consent Provenance & Downstream Copy Limits

- **Privacy Data Model**: Map consent fields to the standard Privacy Data Model where supported, or document the custom model, source precedence, and timestamp provenance.
- **Explicit edge states**: Obtain business-owner definitions for opt-out, unknown/missing, expired, and revoked consent states. A consent field in a DMO does not enforce itself — consuming segments, queries, and agents must apply explicit filters.
- **Masking is not deletion**: Distinguish query-time masking, Data Space filtering, and physical retention/deletion procedures. Query-time policies do not retract rows already exported to external destinations or cached downstream; avoid promising universal deletion propagation.

## Sandbox Evidence Protocol

- Construct synthetic public and restricted test records inside an authorized sandbox.
- Test at least three identities on the actual consumer: an **authorized user**, an **unauthorized user**, and an **elevated/service identity**.
- Inspect metadata visibility, feature operations, returned rows, masked values, and (for Agentforce consumers) retrieved chunks and citations as separate assertions.
- If a desired governance rule cannot be enforced by the platform in a given consumer, document the gap explicitly and propose a supported alternative rather than silently weakening the control.
