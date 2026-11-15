---
id: D05
name: email-address
category: input-collection
severity: medium
applies_to: [migrate]
detection:
  - keyword: "email address"
    in: [instructions]
  - keyword: "valid email"
    in: [response_templates]
  - regex: 'contain.*@.*symbol'
    in: [instructions]
  - keyword: "top-level domain"
    in: [instructions]
principle_refs: [P2, P12]
pattern_refs: [T-grounding-email]
couples_with: [D07, D08]
---

# Email address

## Why it matters

Email is the hardest single field to capture in voice. The local part can include letters, digits, hyphens, dots, and underscores; the domain has its own delimiters; the TLD is rarely spoken explicitly ("dot com" vs. "dot co dot uk"). Caller speech rate matters: "j-dot-smith-at-gmail-dot-com" is barely intelligible at normal speed.

Strategies, best-first:
0. **Look it up, don't spell it.** The best-captured email is one the caller never spells. If you can capture a clean identifier they say or key — a phone number, an account or order number — retrieve the address already on file and confirm it in a single turn. Reserve spelling out (or a screen handoff) for when there's genuinely no identifier to cross-reference against. Improvised phonetics on a *disputed* character ("was that M as in Mike?") is the repair standard when spelling is unavoidable — the letter-by-letter treatment lives in D07 — but it shouldn't be the default path.
1. **Type-don't-say handoff** (cheapest when there's no identifier and a screen channel exists): text the caller a prompt, have them type the address and say "done", then read it back from the session (D08). This *captures* the address rather than mailing a link to one you haven't confirmed yet. Requires an SMS / screen-handoff channel.
2. **Implicit echo on high confidence, letter-by-letter on low.** Standard T-grounding-email.
3. **Letter-by-letter on first ask** (most robust, slowest). Use only when audience is older or accent-mismatch-prone.

## Detection

Source has email collection (`save_patient_email`, `patient_email` variable, `customerEmail` field) without spell-confirm logic. Sometimes accompanied by a strict format-validation rule ("must contain exactly one '@' symbol, a recognized TLD") — treat the format rule as Tier-2 only, not first ask.

## Chat example (before)

```
"Please provide your email address."
```

```
"The email address you provided appears to be invalid. Please provide a
valid email address (for example john.smith@example.com)."
```

## Voice example (after) — recommended

**Single ask, implicit echo on high confidence:**

> Agent: What's your email address?
>
> Caller: john dot smith at gmail dot com.
>
> Agent: J-O-H-N dot S-M-I-T-H, at gmail dot com. Got it.

**On low confidence — explicit letter-by-letter for the local part, spell-out for the domain:**

> Agent: Just to confirm, J, O, H, N, dot, S, M, I, T, H, at gmail dot com. Is that right?

**Tier-1 repair on miss:**

> Agent: Sorry, missed part of that. What's the email again?

**Tier-2 repair (constrained, second miss):**

> Agent: Could you say it letter by letter for the bit before the at-sign?

**Soft check on apparent inconsistency** (couples with E02 — name vs email mismatch):

> Agent: Quick check. I've got Sarah Jones as the patient and john dot smith at gmail dot com as the email. Is that the right email for this booking, or should it go somewhere else?

## Voice example — alternatives

**Skip email entirely; use phone only.** If the platform can SMS confirmations, email is redundant. Drop the field.

**Crossmodal capture handoff — type, don't say (D08).** When there's no identifier to look the address up by and letter-by-letter is failing, hand off to a screen: text the caller a prompt, have them type the address and say "done", then read it back from the session. This *captures* the address rather than mailing a link to one you haven't confirmed. Production-honest and caller-cued — see D08 for the full pattern (including why event-driven live-sync isn't out-of-the-box).

**Verification round-trip (a different move).** If the goal is to *prove the address works* rather than capture it, sending a confirm-link to a tentatively-heard address and waiting for the caller to click is legitimate — but it's a delivery/verification handoff, not character capture, and it only works if the address was heard closely enough to reach the caller. Verify the SMS / email integration before promising either.

**Spell-back digit-by-digit including the domain:** for medical or legal records where any error is unacceptable.

> Agent: That's J-O-H-N, dot, S-M-I-T-H, at, G-M-A-I-L, dot, C-O-M. Right?

## Anti-patterns

- **Reading the literal "@" symbol as "at-symbol".** Always use "at".
- **Reading "dot" inconsistently as "period" or "full stop".** Pick one — "dot" is the voice-UX standard.
- **Stating the format prescription on first ask.** "Must contain exactly one at-symbol, a domain, and a recognized top-level domain" — voice users can't reverse-parse this.
- **Validation error voiced verbatim.** "The email address you provided appears to be invalid" — replace with Tier-1 repair.
- **Asking the caller to spell it from the start when they're competent.** If the caller spoke clearly and the local part has obvious-letter content, implicit echo is enough.

## Where it lives

- Phase 2 of booking topics.
- No-availability callback flow.
- Variables: `patient_email`, `customerEmail`.
- Validation logic / save action.
