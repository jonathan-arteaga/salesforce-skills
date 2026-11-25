# Apex Authoring, Security, and Async Architecture

## API Version & 2026 Security Model

- **Version discipline**: Preserve existing `apiVersion` in `.cls-meta.xml` / `.trigger-meta.xml` unless an upgrade is requested. For net-new components, pick the latest version supported by the target org and toolchain.
- **API 67.0+ user-mode default**: Database operations default to user mode, and `WITH SECURITY_ENFORCED` fails compilation. API 66.0 and earlier default differently. Write explicit `WITH USER_MODE` on SOQL and `AccessLevel.USER_MODE` on `Database.*` DML so behavior is portable across versions.
- **Permission errors vs empty rows**: User-mode CRUD/FLS violations throw exceptions; empty rows reflect sharing, filters, or missing data. Never relax security to conceal an error.
- **Explicit sharing**: Declare `with sharing` by default on every class. Document any `without sharing` or `inherited sharing` choice. Isolate `without sharing` inside a small helper class gated by `FeatureManagement.checkPermission(...)`.
- **Elevation & stripping**: `SYSTEM_MODE` bypasses object/field permissions, while record sharing still follows the class declaration. When stripping inaccessible fields gracefully with `Security.stripInaccessible(...)`, always use the returned `getRecords()` list and enforce record access separately.
- **Dynamic SOQL injection defense**: Use `Database.queryWithBinds(query, bindMap, AccessLevel.USER_MODE)`. Validate dynamic object, field, or sort identifiers against a strict allowlist or `Schema.getGlobalDescribe()` / `SObjectType.getDescribe()`.
- **UI & secrets hygiene**: Rethrow user-facing `@AuraEnabled` errors as sanitized `AuraHandledException`. Never hardcode IDs or secrets; use Named Credentials, Custom Labels, and Custom Metadata (`MyConfig__mdt.getAll().values()` or `getInstance()`, never SOQL on `__mdt`).

## Layering, Naming & Bulkification

| Layer | Naming Pattern | Responsibility | Must NOT Contain |
| --- | --- | --- | --- |
| Trigger | `{SObject}Trigger` | Event routing to handler or Trigger Actions (`TA_{SObject}_{Action}`) | Business rules, SOQL, DML |
| Service / Handler | `{SObject}Service` | Transaction orchestration, DI seams, partial-success DML | Inline HTTP parsing or raw trigger logic |
| Domain | `{SObject}Domain` | Validation, state transitions, pure business logic | SOQL, DML, callouts |
| Selector / Data | `{SObject}Selector` | Selective `WITH USER_MODE` queries, explicit field lists | Business decisions |

- **Bulkification**: Accept `List`/`Set` inputs on public APIs; delegate single-record overloads. Use `Map<Id, SObject>` and `Map<Id, List<SObject>>` for parent-child grouping, `Set<Id>` for membership checks, and `AggregateResult` for rollups. Compare against `Trigger.oldMap` and DML only modified records.
- **Caching**: Use Platform Cache (`Cache.Org` / `Cache.Session`) with TTL and cache-miss fallback for shared read-mostly data, and `private static Map` lazy caches to avoid duplicate queries within one transaction.
- **Null safety & readability**: Guard null/empty inputs at method entry; return empty collections instead of `null`; use `?.`, `??`, and `String.isBlank()`. Avoid `System.debug()` on hot paths (evaluates arguments even without active logs). Keep classes under 500 lines with ApexDoc (`@param`, `@return`, `@throws`) on classes and public/global methods.
- **Exceptions**: Catch specific exceptions before `Exception`, wrap only throwable operations, and preserve cause chains (`new DomainException('context', ex)`).

## Async Decision Matrix

| Scenario | Recommended Pattern | Key Constraints & 2026 Guidance |
| --- | --- | --- |
| Standard async / callouts | **Queueable** + `System.Finalizer` | Supports non-primitives, chaining, `AsyncOptions` (delay up to 10 min, dedup signature), guaranteed cleanup |
| High-scale pagination (up to 50M rows) | **Apex Cursors** (`Database.getCursor` / `Database.Cursor`) | Fetch up to 2,000 rows per call; chain via Queueable; bypasses 5-job concurrent Batch limit |
| Classic chunked processing | **Batch Apex** (`Database.QueryLocator`) | Max 5 concurrent jobs; up to 50M rows; use `Database.Stateful` sparingly |
| Recurring jobs | Scheduled Flow (preferred) or **Schedulable** | 100-job org limit; use Apex Schedulable only for complex logic or Batch orchestration |
| Long-running LWC/VF callouts | **Continuation** | Up to 3 continuations per transaction, 3 parallel requests |
| Legacy `@future` | **Do not use** | Cannot chain, cannot run from Batch, primitives only; replace with Queueable + Finalizer |

## Authoring Validation Gate

1. Generate `{ClassName}.cls`, `{ClassName}.cls-meta.xml`, and corresponding test files (matching target API version):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>67.0</apiVersion>
    <status>Active</status>
</ApexClass>
```

2. Verify security checklist: explicit sharing keyword, CRUD/FLS enforced on SOQL/DML, no hardcoded IDs/secrets, sanitized `@AuraEnabled` exceptions, no PII in logs.
3. Run Code Analyzer (`run_code_analyzer` MCP or `sf code-analyzer run --target <path>`) and remediate all `sev0`–`sev2` findings.
4. Run org tests and report verbatim analyzer + test results (or explicit `unavailable: <reason>`).
