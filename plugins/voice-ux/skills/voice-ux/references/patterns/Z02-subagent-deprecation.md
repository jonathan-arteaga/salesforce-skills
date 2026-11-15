---
id: Z02
name: subagent-deprecation
category: lint
severity: high
applies_to: [migrate, optimize]
detection:
  - regex: '^topic\s+\w+:'
    in: [topics]
  - regex: '@topic\.\w+'
    in: [transitions, action_targets, instruction_bodies]
auto_fix: true
principle_refs: []
---

# Subagent deprecation — auto-rewrite

## Why it matters

The Agent Script grammar is in transition: the `topic <name>:` block-type keyword is deprecated and replaced with `subagent <name>:`. The `salesforce/agentscript` parser emits a deprecation warning on every `topic` block:

```
WARN  234:1 [deprecated-field]  'topic' is deprecated: Replace topic with subagent.
```

Warnings don't block publish today, but they accumulate in the editor and `topic` will eventually be removed from the parser. The rename is mechanical and runtime semantics are equivalent — confirmed across multiple production NGA deployments — so Z02 auto-fixes rather than surfacing as advisory.

## Detection

Scan the `.agent` file for two anchors:

- `^topic\s+\w+:` — block declarations at line start (one per declared topic)
- `@topic\.\w+` — namespace-prefixed reference paths (transitions, action targets, anywhere a topic is referred to by namespace)

Both anchors must be detected together. The skill records a count for each.

## Auto-fix (recommended)

Two coordinated mechanical rewrites:

**1. Block declarations** — every line matching `^topic\s+\w+:` → `subagent <name>:`

```
topic Foo_Topic:   →   subagent Foo_Topic:
topic Bar_Topic:   →   subagent Bar_Topic:
…
```

**2. Reference paths** — every `@topic.<Name>` → `@subagent.<Name>`

```
go_to_foo: @utils.transition to @topic.Foo_Topic
                              ↓
go_to_foo: @utils.transition to @subagent.Foo_Topic
```

Both passes apply as a single coordinated batch — declarations and references must flip together so the file stays internally consistent. Validate immediately afterward. No prompt — the rewrite is part of the skill's pre-emptive lint pass and runs before pattern application. Hand-back records both counts:

> Z02: rewrote M `topic` block declarations → `subagent`, plus K `@topic.<Name>` references → `@subagent.<Name>`

## Anchors — what is and isn't rewritten

Only these two regex anchors fire. Everything else containing the substring `topic` (descriptions, instruction bodies, comments, names like `My_Topic_Selector`) is left untouched.

| Anchor | Matches | Example |
|---|---|---|
| `^topic\s+\w+:` | Block declaration at line start | `topic My_Topic_Name:` |
| `@topic\.\w+` | Namespace-prefixed reference path | `@topic.My_Topic_Name` |

## Anti-patterns

- **Surfacing as advisory and letting the warning ship.** Prior policy; produced output carrying deprecation warnings into the developer's file.
- **Asking per-occurrence.** The rename is mechanical; per-block prompts add friction without value.
- **Renaming declarations without renaming references** (or vice versa). Always flip both.
- **Generalising Z02's ship-blocking behavior to all deprecation warnings.** Z02 blocks on `topic`-deprecation specifically because the skill knows this rewrite is safe and mechanical. Other deprecation warnings (future parser changes the skill hasn't categorised yet) are NOT ship-blockers by default — they're advisory, the agent compiles and publishes fine. Treat them as a signal to write a new pattern doc, not as a halt.

## Where it lives

Phase 7.2 pre-emptive lint, runs before pattern application. Both modes (migrate, optimize). Z02 is one-shot per file — once `topic` is rewritten, no later edit re-introduces it.

Track upstream parser changes at the [salesforce/agentscript CHANGELOG](https://github.com/salesforce/agentscript/blob/main/packages/language/CHANGELOG.md) — useful if `topic` is removed entirely (Z02 regex would need updating) or if the rewrite ever stops being semantics-preserving.

## Worked example

Verified end-to-end against a real multi-topic source. Pre-rewrite, the offline validator emitted N deprecation warnings — one per `topic` block declaration. After Phase 7.2 applied (M block declarations + K reference paths) coordinated edits in a single batch, the validator returned 0 errors / 0 warnings / 0 info. Char delta is deterministic: exactly (M + K) × 3 bytes (one extra char per `topic`→`subagent`).
