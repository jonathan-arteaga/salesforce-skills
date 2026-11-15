---
id: D08
name: type-dont-say-capture-handoff
category: input-collection
severity: medium
applies_to: [migrate, optimize]
detection:
  - keyword: "verification link"
    in: [instructions, response_templates]
  - keyword: "I'll text you"
    in: [instructions, response_templates]
  - regex: '\b(SMS|text message|send you a link)\b'
    in: [instructions, response_templates]
  - structural: "exact-character value captured by voice on a channel with SMS/screen handoff, no type-dont-say option"
    in: [instructions]
principle_refs: [P12]
pattern_refs: [T-grounding-email, T-repair-tier-3]
couples_with: [D05, D07]
---

# Type-don't-say capture handoff

## Why it matters

Some values simply shouldn't be spoken: a long payment reference, a case-sensitive code, an email the caller keeps mishearing on read-back. Voice can't reliably carry exact characters and can't carry case at all. The elegant top rung of the identifier ladder (D07) is to stop trying — **hand off to a screen and let the caller type it**. This is a *capture* handoff, distinct from the more familiar *delivery* handoff (texting a tracking link, C04); here the screen is the input surface, and voice orchestrates it.

The trap is over-promising the magic. There's a production-honest version that works today, and an aspirational version that isn't out-of-the-box — say which you're designing.

## Detection

- An exact-character value (email, payment / confirmation reference, code) is captured by voice on a channel that *has* SMS or a screen-handoff channel (per the modality trait matrix), with no type-don't-say option offered.
- Copy promises a "verification link" or "I'll text you a link" without confirming the integration exists (D05 flags the same on email).

## Chat example (before)

```
"Please read out your payment reference so I can locate the transaction."
```

(A 16-character case-mixed reference, read aloud, over a phone line. It will not survive.)

## Voice example (after) — recommended

**Production-honest, caller-cued read-back.** The agent texts a prompt; the caller types the value and says when they're done; the agent reads it back from the messaging session and confirms. Announce what / where / why first (P12), and get consent:

> Agent: "That reference is easier to get right typed than spoken. I can text this number a secure link to enter it. Is that okay?"
>
> Caller: "Yeah."
>
> Agent: "Sent. Open the link, type the reference, and tap send. Then just say 'done'."
>
> Caller: "…done."
>
> Agent: "Got it. Reference ending seven-Q-four-two. That's the one. Shall I pull it up?"

Key properties:
- **Caller-cued.** The agent waits for the caller's "done", then reads back the submitted value. It does **not** rely on the value silently appearing mid-turn.
- **Pre-populate + preserve state (P12).** Everything already collected travels to the screen; the caller types only the hard value, and voice resumes where it left off.
- **Voice stays in control.** The caller can always fall back to voice ("I'd rather just say it") — frame the handoff as the smart choice, not a failure (P12).

**Generalises beyond email.** Same shape for payment references, org / error IDs, document uploads — anything needing exact characters (D07 rung 4). D05 is the email-specific instance of this handoff.

## Voice example — alternatives

**Aspirational — event-driven live-sync (flag as not-OOTB).** The "magic" version: the caller submits on the screen and the agent *automatically* continues the instant the write lands — no "say done" cue — via an event-driven barge-in on the live session. This is a genuinely better experience, but it is **not available out-of-the-box** on Agentforce Voice today: it needs a screen / web surface wired to the voice session with event write-back the runtime can react to. Design toward it, but ship the caller-cued read-back above and mark live-sync as a Layer E / roadmap item — don't script it as if it works.

**No crossmodal channel at all.** If the modality traits show no SMS / screen handoff, this rung is unavailable — Tier-3 repair falls back to human handoff with full state (T-repair-tier-3), not a screen.

## Anti-patterns

- **Promising a link the integration can't send.** Verify SMS / screen handoff exists before offering it (same caution as D05).
- **Assuming silent live-sync.** Scripting "once you've submitted, I'll continue automatically" implies event-driven write-back that isn't OOTB — the caller submits, then sits in silence while the agent waits for a signal that never comes. Use the explicit "say done" cue.
- **Dropping collected state at the handoff.** Making the caller re-enter name / DOB on the screen because voice-side state didn't travel (P12 violation).
- **Using it for values that don't need it.** A single spoken word, or a numeric value (keypad, D06), doesn't warrant a screen handoff — reserve it for genuinely exact-character strings.
- **No consent / no framing.** Firing a text without "is that okay?" and the what/where/why is jarring and can read as a phishing attempt.

## Where it lives

- `reasoning.instructions` of the topic collecting the hard value — the handoff turn + the caller-cued read-back + resume.
- Rung 4 of the D07 ladder; the email-specific case is D05.
- The integration itself (SMS / screen channel) is a platform dependency — surface in Layer E if not already wired.

## Mis-applications (optimize mode)

- **Pattern: agent scripts an automatic continue after screen submit.** `[changed]` — live-sync isn't OOTB; switch to the caller-cued "say done" read-back.
- **Pattern: handoff offered but announces only "I'll text you a link" (no what/where/why).** `[consider]` — add purpose + resume framing (P12 mis-application).
- **Pattern: hard exact-character field, SMS channel available, no handoff used.** `[consider]` — the elegant rung is on the table and unused (D07 rung 4).
