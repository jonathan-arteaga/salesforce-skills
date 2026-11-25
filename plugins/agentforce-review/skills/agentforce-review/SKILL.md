---
name: agentforce-review
description: "Inspect deployed Agentforce metadata, audit configuration and permissions, check regulated-industry safeguards, and plan improvement loops strictly read-only. Use agentforce-build for edits, agentforce-test for test runs, or agentforce-observe for runtime traces."
---

# Agentforce Review

Perform strictly read-only inspections and audits of Salesforce Agentforce agents: declared metadata architecture snapshots, multi-dimension configuration and permission reviews, regulated-industry guardrail audits, and structured improvement plans.

## Mode & Reference Routing

Select only the reference(s) needed for the active review and skip unrelated tracks:

| Task / Mode | Load Reference |
| --- | --- |
| Deployed metadata tree (`BotDefinition`/`GenAiPlanner*`/`Flow`/`Apex`) and invocation graph pipeline | [metadata-architecture-inspect.md](references/metadata-architecture-inspect.md) |
| 9-dimension configuration health audit, D8 permissions/identity gate, voice triage, and D9 cost | [config-permission-review.md](references/config-permission-review.md) |
| Regulated-industry compliance & guardrail pass (P1-P8: HIPAA, FinServ, GxP, SOX) | [regulated-industry-safeguards.md](references/regulated-industry-safeguards.md) |
| Structured `REVIEW -> PLAN` improvement loop coordination, state contracts, and gated delegation | [improvement-loop.md](references/improvement-loop.md) |

## Core 2026 Invariants

- **Strictly read-only by default:** Never edit `.agent` bundles, deploy metadata, publish/activate versions, commit/revert git branches, or trigger live Flex Credit consumption without explicit scoped authorization—hand authorized edits to `agentforce-build` and test execution to `agentforce-test`.
- **Three enforcement tiers:** Evaluate guardrails by actual runtime strength: Tier 1 deterministic Agent Script (`run`, `set`, `if`, `transition to`, `available when`), Tier 2 global `system.instructions`, and Tier 3 topic pipe-text (`| ...`, non-binding). Never mark inherently probabilistic intent/crisis detection FAIL for living in instructions—flag residual risk and check deterministic downstream gates.
- **D8 permissions gate (Service & SDR agents):** D8 (running user, Apex access, CRUD, FLS, Named Credentials, Permission Set hygiene) is REQUIRED for Service and SDR agents—supplemental means excluded from the composite score, never optional. Verify queries as the running user, not System Administrator.
- **Voice & Trust Layer accuracy:** Supported Real-Time Streaming setups can record agent call legs—never auto-mark recording notice/consent N/A. Einstein Trust Layer LLM masking is disabled for agents; verify field minimization, zero retention, and transcript access controls instead.
- **Deterministic metadata traversal:** The bundled architecture pipeline runs inline via parallel Tooling SOQL + batched Data SOQL + selective Metadata retrieve, normalizing both classic ReAct and NGA planners while surfacing `_unresolved[]` entries and per-branch cycles explicitly.

## Hard Org & Safety Gates

- **Never invent agent names or org state:** When no agent API name is given, discover `BotDefinition` rows via one read-only `sf data query --json` first. Pin orgs by exact username/org ID—never blindly adopt a stale state file's org.
- **Boundary validation:** Always validate CLI inputs (`agent_api_name`, `org_alias`, `WORK_DIR`) through `scripts/_shared/fs_guard.py` before invoking the pipeline; keep raw user prose out of shell commands.
- **No silent omissions:** If org access is unavailable, perform a bounded static review, set `permissions.status = "NOT_RUN"` with `not_run_reason`, and mark live-only checks (such as `[REQUIRES LIVE TEST CALL]` voice checks) `[UNVERIFIED]`.

## Verification Integrity & Scripts

Run bundled metadata scripts as black-box tools (see [metadata-architecture-inspect.md](references/metadata-architecture-inspect.md) for the full pipeline invocation block):

- **Metadata snapshot pipeline:** `python3 scripts/main.py --org-alias <org> --agent <api_name> --work-dir <dir>` followed by `WORK_DIR=<dir> python3 scripts/emit_result.py` (reads declared metadata only; never reads runtime audit tables).
- **Regression self-check (maintenance):** `python3 -m unittest discover -s scripts/tests -t scripts`.
- **Evidence hygiene:** A rubric score is a structured review aid, never a legal compliance or deployment certification. Separate `[METADATA]` findings from `[REQUIRES LIVE TEST CALL]` and runtime trace verification (`agentforce-observe`).

## Delegate Outside Review

- **Greenfield/redesign architecture, persona, Voice UX & TDDs:** `agentforce-design`
- **Applying `.agent`, grounding, or prompt fixes:** `agentforce-build` (plus `salesforce-apex`, `salesforce-flow`)
- **Executing preview smoke tests, Testing Center suites, or escalation tests:** `agentforce-test`
- **Production session trace & audit telemetry analysis:** `agentforce-observe`
- **Permission sets, sharing remediation & CI/CD rollout:** `salesforce-security-access`, `salesforce-devops-deploy`
