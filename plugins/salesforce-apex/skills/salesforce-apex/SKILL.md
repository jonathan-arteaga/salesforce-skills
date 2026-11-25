---
name: salesforce-apex
description: "Author, test, run, and debug Salesforce Apex classes, triggers, and async jobs using API 67+ user-mode security, Apex Cursors, and governor-limit log diagnosis. Use salesforce-flow for declarative flows, salesforce-lwc for UI components, and salesforce-devops-deploy for org rollouts."
---

# Salesforce Apex

Lifecycle skill for production Apex authoring, unit and Unified Logic testing, test execution, and debug-log root-cause diagnosis.

## Mode Routing

Select the active mode first and load only the matching reference before acting:

| Mode | When to Use | Reference |
| --- | --- | --- |
| Author / Review | New or refactored `.cls`/`.trigger`, async jobs, security/bulkification review | [authoring-security-and-async.md](references/authoring-security-and-async.md) |
| Test / Run / Fix | Author `{Class}Test.cls`, Unified Logic Testing (Apex + Flow), run suites, fix failures | [testing-and-unified-logic.md](references/testing-and-unified-logic.md) |
| Debug Logs | Analyze `.log` files, stack traces, SOQL/DML/CPU/heap governor limits | [debug-logs-and-governor-limits.md](references/debug-logs-and-governor-limits.md) |

## Core 2026 Invariants

- **API 67+ User-Mode Default**: API 67.0+ defaults database operations to user mode and rejects `WITH SECURITY_ENFORCED` at compile time. Preserve an existing component's API version unless an upgrade is in scope. Write explicit sharing (`with sharing` default) plus `WITH USER_MODE` / `AccessLevel.USER_MODE` for predictable behavior across versions.
- **Dynamic Queries & Elevation**: Use `Database.queryWithBinds` with `AccessLevel.USER_MODE` and allowlisted identifiers. Never weaken security to hide permission exceptions. `SYSTEM_MODE` bypasses CRUD/FLS while sharing still follows the class; isolate `without sharing` helpers behind Custom Permission checks.
- **Bulkification & Modern Async**: Zero SOQL or DML inside loops; use `Map`/`Set` lookups, `Database.update(records, false)`, and CMDT `getAll()`/`getInstance()` (never SOQL on `__mdt`). Never use `@future`; choose Queueable + `System.Finalizer`, Apex Cursors (`Database.getCursor` up to 50M rows, 2,000-row fetches), or Batch Apex.
- **Testing & Unified Logic**: Use `Assert` class only (never `System.assert*`), `SeeAllData=false`, `TestDataFactory` in `@TestSetup`, 251+ bulk tests, `System.runAs` least-privileged tests, and Unified Logic Testing across Apex and Flow boundaries.

## Hard Org & Safety Gates

- Confirm target org alias and API version before running org tests, setting trace flags, or upgrading `apiVersion`.
- Never hardcode Salesforce Record IDs, secrets, credentials, or PII in code, tests, or `System.debug()` statements; keep `System.debug()` off production hot paths.
- Never claim a fix works without running static analysis (`sf code-analyzer run` / `run_code_analyzer`) and org tests, or explicitly recording unavailable tools.
- Never modify production data directly; run tests and benchmarks in sandboxes or scratch orgs with synthetic fixtures.

## Deterministic Script (Black-Box Usage)

Format `sf apex run test` JSON or human output for the test-fix loop without inspecting script internals:

```bash
TOOL_INPUT="sf apex run test" TOOL_OUTPUT="$(sf apex run test --class-names MyServiceTest --result-format json --code-coverage --target-org <alias>)" \
  python3 scripts/parse-test-results.py
```

The script summarizes pass/fail counts, extracts failure stack traces, and flags classes below the 75% coverage floor.

## Required Deliverables & Verification Integrity

- **Per class / trigger**: Paired `.cls` + `.cls-meta.xml` (or `.trigger` + `.trigger-meta.xml`), plus `{ClassName}Test.cls` + `.cls-meta.xml` for production changes.
- **Report order**: Summary -> Files -> Design & Security choices -> Analyzer output (or `run_code_analyzer=unavailable: <reason>`) -> Test results (or `test_execution=unavailable: <reason>`) -> Next deploy step.
- Distinguish **static/local checks** (code review, Code Analyzer) from **live org verification** (executed org tests, debug logs). Never fabricate passing tool output.

## Cross-Skill Handoffs

- `salesforce-flow`: declarative Flows and Flow audits
- `salesforce-lwc`: LWC bundles, SLDS 2, and Jest unit tests
- `salesforce-integrations`: Named Credentials, External Client Apps, callout plumbing, and Pub/Sub API
- `salesforce-schema-data`: object/field metadata, SOQL tuning, and synthetic seed data
- `salesforce-security-access`: org-wide Permission Sets and sharing architecture
- `salesforce-devops-deploy`: validation deployments and CI/CD rollouts
- `agentforce-observe`: Agentforce session traces and telemetry debugging
