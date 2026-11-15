---
version: "2.0.0"
date: 2026-09-10
---

## PHASE 4: ENCODE / HANDOFF

ENCODE translates an approved Persona into a handoff for the system that owns the target authoring surface. Persona does not parse, scaffold, mutate, compile, validate, publish, or activate Agent Script.

## Preflight: NAME

Resolve the Persona name decision before handoff. In bounded one-pass mode, use an explicitly supplied working title or a conservative functional placeholder, record the assumption, and never invent a person-like name.

## Select the target

Choose one target:

1. **Agent Script:** default for greenfield and for an existing `.agent` source.
2. **Existing legacy Agentforce Builder:** brownfield maintenance only. Customers cannot create new legacy Builder agents.

Do not load both target guides in one run.

- Agent Script → `references/persona-handoff-guide-agentscript.md` + `templates/persona-handoff-template.md`
- Existing legacy Builder → `references/persona-encoding-guide-builder-legacy.md` + `templates/persona-encoding-template-builder-legacy.md`

## Agent Script path

### Canonical inspection and authoring

For a brownfield `.agent` source, ask `agentforce-generate` or the active Agent Script authoring tool to inspect the file and return current structured evidence. Do not use a Persona-owned parser. Map only the returned character-bearing content to the Persona framework.

For greenfield work, Persona does not select current Agent Script schema values or build a scaffold. It writes the approved character handoff, then delegates creation to `agentforce-generate` or the active Agent Script authoring tool. That owner resolves current agent type, access, metadata, syntax, and target-org requirements.

### Handoff artifact

Write `persona/[agent-name]/persona-handoff.json` from `templates/persona-handoff-template.md`.

The handoff contains:

- the versioned Persona source and SHA-256;
- the complete character contract;
- approved semantic Persona deltas for brownfield work;
- verbatim references to adjacent agent-design constraints;
- downstream acceptance criteria;
- the original `.agent` path when one exists; and
- `next_owner: agentforce-generate`.

It contains no Agent Script syntax, field paths, schema values, scaffold, actions, routes, variables, access users, metadata, or deployment target.

### Brownfield delta

Treat the existing agent as the baseline. A no-op is valid. Add only a semantic Persona delta that is:

- explicitly requested or supported by strong source evidence;
- missing from the current character behavior;
- likely to change expression;
- scoped to global character, an existing subagent calibration, or a static-copy candidate; and
- approved by the user.

Do not produce a source patch or claim structural safety. The canonical Agent Script owner applies the approved delta, freezes the accepted Surface edit list, verifies the candidate, and performs compile/check and preview.

## Legacy Builder path

The legacy guide remains a narrow provisional brownfield adapter because no current canonical sf-skills owner was found for Persona-field maintenance in existing Builder agents. It may map approved Persona content into known Builder fields, but it must:

- remain brownfield-only;
- identify its platform guidance as provisional;
- avoid Agent Script syntax;
- preserve existing configuration outside Persona-bearing fields; and
- recommend migration or canonical platform review when current metadata behavior is uncertain.

Do not expand this adapter with new platform lifecycle guidance.

## Protected instruction text

For explicitly protected instruction blocks, preserve exact text and supplied scope in the optional Persona attachment. Agent Script uses the existing adjacent-constraint handoff with optional preservation metadata; no source mutation or verification is claimed. Existing legacy Builder includes a separate copy-ready protected block only for supplied placement, otherwise an unresolved-placement note. Report prepared, not applied. Never turn these internal instructions into customer-facing response copy, infer approval, or trim them to meet a field limit. This does not expand Persona into policy design or closed-loop lifecycle orchestration.

## Adjacent constraints

Persona may carry explicitly supplied Guardrails, evidence policies, comparison rules, and immutable text to the handoff as verbatim references. It does not infer, score, rewrite, or encode agent-design constraints.

Technical Explanation Policy records only the rhetorical framing preference: stay in frame, bridge selectively, or pair routinely. `agent-architecture` and `agentforce-generate` own evidence sources, factual support, comparability, missing-data behavior, assumptions, recommendation confidence, and product suitability.

## Downstream scenarios and testing

Persona emits acceptance criteria, not runtime evidence:

- use `conversation-design` for representative happy-path, error, fallback, and handoff scenarios;
- use `agentforce-test` for preview/evaluation and regression evidence on a built agent; and
- use `designing-agentforce-labs:evaluating-conversations` for quality scoring of real conversation transcripts.

## Voice-bearing channels

Use this sequence for greenfield work:

`persona` → `agentforce-generate` → `conversation-design` when a representative sample is needed → `voice-ux`

For brownfield work, pass the approved Persona, existing working Script, and representative sample directly to `voice-ux` after the canonical Agent Script owner has applied any approved Persona delta.

Persona retains situational Tone Flex in word choice and response patterns. `voice-ux` owns prosodic realization and voice-specific design. Existing `voice-ux` implementation scope is unchanged by this Persona handoff.

## Completion claim

ENCODE exits when the Persona handoff or provisional legacy Builder artifact is written and approved. For Agent Script, say **Persona handoff ready for `agentforce-generate`**. Do not say the agent is generated, valid, compiled, preview-ready, published, or active.

Present the HUB.
