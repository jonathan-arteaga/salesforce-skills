# Voice UX principles reference

The 14 voice UX principles from the conversation design library. Use as the citation source for the audit's `why:` lines and as the audit rubric (see `audit-rubric.md`).

Source: https://github.com/phil-haenggi/conversation-design-library-v2 — `voice-ux-12-prompts` section.

**Companion white paper (the "why" behind these principles):** *Voice UX for Agentforce: Designing for the ear and encoding it into Agent Script* (Hänggi, 2026) is the citable write-up that grounds this skill. It sets out six consolidated principles (latency, turn-taking, turn composition/end-focus, working memory, repair, multimodal) and the three-surface encoding model, with the conversation-analysis literature behind them (Sacks/Schegloff/Jefferson on turn-taking and repair; Stivers et al. on cross-linguistic timing; Halliday and Quirk et al. on end-focus; Jefferson 1990 on three-part lists). Point stakeholders there for the reasoning; the P1–P14 breakdown below is the operational cut the audit runs against.

Citation prefix: **P** (e.g., `P3-no-input`, `P10-repair`).

---

## P1 — Barge-In & Overlap Management

**Summary:** Normalize user interruption as a feature, not error. Chunk information with clear "safe points" for interruption; distinguish between transitional overlap (natural), corrective (user fixes), and competitive (user interrupts). Design enables user control without repeating key data when interrupted.

**Voice vs. text contrast:** Text scrolls; voice is linear and uninterruptible without design intent. "Inability to interrupt long agent utterances ranks among top voice UX frustrations."

**Migration heuristic:** Long monologues in chat (multi-paragraph answers, lists) must be chunked into interruptible units in voice. **Turn-length budget:** default to 1–2 sentences per turn, around 20 seconds spoken at most. Put the answer in the first sentence. A third short sentence is allowed only for a caveat that has to come before the item it qualifies. Read-back of data the caller just gave may run longer. Anything beyond that, break it up and let the caller pull the rest. (Sources: Voice Quality Heuristics v1.2, 1–2 sentences / 10–20 s; *Designing for the Ear* enablement deck, ≤2 sentences.)

**Common mis-applications (optimize mode):** Chunking present but the chunks are still single utterances at runtime because there's no pause directive between them. Or chunks are short but lack a clear interruptible point ("safe place").

---

## P2 — Grounding & Confirmation

**Summary:** Scaffold confirmation with implicit (weave into next turn), explicit (restate for high-stakes), or graduated (escalate with risk) strategies. Avoid over-confirmation; use digit-by-digit verification for numbers; summarize all fields before irreversible actions.

**Voice vs. text contrast:** Text forms can show all values back at once; voice can't. Confirmation must be selectively allocated.

**Migration heuristic:** Replace "Is that correct?" with restatement that grounds *and* advances ("London, March 15th. Sound right?"). See `telephony-patterns.md#T-grounding` for field-type policy.

**Before/after:**
- Text (fine): "London? March 15? Economy?" [checkboxes]
- Voice (fails): "London?" / "March 15th?" / "Economy?" [six turns]
- Fixed: "London, March 15th, economy. Shall I search?"

**Common mis-applications (optimize mode):** Grounding policy exists but doesn't escalate on low ASR confidence — phone numbers and emails skim past on implicit echo even when the recognizer was uncertain. Or money/irreversible actions get only implicit echo, with no explicit summary + check before commit. Or over-confirms low-stakes fields with explicit "Is that correct?" patterns. Or asks for confirmation but proceeds before the user can object.

---

## P3 — No-Input & No-Match Escalation

**Summary:** Pursue silence without blame ("I didn't catch that," not "You weren't clear"). Vary reprompts; escalate from open to closed options to modality shift after 2–3 failures; preserve context when handing off.

**Voice vs. text contrast:** Text has no silence to interpret; voice must distinguish silence from confusion from disengagement.

**Migration heuristic:** Map every error message in the source script to a tier (1/2/3, see `telephony-patterns.md#T-repair`). Reprompt language varies per attempt.

**Common mis-applications (optimize mode):** Reprompt strings exist but are identical across tiers — the structure is there but the language doesn't escalate. Or reprompts vary but still blame the user ("you weren't clear", "I need you to speak louder").

---

## P4 — Opening & Closing Sequences

**Summary:** Openings: ~5–7s, end with clear question. Closings: three-step negotiation (pre-closing → topic confirmation → terminal exchange). Both must feel collaborative, never abrupt or drop-call-like.

**Voice vs. text contrast:** Chat openings can be paragraph-length welcomes; voice must front-load identity + first question quickly (~5–7s). Chat closings can be one line; voice closings are negotiated.

**Migration heuristic:** Chat openings notably longer than ~7s spoken length should be split. Insert pre-closing token before terminal in any flow that ends a transaction.

**Agent-layer structure:** the spoken welcome carries three elements — AI self-identification, a capability frame that sets scope (not an open-ended "ask me anything"), and a turn-final "how can I help?" question. Institutional/legal disclosures belong in the system layer, not the agent's welcome (see T-opening, B01, B02).

**Bring legal in early:** recording, AI-disclosure, and opt-in vs. opt-out consent requirements vary by country, region, state, and language — confirm them with legal before writing the opening, and revisit whenever the engagement adds a market or language (see B02).

**Common mis-applications (optimize mode):** Two-voice opening defined but the system and agent layers don't sound different — same TTS voice, same pacing, same register — so the user doesn't perceive a layer change. Or agent layer is too long, defeating the split. Or closing has a pre-closing token but no terminal exchange ("Bye now") — the call ends abruptly.

---

## P5 — Prosodic Design & Intonation

**Summary:** Intonation signals turn-taking and information structure; stress marks new vs. known information; pacing at 130–160 wpm for critical content. Use falling intonation for statements, rising for yes/no; lists rise on non-final items, fall on final.

**Voice vs. text contrast:** "The same words with different intonation can be a question, statement, surprise, or sarcasm." Text misses this entirely; voice must compensate.

**Migration heuristic:** Where SSML/prosody markup is supported (Layer E concern), recommend stress and pacing on numbers, names, and unfamiliar terms.

**Common mis-applications (optimize mode):** SSML present but applied generically — same `<prosody>` settings everywhere, no contrast between known/new information. Or stress applied to function words ("THE", "TO") rather than content words.

**Situational prosodic profiles (Persona expression).** When a completed `persona.md` exists, its Persona Tone Flex owns the trigger, semantic shift, lexical/discourse cue, maximum, hard boundary, and reset. This principle maps that policy to audible delivery; it does not redefine it. A voice persona has a *base* prosodic centre of gravity and shifts around it as the moment demands. Four recurring profiles are **Calm Authority** (measured pace, low pitch variation for high-stakes and error moments), **Grounded Warmth** (gently expressive for reassurance and rapport), **Dynamic / High-Energy** (faster, wider pitch for upbeat or celebratory beats), and **Conversational Baseline** (the neutral resting register). Situational shifts modulate toward another profile over 1–2 turns, then settle back according to the Persona reset. On ElevenLabs v3, use audio/tone tags (A08); on other models, use cadence, sentence length, punctuation-driven prosody, and voice settings (A09, H03). If this mapping would change character or lexical Tone Flex, mark `[review needed]`.

**Dimension → delivery.** The four profiles are the realisation vocabulary. This table is the bridge from Persona dimension values to them:

| Persona dimension | Voice realisation (this skill) |
|---|---|
| Warmth, Emotional Coloring | Resting tag (v3) and stability band; agent-layer pace |
| Personality Intensity | Stability range, tag density, breadth of pitch range |
| Empathy | Size of the shift on Tone Flex distress triggers (`[reassuring]` / `[softly]`, pace down to ~90%) |
| Brevity | Spoken turn-length budget and chunking. **Not** speech rate: speed is inert on v3 (H03) |
| Humor | Light prosodic play only. No laughter or body-sound tags (Z05) |
| Formality | Discourse markers; system layer formal. Contractions stay even in a formal register (A09) |
| Reading Level | Lexical load per chunk; number and identifier pacing |
| Punctuation, Formatting, Emoji, Capitalization | Their voice equivalents: pause and intonation; verbal signposting ("two things…"); prosodic affect; focal stress |
| Personification | Expressive ceiling; A10 floor applies regardless (feelings licensed by the Persona → `[review needed]`) |
| Negative Identity | "Must not sound like" items in the Vocal Identity brief (H08) |

**Lexical–prosodic sync.** Each Tone Flex trigger pairs one lexical cue (Persona) with one prosodic shift (this skill). They fire together and reset together. Excited words in a flat voice, or a sober line in a bright one, sound insincere (A08).

---

## P6 — Sequential Information Gathering

**Summary:** One question per turn, asked in natural narrative order (not data-schema order). Acknowledge briefly; leverage user-volunteered info; signal progress for sequences >5 fields. **Cap spoken lists at three items** — conversational lists recurrently follow a three-part structure (Jefferson 1990); reading more than three options at once overruns working memory. Above the threshold, give headlines first and details on request.

**Voice vs. text contrast:** "Stacking multiple questions violates adjacency-pair structure." Text forms can ask many fields at once; voice adjacency pairs demand strict turn-by-turn sequencing.

**Migration heuristic:** Find every place the script asks for two or more pieces of info in one turn. Split. Reorder if data-schema order doesn't match how a person would volunteer it. When a caller volunteers several details at once, capture all of them (see I02) rather than re-asking — one-per-turn governs *asking*, not *accepting*.

**Common mis-applications (optimize mode):** One-question-per-turn followed correctly, but field order matches the database schema rather than natural narrative (e.g., asking DOB before name, or postcode before address line 1). Or progress signaling absent for sequences >5 fields, leaving the user uncertain how much longer.

---

## P7 — Silence & Latency Management

**Summary:** Silences >700ms are perceptible; >1s trigger user remedial action. Pre-announce processing time; use acknowledgment bridges ("Let me check..."); use verbal fillers every 3–5s for longer waits. Never timeout silently.

**Voice vs. text contrast:** Text has no latency perception (spinner suffices); voice requires active communication during processing.

**Migration heuristic:** Audit every action/tool call in the source script. For each, ask: how long does this take? If >1s, the LLM must say *something* before invoking it. For multi-second processing, follow up with verbal fillers every 3–5s. See `telephony-patterns.md#T-latency`.

**Before/after:**
- Text (implicit): [spinning wheel]
- Voice (must be explicit): "Let me search... [pause] Comparing airlines... [pause] Cheapest is $845."

**Common mis-applications (optimize mode):** Pre-announce exists for some actions but not all — usually the slowest ones get covered, but a 2–3 second lookup gets missed. Or pre-announce is identical for every operation regardless of expected duration ("Let me check…" used for both a 1-second cache hit and a 12-second multi-system join). Or processing >3s has no verbal filler, so the user starts wondering if the line dropped.

---

## P8 — Turn Design & Progressivity

**Summary:** Each turn accomplishes *one* action and advances toward completion. Structure as: framing + core action + transition relevance place signaling turn-end. No multi-part requests.

**Voice vs. text contrast:** Text turns can pile on framing, action, and follow-up. Voice turns must be atomic.

**Migration heuristic:** "Multi-part" is anything that asks the user to track more than one thing. Split. Sequence in natural narrative order.

**Common mis-applications (optimize mode):** Turns are atomic by count but still cognitively multi-part — e.g., "I'll need your date of birth and the year you joined" framed as one question because both are dates. The user has to track two things.

---

## P9 — Turn-Final Placement & End-Focus

**Summary:** Put critical/novel information last (recency effect). Questions always at turn-end. Before eliciting a choice, present all options first. Three rules follow from end-focus:
- **Context first, news second.** State the frame before the focal element ("Regarding your Thursday appointment: it's been moved to 3PM").
- **Caveats before the item they qualify.** A price followed by "non-refundable" feels like a bait-and-switch; "This non-refundable option is $100" frames the trade-off honestly.
- **Let information structure win over style dogmas.** Use the passive voice when it places the key information last — "Your claim will be handled by our specialist team" properly emphasizes the team. End-focus outranks "avoid passive voice."

**Voice vs. text contrast:** "Turn-final position carries highest perceptual weight in spoken interaction… spoken language is ephemeral — users cannot re-read." Text allows scanning; voice requires information architecture restructuring.

**Migration heuristic:** Reverse turns where the question comes before context. "What date works for you? I have slots Tuesday, Wednesday, Friday." → "I have slots Tuesday, Wednesday, Friday. What works?" Move any caveat (fee, non-refundable, eligibility) ahead of the item it qualifies.

**Common mis-applications (optimize mode):** End-focus respected for questions, but critical confirmation data is buried mid-turn ("Right, I've booked your appointment for 3pm at the Highgate clinic, and I've sent you a text confirmation"). The user remembers "text confirmation" and forgets the time and location.

---

## P10 — Voice Conversation Repair

**Summary:** Four-level hierarchy: open repair (weakest) → question word + partial → candidate understanding → explicit correction (strongest). Never over-apologize; escalate after 3 failures to alternative modality.

**Voice vs. text contrast:** Text can show "we couldn't find that, please try again"; voice must repair *while* preserving conversational momentum.

**Migration heuristic:** See `telephony-patterns.md#T-repair`. Map each repair instance in the script to a tier; vary reprompt language across tiers.

**Before/after:**
- Turn 1: "Sorry, what was that?" [open]
- Turn 2: "Did you mean change it on the account, or update the number?" [targeted]
- Turn 3: "You mean cancel order 7-8-4-2?" [candidate]
- Turn 4+: "Can you spell that?" or "I'll text you a link" [modality shift]

**Common mis-applications (optimize mode):** Tier ladder defined but tier 2 is not actually a constraint or candidate understanding — it's just a rephrase of tier 1 ("Sorry, could you say that again?" → "Sorry, I didn't catch that — could you say it once more?"). Or tier 3 hands off but doesn't preserve state, forcing the user to restart.

---

## P11 — Voice Persona & Phrasebook

**Summary:** Select a signature set of 4–6 acknowledgment tokens and use it consistently. Avoid register mixing; map lexical choices to prosodic profiles. "Linguistic fingerprint" becomes brand identity in voice-only interfaces.

**Voice vs. text contrast:** Text can survive register mixing (the user re-reads); voice register inconsistency reads as fake or unstable.

**Migration heuristic:** Inventory acknowledgments and discourse markers across the source script. If they don't form a coherent set, build one. See `telephony-patterns.md#T-phrasebook`.

**Common mis-applications (optimize mode):** Phrasebook exists but is below the signature-set minimum (no rotation possible). Or tokens mix registers within a function ("Got it" / "Thank you so much" / "Right" — three different formality levels for the same purpose). Or rotation is defined but the LLM picks the same token every turn anyway because the instructions don't enforce variation.

**Expressing Persona through delivery.** When `persona.md` is supplied, its Phrase Book and lexical Tone Flex determine which words and situation patterns carry the character; delivery determines how they sound. Layer C may expand 2–4 Persona alternatives into a signature set (4–6 for acknowledgments; see T-phrasebook for other functions) only when register, meaning, Never-Say constraints, immutable wording, and Tone Flex boundaries stay intact. On ElevenLabs v3, audio/tone tags in `system.instructions` (A08) map those situations to audible delivery without changing `voice_id`. On non-v3 models, use cadence and voice settings (A09, H03). Keep the palette small and consistent, and never let the agent claim what it should convey; warmth is delivered, not asserted in the first person ("I'm so excited"), which is the self-reference rule A10.

---

## P12 — Voice-to-Screen Handoff

**Summary:** Announce what/where/why before transitioning. Pre-populate all voice-collected data; preserve context with deep links. Offer voice-return option; frame as smart modality choice, not failure.

**Voice vs. text contrast:** Text-to-text handoffs are seamless; voice-to-screen requires explicit announcement and context bridging.

**Migration heuristic:** Read the "crossmodal handoff channels" trait. If a screen / web handoff channel is available, design handoff turns. If SMS or email is available, design link-send patterns. If no crossmodal channel is available, Tier 3 escalation must be human-handoff (see T-repair-tier-3). (Crossmodal = a sequential shift out of voice; distinct from a multimodal voice-over-web channel where a UI co-exists — see the terminology note in `telephony-patterns.md`.)

**Common mis-applications (optimize mode):** Handoff exists but announces only the modality ("I'm sending you a text") without the what/where/why ("I'm sending you a link to upload your ID. Once you've done that, I'll pick up where we left off"). Or handoff drops collected state, forcing the user to re-supply data on the new modality. Or the escalation was triggered by one intent in a multi-intent call and the handoff only forwards state for that intent, silently dropping the caller's other open intents — the "repeat yourself" problem returning through the back door (couples with P14).

**Handoff to *capture*, not only to *deliver*.** The familiar handoff mails something out — a tracking link, a document to read. But a screen handoff can also be the *input* surface: when a value is too exact for voice (an email, a long case-sensitive reference), hand off so the caller **types** it, then bring it back into the call. The production-honest, available-today shape is **caller-cued** — text a prompt, the caller types and says "done", the agent reads the value back from the messaging session and confirms (pattern D08). The tempting *event-driven live-sync* version — where the agent continues automatically the instant the caller submits, with no "done" cue — is **aspirational / not out-of-the-box** on Agentforce Voice today: it needs a screen surface wired to the voice session with event write-back the runtime can react to. Design toward it, but ship the caller-cued read-back and flag live-sync as a Layer E / roadmap item. Everything this principle requires of a delivery handoff — announce what/where/why, pre-populate collected state, offer a voice-return path, frame as the smart choice — applies to a capture handoff too.

---

## P13 — Emotional De-escalation

**Summary:** Distinguish distress from abuse and route them differently. A distressed caller (financial stress, delivery worry, health worry, repeated failure fatigue) needs warmer routing and a faster path to a human; an abusive caller needs a firm named warning and, if it continues, a documented terminate path. Sentiment features flatten the two into one signal — policy must not.

**Voice vs. text contrast:** Text lets the user disengage silently (walk away from the tab); voice keeps the caller on the line, which raises the stakes of any misclassification. A "we're going to end this call" message that fires on frustration reads as punitive; a lack of any de-escalation path when abuse actually happens leaves the human on the other end unprotected.

**Detection is lexical-only (know the limit).** Sentiment and distress are inferred from the STT transcript's *words alone* — the reasoning engine receives text, not the acoustic signal, so tone, pace, volume, and prosodic distress cues are invisible to detection. Where P5 notes prosody is lost on the way **out** (TTS), the same gap exists on the way **in**: a calm-worded but genuinely distressed caller can read as neutral, and a clipped-but-fine caller as negative. Treat any sentiment signal as a lexical proxy, not a read of the caller's actual state — do not gate hard actions (termination, forced transfer) on it alone. Acoustic/prosodic sentiment input is a platform-side (Layer E) limitation, not something the script can fix — a known gap with a VoC request raised, tracked for v2.

**Migration heuristic:** For any script with an auto-terminate path outside a Tier-4 explicit-threats branch, flag it. For any script with no distress branch at all, flag it. The skill's job is to surface presence/absence and route to the right shape — it does not prescribe the tier copy.

**The two hard rules:**
- **Distress ≠ abuse.** Do not conflate. If the audit sees a single "escalate on negative sentiment" path, that is almost always the wrong shape.
- **Termination is a Tier-4 event.** Explicit threats or sustained abuse after a named warning. Not a repair fallback. Not a frustration signal. Hanging up on a distressed caller is the reputational failure mode.

**Common mis-applications (optimize mode):** Auto-hangup path is triggered by any negative-sentiment signal (frustration counted as abuse). Or the script has escalation copy for abuse but no distinct branch for distress — the frustrated caller gets the same firm-warning treatment as the abusive one. Or the distress branch exists but ends the call rather than warm-transferring.

**Couples with:** F01 (crisis-flow-no-hangup) — the "no auto-terminate" rule generalises from crisis into any distress signal.

---

## P14 — Multi-Intent Handling

**Summary:** A single caller turn can contain more than one intent ("Can I change my address, and also when's my next delivery?"). Voice lets the caller volunteer several things at once; the agent needs to hear all of them, address each, and verify all parts resolved before closing. In real transcripts this is common, not exotic — one large delivery had multi-intent turns in over half of escalated calls. Two field deliveries prioritised competing intents in practice, not by order-of-mention — one used a design-time priority list ranking intents by domain importance, and runtime signals (urgency, blocking dependency) drive the same discipline where no fixed list exists. This is the field pattern the sequencing sub-step below encodes.

**Voice vs. text contrast:** Chat can render each intent as a separate message thread or card; voice has only turn order. The agent must (a) not lose intents it didn't answer first, and (b) not answer only the "loudest" one.

**Migration heuristic:** Three-step pattern the audit looks for — **acknowledge → segment → verify**:
1. **Acknowledge and sequence** — echo the intents heard and set the order. When one intent takes precedence — a runtime signal (urgency, blocking dependency, resource contention) or a design-time priority list ranking intents by domain importance — name the reason for the order ("Sounds like a billing question and an outage. Let's start with the outage since that's time-sensitive."). When intents are non-competing, a plain echo with the sequence implicit is enough ("Sure. Balance first, then your next payment date.").
2. **Segment** — answer each in turn, with a brief transition between ("First, the delivery… Now, on the address change…").
3. **Verify** — before closing, check that every part was resolved ("Did that cover the address change and the delivery question, or is there more I can help with?").

Flag as `[consider]` if the script has multi-intent handling that skips step 1 (agent silently addresses one intent), sequences competing intents without naming a reason (e.g., addresses a billing dispute before an outage without acknowledging the outage is time-sensitive, or ignores the topic's priority list where one exists), or skips step 3 (agent closes without verifying all parts). Flag as `[changed]` if a real transcript shows multi-intent turns and the script has no handling at all.

**Handle-time tradeoff.** Acknowledge adds a turn, but the alternative — silently picking one intent and hoping — costs far more when the guess is wrong. Naming a sequencing reason costs another beat; only spend that beat when the order matters (urgency, dependency, resource contention). Don't justify sequencing the caller doesn't need justified.

**Common mis-applications (optimize mode):** Agent addresses the first intent and drops the second silently. Or agent acknowledges both but bundles the answers ("The delivery is Thursday and to change your address say your new postcode") — that's a Turn-Atomicity (P8) violation on top. Or agent answers each but closes without verifying — the caller has to re-raise the second intent. Or agent sequences competing intents arbitrarily (first-mentioned-first) when one is obviously time-sensitive, blocking, or ranked higher on the topic's priority list.

**Couples with:** P8 (turn atomicity — each intent gets its own atomic turn), P6 (sequential info gathering — if answering an intent requires new slots, gather them one at a time), and P12 (handoff — on escalation from a multi-intent call, the handoff must carry all open intents forward, not just the one that triggered escalation).

---

## Gaps in source library (not covered by P1–P14)

The library does not cover these. The skill should not invent rewrites for them in v1:

- Multi-turn cascading error recovery (downstream impact of corrected fields). *Partly addressed:* the single-correction case (replace only what changed, keep the rest, redo the action) is `T-translate-correction`. Corrections that invalidate already-completed downstream actions are still uncovered.
- Multilingual / accent-clash handling
- Agent-to-agent skill transfer

If the audit detects one of these patterns in the source, flag as `out-of-scope` rather than rewrite.
