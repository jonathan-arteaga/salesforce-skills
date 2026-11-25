# Metadata Deploy & Validate Reference

Safe validation, scoped deployment, production promotion gates, destructive changes, test-level rules, and Agent/Data 360 metadata boundaries using `sf` CLI v2.

## 1. Default Dependency Ordering

Sequence multi-layer releases to prevent FLS and cross-reference failures:

| Phase | Metadata | Notes |
| --- | --- | --- |
| 1 | Custom Objects, Custom Fields, Record Types | Must exist before permissions and code reference them |
| 2 | Permission Sets, Permission Set Groups, Muting Sets | Grant access before deploying/testing dependent features |
| 3 | Apex Classes, Triggers, LWC, Named/External Credentials | Deploy backing logic before Flows and Agents |
| 4 | Flows (as Draft) | Avoid premature activation before dependencies settle |
| 5 | Agent metadata (`AiAuthoringBundle` / `Agent:<Name>`), Flow activation, post-verify | Publish/activate after backing actions are live |

## 2. Non-Production Workflow (Dry-Run -> Deploy -> Report)

Always classify the target org first (`references/org-lifecycle.md` Section 2) and pin `--target-org <user-or-alias>`. On non-source-tracking orgs, specify an explicit scope (`--source-dir`, `--metadata`, or `--manifest`).

```bash
# 1. Dry-run validation
sf project deploy start --dry-run --source-dir force-app \
  --target-org <sandbox-or-scratch> --wait 30 --json

# 2. Scoped deploy
sf project deploy start --manifest manifest/package.xml \
  --target-org <sandbox-or-scratch> --test-level RunLocalTests --wait 30 --json

# 3. Spring '26 relevant-test selection (when org policy permits)
sf project deploy start --manifest manifest/package.xml \
  --target-org <sandbox-or-scratch> --test-level RunRelevantTests --wait 30 --json

# 4. Report / poll
sf project deploy report --job-id <job-id> --target-org <sandbox-or-scratch> --json
```

## 3. Production Two-Step Promotion Gate (HARD GATE)

NEVER run `sf project deploy start` against production. Production deploys MUST go through server-side validation followed by gated quick deploy.

### Step P1: Validate Only (`sf project deploy validate`)

```bash
sf project deploy validate --manifest manifest/package.xml \
  --target-org <prod-user-or-alias> --test-level RunLocalTests --wait 30 --json
```

Persist the returned validation `jobId` (valid 10 days) together with the target's immutable `orgId` and `instanceUrl` from `sf org display --target-org <prod> --json` (e.g., in `.sfdx/last-validation.json`). On validation failure, inspect `result.details.componentFailures` and `result.details.runTestResult.failures`, report root causes, and STOP. Never pass `--ignore-errors` or `--ignore-warnings` on production validation.

### Step P2: Five Mandatory Pre-Promotion Checks

Before calling quick deploy, verify ALL five:
1. **Target is production** (per `sf org list --skip-connection-status --json`).
2. **Concrete validation job ID resolved** (never carry an unresolved `--use-most-recent` flag into confirmation).
3. **Immutable `orgId` match**: re-run `sf org display --target-org <prod> --json` and verify `result.id == persisted.orgId`. Any mismatch or missing `orgId` is a HARD STOP — re-validate in P1.
4. **Freshness**: explicit `--job-id` <= 10 days; `--use-most-recent` <= 3 days.
5. **Explicit user confirmation**: display the Production Deploy banner populated from live verified data (org alias, instance URL, `OrganizationType` via SOQL `SELECT OrganizationType FROM Organization`, validation ID, validated timestamp, component count, test summary) and require a literal user `"yes"`. Never auto-confirm.

### Step P3: Quick Deploy & Audit Trail

```bash
# Run ONLY after literal user "yes"
sf project deploy quick --job-id <validation-id> \
  --target-org <prod-user-or-alias> --wait 30 --json
```

Quick deploy generates a **new deployment job ID** (`result.id`) and promotes the validated artifact without re-running tests. Poll and archive `sf project deploy report --job-id <quick-deploy-id> --target-org <prod> --json` using the **quick-deploy ID** (keep the validation ID separately for traceability).

## 4. Test Levels & `RunSpecifiedTests` Coverage Rule

| Test Level | When to Use | Critical Rule |
| --- | --- | --- |
| `NoTestRun` | Non-prod non-Apex or scratch iteration only | Disallowed for production Apex deploys |
| `RunLocalTests` | Default for production validations | Runs all local (non-managed) tests; org-wide >= 75% |
| `RunRelevantTests` | Spring '26 Apex-heavy releases where org policy allows | Pair with `@IsTest(testFor=...)` and `@IsTest(isCritical=true)` |
| `RunSpecifiedTests` | Targeted fast production validation (`--tests ClassA ClassB`) | **Every deployed Apex class and trigger must individually achieve >= 75% coverage AND every specified test must pass.** An org-wide 75% average alone fails deployment. |

Coverage alone does not prove correctness; delegate test authoring to `salesforce-apex`.

## 5. Destructive Changes (`destructiveChanges.xml`)

Require explicit confirmation before running destructive deploys. Choose pre- vs post-deletion deliberately:
- `--pre-destructive-changes manifest/destructiveChangesPre.xml`: deletes components BEFORE new metadata is deployed (use when renaming or removing conflicts).
- `--post-destructive-changes manifest/destructiveChangesPost.xml`: deletes components AFTER new metadata is deployed (use when removing obsolete fields/classes still referenced by old code).

```bash
# Always dry-run destructive changes first
sf project deploy validate --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChangesPost.xml \
  --target-org <target> --test-level RunLocalTests --wait 30 --json
```

Never combine destructive deploys with `--ignore-errors`.

## 6. Agentforce & Data 360 Deployment Boundaries

### Agentforce Metadata
- `Agent:<Name>` pseudo-metadata retrieves/deploys `Bot`, `BotVersion`, `GenAiPlannerBundle`, `GenAiPlugin`, and `GenAiFunction`.
- **NOT included**: Apex classes, Flows, Named/External Credentials, Permission Sets — deploy those first.
- For Agent Script bundles (`AiAuthoringBundle`), validate and publish with CLI:
  ```bash
  sf agent validate authoring-bundle --api-name <AgentApiName> --target-org <org> --json
  sf agent publish authoring-bundle --api-name <AgentApiName> --target-org <org> --json
  sf agent activate --api-name <AgentApiName> --version <N> --target-org <org> --json
  ```
- Modifying an active agent requires `sf agent deactivate --api-name <AgentApiName> --target-org <org> --json` first. Delegate authoring to `agentforce-build`.

### Data 360 Metadata Boundaries
- Not every Data 360 resource (connectors, data streams, calculated insights, identity rulesets, activations, data space policies) is deployable through standard Metadata API.
- Check official Metadata API vs **Data Kit** packaging support for the target org's release before constructing `package.xml`. Do not assume `sf project deploy` migrates runtime data, historical STDM traces, or connector credentials. Delegate Data 360 pipeline/governance design to `data360-data-pipeline` and `data360-activation-governance`.

## 7. High-Signal Failure Triage

| Error | Likely Cause | Fix Direction |
| --- | --- | --- |
| `FIELD_CUSTOM_VALIDATION_EXCEPTION` | Validation rule or bad test fixture | Fix test data or rule sequencing |
| `INVALID_CROSS_REFERENCE_KEY` | Missing upstream dependency | Deploy referenced object/field/permset first |
| `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` | Trigger/Flow cascade exception | Inspect trigger stack; decouple independent side effects via Queueable/Platform Events (`salesforce-apex`) |
| `RunSpecifiedTests` coverage failure | One deployed class/trigger < 75% | Add test classes covering that specific component |
| Field/object missing in Permission Set | Out-of-order deploy | Deploy objects/fields in Phase 1 before Phase 2 |

## Sources Verified

- Running a Subset of Tests in a Deployment: `https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_deploy_run_specific_tests.htm` / `https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_run_specific_tests.htm`
- CustomObject / CustomField Metadata API: `https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customobject.htm`
