---
id: A05
name: congratulatory-language-ban
category: system-instructions
severity: medium
applies_to: [migrate, optimize]
detection:
  - keyword: "Great choice"
    in: [instructions, response_templates]
  - keyword: "Perfect"
    in: [response_templates]
  - keyword: "Awesome"
    in: [response_templates]
  - keyword: "Wonderful"
    in: [response_templates]
  - structural: "instructions don't ban congratulatory phrasing"
    in: [instructions]
principle_refs: [P11]
---

# Congratulatory language ban

## Why it matters

Voice agents that say "Great choice!", "Perfect!", or "Wonderful!" sound patronising and slow the call. In text, these tokens function as visual filler the user can skim past. In voice, every word costs time and the register feels like a sales script. They also often appear in inappropriate contexts ("Great choice!" after the user picked the only available slot).

The persona phrasebook (see `T-phrasebook`) handles this properly: rotating neutral acknowledgments that match the Persona's register without overstepping. With a completed Persona, the tokens come from its Phrase Book (Layer C). Without one, the fallback set is "Got it.", "Right.", "Thanks.", "Okay." (A healthcare engagement added "Lovely." for a warm, measured British register. That's an example of a Persona-specific token, not a default.)

## Detection

Source contains either:
- Explicit congratulatory phrases in user-visible copy: "Great choice", "Perfect", "Wonderful", "Awesome", "Excellent choice", "Brilliant".
- Instructions that allow them by omission — no rule banning them.

## Chat example (before)

```
"Great choice! You've selected the following slot: …"
```

```
"Perfect — let's get you booked in!"
```

```
"Excellent! I'll need a few details from you."
```

## Voice example (after) — recommended

**Add the global rule to `system.instructions`:**

```
REGISTER: {Persona register, e.g. "warm, measured, professional"}. Never
congratulatory ('Great choice', 'Perfect', 'Wonderful', 'Awesome', 'Excellent').
When acknowledging a user's selection, use the persona phrasebook tokens.
Rotate within that set; never use the same token in two consecutive turns.
```

**Replace congratulatory copy with phrasebook acknowledgments:**

> Original: "Great choice! You've selected the following slot: …"
>
> Voice: "Got it. That's Andrew McLeod at Newcastle, Tuesday the fifth at five-thirty."

> Original: "Perfect — let's get you booked in!"
>
> Voice: "Right, let me take a few details."

## Voice example — alternatives

**Keep upbeat tone if the persona is explicitly warm/encouraging** (e.g., a wellness coaching agent) — but suppress in error, escalation, and crisis paths regardless. Even an encouraging persona shouldn't say "Great choice!" when the user has just disclosed a symptom.

**Substantive encouragement ≠ empty congratulation.** The ban targets *content-free* praise ("Great choice!", "Perfect!") — tokens that acknowledge nothing. Encouragement *tied to a concrete fact* is fine, and often good: "That's everything I need for the claim. You're all set", "You're nearly there. Just your date of birth and we're done." The test: strip the sentence of its facts. If nothing's left ("Great!"), cut it; if a real status remains ("that's everything I need"), keep it — the warmth rides on the fact, not on an exclamation. Same suppression applies: in error, escalation, and crisis paths, drop even the substantive version. (Warmth through *delivery* on v3 is A08; not claiming first-person excitement is A10.)

**Cultural / regional adjustment:** in some markets the threshold for what reads as patronising is higher. Confirm with the persona document. The default rule is the safer setting.

## Anti-patterns

- **Replacing one congratulatory token with another.** "Great choice" → "Brilliant!" — same problem, different word.
- **Writing the rule but allowing exceptions in topic instructions.** Per-topic blocks override globals; if any topic still allows congratulatory phrasing the rule is leaky.
- **Banning congratulatory tokens but leaving exclamation marks elsewhere.** "Got it!" sounds congratulatory in TTS depending on the engine. Drop the "!" in spoken acknowledgments.

## Where it lives

- `system.instructions` (global) — add the rule.
- Response template strings — replace each occurrence with a phrasebook token.
- The persona phrasebook itself (Layer C in the rewrite bundle) — define the rotation set.

## Mis-applications (optimize mode)

- **Pattern: rule banning "Great choice" but not the equivalents.** Add the full list ("Perfect", "Wonderful", "Awesome", "Excellent", "Brilliant") — the LLM follows the letter not the spirit.
- **Pattern: phrasebook has neutral tokens but the LLM still defaults to "Perfect" mid-conversation.** Strengthen the rule to "use ONLY tokens from the phrasebook for acknowledgment".
