---
id: Z04
name: em-dash-in-spoken-prose
category: lint
severity: medium
applies_to: [migrate, optimize]
couples_with: [A09]
detection:
  - regex: '^\s*\|.*—'
    in: [instructions, system.instructions]
  - regex: '(welcome|error|progress_indicator_message|speak_up_message|waiting).*—'
    in: [welcome, error, actions, config]
principle_refs: []
---

# Em-dash in spoken prose

## Why it matters

A voice can't render an em-dash (—) cleanly. Depending on the model and voice, TTS treats it as a pause, ignores it, or produces an audible artefact, so the same line sounds different from one call to the next. A full stop, a comma, or an ellipsis gives a predictable break. (Sources: *Designing for the Ear* enablement deck, which bans spoken em-dashes in the persona rules; A09.)

The model also copies the style of its instructions. If the `|` instruction lines are full of em-dashes, the generated replies will be too, so the lint covers instruction prose and not just literal spoken strings. Em-dashes inside multi-line quoted strings have separately broken the Agent Script parser during edits (SKILL.md Phase 7.3), which is one more reason to keep them out.

This is a lint, not a transform. It runs with the other Z-class checks before and after pattern application.

## Detection

Flag any `—` (U+2014) in:
- `|` instruction lines, in `system.instructions` and in every subagent's `reasoning.instructions`
- `messages.welcome` and `messages.error`
- `progress_indicator_message` strings
- `speak_up_config` messages and `outbound_filler_sentences` / `filler_sentences` entries

Don't flag em-dashes in `description:` fields, comments, or the skill's own explanatory documents. They are never spoken.

En-dashes (–) in numeric ranges inside instructions ("1–2 sentences") are fine, because the model reads them as "to". They're out of scope for this lint.

## Auto-fix (recommended)

Rewrite each occurrence by meaning, not by mechanical substitution:

| The em-dash is doing… | Replace with | Before → after |
|---|---|---|
| A sentence break | Full stop | "Booking that now — one moment…" → "Booking that now. One moment…" |
| A parenthetical aside | Commas | "Your order — the blue one — shipped Tuesday." → "Your order, the blue one, shipped Tuesday." |
| A held beat before key information | Ellipsis or full stop | "Your total is — eighty-five pounds." → "Your total is… eighty-five pounds." |
| Joining two clauses in an instruction | Full stop, or a semicolon in instruction prose | "Ask once — don't repeat." → "Ask once. Don't repeat." |

Then add one line to the global `system.instructions`, so the generated replies follow suit: "Don't use dashes in what you say. Use commas and full stops for pauses."

Re-validate after the batch. Replacing a character inside a `|` block is parser-safe; replacing it inside a quoted multi-line string should be done with `Edit`, one occurrence at a time.

## Where it lives

Every user-audible string surface listed under Detection, plus the instruction prose that shapes generated replies.

## Block hand-back?

No. Auto-fixed before hand-back. Report the count in the iteration table.
