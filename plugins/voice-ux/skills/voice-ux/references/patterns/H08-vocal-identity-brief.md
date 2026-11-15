---
id: H08
name: vocal-identity-brief
category: configuration
severity: high
applies_to: [migrate, optimize]
couples_with: [H09, H03, A08]
detection:
  - structural: "voice agent has no written description of what the voice should sound like (perceived gender, age, accent, voice quality, expressive range)"
    in: [config, system.instructions]
  - structural: "voice_id chosen without a recorded rationale tied to the persona or audience"
    in: [config]
  - structural: "persona.md or persona-handoff.json supplied but no vocal interpretation of it exists"
    in: [config]
principle_refs: [P5, P11]
pattern_refs: [T-opening]
---

# Vocal Identity brief

## Why it matters

A voice is identity before it is content. Listeners hear perceived gender, age, accent, and social register in the first second, before any word is understood. Persona decides who the agent is and what it would say. It deliberately says nothing about sound. This skill owns the interpretation of that character in the audio channel, the way a casting director reads a script before calling anyone in.

The **Vocal Identity brief** is that interpretation, written down. It's the spec that casting (H09) and light tuning (H03) are checked against. Without it, voices get picked by whoever opens the voice library first, and nobody can say afterwards why the agent sounds the way it does, or whether a replacement voice is a like-for-like swap.

The brief never contains voice IDs or settings. Those belong to the casting record (H09) and the `modality voice:` block (H03). Keeping the description separate from the pick is what lets you recast when a voice is deprecated without reopening the character.

## Detection

- No brief exists, and `voice_id` is a placeholder or was chosen without a stated reason.
- A `persona.md` / `persona-handoff.json` is supplied, but nothing translates its Register, Warmth, Personality Intensity, Negative Identity, or Tone Flex into sound.
- Optimize mode: a voice is configured, but nobody can say what it was cast against.

## Chat example (before)

(Not applicable. Chat agents have no voice. The chat-side input is the Persona contract, which this pattern interprets.)

## Voice example (after) — recommended

Write the brief to `artifacts/voice-ux/[agent-name]-vocal-identity.md` using `templates/vocal-identity-brief.md`. Derive it from the Persona contract, the audience, the brand, and the locale. When no Persona is supplied, derive from the Script and sample and label every field `inferred`.

**The eight fields:**

1. **Derivation trace.** Persona field → vocal implication, one line each. Example: *Personification = Not personal, Register = Professional → restrained expressivity, no character voice.* *Negative Identity "not a salesperson" → must not sound like a radio ad read.*
2. **Audience and listening conditions.** Caller age profile, share of second-language speakers, likely stress state, hearing-impaired share. The channel: PSTN narrowband (8 kHz), mobile, noisy environments (car, kitchen, warehouse).
3. **Perceived identity.**
   - **Gender presentation:** female, male, or deliberately ambiguous. **Elicit it, never infer it from the role.** Record who decided and why.
   - **Age band:** e.g. "30s–40s adult; not youthful, not elderly".
   - **Accent per locale:** local, neutral-standard, or brand-specified.
   - **Pitch zone:** e.g. "mid-range; avoid high or infantilising".
   - **Voice quality:** clear, resonant, low breathiness. Breathy and whispery voices lose the most on narrowband.
   - **Baseline tempo:** brisk, moderate, or unhurried (realised by turn length and punctuation on v3; by `outbound_speed` only on Flash, H03).
4. **Perceptual target.** Three to five adjectives the voice must earn ("calm, competent, warm but not saccharine"), plus two or three "must not sound like" items drawn from Persona's Negative Identity ("not a radio DJ", "not a children's presenter").
5. **Expressive range.** The resting profile (P5), the allowed shifts and their ceilings (from Persona Tone Flex), and forbidden effects: laughter, breaths, sighs, filler sounds, simulated presence (Z05).
6. **Two-voice relation.** What the system/IVR voice is (T-opening) and how it contrasts: a different timbre or gender, formal, no persona expression.
7. **Locale variants.** Same character, a locale-native voice per locale, and pronunciation notes per locale. Generating non-English copy stays out of scope.
8. **Name block.** Agent name and brand, with IPA or respelling and an STT keyword entry (H04, H05).

**On "deliberately ambiguous".** Today's voice catalogs are effectively binary: voices are tagged male or female. A gender-ambiguous presentation is still a legitimate brief, but its realisation is a search, not a setting. Look for the voice that *sounds* most neutral in the available catalog (often a mid-pitch or lower female voice, or a higher, softer male voice), then validate with listeners in the audition (H09). Don't promise the client that a neutral voice exists before you've heard one. Perceived gender is a continuum driven by pitch, resonance, and articulation cues together, so a voice that reads as ambiguous to one listener may not to another. That's why the audition records how each listener heard it.

**Worked example (fictitious brand):**

```
VOCAL IDENTITY: Harbor Bank "Jordan" (en_US)
Derivation:  Register = Professional, Warmth = moderate, Intensity = low
             → steady resting delivery, small shifts only
             Negative Identity "not a pushy salesperson" → must not sound like an ad read
Audience:    adults 35–75, ~15% L2 English, often calling about a problem; PSTN + mobile
Identity:    gender presentation deliberately ambiguous (client brand team, 2026-10-14:
             "Jordan" is unisex by design); age 35–50; General American;
             mid pitch; clear, resonant, low breathiness; unhurried
Target:      calm, competent, approachable, plain-spoken
Must not:    an ad read; a children's presenter; a late-night radio host
Range:       rests on Calm Authority; Grounded Warmth on distress triggers (Tone Flex T2),
             reset after the issue is resolved; no laughter, breaths, or filler sounds
System voice: IVR uses a contrasting, formal voice; no persona expression
Locales:     en_US only (es_US planned: same character, native Spanish voice)
Name:        "Jordan" /ˈdʒɔːrdən/; "Harbor Bank" both added as STT keywords
```

## Voice example — alternatives

**No Persona supplied.** Write the brief from the Script, sample, and brand, label each field `inferred`, and mark the brief `[review needed]`. Recommend running `persona` if the character itself is unclear; don't design the character here.

**Optimize mode with a voice already live.** Write the brief anyway, then audit the current voice against it (H09 optimize mode). The brief is how you tell a good voice from a merely familiar one.

**Brand-mandated voice.** If the client has already chosen the voice (a custom or brand voice), still write the brief. It documents what the voice is meant to carry and gives the next recast something to match.

## Anti-patterns

- **Inferring gender from the role.** "It's a nurse line, so a female voice." Ask. Record who decided.
- **Putting voice IDs in the brief.** The brief outlives any single voice. IDs go in the casting record (H09).
- **Adjectives that can't be heard.** "Innovative", "trustworthy brand". Use words a listener could rate: calm, brisk, warm, crisp, unhurried.
- **Writing the brief after the voice is picked.** That's a description of the pick, not a brief. It can't catch a bad cast.
- **Promising an ambiguous voice before auditioning one.** The catalog may not have one that works for this audience.

## Where it lives

- Side artifact: `artifacts/voice-ux/[agent-name]-vocal-identity.md` (template: `templates/vocal-identity-brief.md`). It also holds the casting sides, scores, and decision record (H09).
- Summarised and linked from the rewrite bundle's "Vocal identity and casting" section.
- Nothing from the brief is written into the `.agent` directly. It drives H09 (casting), H03 (light tuning), A08 (tags), and H04/H05 (the name block).

## Mis-applications (optimize mode)

- **Pattern: brief exists but is a copy of the Persona traits** ("friendly, helpful, professional") with no sound-level description. `[consider]` — add perceived identity, voice quality, and must-not-sound-like.
- **Pattern: brief says "deliberately ambiguous" but no listener validation was recorded.** `[consider]` — run the audition (H09) and record how each listener heard it.
- **Pattern: brief and configured voice disagree** (brief says unhurried, mid pitch; the voice is bright and fast). `[consider]` recast, via H09.
