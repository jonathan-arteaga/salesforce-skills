---
id: A09
name: contractions-and-cadence
category: system-instructions
severity: medium
applies_to: [migrate, optimize]
detection:
  - regex: '\b(I will|you are|we will|it is|do not|does not|cannot|I am|you will|that is|I would)\b'
    in: [system.instructions, response_templates, welcome]
  - keyword: "I am unable to"
    in: [response_templates]
  - structural: "instructions give no spoken-register or cadence guidance"
    in: [system.instructions]
principle_refs: [P4, P9, P11]
pattern_refs: [T-translate-3]
couples_with: [A08, A10, B02]
---

# Contractions and cadence

## Why it matters

Written register survives the eye; the ear hears it as stiff. "I will need your date of birth. Do not worry if you cannot remember the exact day." is grammatical and cold. Spoken, people contract ("I'll", "don't", "can't") and vary their sentence length — a short line, then a longer one, then the key fact on its own. This is the model-agnostic layer of naturalness: it works on **every** voice model, unlike tone tags (A08, v3-only). It's also where end-focus lives out loud — land the turn on the fact that matters (P9).

**Naturalness ≠ deception.** The goal is speech that's easy to *listen to*, not speech that fools the caller into thinking the agent is human. **Sound natural, not human.** Sound natural; still disclose you're an AI at the opening (B02) and answer plainly if asked (A10). Ease and honesty aren't in tension — a warm, fluent agent that says it's an AI is exactly the target.

## Detection

- Uncontracted forms in spoken-facing strings: "I will", "you are", "do not", "cannot", "I am unable to".
- Uniform sentence length — every turn the same medium-long shape, no short beats.
- Instructions specify *what* to say but give no guidance on spoken register or cadence.

## Chat example (before)

```
"I will now require your date of birth. Please do not be concerned if you are
unable to recall the exact date; an approximate date is acceptable."
```

(Reads fine on screen. Spoken, it's stilted and long-winded.)

## Voice example (after) — recommended

**Add a register + cadence rule to `system.instructions`:**

```
REGISTER (spoken): Use contractions throughout — "I'll", "you're", "don't", "can't",
"that's". Vary sentence length: a short line, then a longer one. Put the key fact last
(P9). Speak the way a competent colleague would on the phone — never read written prose
aloud.
```

**Rewrite the line:**

> "I'll need your date of birth next. Don't worry if you can't remember the exact day. Roughly is fine."

Short ask, then the reassurance, key permission ("roughly is fine") last.

**Punctuation carries prosody on any model.** A comma buys a short beat; a full stop resets pitch and pace; an ellipsis holds a longer, trailing pause. Write the punctuation you want *heard*, not the punctuation a style guide wants seen — this is the one prosodic control that works even on Flash models where tone tags don't (A08). Punctuation is also more reliable than pause tags (`[pause]`, `[short pause]`), which aren't officially supported on v3. Lead with punctuation; treat tags as something to try and check by ear.

**No em-dashes in spoken prose.** TTS handles them inconsistently: sometimes a pause, sometimes nothing, and on some voices a spoken artefact. Use a full stop or a comma instead. Em-dashes in multi-line quoted strings have also broken the Agent Script parser during edits (see SKILL.md, Phase 7). Z04 flags them in `|` instruction lines and spoken string fields.

## Voice example — alternatives

**Formal personas still contract.** Even a financial or legal register uses "you'll" and "we'll" in speech — dropping contractions entirely reads as robotic, not authoritative. Keep the contractions; carry the formality through word choice and a measured cadence (and, on v3, a `[calm]` / `[serious]` resting tag — A08).

**Regional cadence.** Sentence rhythm and filler vary by market; confirm against the persona document rather than defaulting to a US-newsreader cadence.

## Anti-patterns

- **Reading written prose aloud.** The single most common voice tell — full uncontracted sentences of even length. Contract and vary.
- **Over-contracting into slang.** "gonna", "wanna", "lemme" overshoot for most brand personas. Contractions, not a transcript of casual speech.
- **Treating contractions as the two-voice opening's contrast mechanism.** They are **not.** The opening's load-bearing contrast is *auditory* — a distinct system-layer voice vs. the agent voice (P4, B01, T-opening). A09 is a global register rule; it does not create or replace that contrast. (Removing contractions from the system layer is the wrong way to make it sound different — cast a different voice instead.)
- **Simulating humanness.** Don't instruct the agent to make the caller believe they're talking to a person — that crosses from naturalness into deception (see "Why it matters", B02, A10).
- **"You are a human" persona prompts.** It does loosen the delivery, but it walks the model right up to claiming to be a person. "Speak like a thoughtful friend on a casual call" gets you the same ease without that risk.
- **Em-dashes for pacing.** Unreliable in TTS and a parser risk in quoted strings. Use full stops, commas and ellipses (Z04). Natural *and* disclosed.

## Where it lives

- `system.instructions` (global) — the register + cadence rule.
- Every user-facing copy string (Layer B) and `messages.welcome` — contract and vary length.
- Couples with A08 (v3 tone tags) and A10 (self-reference honesty); the naturalness ≠ deception line ties to B02.

## Mis-applications (optimize mode)

- **Pattern: voice-shaped agent but copy still uncontracted in a few legacy strings.** Half-migrated. `[changed]` on the stragglers.
- **Pattern: contractions present but every turn is the same length.** `[consider]` — add short beats; land the key fact last.
- **Pattern: an instruction to "sound human / like a real person", or a persona line like "You are a human".** `[changed]` — reword to "sound natural, not human" (e.g. "Speak like a thoughtful friend on a casual call"); naturalness is the goal, deception isn't (B02, A10).
- **Pattern: em-dashes used for pacing in spoken copy.** `[changed]` — replace with a full stop or comma (Z04).
