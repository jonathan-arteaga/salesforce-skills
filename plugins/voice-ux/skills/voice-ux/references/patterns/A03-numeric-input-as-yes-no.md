---
id: A03
name: numeric-input-as-yes-no
category: system-instructions
severity: low
applies_to: [migrate]
detection:
  - keyword: "Do not interpret 0 or 1 as yes or no"
    in: [instructions]
  - keyword: "numeric inputs such as 0 or 1"
    in: [instructions]
  - keyword: "DTMF"
    in: [instructions]
principle_refs: [P8]
---

# Numeric input as yes/no

## Why it matters

Rules guarding against "0 or 1 = yes/no" are chat-shaped dead code in voice. They take up token budget and create cognitive load for the LLM during every turn, for no benefit.

DTMF (touch-tone keypad input) **is** available in Agentforce Voice (shipped 2026-07-28), but it doesn't reintroduce the need for this rule. Keyed digits arrive at the reasoning engine as **plain text**, identical to a transcribed spoken turn — there is no separate "keypad" channel the agent has to interpret, and nothing DTMF-specific to encode in the `.agent` file. A caller pressing `1` and a caller saying "one" reach the agent the same way; neither is a confirmation. So the guard is dead whether or not DTMF is in play, and A02's affirmative-detection handles any genuine ambiguity.

## Detection

Source has a directive like:
- "Do not interpret numeric inputs such as 0 or 1 as yes or no"
- "When asking the user to confirm or refuse, only accept explicit textual responses. Do not interpret numeric inputs such as 0 or 1 as yes or no."

This pattern coexists with A02 (confirmation rule) — usually they're sentences in the same paragraph.

## Chat example (before)

```
When asking the user to confirm or refuse, only accept explicit textual
responses. Do not interpret numeric inputs such as 0 or 1 as yes or no. If
the response is ambiguous or numeric-only, prompt the user again with a
clear question.
```

## Voice example (after) — recommended

Strip the rule entirely.

```
[deleted]
```

The rule about ambiguous responses is preserved by A02 (confirmation rule); the numeric-input clause is the only piece that's dead in voice.

## Voice example — alternatives

**No alternative retains this rule.** Even where DTMF is enabled, keyed digits arrive as plain text and are not confirmations, so the numeric-guard clause stays deleted. If the design uses the keypad for character-exact numeric capture (order/reference/card numbers), that's a *capture* concern — the digits flow into a variable like any spoken number (see D06) — not a reason to guard against `0`/`1` meaning yes/no.

## Anti-patterns

- **Keeping the rule "just in case".** It bloats every turn's prompt and the LLM has to evaluate it on irrelevant inputs (e.g., when the user says a phone number).
- **Replacing "0 or 1" with "zero or one" thinking it now applies to voice.** A user saying "zero" or "one" in voice is not confirming anything; the affirmative-detection in A02 handles legitimate ambiguity.
- **Re-adding the guard because "DTMF is on now".** Keyed digits are plain text, not a distinct signal the agent must special-case. The rule is dead regardless.

## Where it lives

`system.instructions` — usually a single sentence inside the broader confirmation rule paragraph. Edit out, leave the rest of A02 in place.
