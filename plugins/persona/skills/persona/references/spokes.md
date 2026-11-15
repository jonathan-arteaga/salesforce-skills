---
version: "2.4.0"
date: 2026-10-12
---

## SPOKES

NAME, FILL OUT, ADJUST, and CHECKLIST are available after DRAFT. WORKSHEET and WORKSHOP may run independently before DRAFT, including with no source material beyond the agent concept and the target stakeholders. A draft is useful context, not a prerequisite. After DRAFT these outputs are repeatable and return to the HUB; for standalone requests return only the requested output.

### ⊙ NAME

> "Should users experience a separate agent identity here, or should the product/service itself remain the identity?"

If a working title was detected in DRAFT (`display_name_placeholder` set):
> "I picked up '[working title]' from your input. Confirm it, or pick from suggestions?"

Apply the selected Degree of Personification:
- **Not personal** → no separate proper name or capitalized agent label. Use the product/service identity or a lowercase role description only when disclosure requires it.
- **Individuated** → suggest 2–3 distinct descriptive labels that clarify function without implying a human-like identity.
- **Anthropomorphic** → suggest up to 3 individual names that distill the Identity and fit the intended person-like presentation.

Apply naming principles from the framework:
- Descriptive ("Service Agent") • Evocative ("Striker") • Sticky ("Clover") • Culturally aligned ("Bug Squasher") • Brand-aligned ("Lex") • Easy to say (radio test: hear once → pronounce, repeat, distinguish, and find) • Obviously artificial ("Song," "Cortana") • Functional ("Scripty") • Abstract ("Koda," "Lumi") • Null (deliberate non-name)
- **Anti-pattern:** API-style names like `Tech_Assist_Agent_v2_Internal_Test` are NOT persona names.

If no separate identity: set `name_decision: unnamed` or `brand-as-name`; Personification must be Not personal. If the user chooses an individual name, confirm Anthropomorphic; if they choose a descriptive agent label, confirm Individuated.

State update: `name_decision` ∈ {named, unnamed, brand-as-name}. Display name populated.

### ⊙ FILL OUT

> "You're in FILL OUT. What would you like to work on?
> - Phrase book additions
> - Never-say expansions
> - Lexicon additions (global or per-subagent)
> - Technical Explanation framing preference
> - Immutable content marking
> - I'm done with this spoke
> (Pick one; you'll come back here after each, or pick multiple by listing.)"

For each sub-activity, present current state and gather additions/edits. Lexicon additions always require **Term + Definition**. Usage / preferred contrast and Immutable status are optional. The same shape applies globally and per existing subagent returned by canonical inspection. Never accept a bare keyword list as a complete lexicon. When Technical Explanation Policy applies, keep its rhetorical framing preference separate from Reading Level and record the agent-design evidence policy only by reference. Update the Persona document on exit.

### ⊙ ADJUST

**Gated:** only offered when `agentforce-generate`, `agent-architecture`, or the active Agent Script authoring tool returns an existing subagent or static-copy surface. Persona does not inspect the DSL or infer architecture.

> "You're in ADJUST. What would you like to work on?
> - Semantic Persona calibration for an existing subagent (for example, 'in escalation, drop humor to zero')
> - Static-copy wording candidate in Persona voice
> - I'm done with this spoke"

Global Persona is inherited. Add a targeted semantic delta only for a deliberate local expression difference or observed friction point. Do not repeat the full global Persona and do not name an Agent Script field. The canonical authoring owner decides where and how to apply approved changes, then verifies structure and runtime behavior.

### ⊙ CHECKLIST — "What's filled in?"

Reads the persona document; produces a markdown checklist marking each element as ✓ present, ⨯ missing, or — not applicable. Definitions pulled directly from the framework.

Output template at `templates/checklist-template.md`. Each suggested next step is **quotable** (e.g., "go to NAME", "go to FILL OUT, add Lexicon") so the user can paste back rather than retype.

Useful before SCORE for a quick gap scan, and before ENCODE for a readiness check.

Write to `persona/[agent-name]/checklist.md`.

### ⊙ WORKSHEET

Produce **stakeholder questions to answer independently**, not a persona draft or a facilitated workshop plan. Read `references/stakeholder-question-policy.md` and `templates/stakeholder-worksheet-template.md`. Use the user's named stakeholder(s), source material, channel, and use case when provided. No persona file, brand guide, or complete requirements are required. If no draft exists, frame any proposed direction as a question rather than a settled design. A draft may be recommended as optional preparation, but do not create one unless asked.

A Legal worksheet should invite Legal to identify risk, responsible-AI and transparency expectations, appropriate personification/anthropomorphization, ethical and humane use, and review/approval requirements as relevant to the use case. These are prompts, not a mandatory checklist or assertions about applicable law. Ask for jurisdiction, exact wording, owner, and applicability when Legal identifies a requirement; do not write legal advice or invent a disclosure. Keep agent-design decisions (escalation protocol, routing, actions) explicitly outside Persona even if Legal flags them for handoff.

If requested inline, show the entire worksheet inline. Only write `persona/[agent-name]/stakeholder-worksheet.md` when a file is requested; document encoding to .docx or Google Docs is outside this skill. Do not call the DRAFT linter or HUB for a standalone worksheet.

### ⊙ WORKSHOP

Produce a **facilitator's plan** for a live collaborative session, not a standalone questionnaire. Read `references/stakeholder-question-policy.md` and `templates/workshop-outline-template.md`; `references/workshop-question-policy.md` and `references/workshop-scenario-seeds.md` supply optional question and scenario techniques. Before DRAFT, work from the concept, stakeholders, and any supplied evidence without claiming a persona is already decided. After DRAFT, use confirmed and open decisions to focus activities.

Choose an in-person whiteboard/poster-paper/sticky-note format or a virtual FigJam/Lucid/Miro/Mural-style board according to the request; if unspecified, describe one medium-neutral board layout. Include session objective, roles, timing, materials or board setup, collaborative activities and prompts, decision capture, and follow-up owner. When asked for a board plan, give the facilitator copy-ready zone titles, prompts, participant input spaces, scenario moments, and decision status, so they can set up the room or board without inventing activities. An opening contrast and good and bad examples are optional ways to elicit brand-specific language. Prune settled questions and keep workflow decisions outside Persona. Avoid a list of independently answered questions masquerading as a workshop.

If requested inline, show the entire plan inline. Only write `persona/[agent-name]/workshop-outline.md` when a file is requested. Do not call the DRAFT linter or HUB for a standalone workshop.

---
