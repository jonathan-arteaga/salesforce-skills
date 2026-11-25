# Structured Agent Improvement Loop

Coordinate repeatable agent improvement cycles (`REVIEW -> PLAN -> [gated IMPLEMENT -> TEST -> EVALUATE] -> RE-REVIEW -> COMPLETE`) with pinned org identity, stable finding IDs, and strict authorization boundaries.

## Read-Only Default vs. Authorized Full Ownership

- **Plan Only *(default in `agentforce-review`)*:** Run Run Identity, Pre-Flight checks, `REVIEW`, and `PLAN`, then stop and hand back a prioritized remediation plan with exact finding IDs (`D<dim>-<SEV><n>`, e.g., `D3-H1`) and batch order. Zero org mutations, zero Flex Credit burn, zero git changes.
- **Full Ownership *(opt-in only)*:** Requires explicit user authorization for the bounded target org, agent, and consent flags (`deploy`, `gitCommit`, `gitRevert`—all OFF by default; detection never equals consent). Delegate code edits to `agentforce-build`, test execution to `agentforce-test`, and deployment to `salesforce-devops-deploy`.

## Run Identity, Org Pinning & State Hygiene

1. **Pin identity every run (including `--resume`):** Resolve `$PROJECT_ROOT` and exact target `$ORG_USERNAME` + 15/18-char `OrgId` before reading state. Never rely on a mutable CLI alias or silently adopt an org from a saved state file.
2. **State file contract:** Store state atomically at `$PROJECT_ROOT/.agent-improvement/loop-state-<AgentName>__<OrgId>.json`. Validate project, org ID, and agent name on every read; archive corrupt files (`*.corrupt`) rather than silently deleting them.
3. **Contained scratch files:** Confine any phase helper scripts or temp artifacts under `$PROJECT_ROOT/.agent-improvement/tmp/` with descriptive `<phase>-<AgentName>-<purpose>.<ext>` names. Sweep stale `tmp/` aside at run start and `COMPLETE`. Keep versioned deliverables (`<date>` suffix) outside `tmp/` so history accumulates instead of clobbering.

## Consumed Contracts & Delegation Boundaries

Validate minimal required fields immediately when a delegated skill returns; halt on missing required fields (except optional persona rubric, which degrades gracefully):

- **Config Review findings JSON:** Agent metadata, dimension scores, finding IDs, severities, and D8 status.
- **Test Results JSON (from `agentforce-test`):** Agent version, execution mode (`simulated` vs. `live`), pass rate, and per-case failures.
- **Persona Evaluation (from `agentforce-design`):** Score and top character gaps when persona calibration is in scope.

## Iteration Caps, Regression Safety & Error Recovery

- **Dual loop limits:** Cap per-batch fix retries at **3 attempts** (skip batch after 3 regressions) independently of `--max-iterations` (default **3** full `REVIEW -> EVALUATE` cycles).
- **Keep working tree and org in sync:** If a batch regresses and `gitRevert` is explicitly authorized, revert the batch's edited/added files AND redeploy the clean baseline before marking the regression handled. If revert is declined, halt and warn that both local files and the target org still contain the regressed change.
- **Auth & tool failures:** On expired org auth, pause and instruct re-authentication (`sf org login web`); never loop silently on failed deploys or timed-out test sessions.
