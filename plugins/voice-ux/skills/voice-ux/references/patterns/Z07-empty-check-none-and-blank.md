---
id: Z07
name: empty-check-none-and-blank
category: lint
severity: medium
applies_to: [migrate, optimize]
couples_with: [I01, I02, B04]
detection:
  - regex: '^\s*if\s+@variables\.\w+\s*==\s*""\s*:'
    in: [before_reasoning, after_reasoning, instructions]
  - regex: '^\s*if\s+@variables\.\w+\s+is\s+None\s*:'
    in: [before_reasoning, after_reasoning, instructions]
  - regex: '^\s*if\s+@variables\.\w+\s*!=\s*""\s*:'
    in: [before_reasoning, after_reasoning, instructions]
principle_refs: []
---

# Empty checks cover both None and ""

## Why it matters

A string variable can be empty in two ways. It's `""` when the script defaults it, and `None` when an action output, a linked variable or a pre-chat field arrives with no value. A check for only one of them lets the other through. (Source: Agentforce Voice Agent Assessor, Script reliability, field-proven, Oct 2026.)

On voice the failure is audible. A spoken-form companion (I01) built from a `None` reads out as "your appointment is on None". An I02 "already captured?" guard that only checks `""` skips the question and moves on with nothing. A B04 pre-chat check passes and the agent greets "Hi, ." This skill writes these guards, so it has to write them in the form that works.

## Detection

- `if @variables.X == "":` or `if @variables.X is None:` used alone as an emptiness test.
- `if @variables.X != "":` used alone as a "we have it" test.

Booleans and numbers are out of scope. `is not None` on a boolean slot (I02's `adult_present`) is the correct test there.

## Auto-fix (recommended)

Test both forms:

```
# Empty
if @variables.postal_code is None or @variables.postal_code == "":
    ...

# Present
if @variables.postal_code is not None and @variables.postal_code != "":
    ...
```

Both forms compile offline (validator 2.9.8). For a long `and` chain of "present" checks, keep each variable's pair together so a reviewer can read it.

## Where it lives

`before_reasoning` and `after_reasoning` guards, procedural `instructions: ->` conditionals, and the variable checks written by I01, I02 and B04/H02.

## Block hand-back?

No. Auto-fixed before hand-back. Report the count in the iteration table.
