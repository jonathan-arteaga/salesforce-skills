# Ingestion, Zero Copy Federation & DLO-to-DMO Modeling

Track every pipeline boundary independently: `Source -> Ingestion or Federation -> DLO -> Transform (optional) -> DMO -> Downstream Consumer`.

## 2026 Zero Copy vs. Physical Ingestion Matrix

| Dimension | Physical Ingestion (Data Streams) | Zero Copy Federation (Lakehouse / Warehouse) |
| --- | --- | --- |
| Storage & movement | Copies rows into Data 360 Lakehouse (DLO) | Virtualizes external tables (Snowflake, Databricks, BigQuery, Redshift, Iceberg) |
| Refresh & freshness | Full refresh, upsert/incremental, or CDC schedule | Live query or accelerated cache/materialization window; document consistency window |
| Downstream triggers | Full support for Data Actions, streaming/batch transforms, segments | Queryable zero-copy data does not automatically guarantee event/change-trigger support — verify per connector |
| Consumption & cost | Ingestion + storage + processing credits | External compute + Data 360 query/federation credits; never claim Zero Copy is free or instant |
| Best fit | High-frequency activation, CDC triggers, CRM/Marketing native streams | Large analytical tables already curated in an external lakehouse |

## Data Cloud One (Multi-Org) Considerations

- **Home org vs. Companion org**: Identify which org hosts the Data 360 tenant (home org) versus connected companion CRM orgs.
- **Scope & permissions**: Verify Data Space assignment and companion-org permissions explicitly; companion metadata visibility does not imply write or cross-space query rights.
- **Source namespace isolation**: Multi-org CRM ingestion can produce colliding Salesforce IDs or duplicate external keys across orgs unless source namespaces and key qualifiers are preserved.

## Modeling, Keys & Mapping Rules

1. **Grain & primary key**: Define exact source row grain and profile null/duplicate keys before stream creation. Specify `Profile`, `Engagement` (with immutable event timestamp), or `Other` category according to target connector support.
2. **Fully Qualified Keys (FQK)**: Where Data 360 assigns key qualifiers (`KQ_*`), join on both the record ID and its corresponding `KQ_*` column. Never guess qualifier names on another object or concatenate source prefixes manually as a substitute for FQK:

```sql
SELECT i.ssot__Id__c, e.ssot__EmailAddress__c
FROM ssot__Individual__dlm i
JOIN ssot__ContactPointEmail__dlm e
  ON i.ssot__Id__c = e.ssot__PartyId__c
 AND i.KQ_Id__c = e.KQ_PartyId__c
```

3. **DLO-to-DMO mapping**: Verify compatible field types, existing mappings, and standard vs. custom DMO collisions before modifying mappings. Inspect dependent Calculated Insights, segments, and Agentforce retrievers before changing a mapping. Never clear all mappings as a troubleshooting shortcut.
4. **Unstructured S3 / file pipelines**: Verify file-notification configuration and observe three stages separately: event notification arrival, content extraction/chunking, and search index readiness. Include a missing-notification test case.

## Boundary Reconciliation & Budget Discipline

Compare source and target at equivalent snapshots; stop promotion on unexplained mismatches:

| Boundary | Required Count / Check |
| --- | --- |
| Source snapshot | Total rows, distinct primary keys, null-key count, delete flags |
| Ingestion / Federation -> DLO | Accepted rows, rejected rows, filtered rows, duplicates, latency window |
| DLO -> Transform / DMO | Mapped row count, type-coercion drops, unmatched foreign keys, `KQ_*` collision check |
| Repeat run (idempotency) | Re-run synthetic batch; confirm updates overwrite cleanly without duplicate rows |

- **Bounded synthetic test**: In an authorized sandbox, ingest or federate a small synthetic sample, wait for terminal processing status, and test updates, late-arriving records, deletes, and repeat runs. A `Succeeded` job status is not proof of complete or accurate data.
- **Consumption run plan**: Record expected row volume, refresh cadence, bounded sample size, observed consumption (when exposed), and explicit stop conditions using current official entitlements — never reuse obsolete forum pricing claims.
- **Recovery & handoff**: Document checkpoints, retry scope, and last known-good mapping for rollback. Provide step-by-step Setup instructions when no supported Metadata/Connect API exists.
