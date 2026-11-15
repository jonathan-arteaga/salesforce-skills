---
id: D06
name: reference-numbers
category: input-collection
severity: medium
applies_to: [migrate]
detection:
  - keyword: "policy number"
    in: [instructions]
  - keyword: "pre-authorisation"
    in: [instructions]
  - keyword: "pre-auth"
    in: [instructions]
  - keyword: "reference number"
    in: [instructions]
  - keyword: "case number"
    in: [instructions]
  - keyword: "appointment ID"
    in: [instructions]
principle_refs: [P2, P10]
pattern_refs: [T-grounding-phone, T-repair-tier-2]
couples_with: [D07]
---

# Reference numbers (policy, pre-auth, IDs)

## Why it matters

Alphanumeric reference numbers (insurance policy numbers, pre-authorisation numbers, case IDs, claim numbers) are STT-hostile in the same ways as phone numbers, with one extra hazard: O/0 (letter-O / zero) ambiguity. "POL-O-2-3-4-5" can transcribe as "POL-zero-two-three-four-five" or "POL-O-23-45" depending on the engine.

Failure mode: the agent passes a wrong reference number to the booking API, the lookup fails, the caller has no idea why.

## Detection

Source collects any of:
- `policyNumber` / `policy_number`
- `preAuthorizationNumber` / `pre_auth_number`
- `caseNumber`
- `appointmentId`
- Free-text "reference" / "ID" fields

Without an explicit spell-confirm step.

## Chat example (before)

```
"Please provide your policy number."
```

(Trusts the chat input. In voice, this silently mishears.)

## Voice example (after) — recommended

**Single ask, digit-by-digit echo (these are always low-confidence cases):**

> Agent: And your policy number?
>
> Caller: POL-O-2-3-4-5.
>
> Agent: Just to confirm, P, O, L, then either letter-O or zero. Was that letter-O or zero? [pause] Got it. P, O, L, letter-O, two, three, four, five. Right?

**Standardize "zero" vs "oh"** — pick one across the agent and stick. "Zero" is the safer choice for ID strings (less ambiguous than "oh").

**For long reference numbers — chunk into groups of 3-4 digits:**

> Agent: Just to confirm, that's three-three-three, four-five-six, seven-eight-nine. Right?

**Tier-1 repair — offer the keypad if the value is all digits:**

> Agent: Sorry, didn't catch that. You can say it again, or if it's all numbers, tap it in on your keypad.

Keyed digits arrive as exact plain text — no STT mishear — so for a numbers-only reference the keypad is the fastest recovery (DTMF is GA; assume it's available). If the reference mixes letters and digits, the keypad can't carry the letters — stay on voice and move to letter-by-letter with improvised phonetics on the disputed segment (D07 rung 3).

**Tier-2 (chunked dictation):**

> Agent: Take it slowly, three or four characters at a time. What's the start?

## Voice example — alternatives

**Partial read-back when the value arrived cleanly.** When the number came in with no ambiguity — keyed on the keypad (DTMF arrives as exact plain text, nothing for STT to mishear), or matched against a record — confirm just the tail rather than every character: "Got it, order ending in six-six-three-one." Full digit-by-digit read-back is for the low-confidence spoken case; a clean capture only needs a light touch. (Keypad entry is also a privacy device for sensitive numbers — what's keyed isn't overheard.)

**Keypad-by-default for sensitive numeric values.** When the number is sensitive — a card, account, or claim number in a payments / fintech / health context — default to the keypad rather than asking the caller to say it aloud, and frame it as the norm, not a fallback: "I'll take that on the keypad. Go ahead and tap it in whenever you're ready." Keyed digits aren't overheard by anyone near the caller and don't sit in the transcript as spoken audio. Now that DTMF is GA, this is first-class capture, not a workaround — reach for it first on sensitive numerics, not only after a mishear. (Anything with letters is off the keypad — that's the alphanumeric path, D07.)

**Skip reference confirmation if the field is short and used only for display.** If the value flows to a confirmation email but isn't used for lookup, looser tolerance.

**Crossmodal lookup as fallback.** If the caller can't recall the number, offer SMS link to look up from email confirmation:

> Agent: No worries. I can text you a link to look it up if you'd prefer.

Verify the SMS integration before promising.

## Anti-patterns

- **Treating reference numbers like phone numbers.** Phone numbers are all-digits; reference numbers often mix letters and digits. The "oh / zero" ambiguity is more acute.
- **Reading characters concatenated.** "POL-23-45" runs as "pol twenty-three forty-five" in some engines. Read individually.
- **Saving without confirming.** A wrong policy number means the insurance check fails downstream — caller hits a confusing error in Phase 5 (booking commit) when the real cause was in Phase 2.
- **Reading "zero" as "oh" inconsistently across the same field.** Pick one read-out convention.

## Where it lives

- `Appointment_Management` Phase 2 step F (insurance branch).
- Any topic that collects case / appointment / claim IDs.
- Variables: `policy_number`, `pre_auth_number`, equivalents.
