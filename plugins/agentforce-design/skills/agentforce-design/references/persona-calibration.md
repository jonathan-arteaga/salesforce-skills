# Persona Design & Calibration

Define WHO the Agentforce agent is through an authoritative character contract (`persona.md`), single-turn calibration examples (`persona-calibration.md`), rubric evaluation (`evaluation.md`), and a semantic handoff (`persona-handoff.json`) consumed by `agentforce-build`.

## Phases, Spokes & Triage

Route on the requested deliverable first: **WORKSHEET** (independently answerable stakeholder questions) and **WORKSHOP** (facilitated collaborative session plan) can run from zero without creating a persona draft or running the linter.

For full persona authoring, run sequenced phases in order:

1. **DRAFT:** Gather Channel, Brand, Audience, and at least one use case. Define 3-5 behavioral Identity Traits and 2-4 Negative Identity statements ("Not ..."), set Personification, walk all 13 expression dimensions, and generate Phrase Book, Never-Say List, Tone Flex, Lexicon, and Immutable Content.
2. **REFINE:** Produce single-turn controlled calibration examples using one fixed utterance and fixed facts (baseline, one lexical Tone Flex shift plus reset, one boundary reply). Hold all unchanged dimensions constant. Multi-turn scenarios belong in [conversation-design.md](conversation-design.md).
3. **SCORE:** Run `python3 scripts/lint_persona.py <persona.md> --json` first, then score the artifact on substance (not routing, actions, or deployed quality).
4. **ENCODE / HANDOFF:** Resolve naming (named, unnamed, or brand-as-name) and emit `persona-handoff.json` for `agentforce-build`. Never emit or patch `.agent` syntax here.

Post-DRAFT spokes: **NAME**, **FILL OUT** (phrase book/lexicon/immutable copy), **ADJUST** (per-subagent semantic calibrations for existing surfaces only), and **CHECKLIST** (gap analysis).

## The 14 Persona Dimensions & Policies

Walk attributes in dependency order so upstream choices anchor downstream ones:

| Group | Dimensions & Allowed Values |
| --- | --- |
| **Personification** | `Not personal`, `Individuated`, `Anthropomorphic` (governs self-reference and opinion ownership) |
| **Register** | `Subordinate`, `Peer`, `Advisor`, `Coach` |
| **Voice** | Formality (`Formal`/`Professional`/`Casual`/`Informal`), Warmth (`Cool`..`Radiant`), Personality Intensity (`Reserved`..`Bold`), Reading Level (`Plain Language`/`Explained`/`Technical`) |
| **Tone** | Emotional Coloring (`Blunt`/`Neutral`/`Encouraging`/`Enthusiastic`/`Clinical`), Empathy Level (`Minimal`/`Understated`/`Moderate`/`Attuned`) + Tone Boundaries & Tone Flex |
| **Delivery** | Brevity (`Terse`/`Concise`/`Moderate`/`Expansive`), Humor (`None`/`Dry`/`Warm`/`Playful`) |
| **Chatting Style** | Emoji (`None`/`Functional`/`Expressive`), Formatting (`Plain`/`Selective`/`Heavy`), Punctuation (`Conservative`/`Standard`/`Expressive`), Capitalization (`Standard`/`Casual`) |

### Technical Framing & Reading Level Flex

- **Reading Level Flex:** Companion policy governing how technical density adapts from baseline; changes presentation only, never factual rigor.
- **Technical Explanation Policy:** Governs rhetorical framing when answering technical questions:
  - **Stay in frame:** Answer directly in the caller's frame without ceremonial cross-frame explanation.
  - **Selective bridge** *(default)*: Add one complementary bridge explanation when approved agent-design policy supports it.
  - **Pair routinely:** Prefer paired technical-evidence and business-outcome framing when approved policy supplies the relationship.

## Mandatory Structural Contracts (Enforced by `lint_persona.py`)

- **Version & date frontmatter:** Stamp every Markdown artifact with version and current local date.
- **Tone Flex:** Every shift row requires both an **Observable cue** and a **Reset condition** back to baseline.
- **Phrase Book:** Minimum 2 alternatives per category plus explicit `"palette, not a script"` and `"do not reuse the same phrase stem"` rules.
- **Never-Say & Lexicon:** At least 5 Never-Say entries; every Lexicon term must have a definition and never collide with an exact Never-Say term.
- **Immutable Content:** Must explicitly declare `"overrides persona and user style requests"` and its `"surrounding response shape"` policy.
- **Scope hygiene:** Never embed `modality voice:`, `voice_id`, `turn_timeout`, or STT config in `persona.md`; voice realization belongs in [voice-ux.md](voice-ux.md). Carry explicit Guardrails verbatim as adjacent handoff notes—never invent or rewrite them.
