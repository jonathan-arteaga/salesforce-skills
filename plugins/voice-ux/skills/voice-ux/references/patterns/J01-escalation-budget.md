---
id: J01
name: escalation-budget
category: flow-control
severity: high
applies_to: [migrate, optimize]
couples_with: [I02]
detection:
  - structural: "repair / no-match handling exists only in instructions, with no deterministic failure counter or after_reasoning guard"
    in: [instructions, config]
  - keyword: "after_reasoning"
    in: [config]
  - regex: 'repair_attempts|failure_count|no_match_count|escalat'
    in: [config, instructions]
principle_refs: [P3, P10]
pattern_refs: [T-repair-tier-3]
---

# Escalation Budget (deterministic repair backstop)

## Why it matters

The repair ladder (P10 / T-repair) is instruction wording — the reasoning engine decides, turn by turn, which tier to use. But *when to give up* should not be left to that same judgement. A caller who has failed three times needs the call handed to a human whether or not the agent thinks it's still making progress. The budget is not a judgement, so it belongs somewhere the reasoning loop can't reach.

`after_reasoning` is a real Agent Script block that runs once per turn, **after** the agent decides what to say, unconditionally. Pairing a failure counter (a variable) with an `after_reasoning` guard gives a hard escalation budget: increment the counter on any turn the caller couldn't be understood, and the moment it hits the limit, `transition to` a handover subagent — no matter what the reasoning engine wanted to do. This is the deterministic backstop under **T-repair-tier-3** (human handoff with full state preservation). The counter can't route on its own, so the handover subagent has to exist and bind `@utils.escalate`.

This is the middle encoding surface in action: conversational behavior lives in prose instructions; the *sequential guarantee* lives in a variable and the deterministic block around the reasoning loop.

## Detection

Source has repair/no-match handling but no deterministic ceiling:
- Repair tiers described in instructions, but nothing counts global failures across the call, and there is no `after_reasoning` guard forcing escalation.
- A no-match/no-input counter exists but is only *read* inside `reasoning` (so the LLM can still decide to ignore it).
- Escalation is described ("hand off after a few tries") but not guaranteed — it depends on the model choosing to.

In optimize mode: an `after_reasoning` guard exists but the counter is incremented unreliably (inside a conditional the LLM controls, or LLM-filled via `with repair_attempts = ...`), the counter is read but never incremented, or the handover target is missing.

## Chat example (before)

```
| If you can't understand the caller after a few tries, transfer them to a human agent.
```

(Instruction-only. In chat, a stuck user can retype or abandon. In voice, "a few tries" is unbounded — the model may loop on repair indefinitely, and the caller hangs up before any handoff fires.)

## Voice example (after) — recommended

**Failure counter + `after_reasoning` guard + handover subagent:**

```yaml
variables:
    repair_attempts: mutable number = 0
        description: "Counts turns where the caller could not be understood."
    turn_unclear: mutable boolean = False
        description: "True when this turn's caller input could not be made out."

subagent account_lookup:
    reasoning:
        instructions:
            | If nothing recognizable was heard, ask once: "Sorry?"
            | If one element is unclear, name it and offer specific choices.
            | If you have a strong candidate, verify it ("Did you mean...?").
            | For names and long numbers, ask for spelling or digit-by-digit.
            | Never blame the caller. Never repeat a failed prompt word-for-word.
        actions:
            flag_unclear: @utils.setVariables
                description: "Call only on a turn where you could not make out what the caller said. Never call it on any other turn."
                with turn_unclear = True
    after_reasoning:
        if @variables.turn_unclear:
            set @variables.repair_attempts = @variables.repair_attempts + 1
            set @variables.turn_unclear = False
        if @variables.repair_attempts >= 3:
            transition to @subagent.handover

subagent handover:
    reasoning:
        actions:
            to_human: @utils.escalate
```

The instructions hold the graduated ladder (P10); `after_reasoning` holds the ceiling **and the arithmetic**. The split matters: the model only has to make a yes/no judgement ("could I make this turn out?") and call `flag_unclear`, whose value is the literal `True`, not an LLM-filled `...`. The increment itself is a deterministic `set` in `after_reasoning`, which also resets the flag for the next turn. Don't let the model fill the count (`with repair_attempts = ...`): it has to read the current value, add one, and write it back correctly every time, and when it doesn't, the counter stalls and the handover never fires. Escalation hands the call to a human through Omni-Channel routing — ideally with the transcript and collected variables attached, so the caller doesn't repeat themselves (T-repair-tier-3: state always travels with the handoff).

## Voice example — alternatives

**Count global trouble, not per-field.** A caller who hit trouble on three *different* questions is telling you the voice channel isn't working for them today, even if no single field failed three times. A single call-scoped `repair_attempts` counter captures that; per-field counters miss it. Reset it only if you genuinely want to forgive early trouble after a clean stretch — usually you don't.

**Lower the budget for high-friction contexts.** Noisy-line or accessibility flows may warrant escalating at 2 rather than 3. It's one number in one place — easy to tune.

**Combine with a repair-tier variable.** If the design also tracks *which* tier the last repair used, the `after_reasoning` guard can escalate on "reached tier 3 twice" rather than a flat count. More precise, more moving parts — start with the flat count.

## Anti-patterns

- **Ceiling in `reasoning`, not `after_reasoning`.** If the escalation decision sits inside the reasoning loop, the LLM can talk itself out of it. The whole point is that the guard fires regardless.
- **Counter incremented by the model at will.** "Increase the counter when you think you're stuck" is soft. Have the model raise a boolean flag through a `setVariables` action with a tight description, and do the increment yourself in `after_reasoning`.
- **Counter filled by the model (`with repair_attempts = ...`).** The model has to do the arithmetic, and it won't always get it right. A counter that never actually increments looks fine in review and never escalates in production. Bind a literal flag (`with turn_unclear = True`) and `set` the count deterministically.
- **Counter read but never incremented.** A guard like `if @variables.repair_attempts >= 3` with nothing anywhere that adds to the counter. It's easy to copy from a slide and it can never fire.
- **Guard with no handover target.** `transition to @subagent.handover` where `handover` doesn't exist, or exists but doesn't bind `@utils.escalate` — the counter maxes out and nothing happens.
- **Escalation that drops state.** Handing off without the transcript/variables forces the caller to start over with the human. Carry state (T-repair-tier-3).

## Where it lives

- `variables:` block — the failure counter.
- The active subagent's `reasoning.actions` — the `@utils.setVariables` flag (`turn_unclear = True`).
- The active subagent's `after_reasoning:` block — the deterministic `set` increment, the flag reset, the guard, and `transition to`.
- A `handover` subagent binding `@utils.escalate`.

## Mis-applications (optimize mode)

- **Pattern: repair ladder is well-written but has no hard ceiling.** Tiers 1–3 exist in instructions; nothing forces the exit. Add the counter + `after_reasoning` guard.
- **Pattern: `after_reasoning` guard exists but the counter is set inside an LLM-controlled conditional.** The guarantee leaks. Move the increment into `after_reasoning` as a deterministic `set`, driven by a boolean flag the model raises.
- **Pattern: the counter is LLM-filled (`with repair_attempts = ...`) or never incremented at all.** `[changed]`: replace it with the flag plus a deterministic `set @variables.repair_attempts = @variables.repair_attempts + 1`.
- **Pattern: escalates but doesn't preserve state.** Same as T-repair-tier-3 mis-application — the handoff must carry transcript + variables.
