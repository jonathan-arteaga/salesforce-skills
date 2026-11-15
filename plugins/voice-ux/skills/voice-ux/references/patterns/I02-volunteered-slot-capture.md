---
id: I02
name: volunteered-slot-capture
category: variables
severity: high
applies_to: [migrate, optimize]
couples_with: [I01, J01]
detection:
  - structural: "slot-filling gathers one field per turn but has no mechanism to capture extra details the caller volunteers in the same turn"
    in: [instructions, config]
  - regex: '@utils\.setVariables'
    in: [config]
principle_refs: [P2, P6]
pattern_refs: [T-grounding]
---

# Volunteered Slot Capture (never ask twice)

## Why it matters

One-question-per-turn (P6) is the right default: it spares working memory and matches how institutional encounters actually gather information. But it has a failure mode if you encode it naively — a caller who volunteers several details at once ("Afternoon, and the gate code is 4521") gets only the asked-for slot stored, and the agent re-asks for the rest a turn later. That's the interaction paying twice for the same information, at a cost in progressivity (the default expectation that talk keeps moving forward).

The fix is deterministic capture. `@utils.setVariables` takes a whole set of slots at once, and the `with <var> = ...` form (the `...` ellipsis means "the agent fills this from what was just said") lets a single action store every detail present in the turn — the asked-for one and any volunteered extras — in one pass. The instruction still enforces one question per turn; the variables just make sure nothing volunteered early is lost. Capture happens turn by turn as each detail arrives, so the closing summary reads back stored values rather than re-eliciting them.

This is the working-memory principle and the middle encoding surface meeting: prose keeps the turn to one question; the variable layer guarantees volunteered data survives.

## Detection

- Slot-filling gathers one field per turn (good) but the capture action stores only the current field, so volunteered extras are dropped and re-asked.
- Read-back / summary logic re-elicits values the caller already gave.
- `@utils.setVariables` is present but binds a single slot per call rather than the full set, OR uses fixed values where `...` (agent-fills) is wanted.

In optimize mode: capture exists but the action's description doesn't tell the agent to store volunteered-but-unasked slots, so the model only fills the one it asked about.

## Chat example (before)

```yaml
capture_time: @utils.setVariables
    description: "Store the caller's preferred time."
    with time_preference = ...
```

```
| Ask for one detail at a time: street address, then time, then gate code, then whether an adult is present.
```

(Each capture stores only its own slot. A caller who says "Afternoon, and the gate code is 4521" has the gate code dropped — the agent asks for it again next turn.)

## Voice example (after) — recommended

**One `setVariables` action that captures the whole set, `...` on each slot, with a description that licenses volunteered capture:**

```yaml
variables:
    street_address: mutable string = ""
        description: "The service street address."
    time_preference: mutable string = ""
        description: "Morning or afternoon."
    gate_code: mutable string = ""
        description: "Gate or entry code."
    adult_present: mutable boolean
        description: "Whether an adult over 18 will be present. Unset means unasked."

subagent book_installation:
    reasoning:
        instructions: ->
            | Ask for exactly one missing detail per turn, echoing the previous answer
              inside the next question ("14 Rosemary Lane. Morning or afternoon?").
        actions:
            capture_details: @utils.setVariables
                description: "Store every detail the caller gives, even several volunteered in one turn. Never re-ask for something already stored correctly."
                with street_address = ...
                with time_preference = ...
                with gate_code = ...
                with adult_present = ...
```

The instruction enforces one question per turn (P6); `capture_details` stores whatever the turn actually contained. A caller who volunteers two slots gets both saved in one pass and is never asked twice. Implicit grounding (T-grounding) rides along — echo the previous answer inside the next question, and the stored value is confirmed as it's saved.

## Voice example — alternatives

**Capture into `_spoken` companions at the same time (couples with I01).** When a volunteered value is high-stakes for read-back (a date, a currency amount), capture both the machine form and the spoken form in the same `setVariables` pass so the closing summary reads naturally without re-formatting.

**Guard the summary on all-slots-filled.** Pair with a conditional (`instructions: ->` with an `if` on the slots being set) so the summary/confirmation turn only fires once every required slot is present — reading back stored values, not re-asking. This is how P4's slot-by-slot example closes.

**Power-user fast path.** For flows a caller runs often (name + DOB in one breath), lean into volunteered capture — accept the whole utterance and store it — rather than stepping through slots the caller already anticipated. One-per-turn is the safe default for first-timers, not a universal law.

## Anti-patterns

- **Single-slot capture actions in a multi-slot flow.** Storing only the asked-for field guarantees re-asks whenever a caller volunteers ahead. Capture the set.
- **Fixed values where `...` is wanted.** `with gate_code = "unknown"` stores a literal; `with gate_code = ...` lets the agent fill it from the turn. Use the ellipsis for anything the caller provides.
- **Description that doesn't license volunteered capture.** Without "even several volunteered in one turn / never re-ask", the model tends to fill only the slot it just asked about.
- **Re-eliciting in the summary.** If the closing turn asks for values already stored, the capture was wasted. Read back `@variables`, don't re-ask.

## Where it lives

- `variables:` block — the slots being gathered.
- The gathering subagent's `reasoning.actions` — a single `@utils.setVariables` action binding the full slot set with `...`.
- `reasoning.instructions` — the one-question-per-turn rule and the all-slots-filled summary guard.
