# Apex guidance

- Preserve an existing component API version unless an upgrade is in scope. For new components select a version supported by the target org/toolchain; inspect release-specific behavior rather than freezing every project at 66.0.
- API 67.0+ defaults database operations to user mode and rejects WITH SECURITY_ENFORCED. API 66.0 and earlier defaults differ. Use explicit sharing and explicit USER_MODE for predictable CRUD/FLS and row access across versions; test least-privileged users.
- Permission violations in user-mode queries can throw exceptions. Empty rows may instead reflect sharing, filters, or missing data. Do not weaken security to conceal an error.
- SYSTEM_MODE bypasses object/field checks; record sharing still follows the calling class. Justify elevation narrowly. For graceful field stripping, use the returned getRecords() from stripInaccessible and separately enforce record access.
- Bind values in dynamic queries (prefer queryWithBinds with AccessLevel.USER_MODE), allowlist dynamic identifiers, bulkify SOQL/DML, and test negative permissions, bulk behavior, and failure handling. Coverage alone is not correctness.

## Sources checked 2026-11-15

- [Apex Security and Sharing Model](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_security_sharing_chapter.htm)
- [Set an Access Mode for Database Operations](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_enforce_usermode.htm)
- [Dynamic SOQL](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dynamic_soql.htm)
