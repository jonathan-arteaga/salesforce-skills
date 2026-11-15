---
name: |-
  agentforce-config-review
description: |-
  Review Agentforce configuration and scoped permission evidence. Return a scored assessment and prioritized improvements. Use agentforce-generate to edit Agent Script.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# agentforce-config-review: Agentforce Configuration Review Skill

Use available metadata for a static review when the Salesforce connection is unavailable. Identify which permission or runtime checks require the org.

Use this skill when a user provides Agentforce agent configuration metadata and wants a structured review document produced.

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## When This Skill Owns the Task

- User pastes topic instructions, actions, variables, or agent role/description
- User asks for a "config review", "agent audit", "health check", or "review doc"
- User wants to assess readiness before go-live
- User wants findings formatted as a branded Word document

Delegate elsewhere when:

- Building or editing agent metadata → `agentforce-generate`
- Health check, pitfall audit, or audit-fix-evaluate loop on a `.agent` file, with no Word deliverable → `agentforce-generate` (Audit and Repair)
- Functional test cases → `agentforce-test`
- Red-teaming / adversarial probes → `agentforce-test`
- Observability / session analysis → `agentforce-observe`

---

## Keep findings and document generation manageable

Record evidence and remediation in compact findings. Use the existing score and permissions checks. Complete the verified findings JSON before building the report. Use an available document authoring capability or render the same structure locally with Python and python-docx. If file output is unavailable, provide the structured findings and identify the missing capability.

**D8 execution gate for Service and SDR agents**

1. Check the agent type confirmed in Step 1.
2. **Service Agent or SDR agent → D8 is REQUIRED.** Run D8 sub-sections A–F before moving to Step 3 (Scores).
   - Running user identified in Step 1 → proceed directly to Section B.
   - Running user NOT identified and org is connected → run Section A (query the org) now. Do NOT skip D8 because the running user was not pre-supplied in context.
   - Org not connected and no metadata available → set `permissions.status = "NOT_RUN"`, populate `not_run_reason`, and flag it explicitly in the scorecard. Do not silently omit D8.
3. **Employee Agent, Field Service Agent, or AgentScript Agent → D8 does not apply.** Set `permissions.status = "NOT_RUN"` with reason `"D8 does not apply to this agent type"`.
4. **"Supplemental" means excluded from composite score — it does NOT mean optional for Service or SDR agents.**

**Voice agents (`isVoiceAgent: true`) require triage and a D8a table.**

- **Triage first:** Before writing any finding, run a silent PASS/CHECK/N/A scan across all voice checks using only metadata (no prose). Only CHECK items advance to finding write-up. PASS items become a single "Voice channel baseline verified" bullet. This is mandatory — do not skip.
- **D8a is a binary table, not prose:** Output D8a as a pass/fail table directly into the JSON (`"d8a_checklist": [{"check": "...", "result": "PASS|FAIL|N/A", "note": "..."}]`). No narrative analysis. Fails in D8a escalate to a finding in the nearest relevant dimension (D2 for timeouts/retries, D3 for consent/PCI, D7 for logging).
- **D7 voice additions split by validatability:** Label each D7 voice finding as `[METADATA]` (can be confirmed from config) or `[REQUIRES LIVE TEST CALL]` (can only be confirmed by placing a call and querying VoiceCall records). Do not mark `[REQUIRES LIVE TEST CALL]` items as PASS — mark them as `[UNVERIFIED]` with a recommendation to validate.

---

## Step 1 — Gather Context

Consult [`references/step-1-gather-context.md`](references/step-1-gather-context.md) before Step 1.

## Step 1b — Run the Static Check Scan

Consult [`references/step-1b-static-check-scan.md`](references/step-1b-static-check-scan.md) before Step 1b.

## Prepare the evidence for the report

Complete and verify the findings JSON before document generation. Follow the report instructions and keep any unverified checks explicit.

## Step 2 — Run the 7 Analysis Dimensions

Consult [`references/step-2-dimensions-1-7.md`](references/step-2-dimensions-1-7.md) before Step 2.

## Dimension 8 — Permissions, Identity & Access Control

Consult [`references/dimension-8-permissions.md`](references/dimension-8-permissions.md) before running Dimension 8.

## Dimension 9 — Cost & Consumption Efficiency

Consult [`references/dimension-9-cost.md`](references/dimension-9-cost.md) before running Dimension 9.

## Step 2b — Regulated-Industry Guardrail Review (conditional)

Consult [`references/step-2b-regulated-industry.md`](references/step-2b-regulated-industry.md) before Step 2b (regulated-industry agents).

## Step 3 — Score Each Dimension

Consult [`references/steps-3-4-score-remediate-kpi-json.md`](references/steps-3-4-score-remediate-kpi-json.md) before Step 3. Covers: Step 4 — Build Priority Remediation Summary; Step 4b — Generate KPI / Success Criteria; Step 4a — Serialize Findings to JSON.

## Step 5 — Optional: Generate Garak Adversarial Test Cases

Consult [`references/step-5-garak-tests.md`](references/step-5-garak-tests.md) before Step 5 (only if the user opts in).

## Step 6 — Produce the Word Document

Consult [`references/step-6-word-document.md`](references/step-6-word-document.md) before Step 6.

## Agent-Type KPI Defaults

Consult [`references/agent-type-kpi-defaults.md`](references/agent-type-kpi-defaults.md) before Step 4b.

## AgentScript Variant

Consult [`references/agentscript-variant.md`](references/agentscript-variant.md) before Step 1 when the agent is an AgentScript (`.agent`) agent.

## Agent-Type Adaptations

The 7 review dimensions apply to all agent types. Adapt the specific checks per type:

| Agent Type | Dimension 2 focus | Dimension 3 extras | Dimension 6 extras | Dimension 7 extras |
| --- | --- | --- | --- | --- |
| SDR / Sales | Topic instruction quality, action sequencing | Competitor handling, CASL opt-out, bilingual (if Canada) | Data residency for LLM calls | Activity logging, email retry handling |
| Service Agent | Topic instruction quality, action sequencing | Escalation to human, case creation guardrails | Zero-retention + field minimization (masking is disabled for agents) | Case logging, CSAT triggers |
| Field Service | Topic instruction quality, action sequencing | No commitments on SLAs/technician timing | Work order data residency | Work order write-back, asset logging |
| Employee Agent | Topic instruction quality, action sequencing | No HR/legal advice guardrails | Internal data classification | Audit trail for HR/Finance actions |
| General / Custom | Topic instruction quality, action sequencing | Scope creep guardrails | Applicable regional law | Logging coverage for agent actions |
| **AgentScript** | **Branch completeness, dead ends, action output handling — see AgentScript Variant section** | Hardcoded SLAs/contacts, escalation gatekeeping, dead-end frustration | Same as agent use case; LLM surface area is lower | Script step error rate, transfer fallback, unreachable step cleanup |
| **Voice (channel modifier)** | <b>Triage gate first; D8a as binary table; D7 split by \[METADATA\] vs \[REQUIRES LIVE TEST CALL\] — see </b>[**agent-type-variants.md**](references/agent-type-variants.md)<b> Voice section</b> | Verbal abuse, crisis language, PCI voice ban, TCPA (outbound only), TTY/TDD; ETL covers injection/persona/leakage — check ETL topic enablement, not topic instructions; Check actual recording configuration; supported Real-Time Streaming setups can record the agent call leg, so recording notice/consent is not automatically N/A | Transcript PII masking (if transcript stored), sensitive data not read aloud by TTS | VoiceCall record creation, CTI adapter health, transcript sync |

---

## Severity Definitions

| Severity | Definition |
| --- | --- |
| CRITICAL | Must fix before go-live. Brand, legal, compliance, or data risk. |
| HIGH | Significant operational or quality risk. Fix before go-live if possible. |
| MEDIUM | Improvement recommended. Acceptable for initial launch with a remediation plan. |
| LOW | Nice to have. Low impact if deferred. |

---

## Output File

Output path: `[OUTPUT_DIR]/agentforce-config-review-[AgentName]-[Date].docx`, where `[OUTPUT_DIR]` is the directory captured in Step 1 and defaults to `~/Downloads` when the user does not specify one. Always include the agent name and date in the filename.

---

## References

- Builder scripts: written to `[OUTPUT_DIR]` — `build_review_doc.py` + `build_review_s1s3.py` + `build_review_s4s7.py` + `build_review_s8.py` + `build_review_s9.py` (`[OUTPUT_DIR]` defaults to `~/Downloads` — see Step 1)
- Prior review example: `[OUTPUT_DIR]/[Customer] - SDR Agent Review.docx`
- Analysis prompt template: `references/review-prompt.md`
- Agent-type variant checks: `references/agent-type-variants.md`
- Garak scoped probe library: `references/garak-scoped-probes.md`
- Static check catalog: `references/static-checks.md`
- Memory: `project_agentforce_config_review_template.md`
- Related skills: `agentforce-generate`, `agentforce-test`, `agentforce-observe`
