---
version: "1.0.0"
date: 2026-09-10
---

# Persona handoff guide for Agent Script

Persona owns the complete character contract. It does not own Agent Script grammar, parsing, scaffolding, mutation, compilation, or deployment. The canonical owner is `agentforce-generate`; in SF Pi, the active `agentscript_authoring` family tool performs the corresponding inspect, mutate, and compile operations.

## Required sequence

### Greenfield

1. Complete and approve `persona.md`.
2. Write `persona-handoff.json` from `templates/persona-handoff-template.md`.
3. Hand the approved Persona contract and use-case context to `agentforce-generate` or the active Agent Script authoring tool.
4. Let that owner resolve current agent-type, access, schema, scaffold, and target-org requirements.
5. Do not claim that Persona produced a valid or preview-ready `.agent` file.
6. After a working Script exists, use `conversation-design` for representative scenarios when none exist. For a voice-bearing channel, pass the working Script, representative sample, `persona.md`, and `persona-handoff.json` to `voice-ux`. `voice-ux` reads the JSON first and checks `source_persona.sha256` against `persona.md`.

### Brownfield

1. Ask `agentforce-generate` or the active Agent Script authoring tool to inspect the existing `.agent` file and return current structured evidence.
2. Map that evidence to the Persona framework by substance.
3. Produce only a semantic Persona delta. A no-op is valid when the source already expresses the approved character.
4. Obtain explicit user approval for the semantic delta.
5. Hand the approved delta and original source path back to the canonical Agent Script owner for structural mutation, candidate verification, compile/check, and preview.

Persona never parses or rewrites `.agent` syntax itself. The handoff preserves each Lexicon term and definition, every exact Never-Say entry, immutable content, and every Tone Flex observable cue and reset condition without translating them into DSL fields.

## Handoff payload

Write `persona/[agent-name]/persona-handoff.json` with these conceptual fields:

- `schema_version`
- `mode`: `greenfield` or `brownfield`
- `source_persona`: path, artifact version, and SHA-256
- `source_agent`: existing `.agent` path or `null`
- `channel`
- `persona_contract`
  - Identity and Negative Identity
  - Personification
  - Register and linguistic Voice
  - Tone Boundaries and lexical Tone Flex
  - Delivery and Chatting Style
  - Phrase Book and Never-Say
  - Lexicon and immutable content
  - Technical Explanation framing preference, when applicable
- `semantic_deltas`: approved character changes described without Agent Script field syntax
- `adjacent_constraints`: verbatim references to explicitly supplied agent-design Guardrails or evidence policies; Persona does not transform them. Client requirements about how the agent should sound (for example, "the voice should read as neither clearly male nor clearly female") are captured the same way with `owner: "voice-ux"`; Persona records them verbatim and does not design or cast the voice
- `downstream_acceptance`: Persona invariants for `conversation-design`, `voice-ux`, and `agentforce-test`
- `next_owner`: `agentforce-generate`
- `status`: `draft` or `approved`

The payload contains no guessed action, route, variable, field, metadata, agent type, access user, or deployment target. Static-copy candidates, including an action progress wording candidate returned by canonical inspection, remain semantic suggestions; the canonical owner maps and validates them.

## Semantic delta contract

Each brownfield delta records:

- the intended character change;
- source evidence or explicit user request;
- scope: global character, an existing subagent calibration, or a static-copy candidate;
- exact Never-Say and immutable constraints that remain in force;
- unchanged facts, business rules, safety rules, routing, action contracts, and uncertainty policy; and
- user approval status.

The canonical Agent Script owner decides where and how the delta is encoded. Persona does not name or edit a DSL field to force the result.

## Technical Explanation boundary

Persona may record one rhetorical preference:

- **Stay in frame**;
- **Selective bridge**; or
- **Pair routinely**.

Agent design owns whether a bridge is factually supported, which sources are authoritative, field comparability, missing-data behavior, assumptions, recommendation confidence, and product suitability. Preserve those items as adjacent-constraint references and hand them to `agent-architecture` or `agentforce-generate`.

## Protected instruction text (opt-in)

Carry each explicitly protected instruction block in `adjacent_constraints`, with exact `verbatim_reference`, `text_role: agent_instruction`, `preservation: exact`, supplied intended scope, source reference and approval authority/status. Record unknown approval or placement as unresolved; do not invent it. Preserve multiple prescribed placements rather than deduplicating them. Never shorten, paraphrase, merge, recase, or repunctuate the block. Do not recite internal instructions as response copy or convert them into Persona traits. If another requirement conflicts, surface the conflict for the designated owner; do not silently resolve it.

Protection is an editing constraint; it does not grant higher runtime authority, establish Legal approval, or authorize unsafe behavior or deployment. The canonical authoring owner resolves placement and applies the block. Persona reports handoff prepared, not source encoding verified. Closed-loop application/readback orchestration is outside this change.

## Voice-channel handoff

Persona retains the lexical Tone Flex policy. `voice-ux` maps the approved triggers, maxima, cues, boundaries, and reset conditions to prosody and spoken interaction. It does not redefine the character.

Use this sequence for a new voice agent:

`persona` → `agentforce-generate` → `conversation-design` when a representative sample is needed → `voice-ux`

## Completion claim

ENCODE is complete when the Persona handoff is approved and written. That means the character contract is ready for the next owner. It does not mean an Agent Script artifact has been generated, compiled, previewed, published, or activated.
