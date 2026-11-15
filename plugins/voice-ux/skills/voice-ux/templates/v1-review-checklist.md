# V1 Review Checklist — output skeleton

Generated as a side artifact at the end of Phase 5 (or optional Phase 7 if generating a `.agent` file). Mandatory items the human reviewer must check before deploy. Annotated to reflect what was applied / skipped in this specific migration.

Suggested filename: `artifacts/voice-ux/[agent-name]-v1-review-checklist.md`

---

```markdown
# V1 Review Checklist — [agent-name]

> ⚠️ **V1 baseline, not ship-ready.** Every item below is mandatory before deploy.
> Your business context, compliance requirements, and edge cases require human
> judgment. The skill produces a starting point, not a guarantee of correctness.

**Generated:** [YYYY-MM-DD]
**Source agent:** [path]
**Voice agent:** [path or bundle name]
**Persona source:** [path + SHA-256 / inferred]
**Mode:** migrate / optimize
**Modality traits:** channel type: [voice-only / multimodal voice-over-web], crossmodal handoff channels: [screen, SMS, email, other / none], IVR / carrier-side announcement: [y/n] _(barge-in and keypad / DTMF both assumed on — Agentforce defaults)_

---

## 0. Persona preservation

- [ ] Persona source recorded (`persona-handoff.json` and/or `persona.md`, SHA-256, handoff status), or character evidence labeled inferred
- [ ] If both files were supplied, the handoff's `source_persona.sha256` matches `persona.md` (otherwise the stale handoff was resolved)
- [ ] Extraction complete: Personification + organizational "we", Negative Identity, agent name + radio test, Warmth/Emotional Coloring, Empathy, Personality Intensity, Humor, Brevity intent, Reading Level
- [ ] Every exact Never-Say entry remains prohibited with its preferred behavior
- [ ] Immutable spans, surrounding response shape, Lexicon meaning, and explicit Guardrails remain unchanged
- [ ] Persona Tone Flex triggers, semantic shifts, maxima, hard boundaries, lexical cues, and resets remain intact
- [ ] P5/A08 adds situational prosody without redefining the Persona policy
- [ ] Lexical–prosodic sync: each Tone Flex trigger's lexical cue and prosodic shift fire together and reset together
- [ ] Persona-licensed feelings (if any) were held to the A10 floor and the `[review needed]` was decided by a human
- [ ] Welcome keeps the Persona's meaning; only its spoken structure changed (B01)
- [ ] Any character or source-authority conflict is `[review needed]` and was resolved by a human

## 1. Vocal identity, casting, voice settings + channel config (H08, H09, H03, H06)

- [ ] Vocal Identity brief written (`[agent-name]-vocal-identity.md`); gender presentation, age band, and accent confirmed by a human, not inferred
- [ ] Casting sides generated from this agent (welcome, readback, distress turn, repair turn, name/brand/Lexicon, ~25s long turn)
- [ ] Audition run and recorded: channel (phone recommended; Preview acceptable with the caveat that phone rendering may differ) and listener tier (minimum 1; 3–5 independent listeners recommended for go-live or brand-critical agents)
- [ ] "Deliberately ambiguous" brief (if used): listeners' gender perception recorded
- [ ] Runner-up voice recorded
- [ ] Voice picked in the org library and listening sign-off recorded (human steps)
- [ ] Z05 clean: no "you are a human", disclosure dodges, body-sound tags, or scripted fillers left (or each remaining one has a written client/legal decision)
- [ ] Agent name and brand have a pronunciation entry (H04) and an STT keyword (H05), and sound right in the casting sides
- [ ] `voice_id` set to a real ID from this org's voice library (not a placeholder), matching the casting record
- [ ] Voice model chosen deliberately — default **v3 Conversational** unless you need **Flash v2** (custom pronunciation / non-US English accents) or **Flash v2.5** (non-English regional accents); model selection requires the emerging nested format (H03)
- [ ] `outbound_stability` tuned to the brief, one parameter at a time (honored on the default v3 model; v3's default is 0.5, Flash's starting point is 0.85)
- [ ] If tone / audio tags are used for expressivity (A08), the voice runs on **v3** and `outbound_stability` is low enough (~0.5–0.7) for them to modulate — tags are v3-only and inert (or read aloud) on Flash (H03)
- [ ] `outbound_speed` / `outbound_similarity` relied on **only if a Flash model is selected** — on the default v3 they're inert (H03); if used, keep speed inside usable 0.7–1.1
- [ ] `additional_configs.beepboop_config.max_wait_time_ms` set to ~500 (not the 6000ms platform default)
- [ ] `additional_configs.speak_up_config` set and tuned by ear (see §9)
- [ ] `speak_up_message` is a phrasebook pursuit token, not a robotic default
- [ ] Voice tested in voice preview against representative utterances (welcome + 3 mid-flow turns)
- [ ] Two-voice opening contrast verified (if applicable — couples with B01)
- [ ] **Compiled voice config checked after publishing:** `voice_id` / `persona_id`, model, `outbound_stability`, `inbound_keywords`, `inbound_filler_words_detection`, `pronunciation_dict` and `additional_configs` all present in the published agent (Builder or retrieved metadata). A nested block can compile to empty voice settings (H03); a clean publish doesn't prove they arrived
- [ ] Model confirmed from a live session trace (compiled planner bundles don't show model names)

## 2. Pronunciation Dictionary (H04)

- [ ] Starter terms transcribed into the in-script `modality voice: → pronunciation_dict` (grapheme / phoneme / type) — or the org's Voice Settings dictionary if you use that instead
- [ ] Custom pronunciation actually takes effect — it's a **Flash v2** capability; on the default v3 model (and Flash v2.5) `pronunciation_dict` is likely inert (H03/H04)
- [ ] Each term tested in voice preview in **sentence context** (not isolated), on the model the agent runs
- [ ] Domain term refresh process documented

## 3. Key-Term Prompting (H05)

- [ ] Predictable terms written in-script at `modality voice: → inbound_keywords → keywords`
- [ ] `inbound_filler_words_detection` set deliberately (often `True` for telephony to strip um/uh; leave `False` where hesitation is signal, e.g. de-escalation) — H05
- [ ] Overflow / vendor-specific vocab loaded into the platform's STT config (if the list exceeds an in-script/vendor cap)
- [ ] Recognition tested with sample utterances for the top 5 trickiest terms
- [ ] Postcode capture tested with 5+ representative postcodes

## 4. Crisis flow (F01)

- [ ] Crisis copy delivers in slowed prose (SSML rate ~85%)
- [ ] All helpline numbers spoken digit-by-digit (verified in preview)
- [ ] `crisis_detected` latch verified — every subsequent turn re-voices
- [ ] Agent never auto-terminates the call after crisis copy
- [ ] Live counsellor transfer (if offered) goes to a trained team, not the general queue

## 5. AI disclosure and recording notice (B02, A10)

- [ ] AI disclosure present in welcome (system layer or agent layer)
- [ ] Recording-may-be-monitored disclosure complies with [jurisdiction]
- [ ] Caller can ask "am I talking to a person?" and get the right answer
- [ ] Agent never claims first-person emotion ("I'm so excited / thrilled") — warmth via delivery + second person (A10)
- [ ] AI status disclosed once at the opening, not re-announced unprompted every topic (A10)

## 6. T&Cs and consent (E03)

- [ ] T&Cs voice script signed off by Legal / Compliance
- [ ] Substantive obligations (cancellation, data sharing) audibly voiced
- [ ] Reference to full text on website included
- [ ] Explicit yes/no required (no "ok" / "sure" acceptance)

## 7. Spell-confirm coverage (D01–D08)

- [ ] Postcode: implicit echo on high confidence, letter-by-letter on low
- [ ] Phone: implicit echo / digit-by-digit logic verified; keypad offered on first mishear (D04)
- [ ] Email: implicit echo / letter-by-letter with improvised phonetics on the disputed segment / type-don't-say handoff path tested (D05, D08)
- [ ] DOB: spoken-form companion variable (`patient_dob_spoken`) used in summary
- [ ] Reference numbers (policy, pre-auth): "zero" vs "oh" convention consistent; keypad offered on first mishear, defaulted for sensitive numerics (D06)
- [ ] Hard / alphanumeric identifiers: process challenged (could it be numbers-only?), then the best-first ladder applied — improvised phonetics on repair, type-don't-say handoff for exact characters (D07)

## 8. Layer E (genuinely out-of-`.agent`) items

> In-script voice-channel config (beepboop / speak-up / `inbound_keywords` / `inbound_filler_words_detection` / `pronunciation_dict`) is checked in §1–§3 — it's written into the `.agent`, not here. This section is only what truly can't be scripted.

- [ ] TTS voice contrast for two-voice opening configured (if applicable — casting is human work; `voice_id` itself is in-script)
- [ ] SSML support enabled at the runtime layer
- [ ] Barge-in tuning (on by default; no in-script sensitivity setting)
- [ ] Sensitive-digit privacy routing for keypad entry (card / PIN, kept out of recording and transcript) — DTMF digits arrive as plain text; this is a routing/privacy concern, not an `.agent` key
- [ ] ASR confidence threshold for grounding escalation (recognizer-side; start at 0.75)
- [ ] Prosodic/paralinguistic sentiment input — not available; distress/sentiment is STT-text-only (recognizer-side; VoC raised, tracked for v2)
- [ ] CTI / ANI screen-pop mapping for `First_Name`, `Last_Name`, `Postal_Code` (if applicable)
- [ ] IVR / carrier-side pre-call announcement configured (if applicable)
- [ ] CSAT delivery channel (SMS or email) wired up post-call
- [ ] Utility-action Apex/Flow implemented (`format_currency`, `format_datetime`, escalation/link Flows)
- [ ] State preservation on Tier-3 human handoff verified (every collected field surfaces in agent screen-pop)

## 9. Pilot testing — with audio, not text

> Typing utterances into a preview verifies the reasoning, not the experience. Barge-in, background noise, accents, and timing are where voice deployments struggle, and none of them show up in a text preview.

- [ ] Tested **over real audio** (an actual call), not just the text preview
- [ ] At least one call from a **noisy environment** (car, kitchen with extractor on, TV in the room)
- [ ] Handed the phone to **someone who has never seen the script** and asked them to complete the task
- [ ] Listened for **undesigned silences** (waits with no filler) and **missed barge-ins** (places you'd have interrupted but the agent kept talking)
- [ ] `speak_up` timing (H06) checked by ear — pursues a silent caller without nagging someone who's mid-task
- [ ] At least 5 happy-path test calls completed
- [ ] At least 3 unhappy-path test calls (recognition failure, T&Cs decline, under-18, crisis)
- [ ] At least 1 mid-flow detour test (FAQ during booking)
- [ ] At least 1 transfer-to-human test
- [ ] Scenario suites added to Testing Center so regressions surface on later subagent edits
- [ ] Test results logged with date and reviewer name
- [ ] **Latency measured per turn from the session trace**, not by ear or from Connect:
  - Response delay = the agent message's `MessageStartTimestamp` minus the caller's previous `MessageEndTimestamp`, from the Data Cloud session-trace message DLM
  - Query about 5 minutes after the call; traces land late
  - If the query returns two sessions (a preview and the live call), keep them apart
  - Don't use Connect REST `serverReceivedTimestamp`: it includes greeting TTS time and once showed a "28 s" gap that was really 3.2 s
- [ ] **One change per version:** publish the change as a new version, activate, place one call on a fixed path, compare each turn against the previous version, then keep it or roll back (`sf agent activate --version N`). Two changes at once can hide a regression. One call per version is directional, not statistical

## 10. Activation pre-flight ("rings then hangs up")

- [ ] `config: → default_agent_user` set to a real, active user
- [ ] That user has access to every Apex class and flow the actions call
- [ ] Agent **re-activated after** any permission was granted (the runtime plan is cached at activation)
- [ ] Apex running `with sharing` can see the records it needs as that user
- [ ] Compliance-sensitive spoken lines (figures, recording notice, AI status) reviewed before activation

## 11. Rollback plan

- [ ] Previous chat agent stays deployed (parallel rollout, not replacement)
- [ ] Voice agent activatable / deactivatable independently
- [ ] Documented rollback procedure if voice agent must be paused

---

## Items applied in this migration

[Auto-populated from the audit — list each `[changed]` entry here as a check.]

- [x] A01 — numbered list rule (system instructions)
- [x] B01 — welcome length (split to two-layer opening)
- [x] D01 — postcode collection (Tier-1/Tier-2 repair added)
- [...]

## Items skipped

[Auto-populated from `[review needed]` and developer overrides during walk-through.]

- [ ] F02 — red-flag symptom checklist kept as 9-item list (clinical governance review pending)

## Items flagged out-of-scope

- Multi-turn cascading error recovery — gap in voice library v1
- Multilingual / accent-clash handling — gap in voice library v1
- Agent-to-agent skill transfer — gap in voice library v1

---

## Reviewer sign-off

| Section | Reviewer | Date | Notes |
|---|---|---|---|
| Voice settings | | | |
| Crisis flow | | | |
| T&Cs / Compliance | | | |
| Pilot testing | | | |
| Final approval | | | |
```
