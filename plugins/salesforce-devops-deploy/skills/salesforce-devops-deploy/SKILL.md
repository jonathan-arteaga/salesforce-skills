---
name: salesforce-devops-deploy
description: "Manage Salesforce scratch orgs, snapshots, metadata validation and deploys, destructive changes, 2GP packaging, and DevOps Center CI/CD with explicit target-org pinning and production gates. Use salesforce-apex, salesforce-flow, salesforce-lwc, or agentforce-build to author source."
---

# Salesforce DevOps & Deploy

End-to-end Salesforce CLI v2 (`sf`) org lifecycle, metadata validation and deployment, 2GP packaging, and DevOps Center / CI pipelines. Select the mode below and load only its reference first.

## Mode Routing

| Mode | When to use | Reference |
| --- | --- | --- |
| Org Lifecycle | Scratch org create/list/display/resume/delete, snapshots, org shapes, Dev Hub resolution, org classification | [org-lifecycle.md](references/org-lifecycle.md) |
| Metadata Deploy & Validate | `sf project deploy validate/start/quick/report`, `RunSpecifiedTests` / `RunRelevantTests`, `destructiveChanges.xml`, Agent & Data 360 deploy boundaries | [metadata-deploy-validate.md](references/metadata-deploy-validate.md) |
| 2GP Packaging & DevOps CI | 2GP Unlocked/Managed packages (`sf package version create/promote`), DevOps Center promotions, Code Analyzer v5, Spring '26 Unified Logic Testing | [packaging-devops-ci.md](references/packaging-devops-ci.md) |

## Core 2026 Invariants

- **Salesforce CLI v2 only**: Use `sf` commands with `--json` for structured output (except `sf org open`, which must never use `--json` or `--url-only`).
- **Explicit target pinning**: Always pass an explicit `--target-org <username-or-alias>` and `--target-dev-hub <username-or-alias>` on mutations; never rely on an ambient default org. Resolve Dev Hub across all `sf org list --json` buckets and never fabricate a placeholder alias.
- **Classify from `sf org list`**: Classify production vs non-production using `sf org list --skip-connection-status --json`, NOT `sf org display` (which omits sandbox/scratch/trial flags and misclassifies SDOs).
- **`RunSpecifiedTests` 75%-per-component rule**: Every deployed Apex class and trigger must individually reach at least 75% coverage AND every specified test must pass; an org-wide coverage percentage alone is insufficient.
- **Spring '26 CI modernization**: Prefer `--test-level RunRelevantTests` (paired with `@IsTest(testFor=...)` / `@IsTest(isCritical=true)`) where org policy allows, Code Analyzer v5 (`sf code-analyzer`, replacing retired `sf scanner`), and Spring '26 Unified Logic Testing for combined Apex + Flow CI suites.
- **Deployment boundaries**: `Agent:<Name>` deploys bot/planner/plugin/function metadata only — deploy backing Apex, Flows, and Named Credentials first. Do not assume every Data 360 resource is deployable via Metadata API; verify official Metadata API / Data Kit support per resource.

## Hard Org & Safety Gates

1. **Production deploy hard gate**: NEVER run `sf project deploy start` against production, and NEVER promote to production without explicit user approval. Production uses two-step `sf project deploy validate` -> verify `orgId` + freshness + print Production Deploy banner -> literal user "yes" -> `sf project deploy quick`.
2. **Destructive action gate**: Scratch org deletion (`sf org delete scratch`) and destructive metadata deploys (`destructiveChangesPre/Post.xml`) require explicit confirmation before execution; never pair destructive deploys with `--ignore-errors`.
3. **Zero credential leakage**: Never run `sf org display --verbose`, `sf org open --json`, or `sf org open --url-only` in agent context; they emit live refresh tokens or `frontdoor.jsp` login URLs. Instruct the user to run those locally if needed.

## Standard Release Sequence

1. **Preflight & classify**: Verify `sf --version`, `sfdx-project.json`, and target org type via `sf org list --skip-connection-status --json`.
2. **Static check & dry-run**: Run `sf code-analyzer run` and check-only validation (`sf project deploy validate` or `--dry-run`) in dependency order (Objects/Fields -> Permission Sets -> Apex/LWC -> Flows as Draft -> Agents & activation).
3. **Promote & archive**: Deploy only the minimal verified scope; persist the validation record (`jobId`, `orgId`, `instanceUrl`) and post-deploy report (`<quick-deploy-id>.json`).

## Verification Integrity

- Record exact target org (`alias`, `username`, `orgId`, `instanceUrl`), deployment or package job ID, test level, component successes/failures, and test pass/fail counts from actual CLI output.
- For quick deploys, poll and archive the **new quick-deploy job ID** — never report the validation job ID as the completed production deployment.
- Without live org auth, return a validated manifest, ordering plan, and exact CLI commands with unresolved org checks listed explicitly.

## Companion Handoffs

- Authoring Apex, Flows, LWC, or Integrations: `salesforce-apex`, `salesforce-flow`, `salesforce-lwc`, `salesforce-integrations`
- Custom objects, fields, and synthetic test data: `salesforce-schema-data`
- Permission set design and access verification: `salesforce-security-access`
- Agent authoring, review, and test execution: `agentforce-build`, `agentforce-review`, `agentforce-test`
- Data 360 pipeline/governance setup: `data360-data-pipeline`, `data360-activation-governance`
