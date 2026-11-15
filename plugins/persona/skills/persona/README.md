# Agentforce Persona

Design AI agent personas for Salesforce Agentforce using **Identity + Degree of Personification + 13 expression dimensions**, including scoped Reading Level Flex, definition-bearing lexicons, and evidence-bound technical explanation policy.

An agent persona is a designed personality that tells an AI agent who it is and how to express itself so it comes across naturally as a consistent character suited to its context and users.

This skill designs a versioned Persona contract, controlled calibration examples, a Persona-specific evaluation, and a semantic handoff to downstream owners. It does not recreate Agent Script parsing, syntax, mutation, validation, conversation-flow design, or runtime testing.

Persona owns situational Tone Flex in word choice and response patterns. `agentforce-generate` owns Agent Script authoring. `conversation-design` owns representative scenarios. `agentforce-test` owns runtime proof. For voice-bearing channels, `voice-ux` owns spoken adaptation and prosody after a working Script and representative sample exist.

## Quick Start

Provide a brand guide, URL, prior Persona, or text description. The skill drafts the character contract, shows controlled calibration examples, and prepares explicit handoffs to downstream design and build owners.

The default interactive practitioner mode pauses at designed checkpoints. If the user explicitly says they are unavailable for follow-up or asks to finish end to end, bounded one-pass mode records safe assumptions, writes all requested artifacts first, and returns a compact artifact index.

```text
PHASE 1:  INPUT → CONTEXT → IDENTITY → DIMENSIONS → PERSONA
PHASE 2:  HUB → calibrate / phrase book / never-say / lexicon / score / handoff
```

## Output

Files land in `./persona/[agent-name]/` relative to the user's working directory:

- `persona.md` — design artifact: who the agent is, how it sounds, what it never does
- `persona-calibration.md` — controlled Persona response examples, not a conversation flow
- `evaluation.md` — 100-point Persona rubric (on request)
- `persona-handoff.json` — semantic contract for `agentforce-generate`
- `builder-fields.md` — provisional existing-Builder maintenance output only
- `checklist.md` — completeness review on request
- `stakeholder-worksheet.md`, `workshop-outline.md` — stakeholder questions or a facilitated workshop plan, available before or after a draft; worksheets can also be delivered inline

## Resources

| File | Purpose |
|---|---|
| `SKILL.md` | Compact phase/spoke dispatcher and output contract |
| `references/draft-phase.md` | DRAFT procedure and state contract |
| `references/refinement-mappings.md` | REFINE calibration examples, mappings, and single-axis regeneration |
| `references/scoring-rubric.md` | SCORE extraction rules and 100-point rubric |
| `references/encode-detail.md` | ENCODE target selection and downstream handoff contract |
| `references/spokes.md` | NAME, FILL OUT, ADJUST, CHECKLIST, WORKSHEET, and WORKSHOP procedures |
| `references/stakeholder-question-policy.md` | Standalone stakeholder worksheet and workshop guidance |
| `references/interaction-design-notes.md` | Cross-surface interaction guidance |
| `references/persona-framework.md` | Identity + Degree of Personification + 13 expression dimensions |
| `references/framework-manifest.json` | Machine-readable dimension, component, workflow, and encoding inventory |
| `references/personification-migration.md` | Retired-to-current Personification mapping and review rules |
| `references/persona-encoding-guide.md` | Base-encoder selector; load exactly one strategy |
| `references/persona-handoff-guide-agentscript.md` | Semantic Persona handoff to the canonical Agent Script owner |
| `references/persona-encoding-guide-builder-legacy.md` | Legacy Agentforce Builder persona encoding |
| `references/workshop-question-policy.md`, `workshop-scenario-seeds.md` | WORKSHOP spoke inputs |
| Archetype examples | Drover, Steady Hand, Y.T., and Concierge: configured examples to adapt, not certified drop-in personas |
| Templates | Persona, calibration, stakeholder worksheet, workshop, checklist, semantic handoff, and legacy Builder maintenance outputs |
| `scripts/check_framework_manifest.py` | Validates the machine-readable framework inventory against shipping source |
| [`references/attributions.md`](references/attributions.md) | Required license attribution |
| [`RELATED-READING.md`](RELATED-READING.md) | Optional related research, books, and platform guidance |
