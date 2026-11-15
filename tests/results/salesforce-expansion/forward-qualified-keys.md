# Qualified customer keys: join and mapping review

Status: **draft; synthetic arithmetic locally checked**. No Salesforce connection, schema inspection, target compilation, sandbox execution, ingestion, or deployment occurred.

## Scope and evidence

Finance joins `Customers.Id = Orders.CustomerId`. In the supplied fixture, ID 42 denotes two different customers distinguished by key qualifier. The intended grain is one output row per `(Customers.Id, Customers.KeyQualifier)`, with `Name` as an attribute. This is an ad hoc query draft, not a deployed calculated insight.

Target org, data space, release/API, execution identity, licenses, actual DLO/DMO names, field API names/types, connector, mapping and relationship configuration are unknown. All names below are supplied synthetic identifiers, not asserted Salesforce API names.

Read both requested skills and their current-Salesforce guide, workflow, workbook and acceptance references. Their qualified-key guidance cites [Write a Simple Query](https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/write-simple-query.html), fetched by the reference authors on 2026-11-15. Mapping guidance cites [Map Data Model Objects](https://help.salesforce.com/s/articleView?id=data.c360_a_map_custom_data_model_objects.htm&release=264.0.0&type=5), also dated 2026-11-15. These are bundled-reference evidence; no live documentation verification was performed for this review.

## Expected rows and the defect

| Customer ID | Qualifier | Name | Correct total | Current ID-only total |
| --- | --- | --- | ---: | ---: |
| 42 | CRM | A | 10 | 30 |
| 42 | ERP | B | 20 | 30 |
| **Grand total** | | | **30** | **60** |

The ID-only join matches each of two orders to both customers, producing four joined rows. The qualified join produces two rows: order 1 → CRM/A and order 2 → ERP/B. The desired Orders-to-Customers relationship is many-to-one; it is one-to-one in this tiny fixture. Joining on ID alone creates fan-out across namespaces. Grouping only by ID would also collapse these distinct customers. `DISTINCT` on amounts is not a correction.

## Query design

| Output grain | Dimensions | Measure | Null/empty rule | Time | Cardinality |
| --- | --- | --- | --- | --- | --- |
| One row per customer qualified key | ID, qualifier; stable Name attribute | Sum of order Amount | Null key parts are invalid/unmatched; null amounts must be flagged before acceptance; no orders displays 0 | All supplied rows; no date filter or timezone | Orders many-to-one Customers, conditional on parent-key uniqueness |

The following SQL is **schema-conditional pseudoproduction SQL using fixture names**. Substitute only verified actual identifiers and adapt quoting, functions and types to the target engine/API. It assumes compatible key types and exactly one Customers row per qualified key. `SUM` ignores null amounts; finance totals must not be certified until null amounts are resolved or an explicit business policy permits that behavior. `COALESCE` displays zero for customers without orders and can also conceal all-null order amounts, so validate null measures separately.

```sql
SELECT
    c.Id,
    c.KeyQualifier,
    c.Name,
    COALESCE(SUM(o.Amount), 0) AS TotalAmount
FROM Customers AS c
LEFT JOIN Orders AS o
    ON c.Id = o.CustomerId
   AND c.KeyQualifier = o.CustomerKeyQualifier
GROUP BY c.Id, c.KeyQualifier, c.Name;
```

Use the child's **customer-reference qualifier**, not an assumed qualifier for the order's own primary key. Do not guess that another object's field shares the same API name. If the real schema exposes no compatible relationship qualifier, this draft cannot be safely translated until the namespace mapping is established. Do not create arbitrary concatenated keys as a substitute for platform-qualified-key semantics. Unmatched orders are excluded by this customer-led report and must be counted and reconciled separately.

## Source-to-target mapping review

| Source | Grain/key | DLO field/type | DMO field/type | Relationship/cardinality | Null/duplicate rule |
| --- | --- | --- | --- | --- | --- |
| Customers | One source customer per `(Id, KeyQualifier)` | Discover actual ID and qualifier fields/types | Discover actual primary key and qualifier mapping | Parent; one row per qualified key | Quarantine null key parts and conflicting duplicate qualified keys |
| Customers.Name | Customer attribute, not a key | Discover actual attribute field/type | Discover actual name mapping | Attribute of qualified customer | Confirm policy for conflicting names; do not split key grain silently |
| Orders | One order per durable order key; `OrderId` unique only in fixture | Discover actual order key and any own namespace | Discover actual order primary key/qualifier | Child | Verify actual order uniqueness; do not assume cross-source OrderId uniqueness |
| Orders.CustomerId + CustomerKeyQualifier | Reference to customer qualified key | Preserve both reference parts and source namespace | Verify both parent-reference mappings and relationship | Many orders to one qualified customer | Quarantine or report null/orphan references; never cross-match namespaces |
| Orders.Amount | One monetary amount per order | Discover numeric type, currency and precision | Verify compatible numeric/currency semantics | Measure | Flag nulls; agree currency and rounding before real aggregation |

Preserve CRM and ERP as distinct namespaces for this fixture. A shared ID does not imply identity resolution or that A and B represent the same person. Verify compatible field types, qualifier value semantics/case, standard/custom name collisions, existing relationships and downstream consumers before proposing a mapping change. No mapping removal or replacement is authorized or performed here.

## Validation and change record

The synthetic checks below were executed as Python equality joins and integer sums, not SQL or Salesforce operations.

| Fixture | Expected | Actual local arithmetic | Environment | Result |
| --- | --- | --- | --- | --- |
| ID-only join | A=30, B=30, grand total 60 | A=30, B=30, grand total 60 | Local Python, supplied synthetic rows | Defect reproduced |
| ID + qualifier join | A=10, B=20, grand total 30 | A=10, B=20, grand total 30 | Local Python, supplied synthetic rows | Arithmetic passes |

| Boundary/window | Input | Accepted | Rejected | Filtered | Expected output | Actual output | Explanation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Supplied source fixture | 2 customers; 2 orders; amount 30 | N/A | N/A | N/A | 2 qualified customers, 2 orders | Fixture only | No ingestion performed |
| Source → DLO → DMO | Not observed | Not observed | Not observed | Not observed | Preserve both namespaces and two orders at equal snapshot | Not observed | Requires authorized target evidence |
| DMO → report | Target not observed | N/A | N/A | N/A | CRM/A=10; ERP/B=20 | Not observed in Salesforce | Local arithmetic is not target execution |

Before acceptance, inspect target schemas, profile duplicate/null qualified keys, verify zero orphan references for the fixture, and reconcile order count and amount before/after the join. Test duplicate parent keys (must block fan-out), repeated order ingestion (must not double amounts), null references, orphan references, equal-value legitimate orders, empty input, customers without orders, null measures, updates and deletions. For this fixture, a repeat run should retain two orders and amount 30 if the verified path provides intended upsert/idempotent semantics; that behavior remains untested. Record rejects and filtered records explicitly rather than discarding them to force counts to match.

## Failures and handoff

- **Draft checks:** supplied collision fixture and expected arithmetic checked locally. No SQL parser or target dialect validation claimed.
- **Sandbox checks:** none executed. Compile and run the adapted query under the intended identity and data space; retrieve all result pages and distinguish query success from complete retrieval and reconciliation.
- **Production behavior:** untested, including freshness, costs, connector behavior, mapping propagation, access, scheduling and downstream dependencies. No calculated insight was saved or activated.
- **Recovery:** before any separately authorized mapping change, capture prior mappings and dependent consumers, test a bounded sample and repeat run, and stop promotion on unexplained mismatches. Use the verified path's documented rollback/reprocessing procedure; no rollback execution is claimed.
- **Next owners:** data modeling owner verifies qualified-key and relationship mappings; finance owner confirms amount/null/currency semantics; query owner compiles and reconciles in the authorized sandbox. No live-org evidence is available to certify the change.
