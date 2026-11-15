# Step 2b — Regulated-Industry Guardrail Review (conditional)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Step 2b — Regulated-Industry Guardrail Review (conditional)

**Gate:** run this step only if the agent serves a **regulated industry** — i.e. the
`industry` captured in Step 1 is healthcare, life sciences, financial services,
insurance, or pharma distribution (or the user answers **yes** to *"Is this agent part
of a regulated industry?"*). If not regulated, skip — no section, no findings.

When the gate is true, invoke the **`regulated-industry-agents-review`** skill to run its 8
guardrail patterns (P1–P8: confirmation gate before writes, grounded output,
enforcement-strength of mandatory steps, least-privilege scoping, sensitive-identifier
handling, audit/traceability, resolve-before-act, regulated-vocabulary classifier
pitfall). Pass it the already-gathered context (`AGENT_FILE`, org alias, `industry`,
channel) so it does not re-ask.

**Fold its results into this review:**
- Add one section to the findings JSON (`## Step 4a`) as the **next section number** after the dimensions:
  ```json
  { "number": 9, "title": "Regulated-Industry Guardrails", "score": <1-10>,
    "passes": [ ... PASS patterns ... ],
    "findings": [ {"severity": "...", "label": "P#  <pattern>", "text": "<gap + file:line>"} ],
    "fixes": [ "<recipe-based fix per finding>" ] }
  ```
- Each **PARTIAL/GAP** pattern at CRITICAL or HIGH also becomes a **`remediation[]`** entry
  (`area: "Regulated Guardrails"`).
- Map verdicts to the doc: **GAP/PARTIAL → finding** at its severity; **PASS → pass**;
  **N/A → omit** (don't list non-applicable patterns as findings).
- This section is **supplemental** — like D8, its findings feed Priority Remediation at
  full severity, but it is **excluded from the composite score** (it's a focused
  compliance overlay, not one of the 7 health dimensions).

If `regulated-industry-agents-review` is not installed in this environment, note in the section
that the regulated review was requested but the skill was unavailable, and fall back to
Dimension 3's existing Responsible-AI checks — do not fabricate guardrail findings.

---
