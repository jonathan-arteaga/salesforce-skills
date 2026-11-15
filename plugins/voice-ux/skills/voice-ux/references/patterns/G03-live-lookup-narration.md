---
id: G03
name: live-lookup-narration
category: latency-masking
severity: medium
applies_to: [migrate, optimize]
detection:
  - structural: "read/lookup action narrated with false certainty or not at all during the wait"
    in: [instructions]
  - regex: '\b(retrieving|fetching|querying|processing your request)\b'
    in: [instructions, response_templates]
  - keyword: "please wait while"
    in: [instructions, response_templates]
principle_refs: [P7]
pattern_refs: [T-latency-lookup, T-latency-pre-announce]
couples_with: [G01, G02]
---

# Live-lookup narration

## Why it matters

When the agent looks something up mid-call — an order, an availability window, an account — the caller hears a pause and then a result. Two things make that stretch feel natural or not: *how the agent narrates the wait*, and *how it hedges the result*. This is the spoken-register companion to the latency machinery: G01 is the `progress_indicator_message` **field** (the mechanism that plays a line during an action); G02 is pre-action narration before an **irreversible commit**. G03 is about a **read / lookup** — the honest, present-tense way an agent talks *while and just after* it fetches data it doesn't yet have.

Two moves:
1. **Narrate the lookup in the present, like a colleague.** "Let me pull that up… okay, I've got your order here." Not silence, not a chat-shaped status ("Retrieving your request…").
2. **Hedge the result until it's confirmed.** "Looks like your order shipped Tuesday" / "I'm showing two slots on Thursday" reads as honest and correctable; "Your order shipped Tuesday", stated flat off a fuzzy lookup, sets up a hard contradiction if the caller says "no it didn't". Hedging leaves room for repair (P10) and matches how people actually report what they're reading off a screen.

## Detection

- A read / lookup action runs with no verbal narration during the wait (silence), or with chat-shaped status language ("Retrieving…", "Processing your request…", "Please wait while I…").
- Lookup results are stated with flat certainty regardless of match confidence — no "looks like", "I'm showing", "it seems".

## Chat example (before)

```
| Call get_order_status.
| Respond with: "Your order status is: {{status}}."
```

(Chat shows a spinner then a field value. In voice this is silence, then a blunt declaration.)

## Voice example (after) — recommended

**Narrate the lookup, then hedge the read-back:**

```
| Pre-announce, present tense: "Let me pull that up…" (see G01 for the
| progress_indicator_message on the action itself).
| Call get_order_status.
| Report the result hedged, not flat: "Okay, looks like your order shipped
| Tuesday and it's due Friday." Land the useful fact last (P9).
```

> Agent: "Let me pull up your order… okay, I've got it here. Looks like it shipped Tuesday, due with you Friday."

**Rotate the narration tokens** (T-phrasebook holding set) so a caller who triggers several lookups doesn't hear "let me pull that up" four times: "let me check…", "one sec, pulling that up…", "let me take a look…".

**Hedge vocabulary:** "looks like…", "I'm showing…", "it seems…", "I've got … here". Reserve flat certainty for values you've grounded (a confirmed booking, a summarised commit).

## Voice example — alternatives

**High-confidence, low-stakes reads can skip the hedge.** If the lookup is deterministic and unambiguous (the caller's own name on file), a flat statement is fine — hedging everything sounds evasive. Hedge where the value is fuzzy, freshly fetched, or the caller might contradict it.

**Layered with G01 / G02.** On a slow lookup, the `progress_indicator_message` (G01) covers the wait; G03 governs the *words* of the lead-in and the read-back register. On a lookup that precedes an irreversible action, G02's pre-commit narration takes over for the commit itself.

## Anti-patterns

- **Silence during the lookup.** The caller assumes the line dropped (P7). Narrate.
- **Chat-shaped status.** "Retrieving your request", "Processing…", "Please wait while I query the system" — status-banner language, not speech. Say what a person would say.
- **Flat certainty off a fuzzy lookup.** "Your order shipped Tuesday" stated as fact, then the caller says it didn't — now you're contradicting yourself. Hedge freshly-read values.
- **Narrating the implementation.** "Querying get_order_status" — never expose the action name (same rule as G01/G02).
- **Over-hedging grounded facts.** "It looks like your appointment might be confirmed" after you just committed it — undermines trust. Once grounded, state it plainly.

## Where it lives

- `reasoning.instructions` of any topic that performs a read / lookup — the present-tense lead-in and the hedged read-back register.
- Pairs with the action's `progress_indicator_message` (G01) on slow lookups.

## Mis-applications (optimize mode)

- **Pattern: pre-announce present but results stated flat off low-confidence lookups.** `[consider]` — add hedge vocabulary so a wrong read is correctable.
- **Pattern: chat-shaped "Processing…" carried into a voice lookup.** `[changed]` — replace with conversational present-tense narration.
- **Pattern: same lookup line every time.** `[consider]` — rotate the holding tokens (T-phrasebook).
