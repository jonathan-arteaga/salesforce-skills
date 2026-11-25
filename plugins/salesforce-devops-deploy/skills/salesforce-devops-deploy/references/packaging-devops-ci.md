# 2GP Packaging & DevOps CI Reference

Second-Generation Packaging (2GP Unlocked and Managed), DevOps Center release promotions, Code Analyzer v5 static gates, and Spring '26 Unified Logic Testing in CI/CD.

## 1. 2GP Unlocked & Managed Packaging

Configure `sfdx-project.json` with explicit `packageDirectories`, semantic `versionNumber` (`MAJOR.MINOR.PATCH.NEXT`), `dependencies`, and `packageAliases`. Always pin `--target-dev-hub <devhub>` explicitly.

```bash
# 1. Create a 2GP package (Unlocked or Managed)
sf package create --name "CoreDomain" --package-type Unlocked \
  --path force-app --target-dev-hub <devhub> --json

# 2. Create a package version (use --code-coverage for promotable versions)
sf package version create --package "CoreDomain" \
  --installation-key-bypass --code-coverage --wait 30 \
  --target-dev-hub <devhub> --json

# 3. Check status if async or timed out
sf package version create report --package-create-request-id <08c...> \
  --target-dev-hub <devhub> --json

# 4. Promote validated beta version to Released (irreversible — confirm with user first)
sf package version promote --package "CoreDomain@1.2.0-1" \
  --target-dev-hub <devhub> --json

# 5. Install into target org (pin --target-org; gate production installs behind explicit approval)
sf package install --package "CoreDomain@1.2.0-1" \
  --target-org <target-org> --security-type AdminsOnly \
  --apex-compile package --wait 30 --json
```

Key 2GP invariants:
- **`--skip-validation` trade-off**: Useful ONLY for fast ephemeral PR feedback builds; `--skip-validation` versions CANNOT be promoted to Released. Always build a validated `--code-coverage` version before promotion.
- **Managed 2GP ancestors**: Specify `ancestorVersion` / `ancestorId` in `sfdx-project.json` to preserve upgrade paths; never delete or break published global interfaces without deprecation strategy.
- **Data Kits & Agent components in 2GP**: Verify target release packaging support for Data 360 Data Kits and Agentforce metadata types before adding them to a 2GP directory.

## 2. DevOps Center Promotions

DevOps Center uses Git as source of truth and models release pipelines across environments (e.g., Dev Sandboxes -> Integration -> UAT -> Staging -> Production):

- **Work Items**: Bind feature branches to Work Items; pull declarative and pro-code changes from tracked sandboxes or commit directly via Git.
- **Bundling & Stages**: Combine Work Items at a designated bundling stage (typically UAT/Staging) so downstream promotions move tested release bundles atomically.
- **Hybrid CLI + DevOps Center**: Run CI static analysis, scratch-org verification, and `sf project deploy validate` checks on Work Item pull requests before promoting in DevOps Center. Never bypass branch protection or production promotion approvals.
- **Drift control**: Reconcile hotfixes back into the release branch immediately so DevOps Center does not overwrite emergency production fixes on the next promotion.

## 3. 2026 CI/CD Pipeline Architecture

Recommended pull-request and release pipeline sequence:

1. **Authenticate securely**: Use JWT Bearer flow (`sf org login jwt`) or OAuth Client Credentials / SFDX Auth URL stored exclusively in CI secret vaults. Never echo tokens or `--verbose` output in build logs.
2. **Static analysis — Code Analyzer v5**:
   - Use **Code Analyzer v5** (`sf code-analyzer run`), NOT retired `sf scanner`.
   - Enforce severity thresholds (fail CI on Critical/High security, PMD, ESLint, Graph Engine, or Flow Scanner findings):
     ```bash
     sf code-analyzer run --workspace force-app --output-file reports/code-analyzer.sarif
     ```
3. **Ephemeral Scratch Org or Target Sandbox Validation**:
   - PR check: spin up scratch org (`--no-track-source`), push source, run tests, delete scratch org in `always()` teardown.
   - Integration / Staging / Prod check: run `sf project deploy validate` (check-only) with explicit `--target-org` and appropriate test level (`RunRelevantTests` or `RunLocalTests`).
4. **Spring '26 Unified Logic Testing in CI**:
   - Combine Apex tests and Flow tests in CI rather than treating Flow testing as manual-only. Where the target org and CLI version support Spring '26 Unified Logic Testing (`sf logic test run` / unified test runners alongside `sf apex run test` and Flow tests), verify exact subcommand syntax via `sf logic test --help` before wiring into pipelines.
   - Pair `--test-level RunRelevantTests` with `@IsTest(testFor=...)` and `@IsTest(isCritical=true)` on Apex tests to cut CI wall-clock time without sacrificing release safety.
   - Maintain per-component >= 75% coverage for any `RunSpecifiedTests` gate.
5. **Agentforce & LWC CI Checks**:
   - LWC unit tests (`npm test` / Jest) — author via `salesforce-lwc`.
   - Agent Script compile/validate (`sf agent validate authoring-bundle`) and sandbox Testing Center suites — author/run via `agentforce-build` and `agentforce-test`.
6. **Gated Production Promotion & Audit**:
   - Require manual approval gate in CI (GitHub Environments / DevOps Center approval) before running `sf project deploy quick` or `sf package install` against production.
   - Archive validation report, quick-deploy report (`<quick-deploy-id>.json`), Code Analyzer SARIF, and test JUnit results as CI artifacts.
   - Maintain a documented rollback plan (prior 2GP version notes, feature flags/Custom Metadata kill switches, Flow version deactivation, or reverse Git commit — noting that managed package downgrades are not supported).
