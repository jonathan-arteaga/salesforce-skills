# SOQL & SOSL Authoring and Optimization (API 67+)

Write selective, governor-safe SOQL and SOSL queries using `WITH USER_MODE` and verify selectivity with Query Plan before production use.

## Choosing the Right Query Shape

| Need | Pattern | Notes |
| --- | --- | --- |
| Parent fields from child | Child-to-parent dot notation (`Account.Name`) | Up to 5 relationship levels; use `__r` for custom lookups |
| Child rows from parent | Parent-to-child subquery (`SELECT Id, (SELECT Id FROM Contacts)`) | Use plural child `relationshipName`; avoid deep nesting |
| Counts & grouped summaries | Aggregate (`COUNT()`, `SUM()`, `GROUP BY`, `HAVING`) | Avoid loading raw records into Apex just to count |
| Records with / without children | Semi-join (`Id IN (SELECT ...)`) / anti-join (`Id NOT IN (...)`) | Max 2 semi/anti-joins per query; keep inner filter selective |
| Polymorphic lookups | `TYPEOF What WHEN Account THEN Name ELSE Id END` | Preferred over multiple follow-up queries on `Task`/`Event` |
| Multi-object text search | SOSL (`FIND {term} IN NAME FIELDS RETURNING Account(Id, Name)`) | Uses search index; avoids leading-wildcard SOQL table scans |

## API 67+ Security Enforcement (`WITH USER_MODE`)

Always enforce CRUD, FLS, and sharing cleanly with `WITH USER_MODE` in SOQL (and `AccessLevel.USER_MODE` in Apex `Database.queryWithBinds` / DML):

```sql
SELECT Id, Name, Industry, AnnualRevenue
FROM Account
WHERE Industry = :industryFilter
  AND IsDeleted = false
WITH USER_MODE
ORDER BY LastModifiedDate DESC
LIMIT 200
```

- `WITH USER_MODE` evaluates object CRUD, field-level security across `SELECT`, `WHERE`, and `ORDER BY`, polymorphic fields, and sharing rules consistently, returning all inaccessible fields in `QueryException.getInaccessibleFields()`.
- For dynamic SOQL in Apex, use `Database.queryWithBinds(query, bindMap, AccessLevel.USER_MODE)` to prevent SOQL injection and avoid string interpolation.

## Selectivity, Indexing & Governor Limits

1. **Standard & custom indexes**: Filter on `Id`, `Name`, `OwnerId`, `CreatedDate`, `LastModifiedDate`, `SystemModstamp`, `RecordTypeId`, External IDs, Unique fields, and Lookup/Master-Detail foreign keys.
2. **Avoid non-selective filters**: Leading wildcards (`LIKE '%acme'`), negative operators (`!=`, `NOT IN`, `!= null`), unindexed formula fields, and filtering on null values defeat standard indexes.
3. **Query Plan check**: Run the Query Plan tool against realistic org volumes (`sf data query --query "..." --target-org <alias> --use-tooling-api` or REST `/query/?explain=...`). Aim for `relativeCost <= 1.0` with an `Index` leading operation rather than `TableScan`.
4. **Limits & bulk safety**: Select only required fields (never emulate `SELECT *`), never run SOQL inside loops, apply explicit `LIMIT` on interactive queries, and use `FOR UPDATE` only when row locking is required.

## CLI Execution & Bundled Validators

- Execute ad hoc read queries: `sf data query --query "SELECT Id, Name FROM Account LIMIT 10" --target-org <alias>`
- Bulk export (> 50,000 rows): `sf data query --file query.soql --bulk --wait 10 --result-format csv --target-org <alias>`
- Validate `.soql` files locally via bundled CLI scripts:
  - `python3 ./scripts/soql_validator.py path/to/query.soql`
  - `echo '{"tool_input":{"file_path":"path/to/query.soql"},"tool_response":{"success":true}}' | python3 ./scripts/soql-post-validate.py`
