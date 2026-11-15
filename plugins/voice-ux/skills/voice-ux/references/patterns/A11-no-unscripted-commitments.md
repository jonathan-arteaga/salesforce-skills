---
id: A11
name: no-unscripted-commitments
category: system-instructions
severity: high
applies_to: [migrate, optimize]
couples_with: [G02, A10]
detection:
  - keyword: "I've noted that"
    in: [response_templates, instructions, system.instructions]
  - keyword: "I've saved"
    in: [response_templates, instructions, system.instructions]
  - keyword: "someone will call you back"
    in: [response_templates, instructions, system.instructions]
  - structural: "no global rule against improvising answers or promising actions the script doesn't perform"
    in: [system.instructions]
principle_refs: [P2, P11]
pattern_refs: [T-translate-empty, T-grounding]
---

# No unscripted commitments

## Why it matters

On a call, anything the agent says it did is heard as a promise. "I've noted that for the team", "someone will call you back tomorrow" and "I've updated your address" all sound like commitments, and the caller hangs up believing them. In chat the same words sit next to a visible confirmation, or the lack of one. On voice there's nothing else to check against.

The model makes these up easily. When a request falls outside what its actions can do, the helpful-sounding move is to say it's been handled. And when a write runs after the reply (the after-speech pattern in Layer E), the model is speaking before the action has happened, so it can't know the action worked. (Sources: Voice Agent Optimization Guide, appendix fail-safe rule; Agentforce Voice Agent Assessor, Personality, field-proven, Oct 2026.)

This is the commitment-side twin of T-translate-empty ("say nothing found instead of inventing"). That rule covers invented facts; this one covers invented actions.

## Detection

- Copy or instructions in which the agent claims an action without a matching action or flow behind it: "I've noted that", "I've saved", "I've passed that on", "someone will call you back".
- A spoken success line on a turn where the write runs in `after_reasoning` (it can't have finished yet).
- No global rule telling the agent what to do when it's unsure or the request is out of scope.

## Chat example (before)

```
system:
    instructions: "You are a helpful assistant for Northwind. Help customers with their orders and resolve any issue they raise."
```

> Customer: Can you make sure the driver knows to leave it round the back?
> Agent: Of course! I've noted that for the driver. Is there anything else I can help with?

(No action writes delivery notes. Nothing was noted.)

## Voice example (after) — recommended

**Add a fail-safe rule to `system.instructions`:**

```
FAIL-SAFE: If you're unsure, or the caller asks for something your actions can't do,
don't improvise and don't invent a commitment. Say plainly what you can't do here
and offer the one way forward you have. Never say anything was saved, noted, sent,
or arranged unless an action in this conversation did it and returned success.
```

> Caller: Can you make sure the driver knows to leave it round the back?
> Agent: I can't add delivery notes on this call, I'm afraid. The tracking link in your email lets you add one. Is there anything else on the order?

## Voice example — alternatives

**After-speech write (fire-and-forget logging).** When a call-result or case-note write runs in `after_reasoning` for latency, the spoken line describes what *will* happen, not what did: "I'll log that for the team" rather than "I've logged that." Keep G02 for writes whose outcome the caller has to hear (booking, payment): run them first and confirm on success.

**Escalation as the way forward.** If a human can do what the agent can't, offer the handover: "That's something the team can sort out. Want me to put you through?" Don't promise a callback the flow doesn't schedule.

## Anti-patterns

- **"I'll make a note of that"** with no note-writing action. The most common form, and the hardest to spot in review because it sounds polite.
- **Confirming a write before it's run.** "Done, your address is updated" on the same turn the update action is first called.
- **Promising a timeframe the agent doesn't control.** "You'll hear back within the hour."

## Where it lives

- `system.instructions` (global): the fail-safe rule.
- Per-subagent `reasoning.instructions` where an after-speech write runs: the "describe what will happen" wording.

## Mis-applications (optimize mode)

- **Pattern: rule present but contradicted locally.** A subagent instruction still says "confirm that you've saved it". Audit each subagent with a write action.
- **Pattern: over-hedged agent.** The rule is applied to scripted successes too, and the agent stops confirming bookings that did succeed. The rule only bites when no action returned success.
