---
version: "2.0.0"
date: 2026-09-10
---

# Persona target selector

Select the downstream owner before loading handoff guidance.

| Evidence | Persona output |
|---|---|
| Greenfield agent | Agent Script Persona handoff |
| Existing `.agent` source | Agent Script Persona handoff with approved semantic deltas |
| Existing legacy Agentforce Builder agent | Provisional legacy Builder field adapter |
| Greenfield request naming legacy Builder | Explain that customers cannot create new legacy Builder agents; produce an Agent Script handoff |

## Load contract

For Agent Script, load only:

- `references/persona-handoff-guide-agentscript.md`
- `templates/persona-handoff-template.md`

For existing legacy Builder maintenance, load only:

- `references/persona-encoding-guide-builder-legacy.md`
- `templates/persona-encoding-template-builder-legacy.md`

Never load both paths in one ENCODE run.

## Shared Persona invariants

- Preserve the approved Identity, Personification, dimensions, lexical Tone Flex, Phrase Book, Never-Say, Lexicon, and immutable content.
- Keep adjacent agent-design Guardrails and evidence policies as verbatim handoff references, not Persona content.
- Do not invent subagents, actions, routes, variables, metadata, access users, or deployment targets.
- Do not claim runtime or compile evidence from a Persona artifact.

## Agent Script authority

`agentforce-generate` or the active Agent Script authoring tool owns current parsing, structure, syntax, scaffolding, mutation, candidate verification, compilation, validation, preview, publication, and activation.

Persona owns only the semantic character contract and approved character deltas. Its Agent Script output is:

`persona/[agent-name]/persona-handoff.json`

## Voice handoff

For voice-bearing channels, first obtain a working Script through the canonical Agent Script owner. Use `conversation-design` when a representative sample is still needed, then pass the Script, sample, `persona.md`, and `persona-handoff.json` when present to `voice-ux`.

## Legacy Builder caveat

The legacy Builder path is a narrow provisional brownfield adapter because no current canonical sf-skills owner was found for this maintenance surface. Do not expand it into lifecycle or migration guidance.
