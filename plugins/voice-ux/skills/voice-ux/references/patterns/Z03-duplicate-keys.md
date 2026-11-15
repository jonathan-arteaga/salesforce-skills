---
id: Z03
name: duplicate-keys
category: lint
severity: high
applies_to: [migrate, optimize]
detection:
  - structural: "offline validator emits a warning matching Duplicate key '<key>'"
    in: [config]
auto_fix: false
principle_refs: []
---

# Duplicate keys — surface and resolve

## Why it matters

The offline validator emits a warning when the same key appears twice in the same map:

```
WARN  <line>:<col> [duplicate-key]  Duplicate key '<key_name>'
```

Usually a copy-paste error, merge artefact, or accidental redeclaration. YAML "later wins" semantics mean one declaration is silently dropped at runtime — almost always a bug, but the validator only warns, so the prior policy let it ship.

## Detection

Parse the validator output. For every diagnostic with code/message matching `Duplicate key '<key>'`, record:
- Line number (and a small context window — usually a couple of lines either side)
- The duplicated key name
- The two (or more) values associated with that key

## No auto-fix (surface only)

Surface to the developer with the location, the duplicated key, and both values. Schematic of the prompt the skill should produce:

```
Z03 — Duplicate key warning at line <L1>:
  Key: <key_name>
  First occurrence (line <L1>):
    <key_name>: <value_a>
  Second occurrence (line <L2>):
    <key_name>: <value_b>

YAML semantics make the LATER occurrence (line <L2>, <value_b>) win at runtime.
The earlier one is silently dropped.

Choose one of:
  (a) Keep the LATER occurrence (delete line <L1>). YAML default; usually safe.
  (b) Keep the EARLIER occurrence (delete line <L2> — and update any downstream
      logic that assumed the later value).
  (c) Both are wrong — show me the broader context, I'll patch manually.
```

Phase 7 does not proceed to hand-back while Z03 warnings remain. Auto-fixing is off the table because picking the wrong duplicate silently breaks runtime in a way that's hard to spot in review.

## Anti-patterns

- **Auto-deleting the earlier occurrence because YAML says later wins.** Most common case but not universal — sometimes the developer added the second declaration by accident and the first is intended.
- **Conflating Z03 with the "per-topic action declarations are NOT duplicates" rule.** That rule is about action-name reuse across separate topic scopes (legitimate). Z03 is about the same key appearing twice inside a single map (always a bug).

## Where it lives

Phase 7.2 pre-emptive lint. Detected from validator warnings (not source pre-scan). Re-runs after every iteration — a Phase 7 edit could introduce a new duplicate.

## Worked example

A field-test run produced a `.agent` with `Duplicate key '<key>'` warnings on a single map (a variable block declaring the same key twice). Under the prior policy, warnings didn't block hand-back, so the duplicate slipped through to publish, where YAML "later wins" semantics silently dropped one declaration. Z03 detects the same case post-iteration and halts hand-back, requiring the developer to choose which occurrence to keep.
