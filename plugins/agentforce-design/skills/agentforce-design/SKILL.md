---
name: agentforce-design
description: "Design Agentforce architecture, subagent authority, persona contracts, starter dialogues, Voice UX, and HTML technical design docs. Use salesforce-discovery for workshops, agentforce-build for Agent Script, agentforce-review for org audits, or agentforce-test for suites."
---

# Agentforce Design

Own design-time Agentforce artifacts: subagent architecture and authority boundaries, character personas, bounded starter dialogues, Voice UX adaptations, and customer-facing HTML technical design documents (TDDs). Keep design strictly separate from org implementation and runtime testing.

## Mode & Reference Routing

Select only the reference(s) needed for the active task and skip unrelated tracks:

| Task / Mode | Load Reference |
| --- | --- |
| Greenfield, redesign, channel-overlay, or script-comparison architecture and action authority | [architecture-authority.md](references/architecture-authority.md) |
| Persona drafting, 14 dimensions, technical framing, scoring, and `persona-handoff.json` | [persona-calibration.md](references/persona-calibration.md) |
| Three-scenario starter dialogues (happy path, error state, fallback) and CD1-CD6 checks | [conversation-design.md](references/conversation-design.md) |
| Chat-to-voice migration, `modality voice:` tuning, vocal casting, recording, and latency budgets | [voice-ux.md](references/voice-ux.md) |
| Customer-facing 10-section HTML Technical Design Document with Mermaid diagrams | [technical-design-doc.md](references/technical-design-doc.md) |

## Core 2026 Invariants

- **Hybrid Reasoning model:** Design for Agentforce Builder, Agent Script, Agent Graph, and the Atlas Reasoning Engine. Separate probabilistic reasoning (intent, recovery, phrasing) from deterministic control (prerequisites, transitions, eligibility, writes). Start with one execution block; add subagents only for distinct objectives, tools, authority, or handoffs.
- **Three-way deliverable boundary:** Separate **persona** (WHO the agent is and lexical Tone Flex), **task instructions** (goals, grounding, clarification), and **enforced controls** (authorization, prerequisites, side effects in Apex/Flow/Agent Script). Persona never encodes `.agent` syntax, guardrails, or platform voice settings.
- **Persona technical framing:** Specify Reading Level Flex separately from Technical Explanation Policy (`Stay in frame`, `Selective bridge` default, or `Pair routinely`). Never let confident wording imply verified facts or completed actions.
- **Voice UX & telephony constraints:** Map completed personas into spoken delivery (`modality voice:`, casting, prosody, pronunciation, STT bias) without redefining character contracts. Treat latency by sequential LLM pass count plus three-layer fillers (`beepboop_config` 500ms default override, `outbound_filler_sentences`, per-action `progress_indicator_message`).
- **Voice recording & language caveats:** Supported Real-Time Streaming configurations can record agent calls; always check Record Voice Calls with Agents, per-agent Flow overrides, and participant notice/consent—never auto-mark recording N/A. Current voice guidance is monolingual on the configured default language; text Allowed Languages does not prove multilingual voice.
- **Honest gating:** Never fabricate action IDs, component slugs, continuity rationales, or transcript verdicts when upstream artifacts (`actions.yaml`, visual specs, traces) are absent; leave gated fields empty and flag `[inferred]` or `[review needed]`.

## Hard Org & Safety Gates

- **Design-only posture:** Never deploy metadata, mutate orgs, publish/activate agents, or edit `.agent` bundles directly—hand approved design artifacts (`architecture.json`, `persona-handoff.json`, `decision-points.yaml`, voice rewrite bundle) to `agentforce-build`.
- **Execution identity & access:** Document actual execution context (logged-in user for Employee Agents; Agent User or verified site user for Service Agents). A Contact ID in context never enforces record access; require backing Apex/Flow authorization for every sensitive action.
- **Zero internal leakage in customer TDDs:** Omit internal Salesforce metadata jargon (`InternalCopilot`, `ExternalCopilot`, `GenAiPlanner`, `isUsedByPlanner`, `ReAct Planner`) and internal file paths from customer-facing HTML TDDs.

## Verification Integrity & Scripts

Run bundled scripts as black-box validators (pass `--help` if unsure of flags; do not rewrite them mid-task):

- **Persona contract lint:** `python3 scripts/lint_persona.py <path/to/persona.md> [--json]` — resolve all deterministic errors before exiting DRAFT/SCORE; confirm warnings consciously.
- **Voice pattern catalog lint:** `python3 scripts/lint-patterns.py <patterns-dir> [--references-dir references]` — validates custom Voice UX pattern files against schema and citation IDs.
- Label design outputs `draft` until stakeholder sign-off; separate static lint checks from org compilation (`agentforce-build`) and live test calls or suites (`agentforce-test`). Static voice specs never prove live barge-in, ASR accuracy, latency, or recording behavior.

## Delegate Outside Design

- **Discovery & workshops:** `salesforce-discovery`
- **Agent Script, grounding & prompts:** `agentforce-build` (plus `salesforce-apex`, `salesforce-flow`, `salesforce-integrations`)
- **Deployed metadata inspection & audits:** `agentforce-review`
- **Test suites, escalation plans & voice checks:** `agentforce-test`
- **Production traces & telemetry:** `agentforce-observe`
- **RBAC, security & rollout:** `salesforce-security-access`, `salesforce-devops-deploy`
