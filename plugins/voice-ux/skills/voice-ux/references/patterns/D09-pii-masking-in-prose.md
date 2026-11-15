---
id: D09
name: pii-masking-in-prose
category: input-collection
severity: high
applies_to: [migrate, optimize]
couples_with: [D04, D06, E02]
detection:
  - keyword: "card number"
    in: [instructions, response_templates]
  - keyword: "social security"
    in: [instructions, response_templates]
  - keyword: "account number"
    in: [instructions, response_templates]
  - regex: '(?i)(read|repeat|confirm) (back )?(the |their )?(full )?(card|account|ssn|social security|routing) (number|digits)'
    in: [instructions]
  - structural: "agent output or readback includes a variable holding a full card, bank-account, or national ID number"
    in: [instructions, response_templates]
principle_refs: [P2]
pattern_refs: [T-grounding-money]
---

# PII masking in spoken prose

## Why it matters

A voice reply is heard by whoever is near the phone: a speakerphone in an open office, a car with passengers, a family kitchen. It also lands in the call recording and the transcript. Reading a full card number or national ID aloud exposes it in all three places, even if the caller said it a moment earlier.

The platform won't do this for you. Trust Layer PII masking doesn't apply to agent output, so masking has to be written into the instructions. The Voice Quality Heuristics v1.2 (Trust) score a full 16-digit card or 9-digit SSN read-back at the floor, *even if the caller just said it*. The rule: refer to sensitive identifiers by their last four digits ("the card ending in 1234").

Scope matters. This applies to **financial and government identifiers**: payment cards, bank account and routing numbers, SSNs and national IDs, tax IDs. Ordinary lookup IDs (order numbers, case numbers, customer numbers) aren't gated and keep their normal digit-by-digit confirmation (D06). Phone numbers keep D04's confirmation rules. If you can't tell which kind an identifier is, treat it as financial.

## Detection

- Instructions that read back or confirm a full card, account or national ID number.
- Response templates or readback summaries (E02) that interpolate a variable holding the whole value.
- Optimize mode: transcripts where the agent repeats a full card or SSN, including on the confirmation turn.

## Chat example (before)

```
| Confirm the payment details with the customer: "You'd like to pay with card {!@variables.card_number}, is that right?"
```

(In chat, the UI usually masks this field, or the customer is the only one looking at the screen. In voice, all 16 digits are spoken aloud and recorded.)

## Voice example (after) — recommended

```
| Never say a full card, bank account, or social security number aloud, even if the caller has just said it.
| Refer to it by its last four digits only: "the card ending in 1234".
| To confirm a card, say: "That's the card ending in {!@variables.card_last4}. Shall I use it?"
```

Hold the last four in their own variable (`card_last4`), set by the action that captures or looks up the card, so the full value is never in the spoken template.

> **Agent:** That's the Visa ending in four-four-one-two. Shall I use it?
> **Caller:** Yes.
> **Agent:** Done. The payment's gone through.

## Voice example — alternatives

**Masked readback inside a summary (couples with E02).** In an irreversible-action summary (T-grounding-money), mask inside the summary as well: "So that's eighty-five pounds, on the card ending in four-four-one-two, paid today. Shall I go ahead?"

**Collection via keypad.** For collecting the full number in the first place, prefer DTMF entry (D07's keypad step), so the digits are never spoken by either side. The confirmation then uses the masked form above.

## Anti-patterns

- **"Just confirming, that's 4111 1111 1111 4412?"** Full read-back for confirmation. Confirm the last four instead; if the caller's entry was wrong, the downstream validation catches it.
- **Masking only the agent's first mention.** A later summary or error message ("I couldn't charge card 4111…") puts the full number back. Mask on every turn.
- **Relying on the Trust Layer.** It doesn't mask agent output. The instruction is the only control.
- **Masking ordinary lookup IDs.** "Order ending in 789" makes order confirmation harder for no privacy gain. Use D06.

## Where it lives

Global `system.instructions` (the never-say-in-full rule), plus any subagent `reasoning.instructions` and response templates that confirm or summarise payment or identity data. A last-four companion variable (`card_last4`, I01-style) set by the capturing action.

Where the model doesn't need the full value at all, the stronger fix is upstream: anything in an action output the model can see, it can say. Recommend `filter_from_agent: True` on that output as a `[consider]`, and route the choice between it and `is_used_by_planner` to `agent-architecture` (see `T-translate-plumbing`).

## Mis-applications (optimize mode)

- **Pattern: the instruction masks, but the template interpolates the full variable.** The model follows the template. Swap the variable for the last-four companion.
- **Pattern: masking applied to phone numbers.** D04's digit-by-digit confirmation is the right control for phone numbers; masking them breaks callback confirmation.
