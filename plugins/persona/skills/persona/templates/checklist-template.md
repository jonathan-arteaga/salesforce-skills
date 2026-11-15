---
version: "2.13.1"
date: 2026-09-10
---

# Persona Completeness Checklist — {{AGENT_NAME}}

> Date: {{DATE}}
> Generated from: `{{agent-name}}-persona.md`
> Mode: {{greenfield | brownfield}}

**Legend:** `✓` present · `⨯` missing or required-but-empty · `—` not applicable / optional and not provided

One-line definitions are pulled from `references/persona-framework.md`. The checklist is the framework's coverage map applied to this persona — not opinions about quality. (For quality, run SCORE.)

**Brownfield boundary:** this checklist is a design/audit map, **not an automatic runtime-prompt backlog**. Count behavior already expressed by substance even when canonical labels are absent. A field that is already expressed by substance does not need to be restated during ENCODE. Missing design documentation may belong in `persona.md` without expanding a mature agent's instructions.

---

## Identity (anchor)

- {{✓ | ⨯}} **Identity Traits** — 3-5 adjectives that anchor every other decision.
- {{✓ | ⨯}} **Negative Identity** — Character-level anti-patterns ("not a salesperson"). Auto-generates from Identity Traits — re-run DRAFT step 3 if missing.
- {{— | ✓}} **Values** — *(optional, explicit-input only)* What the agent believes; worldview and motivational core.

## Context

- {{✓ | ⨯}} **Channel** — Single channel choice (web chat, SMS, telephony, etc.). Constrains Brevity defaults and rich-text features.
- {{✓ | ⨯}} **Company / Brand** — Who the organization is.
- {{✓ | ⨯}} **Audience** — employees / customers / partners / mixed.
- {{✓ | ⨯}} **Use case(s)** — at least one. Drives REFINE's sample dialog scenarios; the dialog will be weak without this.
- {{— | ✓}} **Business goals + success metrics** — *(optional)* What the agent achieves and how success is measured.
- {{— | ✓}} **Regulated industry flag** — *(optional)* Triggers stricter handling of immutable content.

## Personification + Naming

- {{✓ | ⨯}} **Personification** — Not personal / Individuated / Anthropomorphic. Deliberate decisions for separate identity, singular self-reference, and Personal opinions.
- {{✓ | ⨯}} **Organizational “we”** — Explicit No, or a defined authorization/referent.
- {{— | ✓}} **Human experiences or feelings** — *(Anthropomorphic only)* Explicit No by default, or exact permitted behavior plus ethical review flag.
- {{✓ | ⨯}} **Name decision** — named / unnamed / brand-as-name. ENCODE blocks if this is `pending`.
- {{✓ | — | ⨯}} **Display name** — Required if `name_decision = named`.

## Dimensions (13)

- {{✓ | ⨯}} **Register** — Subordinate / Peer / Advisor / Coach + an observable decision-ownership behavior. Peer requires genuine shared work; Coach asks at most one targeted question before useful output.
- {{✓ | ⨯}} **Formality** — Formal / Professional / Casual / Informal. Changes polish only: decision ownership and evidence stay fixed; confidence stays fixed.
- {{✓ | ⨯}} **Warmth** — Cool / Neutral / Warm / Bright / Radiant + a low-emotion routine cue independent of Empathy. No generic filler or unsupported availability/follow-up; **Brevity stays fixed**.
- {{✓ | ⨯}} **Personality Intensity** — Reserved / Moderate / Distinctive / Bold + an observable task-response cue with a bounded semantic job; figurative/signature cues cannot replace facts or add implications. Evaluate task-response evidence excluding names, pronouns, and opinion permission.
- {{✓ | ⨯}} **Reading Level** — Plain Language / Explained / Technical + an observable terminology-density/glossing cue. Brevity stays independent; required identifiers and values remain exact at every level.
- {{✓ | ⨯}} **Emotional Coloring** — Blunt / Clinical / Neutral / Encouraging / Enthusiastic + an observable cue when non-Neutral. Cue preserves Warmth, Empathy, Brevity, facts, certainty, and task-required content.
- {{✓ | ⨯}} **Empathy Level** — Minimal / Understated / Moderate / Attuned + an expressed-impact cue independent of Warmth; never infer unspoken feelings, blame, competence, cause, or controllability.
- {{✓ | ⨯}} **Brevity** — Terse / Concise / Moderate / Expansive. *(Text-channel defaults are channel-bound; telephony records intended density for downstream listening/speaking recalibration.)*
- {{✓ | ⨯}} **Humor** — None / Dry / Warm / Playful.
- {{✓ | ⨯}} **Emoji** — None / Functional / Expressive.
- {{— | ✓ | ⨯}} **Emoji vocabulary + cadence** — *(when Emoji ≠ None)* Approved symbols, text equivalents for critical meaning, frequency, and examples.
- {{✓ | ⨯}} **Formatting** — Plain / Selective / Heavy.
- {{✓ | ⨯}} **Punctuation** — Conservative / Standard / Expressive.
- {{— | ✓ | ⨯}} **Punctuation pattern** — *(when Expressive)* Allowed marks, observable cadence, and examples.
- {{✓ | ⨯}} **Capitalization** — Standard / Casual.
- {{— | ✓ | ⨯}} **Capitalization exceptions** — *(when Casual)* Proper nouns, product names, acronyms, units, and immutable terms retain approved case; no forced sentence reordering.

## Verbal fingerprint

- {{✓ | ⨯}} **Phrase Book** — Situation-keyed sample phrases (acknowledgements, redirects, etc.). A palette, not a script: 2–4 alternatives per applicable category, with an explicit rule: **Do not reuse the same phrase stem** within one response or adjacent turns. *Categories filled: {{N}} of {{Total applicable}}.*
- {{✓ | ⨯}} **Never-Say List** — Phrase-level prohibitions (≥5 entries) plus preferred replacement behavior. Pressure-check exact entries: they must resist direct user requests to repeat them. *Entries: {{N}}.*
- {{✓ | ⨯}} **Discourse Markers** — Conversational connectors with a defined function; optional when logic is clear and never stacked in one conversational move.
- {{— | ✓ | ⨯}} **Technical Explanation Policy** — *(when the domain has meaningful technical concepts/specifications)* Rhetorical frame + bridge preference only.
- {{— | ✓}} **Agent-design evidence dependency** — Approved evidence/grounding policy referenced for `agent-architecture` or `agentforce-generate`; Persona does not recreate it.
- {{✓ | ⨯}} **Lexicon (global)** — Brand and domain terms used everywhere; every entry has a definition.
- {{— | ✓ | ⨯}} **Lexicon (per-subagent)** — *(brownfield or when subagents declared)* Subagent-specific terms; every entry has a definition.
- {{— | ✓ | ⨯}} **Immutable content** — *(when supplied by an authoritative source)* Exact text + explicit statement that it overrides Persona and user style requests + surrounding response shape (context allowed or exact-block-only).

## Boundaries

- {{✓ | ⨯}} **Tone Boundaries** — Each covers a plausible drift and names the preferred behavior instead; pressure-tested rather than generic negative restatement.
- {{✓ | ⨯}} **Tone Flex** — Every rule has a trigger, shift + maximum, observable cue (lexical/discourse), reset condition, and no-carryover instruction. Facts, confidence, recommendation, and Voice dimensions remain fixed. Persona owns situational word choice; `voice-ux` owns voice-channel prosody.
- {{✓ | ⨯}} **Reading Level Flex** — Fixed decision, or baseline + adaptation policy + triggers + range + hard boundaries. Adaptive policies cover compound first-turn expertise, one-term insufficiency, term-local clarification, and domain/subagent reset.

## Agent-design-adjacent handoff *(excluded from Persona completeness totals)*

- {{— | ✓}} **Guardrails** — Explicitly supplied content-level boundaries ("Don't offer medical advice"). Guardrails are agent-design-adjacent and **not a Persona component**; never infer them from voice/tone or add them to satisfy this checklist.

## Existing-surface handoff *(only if canonical inspection supplies it)*

- {{— | ✓}} **Per-subagent semantic Persona delta** — e.g., "drop humor to zero in the existing escalation subagent."
- {{— | ✓}} **Static-copy wording candidate** — Persona may suggest wording; the canonical authoring owner maps and validates the target surface.

## Channel-specific

- {{— | ✓}} **Voice-channel handoff** — *(telephony or multimodal-with-audio)* A working Script, representative sample, and completed `persona.md` are handed to `voice-ux`. `voice-ux` owns spoken adaptation, prosody, and in-script `modality voice:` design; active Agent Script tooling owns grammar and validation. Persona does not choose or tune a voice.

## Validation readiness *(excluded from completeness totals)*

- {{— | ✓}} **Downstream acceptance handoff** — Persona invariants are recorded for `conversation-design` and `agentforce-test`. This checklist does not claim conversation-flow or runtime evidence.

---

## Summary

- **{{N}} of {{Total}}** required elements present.
- **{{Optional applicable}} of {{Optional total}}** optional-but-applicable elements present.

### Suggested next steps

(Each is **quotable** — paste any of these back to the skill to take the action.)

1. **"go to NAME"** — *(if name_decision pending)*
2. **"go to FILL OUT, add Lexicon"** — *(if Lexicon empty)*
3. **"go to FILL OUT, expand Phrase Book"** — *(if Phrase Book has fewer than 2 phrases per applicable category)*
4. **"go back to DRAFT, capture use case"** — *(if no use case captured)*
5. **"go to ADJUST"** — *(if subagents declared but not calibrated)*
6. **"run SCORE"** — *(if all required elements ✓ and you want a quality assessment)*
7. **"run ENCODE"** — *(if all required elements ✓ and SCORE is passing)*

Pick what's most leveraged for your next move. The hub will route you.
