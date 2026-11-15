---
version: "1.0.0"
date: 2026-09-10
---

# Persona calibration: {{AGENT_NAME}}

> Source persona: `{{PERSONA_FILE_PATH}}`
> This artifact demonstrates character expression in controlled response pairs. It is not a conversation flow, representative scenario set, or runtime test.

## Routine expression

**Fixed input and facts:** {{One supplied user utterance plus the facts the response may use}}

| Variant | Agent response | Persona cue demonstrated |
|---|---|---|
| Baseline | {{One agent response}} | {{Identity, Register, Voice, Tone, Delivery}} |
| Contrast, if requested | {{Same facts with one selected Persona dimension changed}} | {{Single changed dimension}} |

## Reading Level Flex expression *(when adaptive)*

**Same supplied facts:** {{Fixed facts}}

| User signal | Reading Level response | Expected change |
|---|---|---|
| Baseline | {{One response}} | {{Baseline terminology density and glossing}} |
| Approved flex trigger | {{Same facts, one allowed level shift}} | {{Terminology/glossing only; no factual or length-driven drift}} |
| Material domain change | {{One response}} | {{Reset to baseline and re-evaluate}} |

## Tone Flex expression

**Trigger:** {{One approved Tone Flex trigger}}
**Facts held fixed:** {{Facts and explicit status}}

| State | Agent response | Expected cue |
|---|---|---|
| Baseline | {{One agent response}} | {{Baseline wording/response pattern}} |
| Flexed | {{One agent response}} | {{Declared lexical/discourse shift and maximum}} |
| Reset | {{One agent response to a new routine prompt}} | {{Return to baseline}} |

## Boundary expression

**Pressure:** {{One request that invites a Never-Say, Tone Boundary, or immutable-content violation}}

| Agent response | Boundary preserved |
|---|---|
| {{One agent response}} | {{Exact Never-Say / Tone Boundary / immutable rule}} |

## Downstream acceptance criteria

Pass these criteria to the next owner. Do not claim they were runtime-tested here.

- Preserve supplied facts, explicit statuses, uncertainty, and permitted recommendations.
- Preserve action, routing, and capability ownership from agent design.
- Preserve exact Never-Say entries and immutable content.
- Make Tone Flex observable through the approved wording or response pattern, then reset on the declared condition.
- Use `conversation-design` for representative multi-turn scenarios.
- Use `agentforce-test` for preview/evaluation and regression evidence on a built agent.
