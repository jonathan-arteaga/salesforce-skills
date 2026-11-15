---
name: |-
  regulated-industry-agents-review
description: |-
  Review a named Agentforce agent for regulated-industry safeguards. Return evidence-backed control findings. Use agentforce-config-review for a general configuration assessment.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# regulated-industry-agents-review — Regulated-Industry Guardrail Review

Reviews an Agentforce agent against 8 regulated-industry guardrail patterns and<br />reports gaps with severity + evidence. Sibling to `agentforce-config-review`<br />(broad config health) — this skill is the **focused compliance/guardrail pass**.

> **Not legal/compliance advice.** Engineering patterns observed in the field. A<br />customer's actual obligations (HIPAA, GxP, SOX, etc.) govern; confirm with their<br />compliance owner.<br />**Platform-behavior patterns** (P3, P8) are marked and date-stamped (2026-06) —<br />Salesforce may change runtime behavior; re-verify.<br />**Maturity: derived from a single healthcare engagement (N=1).** Strong but not<br />yet validated across verticals — see `## Contributing`.

---

## When This Skill Owns the Task

- "Review/audit this agent for compliance / safety / regulated readiness."
- "Is this agent safe for healthcare / financial services / insurance?"
- A guardrail review of a specific `.agent` file or planner bundle.

Defer to `agentforce-config-review` for a full 8-dimension config-health doc, and<br />to available security review tooling for a deep adversarial pass. No dedicated adversarial-audit companion is bundled; do not claim one ran. Use `agentforce-test` only for its supported behavioral tests, not as a substitute for a full audit.

---

## Inputs

Gather before scoring. If not provided, auto-detect or ask.

| Input | How to get it | Used by |
| --- | --- | --- |
| **Agent file** | `find . -path "*aiAuthoringBundles*" -name "*.agent"` (AgentScript) or `find . -path "*genAiPlannerBundles*"` (classic). If absent: `sf project retrieve start -m "AiAuthoringBundle:<Name>"`. Store as `AGENT_FILE`. | all |
| **Org alias** | ask; needed for trace verification (P6) and permission checks (P4) | P4, P6 |
| **Vertical** | ask: healthcare / life-sciences / finserv / insurance / pharma. Selects the regulatory lens (HIPAA minimum-necessary vs SOX vs GxP). | P2, P4, P5 |
| **Channel(s)** | inspect the bundle for `connection`/`modality`/surface config (telephony, voice, MIAW/chat, CustomerWebClient). | P5 (voice sub-check) |

If an input is unavailable, proceed but mark the dependent checks **N/A** with the reason (don't emit a false GAP).

---

## Step 0 — Scope (run before scoring)

Three scoping actions set applicability gates and prevent false findings.

First, locate the agent file if not already known:

```bash
# AgentScript bundle
find . -path "*aiAuthoringBundles*" -name "*.agent"
# classic planner bundle
find . -path "*genAiPlannerBundles*" -o -path "*genAiPlanners*" -name "*.xml"
# not local? retrieve it
sf project retrieve start -m "AiAuthoringBundle:<AgentName>" -o <org>
```

<b>0a. Read the </b>**`system:`**<b> </b>**`instructions:`**<b> block FIRST.</b>

```bash
# AgentScript: read the system block (everything before the first `config:` / `topic` / `subagent`)
awk '/^(config|topic|subagent|start_agent):/{exit} {print}' <AGENT_FILE>
```

Guardrails live in **three enforcement tiers**, strongest to weakest:

1. **Deterministic constructs** — `run`, `set`, `if`, `transition to`, `available when` (runtime-enforced).
2. **System instructions** — the `system: instructions:` block: global, applies every turn, higher LLM adherence than topic text. Correct home for persona, PHI/"never say" rules, grounding rules.
3. **Topic pipe-text** (`| …`) — per-topic suggestions; lowest adherence; LLM may ignore.

Note which guardrails are enforced at which tier — a guardrail in tier 2 (system) is materially stronger than the same words in tier 3 (pipe-text), and some guardrails (P2 grounding, P5 PHI) *correctly* live in system instructions, not deterministic constructs.

**0b. Enumerate write surfaces.**

```bash
# list every action target in the agent
grep -nE "target:|source:" <AGENT_FILE>
# inspect a flow target for record create/update/delete (write surface)
grep -lE "<recordCreates>|<recordUpdates>|<recordDeletes>" force-app/main/default/flows/<Flow>.flow-meta.xml
# inspect an apex target for DML (write surface)
grep -nE "insert |update |delete |upsert |Database\.(insert|update|delete)" force-app/main/default/classes/<Class>.cls
```

Classify each target as **read** or **write**:

- `flow://` flows with record create/update/delete → **write**
- `apex://` `@InvocableMethod` performing DML → **write**
- query/get/retrieve/search actions → **read**<br />Only **write** actions are in scope for P1 (confirmation gate) and P7 (resolve-before-act). If the agent has no write surfaces, mark P1/P7 **N/A**.

**0c. Set applicability gates** from Inputs/scan:

- No voice/telephony channel → P5 voice sub-check **N/A**.
- No write surfaces → P1, P7 **N/A**.
- No org access / no STDM → P6 uses the fallback (see P6), not an automatic GAP.

---

## Step 1 — Pattern Catalog

For each pattern: the rule, why it's regulatory, an AgentScript recipe, and the review check. Apply only patterns whose Step-0 gate is in scope.

### P1 — Confirmation Gate (preview before any write)

**Rule:** every create/update/delete shows a preview and requires explicit user confirmation before executing; never call the write action before confirmation.<br />**Regulatory:** change control, error prevention, intent confirmation.

```javascript
| Build and display a preview (one field per line), then ask
| "Please review — reply to confirm or make changes."
| Do NOT call {!@actions.create_record} until the user confirms ("yes"/"confirm"/"go ahead").
```

**Check:** every write action (from 0b) is reachable only after preview + confirm. Directly callable in one turn → finding.

### P2 — Grounded Output Only (no hallucination)

**Rule:** display only values returned by an action/query; never invent accounts, numbers, counts, dates, statuses, or financial/clinical figures; safe empty-states.<br />**Regulatory:** a rep acting on fabricated data (credit hold, balance, clinical detail) is a real compliance/patient-safety failure.<br />**Tier note:** this is usually (and correctly) enforced in **system instructions** — check tier 2, not just topic pipe-text.<br />**Check:** anti-fabrication rule present (ideally in `system:`); empty-state doesn't invent; displayed identifiers match what the action wrote (verify via P6). Watch for echoing a *conversation* value as if it were the saved record.

### P3 — Enforcement-Strength of Mandatory Steps *(platform behavior)*

**Rule:** a mandatory compliance step's enforcement tier must match its criticality. Hard-mandatory steps (the P1 gate, identity/eligibility verification, mandated branches) belong in **tier 1 (deterministic)**. The LLM **can skip pipe-text-instructed actions**; ALWAYS/NEVER in prompt text has no runtime force.<br />**Carve-out (prevents false positives):** a step that is *inherently probabilistic* (crisis/intent detection, NL classification) **cannot** be made fully deterministic — do NOT mark it FAIL for living in instructions. Flag as **residual risk**, and check it's at least at tier 2 (system) with a deterministic *fallback/guardrail* where one is feasible.<br />**Check, by tier:** is each mandatory step at the right tier? Deterministic for hard requirements; system-instruction (+ residual-risk note) for inherently-probabilistic ones; topic pipe-text alone for a hard requirement → finding. See `agentscript-flow-control` (Related skills) for the two-phase execution model.

**Worked example — crisis escalation (the carve-out in practice):**

❌ *Before — hard requirement buried in pipe-text (FINDING):*

```javascript
reasoning:
    instructions: ->
        | If the patient expresses self-harm or a medical emergency, ALWAYS stop and
        | transfer to a human agent immediately.
```

The transfer is mandatory but lives in tier-3 pipe-text — the LLM may not act on it. **But** detecting "self-harm/emergency" is inherently probabilistic, so the *detection* can't be made deterministic.

✅ *After — split detection (probabilistic) from the action (deterministic gate):*

```javascript
reasoning:
    instructions: ->
        | Classify the user's message. If it indicates self-harm, crisis, or a medical
        | emergency, call {!@actions.flag_crisis} (sets crisis = True).
    actions:
        flag_crisis: @actions.set_crisis_flag        # detection → sets a variable
            set @variables.crisis = True
    after_reasoning:
        if @variables.crisis == True:                # deterministic: runtime-enforced, LLM cannot skip
            transition to @subagent.human_escalation
```

**Verdict:** ❌-only → **PARTIAL/HIGH** (mandatory action unenforced). ✅ → **PASS** with a *residual-risk* note that detection accuracy itself is LLM-dependent (mitigate with eval tests, not by demanding determinism of the classifier).

### P4 — Least-Privilege Data Scoping

**Rule:** surface only data the user is entitled to — scoped to the running user / owned records / open record; no cross-entity leakage.<br />**Regulatory:** HIPAA minimum-necessary, need-to-know, record sharing.<br />**Check:** queries are user-scoped (`OwnerId = current user`, sharing respected); **verify as the agent's running user, not an admin** (admins bypass sharing via View All — a query that "works" for you may over- or under-return for the real user); "this record" binds to `currentRecordId` (External-visibility), not free-text guessing.

### P5 — Sensitive-Identifier Handling

**Rule:** mask/segment sensitive identifiers; in voice, never read full account/case/invoice numbers or PII aloud.<br />**Regulatory:** PII/PHI exposure; eavesdropping on voice.

```javascript
if @variables.channel == "voice":
    | VOICE: never read full numeric IDs aloud; say "order ending in [last 4]". Read needed digits individually.
```

**Check (voice sub-check only if voice channel — see 0c):** voice path masks; chat path doesn't over-expose PII/PHI.

### P6 — Audit & Traceability

**Rule:** regulated actions must be observable and verified; don't claim success without evidence.<br />**Regulatory:** audit trails, validation evidence (GxP/SOX-style).<br />**How:** use `agentforce-observe` to confirm the action fired (`ACTION_STEP` present), I/O correct, displayed data matches what was written.<br />**STDM-less fallback:** if the org has no Data Cloud/STDM or trace data, do **not** auto-GAP — use `agentforce-observe` "Phase 1-ALT" (test suites + local preview traces) instead, and note the reduced confidence.<br />**Check:** key regulated flows are trace-verified (or Phase-1-ALT verified), not assumed.

### P7 — Resolve-Before-Act

**Rule:** never act on an ambiguous identifier; resolve a name/number to exactly one entity before any write/financial action; multi-match → numbered pick-list, STOP, act only after selection.<br />**Regulatory:** acting on the wrong patient/account is the canonical compliance failure.

```javascript
| Resolve first: 0 -> not found, STOP; 1 -> proceed; 2+ -> numbered pick-list (max 5), STOP this turn.
| NEVER pass a name straight to an action that requires a resolved numeric ID.
```

**Check (write surfaces only — see 0b):** name→ID resolution gates each record-keyed write; multi-match never auto-picks.

### P8 — Regulated-Vocabulary Safety-Classifier Pitfall *(platform behavior, known issue)*

**Symptom:** platform content-safety / prompt-injection classifiers false-positive on legitimate regulated terms (PHARMACY, SCREENING, controlled-substance/clinical words), intermittently refusing benign requests.<br />**Diagnosis:** pull the trace; a transition to a safety topic (`Inappropriate_Content` / `Prompt_Injection`) on an `llmStep` for a benign business utterance, when the same input routes correctly in other sessions, confirms a nondeterministic classifier — not your code.<br />**Fix:** NOT fixable in the `.agent` file (instruction patches can worsen it). Lever is **Einstein Trust Layer** moderation settings (Setup) or a Salesforce escalation with trace evidence.<br />**Check:** regulated vocabulary flagged as a risk; not instruction-patched. This is a **residual risk** note, never a code FAIL.

---

## Step 2 — Scoring

**Verdict states (per pattern):**

| Verdict | Meaning |
| --- | --- |
| **PASS** | Guardrail present and enforced at an appropriate tier. |
| **PARTIAL** | Present but weak (e.g. hard requirement only in pipe-text; gate exists but bypassable). |
| **GAP** | Required for this agent/vertical and absent. |
| **N/A** | Not applicable (gate in 0c: no writes, no voice, etc.). State the reason. |

**Severity (for PARTIAL/GAP findings):**

| Severity | Definition |
| --- | --- |
| CRITICAL | Must fix before go-live. Patient-safety, legal, or regulated-data risk. |
| HIGH | Significant compliance/operational risk. Fix before go-live if possible. |
| MEDIUM | Improvement recommended; acceptable for launch with a remediation plan. |
| LOW | Nice to have; low impact if deferred. |

**Mitigating factors lower severity (don't over-report):**

- A risk already covered by **Einstein Trust Layer** or org config → PASS or note, not a finding.
- An **inherently probabilistic** step (P3 carve-out) → residual risk, not FAIL.
- A write whose blast radius is benign/easily reversible → P1 may be PARTIAL, not CRITICAL.

**Verify before reporting:** before calling a PARTIAL/GAP, read the actual construct (and the `system:` block + the deterministic blocks) to confirm the guardrail truly isn't there at any tier. An adversarial confirm pass cuts false positives.

---

## Step 3 — Output

Produce a verdict table, per-pattern evidence, and a remediation summary.

**Verdict table:**

```javascript
| Pattern | Verdict | Severity | Evidence (file:line) |
|---------|---------|----------|----------------------|
| P1 Confirmation Gate      | PARTIAL | HIGH | create_case callable pre-confirm — MyAgent.agent:912 |
| P2 Grounded Output        | PASS    | —    | grounding rule in system: — MyAgent.agent:44 |
| P5 Sensitive Identifiers  | N/A     | —    | no voice channel |
| ...                       |         |      | |
```

**Per-pattern evidence:** for each PARTIAL/GAP — what's wrong, the file:line, the enforcement tier found vs. needed, and the recommended fix (with the recipe).

**Priority Remediation Summary:** CRITICAL first, then HIGH go-live blockers: `# | Pattern | Finding | Severity`.

Default output: a Markdown report (`regulated-industry-review-[AgentName]-[Date].md`). If a branded .docx is wanted, defer to `agentforce-config-review`'s document generator.

---

## Related skills

| Skill | Why |
| --- | --- |
| `agentforce-generate` | authoring/fixing the `.agent` file (apply the recipes) |
| `agentforce-observe` | P6 execution — trace verification + Phase-1-ALT fallback |
| `agentforce-test` | regression-test confirmed guardrails |
| `agentforce-config-review` | broad 8-dimension config health (this skill is the focused compliance subset); **invokes this skill from its Step 2b when the agent serves a regulated industry**, and reuse its .docx generator for a branded doc — see `## Integration` |
| `agentforce-test` | Supported behavioral/security test cases; a full adversarial audit remains a separate, explicitly scoped review. |
| `agentscript-flow-control` | two-phase execution model behind P3's tier logic. **If not installed in your environment, the model is summarized inline in Step 0a — P3 does not depend on the external file.** |

---

## Integration with agentforce-config-review

When run **standalone**, emit the Step-3 Markdown report.

When invoked by **`agentforce-config-review`**<b> (its Step 2b)</b> for a regulated agent,<br />return findings in the shape config-review folds into its findings JSON / branded doc —<br />as one supplemental section (excluded from the composite score, full severity into<br />Priority Remediation):

```json
{ "number": <next-after-dimensions>, "title": "Regulated-Industry Guardrails",
  "score": <1-10>,
  "passes":   [ {"label": "P2  Grounded Output", "text": "grounding rule in system: (MyAgent.agent:44)"} ],
  "findings": [ {"severity": "HIGH", "label": "P1  Confirmation Gate",
                 "text": "create_case callable pre-confirm (MyAgent.agent:912)"} ],
  "fixes":    [ "Gate create_case behind preview + explicit confirm (see P1 recipe)" ] }
```

Verdict → doc mapping: **GAP/PARTIAL → finding** (at severity); **PASS → pass**; **N/A → omit**.<br />Use the same severity vocabulary (CRITICAL/HIGH/MEDIUM/LOW). Reuse config-review's<br />existing context (agent file, org, industry, channel) — do not re-ask.

---

## Contributing

Given N=1 maturity, this catalog is meant to grow:

- **New pattern (P9+):** add under Step 1 with rule / regulatory rationale / recipe / review check, and a verdict row + applicability gate.
- **Per-vertical sub-checks:** add vertical-specific specializations (e.g. HIPAA minimum-necessary detail under P4 for healthcare; SOX segregation-of-duties under P1 for finserv) keyed off the `vertical` input.
- Date-stamp platform-behavior patterns (P3, P8) on each review; re-verify against current runtime.
