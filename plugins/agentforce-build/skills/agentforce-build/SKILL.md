---
name: agentforce-build
description: "Build, edit, ground, and compile Agentforce agents with Agent Script, aiAuthoringBundle metadata, Data Libraries, custom retrievers, and Prompt Builder templates. Use agentforce-design for specs, agentforce-review for read-only audits, or agentforce-test for test suites."
---

# Agentforce Build

Author, repair, compile, ground, and package Salesforce Agentforce implementations: Agent Script `aiAuthoringBundle` metadata, subagent transitions and actions, Data Libraries and custom retrievers, and versioned Prompt Builder templates.

## Mode & Reference Routing

Select only the reference(s) needed for the active build task and skip unrelated tracks:

| Task / Mode | Load Reference |
| --- | --- |
| Agent Script DSL, `aiAuthoringBundle` pairing, local SDK compilation, preview, and publish lifecycle | [agent-script-bundle.md](references/agent-script-bundle.md) |
| Subagents, transitions, `before_reasoning`/`after_reasoning` hooks, system overrides, and action wiring | [topics-actions-overrides.md](references/topics-actions-overrides.md) |
| Agentforce Data Libraries, Knowledge/file indexing, custom retrievers, and retrieval troubleshooting | [grounding-retrievers.md](references/grounding-retrievers.md) |
| Prompt Builder template authoring, grounding inputs, version comparisons, and immutable activation | [prompt-templates.md](references/prompt-templates.md) |

## Core 2026 Invariants

- **Agent Script is a dedicated DSL:** Never confuse Agent Script with AppleScript, JS, or Python. Under `aiAuthoringBundles/<ApiName>/`, keep the exact case-sensitive pair `<ApiName>.agent` and `<ApiName>.bundle-meta.xml` (never literal `bundle-meta.xml`), 4-space indentation, and zero nested `if` blocks.
- **Deterministic vs. reasoning boundary:** Use runtime predicates (`if`, `run`, `set`, `transition to`, `available when`) for mandatory gates and transitions. Prompt words (`STOP`, `ALWAYS`, numbered lists inside pipe text) are non-binding instructions; a model cannot read stored variables unless interpolated via `{!@variables.X}`.
- **Subagent overrides & lifecycle hooks:** A subagent `system` block **replaces** global `system.instructions` rather than appending—audit every override for dropped persona/compliance rules. `after_reasoning` runs per turn after reasoning, is **skipped** if the subagent transitions away mid-execution, and is unsupported with `EinsteinHyperClassifier`; never treat it as a guaranteed commit hook.
- **Grounding & retriever limits:** Separate source quality, indexing, retrieval, action binding, and answer generation. For Answer Questions with Knowledge, custom retrievers support **static prefilters** only—never assume dynamic per-user filtering or treat relevance filtering as authorization.
- **Immutable Prompt Builder versions:** Any prompt template version that was ever activated remains permanently immutable even after deactivation—create a new version to revise it. Einstein Trust Layer LLM masking is disabled for agents (including prompt templates invoked as agent actions).
- **Minimalist architecture:** Start in `start_agent` without mutable state; add subagents or state variables only for named deterministic consumers. Verify `runtime.reset_to_initial_node` multi-turn behavior with a two-turn preview trace.

## Hard Org & Safety Gates

- **Verify target org & `--json`:** Before any org command, run `sf config get target-org --json`. Always pass `--json` on `sf` CLI calls; read JSON directly without piping through `jq` or hiding stderr.
- **Draft-first lifecycle & explicit publish/activation gate:** Edit, compile locally, deploy draft, and preview freely within authorized scope. **NEVER publish an agent bundle or activate a Prompt Builder version without explicit user approval** confirming release readiness and target org.
- **Action stubs & live execution:** Default new action implementations to `NEEDS STUB` until the user approves scanning/generating Apex, Flow, or Prompt code. Use `--simulate-actions` by default; require explicit approval plus non-production sandbox confirmation before `--use-live-actions`, live DML, or deleting/renaming agents.
- **Execution identity & authorization:** Enforce record/field authorization in backing Apex/Flow/APIs—never rely on prompts, context Contact IDs, or topic filters. Never delete/recreate a production Data Library as a retry.

## Verification Integrity & Scripts

Run bundled scripts as black-box tools (pass `--help` for flags; do not rewrite them mid-task):

- **Local Agent Script compile/index (always run first):** `node scripts/index-agent.mjs <path/to/Agent.agent>` (and `node scripts/setup-agentscript-sdk.mjs` if SDK setup is needed). Fix all severity-1 diagnostics before org validation; report compiler version/commit or explicitly state **compiler not used**.
- **Discovery & scaffolding:** `python3 scripts/discover.py --help`, `python3 scripts/org_describe.py --help`, `python3 scripts/scaffold.py --help`, `python3 scripts/upgrade-legacy-nga-analyze.py --help`.
- **Evidence separation:** Local compilation does not validate `<ApiName>.bundle-meta.xml`, org permissions, retrieval freshness, or live side effects. Report local compile, org validation, preview traces, and untested production behavior separately.

## Delegate Outside Build

- **Architecture, persona, dialogue, Voice UX & TDDs:** `agentforce-design`
- **Read-only metadata snapshots, config & compliance audits:** `agentforce-review`
- **Testing Center suites, escalation plans & security probes:** `agentforce-test`
- **Production session traces:** `agentforce-observe`
- **Deep Apex, Flow, LWC, integrations, RBAC & CI/CD:** `salesforce-apex`, `salesforce-flow`, `salesforce-lwc`, `salesforce-integrations`, `salesforce-security-access`, `salesforce-devops-deploy`
