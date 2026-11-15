---
id: F03
name: sensitive-flag-redaction
category: crisis-and-safety
severity: high
applies_to: [migrate, optimize]
couples_with: [F01]
detection:
  - structural: "record fields include a marker that changes what is safe to say aloud (e.g. dv_flag, confidential_address, protected_caseworker, safeguarding_marker)"
    in: [instructions, config]
  - keyword: "confidential"
    in: [instructions, response_templates]
  - keyword: "safeguarding"
    in: [instructions, response_templates]
  - regex: 'dv_flag|domestic_violence|protected_address|caseworker_flag'
    in: [instructions, config, response_templates]
principle_refs: [P9, P12]
---

# Sensitive-flag redaction

## Why it matters

Some records carry a marker that changes what is safe to say aloud. Common examples: a domestic-violence bypass flag on a customer account, a confidential-address flag on a healthcare record, a protected-caseworker flag on a government or social-services record, a safeguarding marker on a young or vulnerable-adult record. The names differ by domain; the shape is the same.

Voice has two failure modes text doesn't:
1. **Earshot.** Anyone within audible range of the caller hears the answer. A "your address is 14 Rosemary Lane" that would sit on a chat panel becomes a broadcast when a coercive partner is in the room.
2. **The flag itself is sensitive.** "I see there's a note on your account…" tips off anyone listening that the account has protection on it. The flag being spoken aloud is itself the leak.

When a sensitive flag is set, the agent needs four behaviours in combination. Missing any one of them breaks the protection.

## Detection

Source has fields that indicate protection status on a record, and the agent's readouts include any of those fields or acknowledge the flag itself. Look for:
- Field names like `dv_flag`, `confidential_address`, `protected_caseworker_flag`, `safeguarding_marker`, `sensitive_contact`.
- Any readout that uses `First_Name`, `Address_Line_1`, `Recipient_Name`, `Contact_Phone`, or similar without a guard for the sensitive flag.
- Instructions that voice the flag itself ("I can see there's a note on your account", "You have a confidentiality marker set").

In optimize mode: a redaction guard exists but only covers *some* of the fields the flag protects, OR the guard covers fields but the agent still acknowledges the flag verbally.

## Chat example (before)

```
| Read the recipient's name and delivery address back to the caller
| for confirmation before proceeding.

| If the record has a dv_flag set, add: "I've noted the confidentiality
| flag on this account — I'll be careful with what I say."
```

(Two problems: the readback voices the fields the flag protects, and the "I've noted" line acknowledges the flag out loud — exactly what a coercive listener would need to know.)

## Voice example (after) — recommended

**Four behaviours in combination:**

```
| Before voicing any personal detail, recipient name, delivery address,
| phone number, contact email, check whether a sensitive-record flag is
| set on the record (dv_flag, confidential_address, protected_caseworker,
| safeguarding_marker).

| If any such flag is set:
| 1. Do NOT voice the protected fields. Do not read the name, address,
|    or other flagged fields aloud, even for confirmation.
| 2. Do NOT acknowledge the flag itself. Never say "I see there's a
|    note", "you have a marker set", "I'll be careful", or any variant.
|    The flag being spoken is itself the leak.
| 3. Route detail delivery to SMS or email if a crossmodal channel is
|    available on this record: "I'll send that to your phone / your
|    email on file. You'll have it in a moment." Do not voice which
|    channel or which number; the record already has it.
| 4. Surface a silent-escalation path, a code word or phrase the caller
|    can use to be transferred to a trained specialist without the
|    listener understanding what happened. The code word is defined by
|    the customer's safeguarding team, not by the skill. If none has
|    been defined, that itself is a [review needed] item.

| For any confirmation the flow needs, use an implicit-echo alternative
| that references the record without voicing the field ("the delivery
| address we have on file" rather than the address itself).
```

The four behaviours are non-negotiable together. Doing three of them is not the pattern — a script that redacts the fields but still says "I've noted the flag on your account" fails.

## Voice example — alternatives

**Route the whole call to a trained specialist when the flag is set.** For high-risk flags (DV bypass, active safeguarding case), the safest design is to detect the flag at intake and warm-transfer the entire call to a human trained in the specific protection regime, rather than continuing the flow with redaction. Preserves state as usual. The tradeoff: waiting time. Use where the protection regime demands it.

**Fully offline verification.** For records where any read-aloud is unacceptable (some protected-caseworker regimes), all verification and detail delivery moves to SMS/email/portal; the voice call becomes purely a routing and transfer step. Rare, but the pattern exists.

## Anti-patterns

- **Redacting fields but acknowledging the flag.** "I can see there's a note on your account, so I'll skip that part" — the listener now knows there's a note. Just skip it.
- **Confirming redacted fields by voicing them.** "So that's the confidential address, correct?" — the whole point was not to voice it.
- **Silent failure when no crossmodal channel is available.** If the record has a sensitive flag and no SMS/email channel is configured, the agent should transfer to a human, not continue and hope. Flag as `[review needed]` in the audit.
- **A single global redaction rule that catches only some fields.** Sensitive flags typically protect a named set of fields (address, phone, dependents' names). The rule needs to enumerate them; a rule that only redacts `Address_Line_1` misses `Recipient_Name`.
- **Assuming the code word is generic.** The silent-escalation phrase is defined by the customer's safeguarding team for their trained specialists. The skill does not invent one.

## Where it lives

- `system.instructions` or the intake topic's `reasoning.instructions` — the flag check happens before any personal-detail readout.
- Any topic with a spell-back / readback flow (couples with D02, D04, D05, A02) — the redaction guard sits at the top of each readback.
- Layer E of the rewrite bundle — the customer's safeguarding-team-defined code word and the trained-specialist routing target are runtime configuration, not `.agent` content.

## Mis-applications (optimize mode)

- **Pattern: redaction guard covers only a subset of protected fields.** Enumerate the full field set the flag protects and guard each. A partial guard is not a guard.
- **Pattern: flag acknowledged verbally despite fields being redacted.** Remove the acknowledgment. The redaction is silent by design.
- **Pattern: silent-escalation path missing.** The four behaviours are a set; a script with only the first three is a `[review needed]` — the customer's safeguarding team owns defining the code word, but the audit should surface that it's absent.
- **Pattern: sensitive flag detected but no crossmodal channel configured on the record.** If the flow relies on SMS/email delivery, the fallback for "no channel" needs to be a warm human transfer, not silent continuation.
