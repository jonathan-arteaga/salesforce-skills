---
id: A12
name: times-and-dates-spoken-form
category: system-instructions
severity: medium
applies_to: [migrate, optimize]
couples_with: [I01, A06, D03]
detection:
  - regex: '\b([01]?\d|2[0-3]):[0-5]\d\b'
    in: [instructions, response_templates, variables]
  - regex: '\b(GMT|UTC|BST|EST|EDT|PST|PDT|CET)\b'
    in: [instructions, response_templates]
  - regex: '\b\d{4}-\d{2}-\d{2}\b'
    in: [instructions, response_templates, variables]
  - regex: '\b\d{1,2}/\d{1,2}/\d{2,4}\b'
    in: [instructions, response_templates]
principle_refs: [P5, P9]
pattern_refs: [T-grounding]
---

# Times and dates spoken form

## Why it matters

Times and dates come out of APIs in display or machine form: `14:00–19:00 GMT`, `2026-11-03`, `03/11/2026`. TTS reads them literally ("fourteen hundred to nineteen hundred G M T") or guesses ("the third of November" in one locale, "March eleventh" in another). People say times as "between 2 and 7 in the afternoon" and dates as "Tuesday the 3rd of November". (Source: Voice Agent Optimization Guide §2.7.)

Leave out what the caller already knows. A timezone is noise when caller and business share one, and the year is noise for a date in the next few months. Each extra token is one more thing to hold by ear, and it pushes the important part (the day, the window) away from the end of the sentence (P9).

A06 covers money, D03 covers dates of birth the caller gives, and I01 covers companion variables. This pattern covers times and dates the agent *says*.

## Detection

- Clock times in digit form (`14:00`, `9:30`) in instructions, templates or variables read back to the caller.
- Timezone abbreviations in spoken copy.
- ISO (`2026-11-03`) or slash (`03/11/2026`) dates in spoken copy or read-back variables.
- A delivery window, appointment slot or opening-hours string read back without a spoken-form companion.

## Chat example (before)

```
"Your delivery is booked for 2026-11-03 between 14:00 and 19:00 GMT."
```

## Voice example (after) — recommended

**Add the rule to `system.instructions`:**

```
TIMES AND DATES: Say times the way people do: "2 in the afternoon", "half past 9",
"between 2 and 7 in the afternoon". Never say a timezone unless the caller is in a
different one. Say dates as weekday plus ordinal ("Tuesday the 3rd of November").
Leave out the year unless it isn't this year or next.
```

> Agent: Your delivery's booked for Tuesday the 3rd of November, between 2 and 7 in the afternoon.

For read-back of an API value, add a spoken-form companion (I01), e.g. `deliveryWindowSpoken`, set by a formatter action.

## Voice example — alternatives

**US English:** "Tuesday, November 3rd, between 2 and 7 p.m." Follow the locale's spoken convention, not the display one.

**Caller in another timezone:** name the caller's time, not the business's: "That's 9 in the morning your time."

**Relative dates for the next few days:** "tomorrow afternoon", "this Thursday". Pair with the weekday when the booking is irreversible (T-grounding): "this Thursday, the 5th".

## Anti-patterns

- **"Fourteen hundred hours."** Military time read aloud.
- **"Two P M to seven P M G M T."** Letter-by-letter abbreviations stack up fast.
- **Year on every date.** "The 3rd of November 2026" when it's October 2026.
- **Mixed formats across subagents.** One says "2 p.m.", another "fourteen hundred".

## Where it lives

- `system.instructions` (global): the rule.
- `variables:`: spoken-form companions for any time or date read back (I01).
- Response templates and instructions that interpolate times or dates.

## Mis-applications (optimize mode)

- **Pattern: rule present, raw variable still interpolated.** The confirmation template still reads `{!@variables.deliveryWindow}`. Audit every interpolation.
- **Pattern: timezone dropped for a caller who needs it.** A travel or cross-border flow drops the zone by rule. Keep it when caller and business can differ.
