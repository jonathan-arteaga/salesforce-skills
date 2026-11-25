# Data 360 SQL & Calculated Insights

Author, validate, and debug Data 360 SQL queries and Calculated Insights (CIOs) with deterministic grain, safe joins, and accurate API pagination.

## Query API Family & Pagination Contracts

Never mix query dialects or pagination contracts across Salesforce API families:

| API Family | Dialect / Scope | Pagination Contract | Key Constraint |
| --- | --- | --- | --- |
| Newer Data 360 Query API | Data 360 SQL (check current docs before new builds) | Verify target release cursor/page token in docs | Preferred for new implementations when target org supports it |
| Query V2 (`/api/v2/query`) | Data 360 SQL (retained implementations) | `done` boolean + `nextBatchId` | Fetch all batches until `done: true`; max 1 hour overall, < 3 min between batches |
| SSOT Connect Metadata | DLO/DMO/CIO metadata collections | `nextPageUrl` / `limit` / `offset` | Metadata discovery only — not query row pagination |
| Core CRM REST / SOQL | Salesforce SOQL | `nextRecordsUrl` | Completely separate from Data 360 SQL; route to `salesforce-schema-data` |

- Always verify whether the target org supports the newer Data 360 Query API successor before building new Query V2 integrations.
- Never infer completeness from the first batch. If a query hits timeout, row limits, or batch expiration, report the result as truncated/incomplete with exact batch count and query/correlation ID.

## SQL Engine, Grain & Fan-Out-Safe Joins

1. **Identify SQL engine**: Distinguish current **Data 360 SQL** from **Legacy SQL** insights. Functions, whitespace trimming, null handling, and type coercions differ between Query Editor and Calculated Insight engines — validate in the target engine, not only in Query Editor or local SQLite.
2. **One-sentence grain contract**: State output grain before writing SQL (for example, "one row per Unified Individual per calendar month in UTC") and write expected golden rows first.
3. **Prevent join fan-out**: Classify every join (`1:1`, `N:1`, `N:M`). Example: 2 orders (10 and 20) joined directly to 3 contact points produce 6 rows and a naive `SUM` of 90 instead of 30. Aggregate orders to customer grain before joining, and join on Fully Qualified Keys (`KQ_*` + ID). Never hide fan-out with `DISTINCT` (two legitimate orders can have the same amount):

```sql
WITH customer_orders AS (
  SELECT
    o.ssot__SoldToCustomerId__c AS customer_id__c,
    o.KQ_SoldToCustomerId__c    AS customer_kq__c,
    SUM(o.ssot__GrandTotalAmount__c) AS total_spend__c
  FROM ssot__SalesOrder__dlm o
  WHERE o.ssot__OrderStartDate__c >= TIMESTAMP '2026-01-01 00:00:00'
    AND o.ssot__OrderStartDate__c <  TIMESTAMP '2026-02-01 00:00:00'
  GROUP BY o.ssot__SoldToCustomerId__c, o.KQ_SoldToCustomerId__c
)
SELECT
  u.ssot__Id__c AS unified_id__c,
  COALESCE(SUM(co.total_spend__c), 0) AS monthly_spend__c
FROM UnifiedssotIndividual__dlm u
LEFT JOIN UnifiedLinkssotIndividual__dlm l
  ON u.ssot__Id__c = l.UnifiedRecordId__c
LEFT JOIN customer_orders co
  ON l.SourceRecordId__c = co.customer_id__c
 AND l.KQ_SourceRecordId__c = co.customer_kq__c
GROUP BY u.ssot__Id__c
```

4. **Calculated Insight specifics**: Verify supported aggregate/window functions, required `GROUP BY` dimensions (adding a dimension changes grain, not just display), and inclusion of the segmented entity's primary key when the CIO is consumed in segmentation. Do not substitute Streaming Insights semantics for batch Calculated Insights.

## Execution State & Validation Checklist

- **Golden fixtures**: Test empty sets, null measures, duplicate keys, identical local IDs from different sources (`KQ_*`), whitespace trimming, and inclusive/exclusive timezone boundaries.
- **Parameter safety**: Quote identifiers and bind parameters only as supported by the target API; never interpolate untrusted user input into SQL strings.
- **Lifecycle separation**: Track request acceptance, insight definition saved, active status, processing job completion, full paginated output, and schedule verification separately. Poll with a bounded deadline, preserve async error/correlation IDs, and never delete/recreate an insight as an automatic workaround.
