---
id: D07
name: hard-to-capture-identifiers
category: input-collection
severity: medium
applies_to: [migrate, optimize]
detection:
  - keyword: "member ID"
    in: [instructions]
  - keyword: "confirmation code"
    in: [instructions]
  - keyword: "order number"
    in: [instructions]
  - regex: '\b(alphanumeric|letters and numbers|case-sensitive|case sensitive)\b'
    in: [instructions, response_templates]
  - structural: "alphanumeric identifier captured by voice with no phonetics/handoff ladder or business-process challenge"
    in: [instructions]
principle_refs: [P2, P10, P12]
pattern_refs: [T-grounding-email, T-repair-tier-2]
couples_with: [D02, D04, D05, D06, D08]
---

# Hard-to-capture identifiers

## Why it matters

Alphanumeric identifiers — emails, member IDs, confirmation codes, order references, error codes — are the single most common friction point in voice UX. Speech makes every hard case harder at once: letter/letter confusion (b/d/p/t/v/e/g), letter/digit ambiguity (O/0, I/1/L, S/5), and case, which voice can't carry at all. The field-specific patterns handle each surface (D02 names, D04 phone, D05 email, D06 reference numbers); **this pattern is the decision ladder that sits above them** — how to *think about* any hard identifier before reaching for a capture technique.

The ladder is best-first: each rung is only worth taking if the rung above it doesn't apply.

## Detection

- The flow captures an alphanumeric identifier by voice (member ID, confirmation code, order/case reference, email) with no phonetic-repair strategy and no handoff option.
- Copy prescribes the format up front ("it's case-sensitive", "letters and numbers") — a chat-shaped instruction voice callers can't act on (T-translate-4).
- Nobody has asked whether the identifier *needs* to be alphanumeric at all.

## Chat example (before)

```
"Please provide your membership ID. It is case-sensitive and contains both
letters and numbers."
```

(In chat the caller reads it off a card and types it. In voice, "case-sensitive" is meaningless aloud and the mixed string mishears constantly.)

## Voice example (after) — recommended

**The ladder, best-first:**

**0 — Look it up; don't capture it at all.** The best-captured identifier is one the caller never says. If a cleaner identifier is available — ANI (the calling number, D04), an account or phone number, an order number — use it to retrieve the record and confirm, rather than collecting the hard string (D05 strategy 0).

**1 — Challenge the business process: does it have to be alphanumeric?** Raise it as an audit finding, not a caller question. A numbers-only identifier is dramatically easier: cleaner STT *and* a clean keypad (DTMF) fallback (D06). Many "IDs" are alphanumeric by legacy habit, not necessity.

> Audit finding (`[consider]` / `[review needed]`): "`member_id` is captured by voice as a case-sensitive alphanumeric string — the hardest possible voice field. Recommend the business consider a numbers-only identifier (or a phone / order-number lookup) for phone callers; it removes the capture problem rather than mitigating it."

**2 — If it can be numeric → keypad.** Numbers-only? Take it on the keypad and read the tail back (D06). Offer the keypad on the first mishear; make it the default for sensitive numbers.

**3 — If it must stay alphanumeric → slow, letter-by-letter, improvised phonetics on repair.** Ask for it slowly, one character at a time. On the *first mishear of a segment*, disambiguate that segment with improvised phonetics — "was that B as in boy, or D as in dog?" — applied only to the disputed characters, not the whole string. (This is the repair *standard*, not an exotic fallback; see D05.) Standardise "zero" not "oh", and don't try to speak case — capture as heard, normalise downstream (D06).

> Agent: "Go ahead and read me the ID slowly, one character at a time."
>
> Caller: "B — four — G — seven — D."
>
> Agent: "Let me check the letters. B as in boy, then G as in golf, then D as in dog? [pause] Got it: B, four, G, seven, D."

**4 — For exact characters → hand off to a screen (type, don't say).** When the string must be captured character-perfect (payment reference, long code) and there's no identifier to look it up by, the elegant move is a **type-don't-say handoff** — text the caller a prompt, have them type it, read it back from the session (D08). This is where P12 (voice-to-screen handoff) does the work voice can't.

## Voice example — alternatives

**Partial capture + lookup.** Sometimes you don't need the whole string — the last four characters plus a name or postcode uniquely identify the record. Capture the minimum discriminating slice, not the full identifier.

**Two rungs at once on a known-hard field.** For a notoriously hard field with older callers, skip straight from ask to offering the keypad (if numeric) or the handoff (if not) rather than grinding through letter-by-letter repair.

## Anti-patterns

- **Format prescription on first ask.** "It's case-sensitive, letters and numbers" — voice callers can't reverse-parse this; constrain only on repair (T-translate-4, T-repair-tier-2).
- **Spelling the whole string phonetically every time.** Improvised phonetics are for the *disputed segment* on a mishear, not a default full-string "A as in apple, B as in boy…" recital — that's slow and patronising when the caller was clear.
- **Reaching for the keypad on alphanumeric fields.** DTMF is numeric-only; a keypad can't send "G" cleanly. Alphanumeric goes to phonetics (rung 3) or handoff (rung 4), never the keypad.
- **Accepting the hard field without ever challenging it.** The cheapest fix is often upstream — a numbers-only identifier — and it never gets raised because capture "works" most of the time.

## Where it lives

- `reasoning.instructions` of any topic that collects an identifier — as the strategy the field-specific patterns (D02/D04/D05/D06) plug into.
- The business-process challenge (rung 1) surfaces in the audit findings and Layer E (process recommendation), not as a runtime turn.
- Handoff mechanics (rung 4) live in D08 / P12.

## Mis-applications (optimize mode)

- **Pattern: voice agent captures a case-sensitive alphanumeric ID with digit-by-digit read-back but no phonetic repair.** `[consider]` — add improvised phonetics on the disputed segment (rung 3).
- **Pattern: hard identifier with no handoff path on a channel that has SMS.** `[consider]` — a type-don't-say handoff (D08) is available and unused.
- **Pattern: the identifier could be numbers-only but is alphanumeric.** `[review needed]` — surface the process challenge; don't silently rewrite a business identifier, but do flag it.
