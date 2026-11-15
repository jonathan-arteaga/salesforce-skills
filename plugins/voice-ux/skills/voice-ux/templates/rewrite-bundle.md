# Rewrite bundle — output skeleton

The skill produces ONE file per migration or optimization, structured as below. Each layer is independently usable: developer can drop Layer A into Agent Script instructions, Layer B into copy fields, etc., without untangling.

Suggested filename: `artifacts/voice-ux/[agent-name]-voice-{migration,optimization}.md`

---

```markdown
# Voice UX work: [agent name]

**Mode:** migrate / optimize
**Mode rationale:** [one-line: text-shaped signals dominated extraction → migrate / voice-shaped signals dominated → optimize / mixed signals, developer chose X]
**Source:** [path to original Agent Script]
**Sample:** [path to provided sample]
**Persona source:** [path to persona-handoff.json and/or persona.md / inferred from Script and sample]
**persona_source_sha256:** [SHA-256 of persona.md / not supplied]
**persona_handoff_status:** [approved / draft / not supplied] [+ "handoff hash matches persona.md" / "stale handoff — review needed"]
**Vocal identity:** [artifacts/voice-ux/[agent-name]-vocal-identity.md]
**Modality traits:**
- Channel type: voice-only telephony / multimodal voice-over-web
- Crossmodal handoff channels: [screen / web handoff, SMS, email, other — list those available, or "none"]
- IVR / carrier-side pre-call announcement: yes / no
- _(Barge-in is assumed available — Agentforce default — so it's not a trait question; P1 chunking applies unconditionally. Keypad / DTMF is GA too — assume it's available and default to offering it for numeric capture; see D04 / D06 / D07 / D08.)_
**Languages:** [list]
**Primary intent:** [from Script or developer answer]

---

## Mode-detection extraction summary

[Optional but recommended — list the signals that drove mode inference. Helps the developer sanity-check.]

**Text-shaped signals found:**
- [signal: where in source / count]
- [...]

**Voice-shaped signals found:**
- [signal: where in source / count]
- [...]

**Inferred mode:** [migrate / optimize / mixed]
**Developer-confirmed mode:** [migrate / optimize]

---

## Persona precedence

[When a Persona is supplied, record what was extracted (structured fields from `persona-handoff.json` first, prose from `persona.md` as fallback):
- Identity, agent name + radio-test result, Personification level, organizational "we"
- Register, Voice dimensions (incl. Warmth, Emotional Coloring, Empathy, Personality Intensity, Humor, Brevity intent, Reading Level), Tone boundaries
- Negative Identity
- lexical Tone Flex triggers / maxima / cues / resets
- Phrase Book, Never-Say entries, Lexicon meaning, explicit Guardrails, immutable spans and surrounding-response rules, `technical_explanation_framing`
- any `adjacent_constraints` with `owner: "voice-ux"` (client voice requirements captured verbatim in the Persona workshop)

The Script remains authoritative for business logic, action contracts, routing, and source-carried compliance. Conflicts are `[review needed]` and block the affected rewrite. Voice floors that override the Persona (A10 feelings, B02/Z05 disclosure) are listed here with their `[review needed]` entries. When no Persona is supplied, label character evidence as inferred.]

---

## Vocal identity and casting

> Summary only. The full brief, casting sides, scores, and decision record live in `artifacts/voice-ux/[agent-name]-vocal-identity.md` (template: `templates/vocal-identity-brief.md`; patterns H08, H09).

- **Perceived identity:** [gender presentation (decided by whom) · age band · accent per locale · pitch zone · voice quality]
- **Perceptual target:** [3–5 adjectives] · **Must not sound like:** [2–3 items]
- **Model:** [eleven_v3 default / Flash v2 / Flash v2.5 / Kotoba] because [H03 reason]
- **Chosen voice:** [name / voice_id] · **Runner-up:** [name / voice_id]
- **Audition:** [phone / Preview (caveat: may differ on a phone line)] · listener tier [minimum / recommended]
- **Sign-off:** [name, date / pending — voice_id stays `[review needed]`]

---

## Summary

| Category | Changed | Review needed | Consider | Out-of-scope | OK |
|---|---|---|---|---|---|
| Turn structure | N | N | N | N | N |
| Repair | N | N | N | N | N |
| Grounding | N | N | N | N | N |
| Copy / translation | N | N | N | N | N |
| Opening / closing | N | N | N | N | N |
| Latency | N | N | N | N | N |
| Phrasebook | N | N | N | N | N |
| Vocal identity / casting | N | N | N | N | N |
| Disclosure / impersonation (B02, A10, Z05) | N | N | N | N | N |

> `Consider` column populated only in optimize mode. In migrate mode it stays at zero.

**Layer E items the developer still owes:** [count and one-line names]

---

## Layer A — Rewritten instructions (LLM-facing)

> Drop into Agent Script `system.instructions` or per-topic `reasoning.instructions`. Voice behavior is baked in as directives.

### Turn structure
- One question per turn. If you need more than one piece of information, ask in sequence.
- Put the question or critical information at the end of the turn. Lead with context, end with what you need from the user.
- State any caveat (fee, non-refundable, eligibility) BEFORE the item it qualifies — "This non-refundable option is $100", never a price followed by "…and it's non-refundable".
- Use the passive voice where it places the key information last; information structure outranks style rules like "avoid passive".
- Never bundle two questions with "and" or "also". Split them.
- Cap spoken lists at three items. Above three, give headlines first and offer the rest on request.
- Keep utterances to 1–2 sentences (about 20 seconds spoken at most), answer first. Allow a third short sentence only for a caveat that must come before the item, or when reading back data the user just gave you.

### Grounding
- Common acknowledgments: no confirmation.
- Single dates, postcodes, single names: implicit echo as you advance ("Tuesday the 15th. And for what time?"). Escalate to phonetic spelling on low ASR confidence.
- Phone numbers: implicit echo on high ASR confidence; on low confidence, read back digit by digit.
- Email: implicit echo on high ASR confidence; on low confidence, read back char by char. SMS handoff is a fallback if char-by-char is impractical.
- Money or irreversible actions: explicit summary + check ("That's £85 to be charged today. Shall I go ahead?") before commit.
- If two fields appear inconsistent (e.g., name and email domain), do a soft check.

### Repair
- First miss: open repair, no blame ("Sorry, I missed that. Could you say it again?").
- Second miss on the same field: rephrase or constrain ("You can say morning, afternoon, or evening. Which works?"). Format prescriptions are allowed here, not before.
- Third miss or user frustration: hand off to a human. Carry all collected state with you. Never make the user start over.
- Vary repair language across attempts. Don't repeat the tier-1 string.

### Latency
- Before any tool/action call expected to take more than a second, say something. "Let me check…" / "One moment…"
- For multi-system or slow operations, check in verbally every 3–5 seconds.
- For anything expected to take more than 10 seconds, warn the user that it may take a while; keep verbal fillers going during processing.

### Opening and commitments
- [If a static welcome or IVR introduction plays] THE WELCOME LINE HAS ALREADY BEEN SPOKEN: "[exact welcome text]". Never greet the caller or introduce yourself again. Answer their first words directly. (T-opening-already-spoken)
- If you're unsure, or the caller asks for something your actions can't do, don't improvise and don't invent a commitment. Never say anything was saved, noted, sent or arranged unless an action in this conversation did it and returned success. (A11)
- Say times the way people do ("between 2 and 7 in the afternoon"), with no timezone unless the caller is in a different one, and dates as weekday plus ordinal, without the year unless it isn't this year or next. (A12)

### Sequential gathering
- Ask in natural narrative order, not data-schema order. If a person would volunteer date before time, ask date first.
- Acknowledge briefly between fields. Don't echo every value.
- For sequences over 5 fields, signal progress ("Just two more things…").

### [Per-topic blocks, if multi-topic — copy this template]
**Topic: [name]**
[Topic-specific instructions — repair, grounding, escalation overrides for this topic]

### Deterministic guarantees (variables + flow-control)
> Sequential guarantees that must hold every time — outside the reasoning loop. Not prose the LLM can talk itself out of.
- Failure counter + `after_reasoning` escalation guard → handover subagent (J01). Budget: [N] attempts.
- Volunteered-slot capture: single `@utils.setVariables` with `...` on the full slot set (I02) — caller never re-asked.
- `require_user_confirmation: True` on hard-to-reverse actions [list them].

---

## Voice channel configuration (in-script)

> Written into the `.agent` `modality voice:` block. `voice-ux` designs the values from the casting record and light-tuning log; active Agent Script tooling validates grammar; the target org supplies valid voice IDs; a human listening sign-off approves the result. Each value is `[review needed]` (H03 / H06 / H05 / H04 / `T-config`). On the default v3 model only `outbound_stability` applies; `outbound_speed`/`outbound_similarity` and `pronunciation_dict` require a Flash model. Preserve the Persona contract while tuning audible delivery.

```yaml
modality voice:
    voice_id: "<from the casting record — H09>"    # [review needed] until sign-off
    # Flat/legacy format → runs on the language default model (v3 Conversational). Model selection needs the emerging nested format — see H03.
    outbound_speed: 0.9                             # usable 0.7–1.1 (schema 0.5–2.0) — NO EFFECT on default v3; Flash-only (H03)
    outbound_stability: 0.5                         # honored on all models; v3 default 0.5 (Flash starting point 0.85) — H03
    outbound_similarity: 0.85                       # NO EFFECT on default v3; Flash-only (H03)
    inbound_filler_words_detection: True            # [review needed] strip um/uh/false starts — often True for telephony (H05)
    additional_configs:
        beepboop_config:
            max_wait_time_ms: 500                   # [review needed] latency floor (was 6000 default)
        speak_up_config:
            speak_up_first_wait_time_ms: 10000      # [review needed] no-input pursuit
            speak_up_follow_up_wait_time_ms: 10000
            speak_up_message: "[phrasebook pursuit token]"
    inbound_keywords:
        keywords: [ "<predicted STT-hostile terms — H05>" ]   # [review needed]
    # pronunciation_dict:                           # optional — custom pronunciation (H04); honored by Flash v2, likely inert on default v3
    #     - grapheme: "<term>"
    #       phoneme: "<IPA>"
    #       type: "IPA"
```

---

## Layer B — Rewritten user-facing copy

> Drop into Agent Script copy fields (welcome, error, prompts, confirmations).

### [original-string-id-or-quoted-source] → [rewritten]
- **Original:** "Please reply with yes or no to confirm."
- **Voice:** "Sound good?"
- **why:** T-translate-1 + T-translate-3

### [next entry…]

[Repeat for every changed string.]

---

## Layer C — Spoken-function phrasebook

> Drop into Agent Script as token sets. A signature set per function: rotate within it, never use the same token in adjacent turns, never invent off-palette tokens at runtime (T-phrasebook). When `persona.md` is supplied, seed it from the Persona's 2–4 alternatives and expand only with variants that are distinct by ear. Every variant must preserve register, function, Never-Say constraints, Lexicon meaning, immutable wording, and lexical Tone Flex. This is channel adaptation, not character redesign.

| Function | Tokens |
|---|---|
| Acknowledgment | [4–6 tokens, register-matched] |
| Holding | [3–4 tokens] |
| Repair (Tier 1) | [2–3 variants] |
| Repair (Tier 2 frame) | [2–3 frames; field-specific constrained vocabulary fills in at runtime] |
| Resumption | [2–3 tokens] |
| Pre-closing | [2–3 specific-offer frames] |
| Terminal | [2–3 tokens] |

**Register notes:** [one paragraph on the Persona register the phrasebook was tuned to — warm/cool, formal/informal, contractions/no-contractions. Without a Persona, say "inferred" and name the fallback register.]

---

## Layer D — Opening sequence

### System layer (formal, distinct voice, measured register)
[Brand + emergency redirect + recording and transcription disclosure + AI disclosure]

> Lives in: [IVR / carrier-side pre-call announcement IF available — see Layer E; otherwise voiced by agent in sequence]
>
> Critical: the system layer must sound clearly different from the agent layer (different TTS voice, pacing, register). The exact register choice is flexible; what matters is contrast.

### Handover
600–900ms pause, optional faint audio cue.

### Agent layer (the cast agent voice in the Persona's register, varied prosody, slightly slower than commercial baseline)
Three recurring elements, in order (see T-opening):
1. AI self-identification — [e.g. "Hi, I'm [Agent Name], [Brand]'s AI assistant." Name and brand from the Persona, each with an H04 pronunciation entry and H05 keyword. Wording from the Persona; structure from B01.]
2. Capability frame — [set scope, not an open-ended "ask me anything"; e.g. "I can answer questions about …" or "I'll take a few details and log a case for the team to follow up by the next business day."]
3. Turn-final CTA — [a "How can I help you today?" variant (P9 end-focus)]

> Lives in: Agent Script `welcome`

---

## Layer E — Out-of-Agent-Script notes

> Items that cannot be encoded in instructions/copy. Hand off to platform/runtime owner.

### Voice latency triage  *(`[consider]` items; the owner makes the change)*

**Stage map** (from Phase 2):

| Stage | Role | Model | Prose words | Tools offered |
|---|---|---|---|---|
| [name] | [logic / router / classifier / speaking] | [pinned / default] | [n] | [n, guarded?] |

**LLM passes on the slowest turn:** [n] → expected delay about [n × 0.85–1.4 s + 0.3–0.7 s] (T-latency-costs)

For each hit: the finding, the field cost, a paste-ready snippet, and the owner (`agentforce-generate` voice-latency heuristics, or the platform owner for the checklist items). Covers router passes, fast model on speaking stages, model parity, `available when` tool guards, after-speech writes, pre-fetched context, prompt budgets, and the dynamic progress indicator (SKILL.md Layer E).

### [Item title]
- **What:** [config/setting]
- **Where it lives:** [carrier config / TTS engine / ASR vendor / SSML / runtime parameter]
- **Recommended value/policy:** [specific recommendation]
- **Why it matters:** [principle citation, e.g., P5-prosody, T-latency-long]

> Layer E is for what genuinely **cannot** be scripted. The in-script voice-channel config (`additional_configs` beepboop/speak-up, `inbound_keywords`, `inbound_filler_words_detection`, `pronunciation_dict`) is NOT here — it lives in the Voice channel configuration block above, written into the `.agent`. See H06 / H05 / H04 / `T-config`.

[Examples to include if relevant:]
- ASR confidence threshold for grounding escalation (recognizer-side, not in `.agent`)
- Barge-in detection tuning (on by default; no in-script sensitivity setting)
- Sensitive-digit capture via keypad (card / PIN / reference numbers, kept out of the recording and transcript) — DTMF is available; keyed digits arrive as plain text, so this is a privacy/routing concern, not an `.agent` key
- System/IVR-layer voice (cast against brief field 6, configured in carrier/IVR). The agent voice is not a Layer E item: its casting is in the vocal identity file (H08/H09) and its `voice_id` is in-script (H03).
- SSML support / prosody markup
- IVR / carrier-side pre-call announcement configuration
- Long-operation handling policy (warning copy + filler cadence) for >10s actions
- Utility-action implementations (Apex/Flow behind `format_currency`, `format_datetime`, escalation/link Flows)

---

## Audit detail (inline changes)

> Every non-trivial entry with rationale. Use `[changed]`, `[review needed]`, `[consider]` (optimize only), or `[out-of-scope]` tags.

### [changed] [location-in-source]
- **Original:** "[quote]"
- **Rewrite:** "[quote]"
- **why:** [principle citation]
- **layer:** [A / B / C / D / E]

### [review needed] [location-in-source]
- **Original:** "[quote]"
- **Voice principle violated:** [citation]
- **Why preserved:** [intentionality signal — e.g., compliance flag]
- **Recommendation:** [one sentence]

### [consider] [location-in-source]  *(optimize mode only)*
- **Current:** "[quote]"
- **Voice principle present but applied weakly:** [citation, e.g., P10-mis-1 — repair tier 2 identical to tier 1]
- **Suggested improvement:** "[quote of improved version]"
- **why:** [principle citation + mis-application ID from audit-rubric.md]

### [out-of-scope] [pattern detected]
- **Pattern:** [e.g., caller code-switches to another language mid-call]
- **Why not rewritten:** [gap in source library]
- **Suggested follow-up:** [e.g., add multilingual repair in v2]
```
