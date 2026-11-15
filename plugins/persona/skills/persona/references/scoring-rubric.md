---
version: "2.5.1"
date: 2026-09-10
---

## PHASE 3 — SCORE — "How good is it?"

Apply the 100-point rubric. Two entry points:
1. **Designed persona** (state from DRAFT/REFINE)
2. **Existing agent instructions** (brownfield mode — `.agent` file, system prompt, subagent instructions, or combination)

**Key principle:** Score the substance, not whether they used the framework's vocabulary. "Personality guidelines" = Identity. "Communication rules" = dimensions. "Banned phrases" = Never-Say. Map first, then score.

Personification is evaluated against the current **Not personal / Individuated / Anthropomorphic** contract: separate identity, singular self-reference, and ownership of Personal opinions.

### Brownfield evidence

For an Agent Script source, ask `agentforce-generate` or the active Agent Script authoring tool for current structured evidence. Do not parse the DSL here. Score only character-bearing content returned by the canonical owner, such as the global character baseline, existing local Persona calibrations, and static-copy candidates. Do not score routing, actions, state, or Agent Script quality.

Common label mappings:

| If you find... | It likely maps to... |
|---|---|
| "Personality," "communication principles," "voice guidelines" | Identity traits |
| "Communication rules," "response guidelines," "style guide" | Dimension selections |
| "Banned phrases," "forbidden phrases," "don't say" | Never-Say List |
| "Vocabulary," "terminology," "glossary" | Lexicon |
| "Jargon level," "technical depth," "plain language" | Reading Level / Reading Level Flex |
| "Tie specs to benefits," "outcome framing," "evidence-first" | Technical Explanation Policy |
| "Tone rules," "emotional guidelines" | Tone Flex / Tone Boundaries |
| "Example responses," "sample language," "approved phrases" | Phrase Book |

Map by substance, not label. Mark inferred mappings: "inferred — [source label]." Normalize glossaries and vocabulary lists into the canonical Lexicon shape. A term without a definition is an explicit gap; never invent a definition when the source doesn't establish one.

Legacy Reading Level mapping: `Suppress` → Plain Language; `Explain` → Explained; `Advanced` → Technical. `Match` requires a deliberate baseline plus Reading Level Flex. If the source doesn't establish the baseline, ask one focused question instead of guessing. Absence of a framework concept ≠ zero score; score what's present.

SCORE evaluates the Persona artifact and controlled calibration evidence only. Export facts/status preservation, boundary resistance, and Tone Flex reset as downstream acceptance criteria. `conversation-design` owns representative scenario design, and `agentforce-test` owns runtime proof on a built agent. A Persona score does not claim runtime proof.

### 100-Point Rubric

| Category | Points | Criteria |
|---|---|---|
| **Identity Coherence** | /11 | Traits distinct + behaviorally defined • Personification has aligned identity, singular self-reference, and opinion rules • Organizational “we” and applicable Human experiences/feelings decisions are explicit • Negative Identity (2-4) • Design Inputs coherent |
| **Dimension Consistency** | /11 | Each of 14 dimensions coherent with Identity, constraints respected • Tone Boundaries consistent with Emotional Coloring/Empathy; Tone Flex within range • Reading Level baseline deliberate and Flex policy within bounds • Chatting Style adapted for channel |
| **Internal Consistency / Conflict-Pair Check** | /10 | No contradictions between Tone Boundaries and Phrase Book entries • Never-Say doesn't overlap Lexicon • Emotional Coloring + Humor compatible • Identity traits aligned with dimension selections • Technical Explanation framing preference is distinct from agent-design evidence policy • Figurative/signature and empathy cues preserve supplied facts • Immutable content not contradicted by lexicon |
| **Behavioral Specificity** | /9 | Concrete behavioral examples, testable rules • Never-Say ≥5 covering chatbot filler + register violations + cognitive markers + persona-specific • Lexicon populated with definitions; immutable terms distinguished where applicable • Brand input extraction depth |
| **Phrase Book Behavioral Coverage** | /11 | Phrases for applicable character functions (acknowledgement, affirmation, redirect, escalation language when explicitly in scope) • 2-4 per applicable category • Rhetorical framing examples when Technical Explanation Policy applies • Match register and dimensions • For Not personal experiences: no separate agent identity, heavily suppressed singular self-reference, and no Personal opinions |
| **Tone Flex & Boundaries** | /9 | Every rule has trigger + shift/maximum + observable cue (lexical/discourse) + reset condition • No tone carryover • Facts, confidence, recommendation, and Voice dimensions stay fixed • Content-sensitivity default present (or overridden) • Each boundary covers a plausible drift and names preferred behavior • Flex range stays within boundaries • Voice-bearing work hands the same semantic policy to `voice-ux` for prosodic realization |
| **Lexicon & Vocabulary** | /7 | Global lexicon populated • Every entry has a term + definition • Per-subagent lexicon where applicable (brownfield) • Reading Level appropriate for audience • Flex triggers/range/boundaries testable • Technical Explanation Policy explicit when applicable • Immutable terms preserved • Scope and usage guidance appropriate |
| **Static Messages** | /7 | Welcome reflects Identity + Register + Voice + Tone + Brevity • Error reflects Formality + Warmth + Coloring + Brevity • All static strings sound like the same agent • SMS: first-message welcome with system identification • Voice-bearing channels: `persona.md`, working Script, and representative sample handoff to `voice-ux` is explicit; active Agent Script tooling retains grammar/validation authority |
| **Business Context Alignment** | /7 | Goals and metrics inform design • Persona supports objectives • Audience demographics reflected |
| **Calibration Quality** | /9 | Persona recognizable without seeing the dimension table • Routine response uses only supplied facts • Single-axis contrast holds all other settings fixed • Tone Flex example shows the approved lexical cue and reset • Boundary example resists an exact Never-Say or immutable-content challenge • No invented action, branch, outcome, or conversation progression • Representative scenarios explicitly handed to `conversation-design` |
| **Completeness** | /9 | All framework sections addressed • Values only if user-provided • No gaps where the framework expects a deliberate decision |

(Total: 100. The rubric scores Persona design and calibration, not conversation-flow or runtime-agent quality.)

### Existing local calibration review (brownfield)

When canonical inspection returns existing subagent-level character guidance:

- confirm that the global Persona is inherited rather than repeated;
- score a local calibration only when purpose or observed drift warrants it;
- verify that Tone Flex and Lexicon changes are a targeted semantic delta; and
- keep action, routing, and state assessment out of the Persona score.

### Recommendations (required output)

For each gap surfaced:
- Cite the framework section the gap relates to
- Provide a specific, actionable fix
- For brownfield: cite the location in the source file (subagent name, line range)

### SCORE Exit

Evaluation written to `persona/[agent-name]/evaluation.md` with YAML **version and date frontmatter** before the report heading. For a newly generated artifact, set `date` to the **current local date**; do not copy the template revision date. Total presented as percentage (90-100 production-ready, 75-89 strong foundation, 50-74 needs revision, <50 significant gaps). Present the HUB; suggested next is FILL OUT or ADJUST if gaps exist, ENCODE if scores are passing.

---
