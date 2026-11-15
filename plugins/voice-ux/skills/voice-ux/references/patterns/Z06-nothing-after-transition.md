---
id: Z06
name: nothing-after-transition
category: lint
severity: high
applies_to: [migrate, optimize]
couples_with: [J01]
detection:
  - structural: "statement (set, run, if) after a `transition to` in the same block"
    in: [before_reasoning, after_reasoning, instructions]
  - keyword: "unreachable-code"
    in: [validator_output]
principle_refs: []
---

# Nothing after a transition

## Why it matters

In Agent Script, a `transition to` ends the block it sits in. Anything after it in the same block never runs. The org-side compiler doesn't error on this: the `set` that resets a counter, or the `run` that logs the call result, just doesn't happen. The call sounds fine in preview and the bug shows up later as a stuck counter or a missing record. (Source: Agentforce Voice Agent Assessor, Script reliability, a field compiler probe, Oct 2026.)

This skill writes exactly the blocks where this bites. J01 puts a counter reset and an escalation `transition` in the same `after_reasoning`, and I02 and the Tier 2 latency advice add `set` and `run` lines next to guards. A reset written below the transition looks correct and never fires.

The offline validator (2.9.8) catches it as a **warning**, `[unreachable-code] Code will never execute after 'transition'`, so it's easy to scroll past. Treat that warning as blocking.

## Detection

- In any `before_reasoning`, `after_reasoning` or `instructions: ->` block: a `set`, `run`, `if` or `|` line that follows a `transition to` at the same indent level.
- Any `unreachable-code` diagnostic in the validator output.

A `transition` inside an `if` doesn't end the outer block. Lines after the `if` still run on the path where the condition is false. That's fine and not a hit.

## Auto-fix (recommended)

Move the work above the transition. Order inside a block is: update state, run side effects, then transition last.

```
# Before: the reset never runs
after_reasoning:
    if @variables.repair_attempts >= 3:
        transition to @subagent.handover
        set @variables.repair_attempts = 0

# After
after_reasoning:
    if @variables.repair_attempts >= 3:
        set @variables.repair_attempts = 0
        transition to @subagent.handover
```

If the work genuinely belongs to the target stage, move it into that subagent's `before_reasoning` instead.

## Where it lives

Every `before_reasoning`, `after_reasoning` and procedural `instructions: ->` block, in source and in anything Phase 7 writes.

## Block hand-back?

Yes, until fixed. The fix is mechanical, so auto-fix it and re-validate. If moving the line would change behavior (it reads a variable the transition's target sets), surface it as `[review needed]` instead.
