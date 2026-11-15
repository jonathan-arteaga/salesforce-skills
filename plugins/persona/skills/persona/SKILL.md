---
name: |-
  persona
description: |-
  Define or review an Agentforce persona. Return a character contract and calibration examples. Route guardrail design to agent-architecture and dialogues to conversation-design. For voice casting, prosody, audio tags, pronunciation, STT bias, or `modality voice:`, use `voice-ux`.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.

For industry-specific agents, cross-industry ideation, or role/personality choices, read the selected patterns in [industry and role design](references/industry-patterns.md). Use them within this skill’s ownership; distinguish documented capabilities from proposed designs.


# Designing Agent Persona

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## How to Use

This skill designs an AI agent persona for Salesforce Agentforce. It can produce a stakeholder WORKSHEET or WORKSHOP before any draft, including total greenfield work. For persona design, it walks through four sequenced phases (DRAFT → REFINE → SCORE → ENCODE) and offers the NAME, FILL OUT, ADJUST, and CHECKLIST spokes after DRAFT. WORKSHEET and WORKSHOP also remain available after DRAFT.

**What it produces:**

- A stakeholder-facing question worksheet or a facilitated workshop plan on request, with or without a persona draft
- A Persona document (`persona/[agent-name]/persona.md`): the authoritative character contract
- Persona calibration examples (`persona/[agent-name]/persona-calibration.md`): controlled response evidence, not conversation flows
- An evaluation report on request (`persona/[agent-name]/evaluation.md`): Persona-specific rubric and recommendations
- A completeness checklist on request
- An Agent Script handoff (`persona/[agent-name]/persona-handoff.json`) for `agentforce-generate`
- Provisional legacy Builder field values for existing Builder agents only

**Artifact invariant:** Every generated Markdown artifact uses its canonical template when one exists and begins with YAML **version and date frontmatter**. Set a new artifact's `date` to the **current local date**; do not copy the template revision date. Preserve and bump artifact version/date appropriately through later phase or spoke updates; SCORE's `evaluation.md` follows the same frontmatter rule even though it has no separate template.

**Session resumption:** If you stop mid-phase, your progress is preserved in the conversation and can be resumed.

## When to Use This Skill

- Designing a new Agentforce agent and need to define its personality before building (greenfield)
- Auditing an existing `.agent` file's persona consistency (brownfield)
- Maintaining Persona-bearing fields in an existing legacy Builder agent while keeping Agent Script migration explicit (brownfield maintenance)
- Translating brand guidelines into a structured persona
- Producing a stakeholder questionnaire or a facilitated workshop plan to gather design input, even before a persona exists
- Aligning teams on what an agent should sound like before development

**Scope boundary:** This skill defines WHO the agent is. It owns the character contract, including situational Tone Flex expressed through word choice and response patterns. It does not parse, scaffold, edit, compile, validate, publish, or activate Agent Script; hand those operations to `agentforce-generate` or the active Agent Script authoring tool. It does not design conversation flows (`conversation-design`), runtime tests (`agentforce-test`), or subagents/actions/Guardrails (`agent-architecture`). Reading Level Flex changes presentation; it does not establish technical-analysis quality, factual grounding, or product-suitability logic. For voice-bearing channels, `voice-ux` maps the completed character contract to spoken interaction and prosody. If a request such as “make it warmer” is ambiguous, ask one question: words/stance belong to `persona`; audible delivery belongs to `voice-ux`; if both, run Persona first.

## Framework Reference

Read `references/persona-framework.md` for the full framework. It defines:

- **Identity** — 3-5 anchoring adjectives + Negative Identity (≥2 character-level anti-patterns)
- **14 dimensions** (Personification + the 13 expression dimensions):
  - **Personification** — Not personal / Individuated / Anthropomorphic; controls separate identity, singular self-reference, and opinion ownership
  - **Register** — Subordinate / Peer / Advisor / Coach
  - **Voice** — Formality, Warmth, Personality Intensity, Reading Level
  - **Tone** — Emotional Coloring, Empathy Level (+ Tone Boundaries, Tone Flex)
  - **Delivery** — Brevity, Humor
  - **Chatting Style** — Emoji, Formatting, Punctuation, Capitalization
- **Persona Artifacts** — Identity (traits + negative identity), Expression (tone boundaries + never-say), Phrasing (phrase book + discourse markers + lexicon + Technical Explanation Policy)
- **Tone Flex** — how tone shifts by context through word choice and response patterns (including per-subagent calibration); audible prosody is downstream in `voice-ux`
- **Reading Level Flex** — how technical density shifts from a deliberate baseline; a companion policy, not a dimension
- **Technical Explanation Policy** — rhetorical preference for staying in-frame or adding a cross-frame explanation; agent design owns factual support
- **Lexicon** — global and per-subagent terms with required definitions, plus optional usage and immutable-term rules
- **Agent-design-adjacent Guardrails** — content boundaries captured only as verbatim handoff references; **not a Persona component**, never inferred, scored, rewritten, or encoded here

Attributes are ordered by dependency. Identity → Personification → Register → Voice → Tone → Delivery → Chatting Style. Constraint notes recommend natural pairings; any combination is valid.

---

## Requested-output triage (before DRAFT)

Route on the requested deliverable before running any phase or asking greenfield/brownfield. **WORKSHEET** means a set of questions stakeholders can answer independently, inline or in a document; **WORKSHOP** means a facilitated collaborative session plan with activities and materials or a virtual board. Both can start from zero with only an agent concept and an intended stakeholder. They work in any folder or no project folder, independently of the Agentic Experience Hub and without a decision log, requirements file, existing persona, or other skill. The HUB below is this skill's optional post-DRAFT phase menu, not the Agentic Experience Hub. Treat “open” as a question the requester has not settled in the supplied input; do not search for or demand a recorded decision. If a concept or stakeholder is missing, ask only for what is needed to make the requested artifact useful; otherwise proceed. Suggest that a persona draft can sharpen either artifact, but never require or silently create one. For WORKSHEET or WORKSHOP, use only supplied facts and stakeholder context; don't assume a brand guide, a draft, or approved decisions exist. Read `references/stakeholder-question-policy.md`, `references/spokes.md`, and the matching template. If the user asks for a worksheet for Legal, tailor the questions to Legal's role; do not substitute a general persona draft, a workshop plan, or a prefilled questionnaire. For an inline request, deliver the full questions inline; document encoding to Google Docs or .docx belongs to the delivery surface, not this skill. Do not create unrelated persona artifacts, run the persona linter, or present the DRAFT HUB for a standalone worksheet/workshop request. Ask a clarification only if worksheet versus workshop remains genuinely ambiguous after reading the user's wording.

**Optional protected instructions:** Preserve designer-supplied text explicitly marked uneditable in a separate companion attachment, distinct from exact response copy. Carry it verbatim with supplied scope and approval provenance into ENCODE; do not infer policy, approval or placement, and do not turn internal instructions into spoken dialogue. See `references/draft-phase.md` and the selected target guide. This is preservation/handoff only, not source encoding verification.

## Pre-DRAFT Triage — Greenfield or Brownfield?

**For DRAFT or later phases,** ask the user which lane they're on only when the supplied context does not already answer it. The two lanes diverge significantly downstream.

<quote>
Welcome. Two ways to use this skill:

1. **Starting fresh** — design a persona from scratch using brand input, audience details, and channel. **Greenfield.**
2. **Auditing an existing agent** — review and improve a `.agent` file or existing legacy Builder configuration. **Brownfield.**

Which one?
</quote>

Set a `mode` flag in state: `greenfield` or `brownfield`.

**Brownfield triggers:**

- When the user supplies a `.agent` file, hand it to `agentforce-generate` or the active Agent Script authoring tool for canonical inspection; consume the returned structured evidence rather than parsing the DSL here.
- Treat an existing legacy Builder configuration as a provisional brownfield maintenance source and preserve all non-Persona fields.
- ADJUST is available only for existing subagents/actions returned by the canonical owner; never infer architecture.
- SCORE may assess local character consistency but does not score routing, actions, or runtime conversation quality.
- ENCODE produces an approved semantic Persona handoff, not a source patch.

**Brownfield runtime rule:** Existing character instructions are the baseline. Record only user-requested or evidence-backed semantic Persona deltas that are missing and likely to change expression. A no-op is valid. The canonical Agent Script owner applies and verifies any approved change.

**Greenfield triggers:**

- ENCODE produces `persona-handoff.json` for `agentforce-generate`; Persona does not create a starter `.agent` skeleton.
- ADJUST remains gated until canonical architecture evidence exists.

## Completion modes

- **Interactive practitioner** *(default)* — pause at designed checkpoints, present the HUB, and let the user choose the next phase or spoke.
- **Bounded one-pass** — when the user explicitly says they are unavailable for follow-up or asks the skill to finish end to end, make only safe labeled assumptions, write every requested artifact, and return a compact artifact-first summary without checkpoint pauses.

The detailed detection and output-budget rules live in `references/draft-phase.md` and `references/interaction-design-notes.md`.

---

## Architecture: Phases and Spokes

**Phases** are sequenced — order matters. **Spokes** orbit the hub after DRAFT; WORKSHEET and WORKSHOP also run independently before DRAFT. The hub is presented after DRAFT-phase or post-DRAFT spoke exits, not standalone worksheet/workshop requests.

```javascript
SEQUENCED PHASES (linear pipeline):
  DRAFT → REFINE → SCORE → ENCODE
                          ↑
              (loop back via phases or spokes if SCORE finds gaps)

STANDALONE BEFORE OR AFTER DRAFT:
  ⊙ WORKSHEET         — stakeholder questions to answer independently
  ⊙ WORKSHOP          — facilitated collaboration plan and activities

SPOKES (radiate from the HUB after DRAFT):
  ⊙ NAME              — pick or confirm the agent's name
  ⊙ FILL OUT          — phrase book, never-say, lexicon, immutable content
  ⊙ ADJUST            — semantic character calibrations for existing surfaces (gated)
  ⊙ CHECKLIST         — "What's filled in?" — completeness gap analysis
```

The HUB suggests the next default but lets the user pick anything, including re-running the phase or spoke they just exited.

---

## PHASE 1 — DRAFT

Read `references/draft-phase.md` for the authoritative procedure. In order:

1. Accept and extract the user's source material.
2. Gather Channel, Company/Brand, Audience, and at least one use case; gather conditional context only when its trigger fires.
3. Draft 3–5 behaviorally defined Identity Traits and 2–4 Negative Identity statements.
4. Write the start-small persona and offer the explicit checkpoint.
5. Set Degree of Personification: Not personal, Individuated, or Anthropomorphic.
6. Walk Register → Voice → Tone → Delivery → Chatting Style, including Reading Level Flex and Technical Explanation Policy when applicable.
7. Generate the Phrase Book, Never-Say List, Tone Boundaries/Flex, Lexicon, and immutable content. Separately preserve any explicitly supplied agent-design Guardrails for handoff; never invent them as Persona content.

**DRAFT Exit:** after the full DRAFT (not the intentionally partial start-small checkpoint), run `scripts/lint_persona.py` on the completed Persona document. Resolve deterministic errors before exit. Surface unusual-pairing warnings and require conscious confirmation or a revision; warnings do not become universal prohibitions. Write the document, retain complete state plus confidence annotations, and present the HUB.

---

## PHASE 2 — REFINE

Read `references/refinement-mappings.md` for controlled Persona calibration, natural-language adjustment mappings, and the refinement loop.

Use one supplied utterance and fixed facts to show the routine baseline, one lexical Tone Flex shift plus reset, and one boundary response when useful. These are single-response calibration examples, not multi-turn scenarios or runtime tests. Hold every unchanged dimension and task fact constant when comparing a requested Persona change.

When representative happy-path, error, fallback, or handoff scenarios are needed, pass `persona.md` and the use cases to `conversation-design`. When a built agent needs behavioral proof, pass Persona acceptance criteria to `agentforce-test`.

**REFINE Exit:** write `persona/[agent-name]/persona-calibration.md`, update changed Persona state, offer the downstream handoff when needed, and present the HUB.

---

## PHASE 3 — SCORE — "How good is it?"

Read `references/scoring-rubric.md` for the Persona-specific 100-point rubric and percentage bands.

Score the Persona design artifact by substance rather than framework vocabulary. Run `scripts/lint_persona.py` first and include its deterministic diagnostics as evidence. For a brownfield Agent Script, consume character-bearing evidence returned by `agentforce-generate` or the active authoring tool; do not parse the source here. Do not score routing, action correctness, deployed conversation quality, or runtime safety. Route those to `agentforce-generate` or `agentforce-test` as appropriate; conversation-quality scoring (`evaluating-conversations`) is not installed.

**SCORE Exit:** write `persona/[agent-name]/evaluation.md`, present the score and largest Persona gaps, and return to the HUB.

---

## PHASE 4 — ENCODE / HANDOFF

Read `references/encode-detail.md`. Resolve the NAME decision, then choose one downstream path:

- Agent Script → `references/persona-handoff-guide-agentscript.md` + `templates/persona-handoff-template.md`
- Existing legacy Builder maintenance → `references/persona-encoding-guide-builder-legacy.md` + `templates/persona-encoding-template-builder-legacy.md`

For Agent Script, write an approved semantic `persona-handoff.json`. Do not write or patch `.agent` syntax. `agentforce-generate` or the active Agent Script authoring tool owns inspection, schema, scaffolding, structural mutation, candidate verification, compile/check, preview, publication, and activation.

For existing legacy Builder agents, the provisional adapter may produce field values but must remain brownfield-only and avoid expansion into lifecycle guidance.

Persona may carry explicit Guardrails and evidence policies only as verbatim adjacent-constraint references for `agent-architecture` or `agentforce-generate`, and client voice requirements only as verbatim references for `voice-ux`. It does not infer, score, rewrite, or encode them. For voice-bearing channels, hand a working Script, representative sample, `persona.md`, and `persona-handoff.json` when present to `voice-ux`; Persona retains lexical Tone Flex and `voice-ux` owns prosodic realization.

**ENCODE Exit:** write and approve the Persona handoff or provisional legacy Builder artifact, state the next owner, and present the HUB. Do not claim Agent Script readiness.

---

## SPOKES

Read `references/spokes.md` for the authoritative interaction prompts and procedures.

| Spoke | Purpose |
| --- | --- |
| **NAME** | Decide named, unnamed, or brand-as-name. |
| **FILL OUT** | Extend Phrase Book, Never-Say, Lexicon, technical framing examples, and immutable content. |
| **ADJUST** | Propose semantic character calibrations for existing subagents or static-copy candidates returned by the canonical owner. |
| **CHECKLIST** | Report present, missing, and not-applicable elements with quotable next steps. |
| **WORKSHEET** | Generate an independently answerable, stakeholder-specific question set. |
| **WORKSHOP** | Generate a facilitated collaborative session plan. |

WORKSHEET and WORKSHOP can run before DRAFT without a persona artifact. After DRAFT they are repeatable and return to the HUB; standalone runs return only the requested deliverable.

---

## HUB

Consult [`references/hub-menu.md`](references/hub-menu.md) before presenting the HUB after any DRAFT-phase or post-DRAFT spoke exit.

## Output Files

The skill produces:

1. **Persona document** (`persona/[agent-name]/persona.md`) — DRAFT and later Persona revisions.
2. **Persona calibration** (`persona/[agent-name]/persona-calibration.md`) — REFINE; controlled response evidence, not a flow.
3. **Evaluation report** (`persona/[agent-name]/evaluation.md`) — SCORE of the Persona artifact only.
4. **Persona handoff** (`persona/[agent-name]/persona-handoff.json`) — ENCODE for Agent Script; consumed by `agentforce-generate`.
5. **Provisional Builder fields** (`persona/[agent-name]/builder-fields.md`) — ENCODE for existing legacy Builder agents only.
6. **Checklist** (`persona/[agent-name]/checklist.md`) — CHECKLIST spoke.
7. **Stakeholder worksheet** (`persona/[agent-name]/stakeholder-worksheet.md`) — WORKSHEET, if a file is requested.
8. **Workshop plan** (`persona/[agent-name]/workshop-outline.md`) — WORKSHOP, if a file is requested.

For inline-only requests, return the requested artifact inline without creating files. A draft or calibration file is an optional source, never a required pre-read.

`persona/` is gitignored at the skill repo level so dogfooding the skill with `cwd` inside this checkout doesn't leak outputs into git. In any other working directory, the user is responsible for whatever gitignore rules they want to apply.

---

## Interaction Design Notes

Read and apply `references/interaction-design-notes.md` across CLI, TUI, web, and IDE surfaces.
