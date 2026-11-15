# regulated-industry-agents-review

A focused compliance/guardrail review of any Agentforce agent built for a
regulated vertical (healthcare, life sciences, financial services, insurance,
pharma distribution). Reviews the agent against **8 guardrail patterns (P1–P8)**
and reports `PASS / PARTIAL / GAP / N/A` per pattern with severity and
`file:line` evidence.

Sibling to `agentforce-config-review`: that skill
runs the broad 8-dimension config-health pass; this one is the **focused
compliance subset**. `agentforce-config-review` invokes this skill from its
**Step 2b** when the agent serves a regulated industry.

> **Not legal/compliance advice.** These are engineering patterns observed in the
> field — a customer's actual obligations (HIPAA, GxP, SOX, etc.) govern. Confirm
> with their compliance owner. Platform-behavior patterns (P3, P8) are date-stamped
> and may change; re-verify against current runtime.

---

## How to invoke

Use `$regulated-industry-agents-review` in Codex, then point it at the
agent (or let it auto-detect a local bundle).

Trigger phrases that route here:

- *"Review / audit this agent for compliance / safety / regulated readiness"*
- *"Is this agent safe for healthcare / financial services / insurance?"*
- *"Guardrail review of this `.agent` file / planner bundle"*

**Does not trigger** when you are building the agent (use `developing-agentforce`),
want a full config-health doc (use `agentforce-config-review`), running functional
tests (use `testing-agentforce`), or analyzing production traces (use
`observing-agentforce`).

---

## Compatibility

Works for any Agentforce agent type — AgentScript (`aiAuthoringBundle`, `.agent`)
and classic (`genAiPlannerBundle`) — and any regulated vertical.

---

## Inputs

The skill auto-detects or asks for what it needs. Providing these up front makes
the review sharper:

| Input | Why it matters |
|---|---|
| **Agent file** | The `.agent` bundle (AgentScript) or planner XML (classic). Auto-located via `find`, or retrieved with `sf project retrieve start`. |
| **Org alias** | Needed for trace verification (P6) and running-user permission checks (P4). |
| **Vertical** | healthcare / life-sciences / finserv / insurance / pharma — selects the regulatory lens (HIPAA minimum-necessary vs SOX vs GxP). |
| **Channel(s)** | telephony / voice / chat / web — gates the P5 voice sub-check. |

If an input is unavailable, the dependent check is marked **N/A** with a reason
rather than emitting a false GAP.

---

## The three-tier enforcement model

Every finding is judged against *where* a guardrail is enforced, strongest to
weakest:

| Tier | Construct | Strength |
|---|---|---|
| 1 — Deterministic | `run`, `set`, `if`, `transition to`, `available when` | Runtime-enforced; the LLM cannot skip it |
| 2 — System instructions | the `system: instructions:` block | Global, every turn; high adherence — correct home for PHI / grounding rules |
| 3 — Topic pipe-text | per-topic `\| …` lines | Suggestion only; lowest adherence; the LLM may ignore it |

A hard-mandatory step living only in tier 3 is the single most common finding.

---

## The 8 guardrail patterns

| # | Pattern | Checks |
|---|---|---|
| P1 | Confirmation Gate | Every create/update/delete shows a preview and requires explicit confirmation before executing |
| P2 | Grounded Output Only | Displays only action-returned values; never invents accounts, numbers, dates, statuses, clinical/financial figures; safe empty-states |
| P3 | Enforcement-Strength *(platform behavior)* | Mandatory step's enforcement tier matches its criticality; probabilistic steps (crisis detection) flagged as residual risk, not FAIL |
| P4 | Least-Privilege Data Scoping | Queries scoped to the running user / owned records / open record; verified as the agent's user, not an admin |
| P5 | Sensitive-Identifier Handling | Masks/segments IDs; voice never reads full account/case/invoice numbers or PII aloud |
| P6 | Audit & Traceability | Regulated actions are trace-verified (or Phase-1-ALT verified), not assumed; success not claimed without evidence |
| P7 | Resolve-Before-Act | Name/number resolved to exactly one entity before any write; multi-match → numbered pick-list, STOP |
| P8 | Regulated-Vocabulary Classifier Pitfall *(platform behavior)* | Content-safety classifiers false-positive on regulated terms (PHARMACY, SCREENING) — flagged as residual risk; lever is Einstein Trust Layer, not the `.agent` file |

Applicability is gated in **Step 0**: no write surfaces → P1/P7 = N/A; no voice
channel → P5 voice sub-check = N/A; no org access / no STDM → P6 uses the
fallback rather than an automatic GAP.

---

## Scoring

| Verdict | Meaning |
|---|---|
| **PASS** | Guardrail present and enforced at an appropriate tier |
| **PARTIAL** | Present but weak (hard requirement only in pipe-text; gate bypassable) |
| **GAP** | Required for this agent/vertical and absent |
| **N/A** | Not applicable (state the reason) |

Findings carry a severity — **CRITICAL / HIGH / MEDIUM / LOW**. Mitigating
factors (Einstein Trust Layer coverage, inherently-probabilistic steps, benign
blast radius) lower severity so the review doesn't over-report. Every PARTIAL/GAP
is verified against the actual construct before it is reported.

---

## Output

Run **standalone**, the skill produces a Markdown report
(`regulated-industry-review-[AgentName]-[Date].md`) with:

- a **verdict table** — `Pattern | Verdict | Severity | Evidence (file:line)`
- **per-pattern evidence** — what's wrong, the enforcement tier found vs. needed, and the recommended fix (with recipe)
- a **Priority Remediation Summary** — CRITICAL first, then HIGH go-live blockers

Run from **`agentforce-config-review` (Step 2b)**, it returns findings shaped for
that skill's findings JSON — folded in as one supplemental section (excluded from
the composite score, findings feed Priority Remediation at full severity). Reuse
config-review's document generator for a branded `.docx`.

---

## Related skills

| Skill | Why |
|---|---|
| `agentforce-config-review` | Broad 8-dimension config health; invokes this skill from its Step 2b and provides the branded `.docx` generator |
| `developing-agentforce` | Authoring/fixing the `.agent` file — apply the P1–P8 recipes |
| `observing-agentforce` | P6 execution — trace verification + Phase-1-ALT fallback |
| `testing-agentforce` | Regression-test confirmed guardrails |
| `agentforce-test` | Supported behavioral tests; not a replacement for a full adversarial audit. |
| `agentscript-flow-control` | Two-phase execution model behind P3's tier logic (summarized inline in Step 0a, so P3 has no external dependency) |

---

## File locations

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition — operational instructions for Codex |
| `README.md` | This file |
| `regulated-industry-review-[AgentName]-[Date].md` | Standalone Markdown output |

---

## Skill version

**v2.2.0** — June 2026

- v2.2 — current catalog (P1–P8) with the three-tier enforcement model.
- v2.1 — added a P3 worked example (crisis-escalation before/after) and concrete inspection command blocks (`find`/`grep`/`awk`/`sf`) in Inputs and Step 0.
- v2.0 — added the executable harness: Inputs, Step 0 scoping (three-tier model + write-surface enumeration + applicability gates), Scoring (severity + verdicts + carve-outs + verify-before-report), Output template, Related-skills wiring, and the P6 STDM-less fallback.

> **Maturity: derived from a single healthcare engagement (N=1).** Strong but not
> yet validated across verticals. The pattern catalog is designed to grow — see
> the **Contributing** section in `SKILL.md` to add a P9+ pattern or per-vertical
> sub-checks.
