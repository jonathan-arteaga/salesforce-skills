# AgentScript Variant

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- AgentScript Variant
  - Step 1 — Metadata to request (AgentScript)
  - Dimension 1 — Persona, Tone & Topic Scope (AgentScript overrides)
  - Dimension 2 — Script Structure, Branch Completeness & Fallback (replaces Instructions/Actions)
  - Dimension 3 — Guardrails & Responsible AI (AgentScript overrides)
  - Dimension 4 — Variable Typing & Data Integrity (AgentScript additions)
  - Dimension 5 — Knowledge Grounding (AgentScript overrides)
  - Dimensions 6 & 7 — Unchanged
  - AgentScript-specific findings to always check

## AgentScript Variant

AgentScript agents (`isScriptCompatibleAgent: true`) use a deterministic DSL instead of a ReAct planner. The review dimensions are the same but the checks, metadata sources, and failure modes differ significantly. Apply the overrides below instead of the standard checks whenever the retrieved metadata contains `.agentScript-meta.xml` files or the botVersion indicates `isScriptCompatibleAgent: true`.

### Step 1 — Metadata to request (AgentScript)

In addition to the standard bot/botVersion XML, request:

| File | Path | Why |
|---|---|---|
| AgentScript definition | `agentScripts/[Name].agentScript-meta.xml` | Primary review input — contains all steps, branches, conditions |
| AgentScript version | `agentScripts/[Name]/[version].agentScriptVersion-meta.xml` | The active version's step tree |
| GenAiFunction (actions) | `genAiFunctions/` | Action definitions called from script steps |
| GenAiPlugin (topics) | `genAiPlugins/` | Any hybrid topics if the script delegates to a planner mid-flow |

Do **not** request `GenAiPlannerBundle` — AgentScript agents do not use a planner.

### Dimension 1 — Persona, Tone & Topic Scope (AgentScript overrides)

Replace topic-routing checks with script-scope checks:
- Is the script's entry condition scoped to the correct use case? Can it be triggered by off-scope inputs?
- Does the script's opening message accurately set expectations for what the agent can and cannot do?
- Is tone consistent across all message steps? Flag casual/formal mismatches across branches.
- Are there any message steps that imply autonomous capability the agent does not have?

### Dimension 2 — Script Structure, Branch Completeness & Fallback (replaces Instructions/Actions)

This is the most important dimension for AgentScript. Check every node type:

**Conditional / Decision steps:**
- Is there a default/else branch on every conditional? A missing else branch creates a dead end.
- Are all condition values exhaustive? (e.g., if branching on a picklist, does every picklist value have a path?)
- Are nested conditions at risk of combinatorial dead ends?

**Message steps:**
- Do message steps that contain LLM-generated text have a guardrail or template constraint?
- Are any message steps hardcoding data (SLAs, URLs, phone numbers) that should come from a variable or action?

**Action steps:**
- Is every action call followed by an output-check step or conditional that handles failure?
- Are action outputs used correctly downstream — right variable, right type?
- Is there a maximum retry or timeout instruction for slow-running actions?

**Transfer steps:**
- Does every script path that reaches a human-transfer step have a valid queue or flow target?
- Is there a fallback if the transfer fails (queue full, outside hours)?

**Terminal steps:**
- Does every path end in either a transfer, case creation, or close step?
- Are there any paths that end in a message step with no subsequent step — effective dead ends?

**Overall:**
- Map all paths from entry to terminal. Flag any path longer than 15 steps as complexity risk.
- Count unreachable steps — steps that no conditional path leads to.
- **Script size ceilings (mechanical — see AF-REL-16 / AF-REL-17 in `references/static-checks.md`):** `wc -l` the active `.agentScript-meta.xml` / `.agentScriptVersion-meta.xml` and size the compiled bundle. Flag a script exceeding **~20,000 lines** (AF-REL-16, HIGH) or a bundle exceeding **~20 MB** (AF-REL-17, HIGH). Past these ceilings compiles slow sharply, the Builder editor and Metadata API retrieve/deploy become unreliable or time out, and the whole bundle taxes every call's context. Treat as a signal to refactor into subagents, not a style note.

### Dimension 3 — Guardrails & Responsible AI (AgentScript overrides)

AgentScript agents have lower LLM autonomy, so some OWASP checks are lower risk. Adjust:

| Check | AgentScript risk | Notes |
|---|---|---|
| Prompt injection (LLM01) | MEDIUM (lower) | Script controls flow; LLM only generates text in message steps, if any |
| Config leakage (LLM06) | LOW-MEDIUM | Script is deterministic; less system prompt surface area |
| Persona hijack (LLM01) | LOW | Fixed script path; user cannot redirect the agent |
| Hardcoded SLA/commitments | HIGH (new) | Message steps commonly hardcode SLAs, hours, phone numbers — these rot |
| Dead-end frustration risk | HIGH (new) | A user reaching a dead end with no exit path is a brand and retention risk |
| Escalation gatekeeping | HIGH (new) | If script blocks human request until specific branch reached, flag as compliance risk |

Still check: Einstein Trust Layer, opt-out handling, bilingual support, legal/regulatory routing.

### Dimension 4 — Variable Typing & Data Integrity (AgentScript additions)

In addition to standard checks:
- Are variables populated in earlier steps before they are referenced in later steps? Flag out-of-order references.
- Are variables used in conditional branches typed correctly for the comparison (e.g., Number not Text for numeric comparisons)?
- Are context variables bound at the script level or only at the topic level? Confirm scope.

### Dimension 5 — Knowledge Grounding (AgentScript overrides)

AgentScript agents are deterministic by default. Grounding risk is scoped to:
- Message steps that use LLM-generated text — do these have knowledge action calls before them?
- Any hybrid delegation steps that call a GenAiPlugin topic mid-script — apply full D5 checks to those topics.
- If the script has no LLM message steps and no topic delegation, mark D5 as N/A and score 8/10 with a note.

### Dimensions 6 & 7 — Unchanged

Data residency, AI governance, CRM integration, logging, and error handling checks apply identically.

### AgentScript-specific findings to always check

| # | Check | Severity if failing |
|---|---|---|
| 1 | Every conditional has a default/else branch | CRITICAL |
| 2 | Every action step has an output-handling step | HIGH |
| 3 | Every terminal path ends in transfer, case, or close | HIGH |
| 4 | No hardcoded SLAs, phone numbers, or URLs in message steps | MEDIUM |
| 5 | Unreachable steps identified and removed | MEDIUM |
| 6 | Script path length ≤15 steps for primary flows | LOW |
| 7 | Transfer steps have fallback for queue-full / out-of-hours | HIGH |
| 8 | Script ≤ ~20,000 lines (AF-REL-16) | HIGH |
| 9 | Compiled bundle ≤ ~20 MB (AF-REL-17) | HIGH |

---
