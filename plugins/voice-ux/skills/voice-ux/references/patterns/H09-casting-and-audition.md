---
id: H09
name: casting-and-audition
category: configuration
severity: high
applies_to: [migrate, optimize]
couples_with: [H08, H03, H04]
applies_after: [H08]
detection:
  - structural: "voice_id is a placeholder, or was set without a shortlist, audition, or recorded decision"
    in: [config]
  - structural: "no runner-up voice recorded for when the chosen voice is deprecated"
    in: [config]
  - structural: "voice approved from a Builder play-button sample only, with no audition against agent-specific lines"
    in: [config]
principle_refs: [P5]
pattern_refs: [T-opening]
---

# Casting and audition

## Why it matters

Casting is choosing the voice that best fits the Vocal Identity brief (H08), among the voices that actually exist in the target org and work on the chosen model. It's a design decision this skill owns: the shortlist, the audition, the decision record, and the emitted `voice_id`. Two parts stay with humans: picking the voice in the org's voice library, and the final listening sign-off.

Voices fail in ways a library sample won't show you. Accents drift partway through a long turn. Loudness creeps. Some voices garble alphanumerics. A voice can sound one gender in the sample and another on the phone. The only reliable test is the agent's own lines, heard on the channel callers will use. And voices get deprecated, so a decision record without a runner-up leaves the next person to start from zero.

## Detection

- `voice_id` is a placeholder, or set with no shortlist or reason.
- The voice was approved from the Builder play-button sample, not from the agent's own lines.
- No runner-up is recorded.
- Optimize mode: the configured voice hasn't been checked against a brief.

## Chat example (before)

(Not applicable. Chat agents have no voice.)

## Voice example (after) — recommended

Record everything below in `artifacts/voice-ux/[agent-name]-vocal-identity.md`, after the brief (H08).

**1. Hard filters.** Drop any voice that fails one:
- **Locale and language** match the brief's locale variants.
- **Model fit** (H03 model table): needs custom pronunciation → Flash v2; needs expressive tags → v3; needs a steady non-US English accent → Flash v2; needs a regional non-English accent → Flash v2.5. A voice is only as good as the model it can run on.
- **Exists in the target org.** Voice IDs are org-scoped. Check the target org's library, not a colleague's sandbox.
- **No static catalog.** Voices are added and deprecated constantly. This skill doesn't ship a voice list; take a fresh snapshot of the target org's library per engagement and date it.

**2. Shortlist of three.** From the dated snapshot, pick three voices that fit the brief's perceived identity and perceptual target. For a "deliberately ambiguous" brief, shortlist the voices that sound most neutral to you, and say so (H08).

**3. Casting sides.** A fixed audition script generated from *this* agent, so every voice is judged on the same lines:
- the agent-layer welcome (B01), including the agent's name and the brand
- a readback of an alphanumeric or number value the agent really handles (D04, D06)
- a Tone Flex distress turn (the agent answering a worried or upset caller)
- a repair turn (T-repair tier 1 or 2)
- the agent name, the brand, and three hard Lexicon terms in a sentence
- one long turn of about 25 seconds, to catch accent or loudness drift

Write the sides in the agent's real register, with the tags it will really use on v3 (A08).

**4. Audition.** Play every side, for every shortlisted voice, the same way.
- **Channel.** A real phone call is recommended, because Builder Preview doesn't render the way callers hear it on a phone line. If no phone number is provisioned for the sandbox, Preview is acceptable. Record the channel, and carry the caveat that phone rendering may differ.
- **Listeners (tiered).** Minimum: one listener. Recommended for go-live or brand-critical agents: three to five independent listeners, at least one close to the target audience. Record which tier you used.
- **Scoring.** Each listener scores on their own, before any discussion: 1–5 per brief adjective, plus defect flags: accent drift, garbled alphanumerics, loudness drift, unintended gender perception, tags read aloud. Ask each listener "did this voice sound female, male, or hard to say?" whenever the brief specifies a gender presentation.

**5. Decision record.**

```
CASTING DECISION: Harbor Bank "Jordan" (en_US)
Catalog snapshot:  2026-10-14, target org "HB-UAT"
Model:             eleven_v3 (default)
Chosen:            <voice name> / <voice_id> / v3
Runner-up:         <voice name> / <voice_id> / v3  (fallback if the chosen voice is deprecated)
Audition channel:  phone (PSTN, mobile handset)
Listener tier:     recommended (4 listeners, 1 from the target age band)
Scores (mean):     calm 4.5, competent 4.25, approachable 4.0, plain-spoken 4.5
Gender perception: 2 "hard to say", 1 female, 1 male → meets "deliberately ambiguous"
Defects:           none; runner-up drifted toward a Southern accent on the long turn
Approved by:       <name, role>, 2026-10-15
```

## Voice example — alternatives

**Optimize mode: audit, don't recast by default.** Run the casting sides through the voice that's already live and score it against the brief. Recommend a recast only when the voice clearly mismatches the brief or has a defect. Familiarity is a real cost to callers; don't churn a working voice for a marginal gain.

**Brand or custom voice.** The hard filters and casting sides still apply. Audition the brand voice against a stock runner-up so the record shows it holds up on the phone.

**Two-voice opening.** Cast the system/IVR voice too, against brief field 6. The test is contrast: a listener should hear the handover without being told (T-opening-mis-1).

## Anti-patterns

- **Casting from the play button.** The sample isn't your lines, and Preview isn't the phone.
- **Discussing before scoring.** The first opinion anchors the room. Score independently, then talk.
- **One long-turn-free audition.** Short lines hide drift. Keep the ~25-second turn.
- **No runner-up.** Deprecation turns into an emergency recast.
- **Copying a voice ID from another org.** It won't resolve, and publish may silently fall back to the default voice.
- **Recording only the winner's scores.** The runner-up's scores are what justify it as the fallback.

## Where it lives

- Side artifact: `artifacts/voice-ux/[agent-name]-vocal-identity.md` (casting sides, scores, decision record).
- The chosen `voice_id` goes into `modality voice:` (H03), marked `[review needed]` until the human sign-off is recorded.
- The pick in the org voice library and the listening sign-off are human steps; list them in the V1 review checklist.

## Mis-applications (optimize mode)

- **Pattern: casting record exists but lists no runner-up.** `[consider]` — add one from the same snapshot.
- **Pattern: audition used the voice library sample, not agent lines.** `[consider]` — re-audition with casting sides.
- **Pattern: Preview-only audition approved for a go-live agent.** `[consider]` — a phone-call check before launch, if a number can be provisioned.
- **Pattern: brief asks for "deliberately ambiguous" and the record has no gender-perception answers.** `[consider]` — the claim is untested.
