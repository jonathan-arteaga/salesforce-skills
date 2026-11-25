# Apex Testing, Unified Logic Testing, and Execution

## Authoring Principles

- **Deliverables**: Always create `{ClassName}Test.cls` + `{ClassName}Test.cls-meta.xml` (matching the target class API version) and a reusable `TestDataFactory.cls` when none exists.
- **Isolation**: Default to `@IsTest` (`SeeAllData=false`). Create shared fixtures in `@TestSetup` via `TestDataFactory` — never rely on org records or hardcoded IDs, and re-query `@TestSetup` records in each test method.
- **Assertions**: Use the modern `Assert` class exclusively (`Assert.areEqual`, `Assert.isTrue`, `Assert.isNotNull`, `Assert.fail`). Never use legacy `System.assert*`. Assert exact expected values with clear failure messages.
- **One scenario per method**: Separate positive, negative, null, empty (`_NullInput_` vs `_EmptyInput_`), security, and bulk paths using `should[Result]_When[Scenario]` naming and Given/When/Then structure.
- **Bulk & async boundaries**: Test trigger/service bulk paths with **251+ records** to cross the 200-record chunk boundary. Wrap code under test in `Test.startTest()` / `Test.stopTest()` to reset governor limits and force async completion. For Batch Apex, remember test context runs only one `execute()` call, so set `batchSize >= testRecordCount`.
- **Security & API 67+ testing**: Test least-privileged personas via `System.runAs(user)` with assigned Permission Sets. Verify both allowed access and expected user-mode CRUD/FLS exceptions on negative permission tests.

## Mocking External Boundaries

- **HTTP callouts**: Register `Test.setMock(HttpCalloutMock.class, mock)` before invoking the callout. Separate setup DML from callouts using `Test.startTest()` to avoid uncommitted-work errors.
- **SOSL**: Seed deterministic results via `Test.setFixedSearchResults(List<Id>)`.
- **Database / Service DI**: Inject selector or DML interfaces (`StubProvider` or lightweight mock implementations) for fast, isolated unit tests alongside integration tests.
- **Platform Events & CDC**: Call `Test.enableChangeDataCapture()` before DML and `Test.getEventBus().deliver()` to execute subscribers synchronously.

## Unified Logic Testing (Apex + Flow)

- Coordinate Apex unit tests and Flow Tests together when triggers, invocable Apex actions, and Record-Triggered Flows interact on the same object.
- Run unified test commands supported by the target org CLI (for example `sf logic run test` when available, or paired `sf apex run test` + Flow test execution) to verify combined governor-limit budgets, recursion safety, and cross-automation regressions.
- Check both Apex code coverage (75% production deploy minimum; 90%+ recommended; 100% on critical security/financial paths) and Flow active-path coverage.

## Execution & Disciplined Fix Loop

Start narrow while debugging, then widen to regression:

```bash
# Single method or class with JSON output for scripts/parse-test-results.py
sf apex run test --tests MyServiceTest.shouldProcessBulk_WhenValid --result-format json --target-org <alias>
sf apex run test --class-names MyServiceTest --result-format human --code-coverage --target-org <alias>

# Full local regression before deployment
sf apex run test --test-level RunLocalTests --result-format human --code-coverage --target-org <alias>
```

**Fix loop (max 3 iterations)**:
1. Parse failing tests (pipe JSON to `scripts/parse-test-results.py`).
2. Inspect both test class and production class stack traces; separate fixture/assertion bugs from production defects and API 67+ permission failures.
3. Apply the minimal fix, rerun the narrow failing test, then widen to the full class and local suite.
4. Stop after 3 iterations if unresolved and report root cause plus concrete remediation options.

## Required Test Report Shape

Report in order: `Test run` (scope) -> `Org` (alias) -> `Result` (pass/fail counts) -> `Coverage` (percentage and low-coverage classes) -> `Issues` (root causes) -> `Next step`.
