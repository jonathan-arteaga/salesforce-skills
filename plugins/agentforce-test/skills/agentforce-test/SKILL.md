---
name: agentforce-test
description: "Author, run, and evaluate Agentforce test suites, preview smoke checks, OWASP security probes, and routing-derived escalation scenarios. Use agentforce-build for script edits, agentforce-review for static audits, or agentforce-observe for production trace analysis."
---

# Agentforce Test

Author, execute, and evaluate Agentforce test coverage across ad-hoc preview smoke checks, Testing Center batch suites (`sf agent test`), OWASP LLM Top 10 security probes, direct Flow/Apex action isolation, and routing-derived Omni-Channel escalation scenarios.

## Mode & Reference Routing

Select only the reference(s) needed for the active testing mode and skip unrelated tracks:

| Task / Mode | Load Reference |
| --- | --- |
| Testing Center YAML spec authoring, grounding/auth regressions, and OWASP security suites | [test-suite-authoring.md](references/test-suite-authoring.md) |
| Routing-derived escalation & handoff scenarios from `.agent` + Omni-Channel/Queue/BusinessHours metadata | [escalation-handoff-scenarios.md](references/escalation-handoff-scenarios.md) |
| `sf agent preview`, `sf agent test run`, isolated REST action execution, voice latency & scoring | [execution-evaluation.md](references/execution-evaluation.md) |

## Core 2026 Invariants

- **Testing Center vs. Agent Script naming:** `@salesforce/agents` YAML specs use `expectedTopic` (matching API terminology), which maps 1:1 to `subagent` blocks in `.agent` files. Author YAML directly—never invoke interactive `sf agent generate test-spec` in agentic workflows.
- **CLI version floor:** `sf agent preview start/send/end` with `--simulate-actions` requires `sf` CLI **2.131.0+** (`plugin-agent` 1.32.16+). Pass `--simulate-actions` or `--use-live-actions` on `start` ONLY (`send` and `end` reject it).
- **Mandatory regression dimensions:** Cover routing ambiguity, grounding/abstention, cross-customer authorization denial, duplicate/idempotent action calls, subagent override inheritance, multi-turn continuation, and escalation handoffs.
- **Routing-derived escalation accuracy:** Derive escalation plans from BOTH the `.agent` connection/gating blocks AND live org routing metadata (`Group`, `QueueRoutingConfig`, `ServiceChannel`, `BusinessHours`, Omni-Channel Flows, presence statuses). Standard Agentforce permission sets do NOT grant Omni-Channel object read access.
- **Voice latency & live-call heuristics:** Measure voice turn latency by sequential generative LLM passes (~0.85-1.4s fast model, up to ~2.8s large model, ~1.3s floor) plus three-layer filler timing (`beepboop_config` 500ms, `outbound_filler_sentences`, per-action progress lines). Static suites and text preview never prove voice barge-in, ASR accuracy, silence timeouts, or call recording.

## Hard Org & Safety Gates

- **Sandbox, synthetic data & Flex Credits:** Testing Center and live previews **can mutate CRM data and consume requests/Flex Credits**. Verify non-production status (`SELECT IsSandbox FROM Organization`), use synthetic fixtures only (`test@example.com`, `000-00-0000`), and never assume automatic rollback.
- **Authoring != Execution:** A request to author a test spec or escalation plan does NOT authorize running tests or live actions. Default preview/probing to `--simulate-actions`; require explicit user opt-in before `--use-live-actions`, direct REST DML calls, or generating/running OWASP security probes (Mode C).
- **Org consent & `--json`:** Always verify `sf config get target-org --json`, use `--json` on `sf` CLI calls, and confirm customer data-handling approval before querying live customer routing metadata.

## Verification Integrity

- **Simulated vs. live evidence boundary:** A `--simulate-actions` pass validates reasoning and action selection ONLY—it NEVER proves runtime permissions, CRUD/FLS/sharing enforcement, live DML, external integrations, or human handoff delivery.
- **Record execution provenance:** Every test report MUST record exact target org, agent API name and version, suite filename, execution mode (`simulated` vs. `live`), synthetic fixture set, pass/fail counts, and exit code (`0` pass, `1` failures, `2` critical block, `3` infra error).
- **No fabricated passes:** Missing traces, unexecuted live voice calls, or skipped security categories remain `UNVERIFIED` or `INCONCLUSIVE`, never `PASS`.

## Delegate Outside Testing

- **Architecture, persona, starter dialogues & Voice UX specs:** `agentforce-design`
- **Fixing `.agent` bundles, grounding, or Prompt Builder templates:** `agentforce-build`
- **Read-only metadata snapshots, config & compliance audits:** `agentforce-review`
- **Production session trace & audit telemetry analysis:** `agentforce-observe`
- **Apex unit tests, Flow debugging, RBAC & CI/CD pipelines:** `salesforce-apex`, `salesforce-flow`, `salesforce-security-access`, `salesforce-devops-deploy`
