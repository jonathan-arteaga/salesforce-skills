---
id: Z08
name: no-silent-generative-turn
category: lint
severity: high
applies_to: [migrate, optimize]
couples_with: [D08, H06]
detection:
  - regex: '(?i)\|.*\b(output|say|respond with|reply with|return)\s+nothing\b'
    in: [instructions, system.instructions]
  - regex: '(?i)\|.*\b(stay|remain|keep)\s+silent\b'
    in: [instructions, system.instructions]
  - regex: '(?i)\|.*\b(don''t|do not)\s+(say|respond|reply|speak)\s+anything\b'
    in: [instructions, system.instructions]
  - regex: '(?i)\|.*\bempty (response|reply|string)\b'
    in: [instructions, system.instructions]
principle_refs: [P7]
---

# No silent generative turn

## Why it matters

A generative stage has to produce a reply. Tell it to output nothing and the model doesn't stop cleanly: the runtime treats the empty turn as a failure and runs the stage again. In one field build a stage told to "output nothing" looped 49 times in a single turn before the call gave up. (Source: Agentforce Voice Agent Assessor, Script reliability, field-proven, Oct 2026.) The caller hears dead air, and each loop is a full LLM pass.

The instruction is tempting in voice, which is why the skill lints for it. D08 (type-don't-say waits), hold-while-the-caller-finds-something turns and "let the caller finish" designs all seem to call for the agent to stay quiet.

## Detection

Any `|` instruction line, in a subagent's `reasoning.instructions` or the global `system.instructions`, that tells the model to output nothing, stay silent, give an empty reply, or not say anything.

Don't flag constrained output ("say only 'Take your time.'") or scoped prohibitions ("don't say the account number").

## Auto-fix (recommended)

Give the turn a short line to say instead, and let the platform handle the waiting:

| The source wanted… | Replace with |
|---|---|
| Wait while the caller types on the keypad (D08) | A short holding line ("Take your time.") and the speak-up timers (H06) for the wait itself |
| Wait while the caller finds a document | "Sure, I'll hold on." Then the speak-up config re-prompts if nothing comes |
| A logic-only step that shouldn't speak | Move the logic into `before_reasoning` / `after_reasoning` or a router with no prompt, so no generative pass runs at all |

## Where it lives

`reasoning.instructions` in every subagent, and `system.instructions`.

## Block hand-back?

Yes, until fixed. The loop doesn't show up in an offline validation or a short preview. If the silent turn is load-bearing for the design, surface it as `[review needed]` with the replacement line.
