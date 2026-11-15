# Data 360 feed and calculated insight draft

Status: **draft; offline arithmetic checked only. No org inspection, provisioning, Salesforce compilation, execution, or live changes.**

## Scope and evidence

Goal: keep two different source customers with local ID 42 separate, reject missing keys, make retries idempotent, protect existing DMO consumers, and produce a correct customer order total.

Evidence: the supplied ingestion/modeling and query/insights SKILL.md files, their workflow references, workbook templates, acceptance cases, and bundled current-Salesforce guidance dated 2026-11-15. No fresh documentation verification was performed under the supplied-reference-only scope. Target org, data space, release/API, insight engine, licensing, connector, schema, effective identity, permissions, volume, latency, ownership, currency and deletion behavior remain unknown. No available connector, org schema or execution tools are assumed.

The following logical names are design labels, **not observed API names or deployable metadata**. Synthetic customers are Alpha:42 (customer A) and Beta:42 (a different person).

## Ingestion and modeling workbook

### Design

| Source | Grain/key | Proposed DLO logical field/type | Proposed DMO logical field/type | Relationship/cardinality | Null/duplicate rule |
| --- | --- | --- | --- | --- | --- |
| Alpha customers | One current customer per immutable Alpha ID | SourceNamespace text; LocalCustomerId text; CustomerKey text | Existing customer PK and source provenance, exact mapping TBD | One customer to many orders/contact points | Reject null/blank local ID; stable Alpha:42 key |
| Beta customers | One current customer per immutable Beta ID | Same logical fields | Same verified target contract | Beta:42 must remain distinct from Alpha:42 | Same rules, namespace Beta |
| Orders | One order per source-qualified immutable order ID | OrderKey text; CustomerKey text; Amount decimal; Currency text; SourceUpdatedAt timestamp | Verified order key, customer FK, amount/currency/time | Many orders to one customer | Missing order key rejected; missing/unmatched customer quarantined for repair |
| Contact points | One contact point per source-qualified immutable contact-point ID | ContactPointKey text; CustomerKey text | Verified contact-point key/customer FK | Many contact points to one customer | Missing keys rejected; no raw join into monetary aggregation |

Namespace and local ID form an unambiguous tuple. A delimiter illustration such as Alpha:42 requires an escape/length-prefix rule if source values can contain the delimiter. Preserve IDs as text, including leading zeros; define whitespace handling explicitly. Never derive the durable key from batch IDs or generate a new random key on retry. A source key correction requires controlled migration. Concatenating IDs prevents collisions; it does not perform identity resolution or establish that cross-source people are the same.

For a logical upsert contract, use durable entity key plus an authoritative source version/sequence (timestamp only if its ordering and ties are resolved). Same key/version/payload is a retry no-op. Same key/version with conflicting payload is quarantined. Newer version updates; older version is ignored and logged or handled by an explicit history model. Confirm that the selected connector actually supports these semantics; otherwise stage and deduplicate upstream before delivery. Do not silently use arrival order as truth.

Reject null/blank customer keys into a restricted reject store with batch/run ID, source, reason and a source-row locator; minimize personal fields. Repair upstream and replay only corrected records. Repeated bad rows should not create unlimited duplicate reject entries. Track reject occurrences separately from distinct rejected records. Do not coalesce missing keys to a shared placeholder person.

### Connector/setup handoff

1. Owner supplies target org/data space and authorized identity, source access, volumes, change rate, latency, retention/classification and deletion contract. Inventory current streams, DLOs, DMOs, fields, keys, relationships and dependencies.
2. Verify supported connector or federation mode, license, refresh/CDC, event-trigger support, types, retries, deletion/tombstone behavior and estimated consumption from current official guidance. These are prerequisites, not promised capabilities. Select ingestion or federation only after this evidence exists.
3. Export/preserve existing configuration and map logical fields to observed names/types. Validate required category/time mappings for the chosen object/path. Keep source timestamp separate from ingestion timestamp.
4. In an authorized sandbox, use a bounded synthetic fixture, inspect rejects and processing states, reconcile every boundary, then repeat exactly. Record actual consumption; stop on unexplained count differences, key collisions, consumer regressions or a pre-agreed usage threshold.
5. Apply a reviewed promotion plan only after tests pass. This document itself is not importable stream metadata.

### Existing DMO consumers and migration

Downstream segments already depend on the DMO. Do not overwrite its primary-key mapping or drop/recreate it as a routine correction. Inventory dependent segments, insights, retrievers and activation relationships; record their keys, filters, baseline counts and membership samples. Determine whether existing IDs are already source-qualified, and whether historical rows were incorrectly merged. If the old key 42 lost provenance, it cannot be safely split by guessing: recover source lineage or quarantine ambiguous rows.

Prefer a staged, versioned mapping with an explicit old-to-new key crosswalk and coordinated child-FK migration. If the platform cannot support the proposed parallel path, stop and obtain a compatible migration design. Validate referential integrity, counts and segment membership in the intended data space before switching consumers. Freeze or coordinate source changes for equivalent snapshots, retain last-good data/configuration, and avoid dual-writing into consumer-visible rows that would double count. Rollback must restore compatible data and FK state as well as configuration; restoring mapping alone does not undo previously rewritten keys.

### Validation and change record: illustrative snapshot

Fixture: Alpha contains (42,A), (null,bad-1), (blank,bad-2); Beta contains (42,B). Then replay the identical batch once. Counts are expected, not observed. No transforms or filters are assumed.

| Boundary/window | Input | Accepted | Rejected | Filtered/no-op | Expected output | Actual output | Explanation |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| Initial source to logical validated landing | 4 | 2 | 2 | 0 | 2 valid keys, 2 distinct rejects | Not run | Alpha:42 and Beta:42 |
| Landing to DLO | 2 | 2 | 0 | 0 | 2 current customer rows | Not run | Path-specific physical counts must be measured |
| DLO to DMO | 2 | 2 | 0 | 0 | 2 distinct customer rows | Not run | No identity unification assumed |
| Exact replay at logical validation boundary | 4 | 0 new writes | 2 reject occurrences | 2 unchanged valid rows | Still 2 current customers; still 2 distinct rejects | Not run | Connector attempt counters may differ |
| DMO to existing consumers | 2 current customers | TBD | TBD | TBD | Membership changes explained against baseline | Not run | Do not assume each segment contains both |

Compare equivalent source snapshots/watermarks; record inserts, updates, deletes, rejects, duplicates and filtered records independently. Physical landing rows may retain retries while the logical current-state target stays unique. Do not claim raw counts match if the connector uses append-only staging.

## Query and insights workbook

### Grain and measure contract

Interpret 10 and 20 as order **amounts**, not order IDs. For A, two orders multiplied by three contact points produce six joined rows: 10+10+10+20+20+20 = 90. Correct customer total is 10+20 = **30**. Contact points are not additional purchases.

| Output grain | Dimension | Measure | Null rule | Time boundary/timezone | Join cardinality |
| --- | --- | --- | --- | --- | --- |
| One row per source-qualified customer for a fixed reporting period and single agreed currency | Customer key mapped to the required segmented-table PK | Sum of eligible order amounts | Quarantine null amounts for finance; never silently treat unknown money as zero | Proposed [2026-10-01 00:00 UTC, 2026-11-01 00:00 UTC); owner must confirm | Orders aggregate to customer before any further join |

Orders are unique by durable order key after retry deduplication. Different orders with equal amounts remain separate purchases. Customer rows with no eligible orders are absent in the base result; if finance needs zeros, use a verified unique customer spine and left join the preaggregate, coalescing only missing aggregate results. Currency must be constrained or normalized by an approved exchange-rate policy; do not sum mixed currencies. Adding currency or contact-point dimensions changes the output grain and requires separate consumer review.

### Schema-conditional SQL draft

This is a logical template, **not executable as written**. Replace every bracketed placeholder with inspected identifiers or properly bound/typed literals as supported by the actual API. Verify Data 360 SQL versus Legacy SQL, grouping, timestamp syntax, aliases, supported calculated-insight features and the segmented-table PK dimension before saving. Do not infer calculated-insight validity from ad hoc Query Editor execution.

```sql
SELECT
  o.[customer_key] AS [customer_dimension],
  SUM(o.[amount]) AS [total_order_amount]
FROM [verified_deduplicated_order_DMO] o
WHERE o.[customer_key] IS NOT NULL
  AND o.[amount] IS NOT NULL
  AND o.[currency] = [bound_single_currency]
  AND o.[order_timestamp] >= [typed_window_start]
  AND o.[order_timestamp] < [typed_window_end]
GROUP BY o.[customer_key]
```

The null filter is only an exclusion guard: reconciliation must expose the rejected amount rows and finance must approve completeness before publication. It is not permission to silently omit unknown amounts.

No contact-point join is needed for the requested total. If eligibility requires at least one contact point, conditionally join the aggregated orders to a separately grouped contact-key relation containing **one row per customer**, or use a supported existence predicate. Never join a one-row order total to all three raw contact points and sum it again: that still yields 90. If one representative contact is required, define a deterministic business rule with tie-breaking first. Validate that the insight engine supports the chosen subquery/join construction. Do not use SUM(DISTINCT amount) as repair: legitimate orders of 10 and 10 must total 20.

### Definition, execution and recovery

Draft insight definition: customer period order total; customer PK dimension; amount measure; fixed window above; agreed single currency; refresh cadence and owner TBD. Keep definition save, component creation, active status, processing completion, complete output retrieval, output correctness and schedule verification as separate evidence checkpoints.

The reported deployment state is **request accepted, asynchronous processing failed**. Accepted is not successful deployment or a validated insight. Component existence/active status, any partial outputs and downstream visibility remain unknown. Do not delete/recreate automatically or repeatedly resubmit.

Recovery handoff:

1. Preserve request/job/correlation identifiers, UTC times, terminal error text, submitted definition/version and last successful artifact/run; redact secrets. Inspect terminal job details and definition status using the supported operation once access exists.
2. Distinguish syntax/type/schema/unsupported-engine errors (fix draft and compile), permission/data-space errors (repair through authorized owner without changing identity/space), transient service errors (bounded, supported retry only after checking no run remains active), and source-data/mapping failures (repair/reconcile inputs first).
3. Check whether the accepted request created or modified a component despite run failure. Determine whether outputs are absent, partial or stale. Preserve prior validated outputs and label freshness explicitly; pause affected consumption only through an authorized change if reliability cannot be established.
4. Use an inspected polling/status interface with a bounded deadline and backoff. A deadline means unknown/incomplete, not success or necessarily terminal failure. Retrieve all result batches under the chosen API's documented pagination rules and record completeness separately from correctness.
5. Test corrected definition in sandbox, compare golden output and consumer relationships, then promote through the agreed scope. Keep last-good definition and consumer binding ready for rollback; do not infer that redeployment or rollback backfills results. Scheduling remains unverified until its actual run and freshness are observed.

### Validation and change record

| Fixture | Expected rows/totals | Actual | Execution environment | Result |
| --- | --- | --- | --- | --- |
| A: amounts 10,20; three contacts | Base insight 1 row, A=30; raw join 6 rows, naive sum=90 | Arithmetic 30 and 90 | Offline reasoning | Target SQL untested |
| A: two distinct orders, amounts 10,10 | A=20 | Not executed | Planned sandbox | Detects DISTINCT misuse |
| Alpha:42 and Beta:42 | Two separate customer identities/keys | Not executed | Planned sandbox | No collision/unification |
| Exact batch replay | Same current-state rows and totals; no extra purchases | Not executed | Planned sandbox | Tests actual connector idempotency |
| Null/blank customer or order key | Rejected/quarantined; no shared placeholder key | Not executed | Planned sandbox | Reject counts reconcile |
| Same key/version, conflicting payload | Quarantine conflict; no arbitrary winner | Not executed | Planned sandbox | Tests deterministic updates |
| Late older update; newer update | Older cannot overwrite newer; newer applied once | Not executed | Planned sandbox | Record version evidence |
| Source deletion/tombstone | Owner-approved removal/history behavior; FK/segment impacts reconciled | Not executed | Planned sandbox | Promotion blocked until semantics chosen |
| Null amount | Explicit quality exception; partial total not certified complete | Not executed | Planned sandbox | Finance sign-off required |
| Empty order input / customer without orders | Base query yields no row; approved customer-spine variant yields zero | Not executed | Planned sandbox | No fabricated customer row |
| At start / at end boundary | Start included; end excluded in agreed timezone | Not executed | Planned sandbox | Tests timestamp conversions |
| Customer with no contact point | Still included by base insight | Not executed | Planned sandbox | Eligibility change requires explicit rule |
| Duplicate customer/contact dimension keys | Quality failure before joining; no hidden multiplication | Not executed | Planned sandbox | Check uniqueness/cardinality |
| Async accepted then failed | Failed processing state; no validated-deployment claim | Given scenario, no logs | Supplied evidence | Recovery remains draft |
| Partial/paginated output, access denial | Incomplete versus denied recorded distinctly; no fallback space | Not executed | Planned sandbox | No false empty-data conclusion |
| Existing DMO segments after key migration | Explained membership deltas and valid relationships | Not executed | Planned sandbox | Required cutover gate |

## Failures and handoff

Blockers: no connector, schema, org tools or target documentation verification; unknown target/version/engine, source semantics, consumer keys and permissions. Owner decisions needed: financial window/currency/null treatment, source delete/version rules, latency/volume, target scope and migration/cutover plan. These block deployment, not preparation of this draft.

Next owners: ingestion owner verifies connector and retry/delete behavior; data model owner supplies exact mappings and dependency inventory; finance approves measure contract; authorized Data 360 operator compiles, executes, captures async diagnostics and reconciles outputs; segment owner validates membership before cutover. No platform cost, freshness, scheduling or production correctness has been measured.

Artifact: `/workspace/forward-ingestion-query.md`.

Reference links supplied by the skills (dated baseline, not freshly fetched):

- [Object Model in Data 360](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-object-model.html)
- [Connect Data](https://help.salesforce.com/s/articleView?id=data.c360_a_data_ingestion.htm&release=264.0.0&type=5)
- [Create a Calculated Insight with SQL](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_calculated_insights_sql_function.htm&release=264.0.0&type=5)
- [Data 360 Connect API](https://developer.salesforce.com/docs/data/connectapi/references/spec)
