# Pipeline and mapping decisions

Track boundaries separately: source → ingestion/federation → DLO → transformation (if any) → DMO → consumer. A zero-copy source still requires verification of schema, access, supported operations and freshness; do not describe it as universally free or instantaneous.

| Decision | Required evidence |
| --- | --- |
| Ingest versus federate | Supported source/path, latency, storage, source availability and measured/estimated usage |
| Primary key | Non-null uniqueness at the stated grain; source namespace and update semantics |
| Relationship | Child/parent key compatibility, unmatched keys and expected cardinality |
| Category/time | Supported category and timestamp mapping for the actual stream/object |
| Incremental processing | Connector-specific updates, late-arrival and delete behavior |
| Recovery | Checkpoint/status, retry scope, duplicate prevention and last known-good mapping |

Use the template's reconciliation table. Count rejects, filtered rows and duplicates explicitly; compare source and target at equivalent snapshots/windows. For federated data, document what consistency window is available. Do not force counts to match by discarding unexplained rows.

When a mapping changes, inspect dependent insights, segments and retrievers before applying it. Use a bounded sample with synthetic identifiers, repeat the run and verify whether reprocessing is idempotent for this path. Identity matching is a later workflow; it does not repair a malformed ingestion key.

Primary source: [Connect Data](https://help.salesforce.com/s/articleView?id=data.c360_a_data_ingestion.htm&release=264.0.0&type=5), reviewed 2026-11-15.

## Readiness and consumption checks

Record a capability matrix for querying, refresh, event/change-trigger behavior and downstream dependencies for the actual connector/mode. Queryable zero-copy data does not by itself prove trigger compatibility. For unstructured S3 paths, verify current file-notification setup and observe notification, extracted content and indexing stages separately. Include a missing-notification case. Record estimated workload, bounded sample size, observed consumption if available and a stop condition; do not reuse forum prices.

## Fully qualified keys

Inspect key qualifiers as well as record IDs. Where Data 360 uses fully qualified keys, join on both the ID and its key-qualifier columns; an ID alone can collide across sources. Do not guess the qualifier field name on another object or replace a platform key qualifier with arbitrary string concatenation. Validate the actual schema and relationship mapping. Include a fixture with identical IDs in different sources and prove they remain distinct.

Source: [Write a Simple Query](https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/write-simple-query.html), fetched 2026-11-15.

For mapping, verify compatible field types, existing mappings and standard/custom object name collisions before changing them. Do not remove all mappings as a troubleshooting shortcut. Source: [Map Data Model Objects](https://help.salesforce.com/s/articleView?id=data.c360_a_map_custom_data_model_objects.htm&release=264.0.0&type=5), fetched 2026-11-15.
