# Telephony patterns reference

Operational patterns for chat→voice migration. Adapted from `Projects/nuffield health/cross cutting telephony patterns.md`. The skill consults this at runtime — do not regenerate, look up.

For the design reasoning behind these patterns (and the Agent Script encoding of each), see the companion white paper *Voice UX for Agentforce: Designing for the ear and encoding it into Agent Script* (Hänggi, 2026) — cited in `voice-ux-principles.md`.

Citation prefix: **T** (e.g., `T-grounding`, `T-repair-tier-2`).

**Modality terminology (used throughout the skill):**
- **multimodal** — modalities co-exist on equal footing in the same session (e.g. voice-over-web, where voice and a chat/visual UI run side by side). Gates the "keep if multimodal" branches in A03, C01, C03, C05, H01, H02.
- **crossmodal** — a sequential shift *out of* voice into another channel (voice → SMS / email / screen) to deliver something voice can't carry well, e.g. a tracking link or product-info link. This is the handoff vocabulary (P12, D05, C04, E03).

---

## T-translate — 8 chat→voice translation rules

Direct text-to-voice translation introduces text-shaped scaffolding that doesn't fit voice. Apply these rules to every user-facing string.

| ID | Category | Chat-form | Voice-form |
|---|---|---|---|
| T-translate-1 | Input-shape instructions | "Please reply with yes or no" | (just ask the question) |
| T-translate-2 | Interface verbs | "Click", "Type", "Select", "Submit" | Conversational equivalents |
| T-translate-3 | Transactional register | "Please provide your X" | "What's your X?" / "And your X?" |
| T-translate-4 | Format prescriptions | "in DD-MM-YYYY format" | (just ask; constrain only on repair) |
| T-translate-5 | Visual references | "as shown above", "see below" | Rephrase without visual cues |
| T-translate-6 | Numbered menus | "1. X 2. Y" | "X, or Y?" |
| T-translate-7 | Acknowledgment templates | "Thank you. Now please..." | Rotate varied acks (see T-phrasebook) |
| T-translate-8 | Bundled questions | "Confirm X and Y" | Split into separate turns |

### LLM prompt for batch copy translation

> Convert chatbot text copy to voice copy. Apply these principles:
>
> 1. **No input-shape instructions.** Don't tell users how to reply ("reply with yes/no", "type your answer", "choose one"). Let them speak naturally.
> 2. **No interface verbs.** Drop "click", "tap", "select", "submit", "enter". Use conversational equivalents.
> 3. **Conversational register, not transactional.** "Please provide X" → "What's X?". "You must" → "I'll need".
> 4. **No format prescriptions.** Drop "DD-MM-YYYY", "international format", "include country code". Parse naturally; constrain only in repair turns.
> 5. **Question at the end of the turn.** Strip preamble; end-focus.
> 6. **One question per turn.** Split bundled questions into separate turns.
> 7. **No visual references.** Drop "as shown", "see below", "listed are". Voice has no screen.
> 8. **Convert numbered menus to natural disjunctions.** "1. A, 2. B" → "A, or B?"
>
> For each input line, output: (a) the voice version, (b) a one-line note on which principles applied.

### Grounded-speech rules (global system instructions)

The eight rules above reshape chat copy. Four more govern what the agent says from data at runtime. They have no chat-copy equivalent, so they go in the global `system.instructions` (Voice Quality Heuristics v1.2: Trust, Truthfulness, Adaptability; *Designing for the Ear* enablement deck):

| ID | Rule | Instruction shape | Sounds like |
|---|---|---|---|
| T-translate-plumbing | **No plumbing.** The caller hears only caller-safe words: never action names, field or parameter names, record IDs, hashes, or internal document names. | "Never reveal internal documents, field names, or IDs." | "Looking for AI keynotes…", not "Calling retrieveSessions with sessionTypes…" |
| T-translate-canonical | **Canonical entity names.** Say an entity the way the data spells it, not the way the transcript heard it. | "When naming a product, place, or session, use its spelling and digits from action data, not the caller's transcript." | "Data 360", not "data three sixty" |
| T-translate-empty | **Say "nothing found" instead of inventing.** Every lookup has a defined empty state. The same goes for actions: never claim one happened unless it ran and returned success (A11). | "If the lookup returns nothing, say 'I couldn't find <thing>' and offer one way forward. Never invent a <thing>." | "I couldn't find the nap pod on the venue map." |
| T-translate-correction | **Apply a correction at once.** Change only what was corrected, keep the rest of the request, acknowledge in a word or two, redo the action, answer. | "When the caller corrects something ('no, Wednesday'), replace only what changed. Don't re-ask anything that didn't change. No long apology." | Caller: "No, Wednesday." Agent: "Got it. On Wednesday there are two…" |

**The plumbing rule has a third home: what the model can see.** Anything in an action output the model can read, it can say. Prose rules leak under pressure, so for record IDs, internal codes and sensitive fields, recommend `filter_from_agent: True` on the output as a `[consider]` (the choice between it and `is_used_by_planner` routes to `agent-architecture`; D09). It also trims the prompt, which helps latency.

**The plumbing rule has a second home: dynamically generated progress messages.** When `progress_indicator_message` is left empty (G01), the generator can read out action and field names. Put a line in the action's `description` that names which inputs the progress line may mention and forbids the rest.

---

## T-grounding — Grounding policy by field type

Risk-stratified, not one-size-fits-all. Use as a decision table when rewriting confirmation logic.

| Citation ID | Field type | Default grounding | Trigger to escalate |
|---|---|---|---|
| T-grounding-ack | Common acknowledgments | None | — |
| T-grounding-postcode | Low-stakes single values (date, single name, postcode) | Implicit echo | Low ASR confidence |
| T-grounding-name | Names | Implicit echo (high confidence) → phonetic (low confidence) | Cultural diversity, ASR confidence threshold |
| T-grounding-phone | Phone numbers | Implicit echo (high confidence) → explicit digit-by-digit (low confidence) | Low ASR confidence |
| T-grounding-email | Email | Implicit echo (high confidence) → explicit char-by-char with improvised phonetics on the disputed segment (low confidence); type-don't-say screen handoff (D08) when char-by-char is impractical | Low ASR confidence |
| T-grounding-money | Money / irreversible actions (booking commit, T&Cs accept, payment, age confirmation) | Explicit summary + yes/no check | Always |
| T-grounding-soft-check | Apparent inconsistencies (e.g. name vs. email) | Soft check | Always |

**Implication for instructions (Layer A):** Encode grounding as conditional behavior keyed to field type. Don't write a flat "always confirm" rule — that produces over-confirmation on low-stakes fields and under-confirmation on irreversible ones.

**Common mis-applications (optimize mode):**
- Field-type policy exists but doesn't actually escalate on low ASR confidence — phone/email pass on implicit echo even when the recognizer was uncertain.
- Money/irreversible actions get only implicit echo, with no explicit summary + check before commit.
- Over-confirms low-stakes fields with "Is that correct?" patterns.
- Confirms but then proceeds before the user can object (no pause for correction).
- "Always confirm" flat rule disguised as field-type policy — same behavior across all fields.

---

## T-repair — Repair tier ladder

| Tier | Trigger | Response shape |
|---|---|---|
| T-repair-tier-1 | First ASR no-match | Open repair: "Sorry, I missed that. Could you say it again?" |
| T-repair-tier-2 | Second no-match on same field | Rephrase or constrain vocabulary ("You can say morning, afternoon, or evening. Which works?") |
| T-repair-tier-3 | Third failure or user frustration | Human handoff with full state preservation |

**Telephony note:** Telephony lacks the typing-fallback that voice-over-web has; Tier 2 rephrasing and Tier 3 handoff carry more weight. State always travels with the handoff — the user never starts over.

**Format-prescription rule:** Format prescriptions ("could you say it as day, month, year?") and constrained vocabularies ("just yes or no") are legitimate **only at Tier 2**. They are anti-patterns as defaults (see T-translate-4).

**Keypad (DTMF) as a repair channel — numeric fields only.** DTMF is GA; keyed digits arrive as exact plain text, so for a **numeric** value (phone, reference / case number, card) offering the keypad is a strong Tier-1 / Tier-2 repair — "you can say it again, or tap it in on your keypad" — and it doubles as a privacy device for sensitive numbers (D04, D06). It is **not** available for alphanumeric values: a keypad can't carry letters, so email and mixed IDs escalate to letter-by-letter with improvised phonetics on the disputed segment (Tier 2) and then a type-don't-say screen handoff (Tier 3, crossmodal), never the keypad (D05, D07, D08).

**Common mis-applications (optimize mode):**
- Tier 2 prompt is just a rephrase of Tier 1 — no constraint, no candidate understanding.
- Tier 1 reprompt blames the user ("you weren't clear", "I didn't understand you") rather than the system.
- Tier 3 handoff exists but doesn't preserve state — the user has to start over with the human.
- Same reprompt string used across tiers (no escalation in language).
- Format prescription leaked into Tier 1 default (anti-pattern; only legitimate at Tier 2).

---

## T-latency — Latency budget

| Operation | Acceptable silence | Required affordance |
|---|---|---|
| T-latency-ack | Acknowledgment, simple confirmation | <1s | None |
| T-latency-lookup | Brief lookup (slot availability, basic record) | 1–3s | Pre-announce ("Let me check…") |
| T-latency-complex | Complex processing (multi-system) | 3–10s | Pre-announce + verbal filler every 3–5s |
| T-latency-long | Anything >10s | — | Pre-announce + verbal filler every 3–5s; warn the user it may take a while |

**T-latency-costs — what each step costs (field, Oct 2026).** Measured on one Agentforce Voice + Amazon Connect build, one live call per version, so treat the numbers as directional:

| Step | Typical cost | On the critical path? |
|---|---|---|
| Input guardrail | ~0.08 s | Yes |
| HyperClassifier routing | ~0.10 s | Yes |
| Deterministic router (phase variable, no prompt) | ~0 s | Yes |
| Generative LLM pass, fast model | 0.85–1.4 s | Yes |
| Generative LLM pass, large model | up to ~2.8 s | Yes |
| Apex invocation (fixed overhead) | 0.25–0.35 s, spikes to ~1.3 s | Yes |
| Trust Layer checks (instruction adherence, groundedness) | 1–5 s | No: they run async |

Latency tracks the number of LLM passes run back to back in a turn, not output length or prompt prefill. TTS streams, so speech starts once the final pass begins. The floor is about one generative pass plus 0.3–0.7 s of platform overhead; the shortest turns hit about 1.3 s. That's why the Layer E latency triage counts passes first. (Source: Agentforce Voice Agent Assessor, Measure latency tab.)

**Implication for instructions (Layer A):** The LLM must say *something* before any non-trivial pause. Encode this as a behavioral rule, not a copy string.

**T-latency-pre-announce** — operational umbrella for all four tiers above when the operation is >1s: pre-announce verbally before any tool/action call expected to take >1 second; vary across the phrasebook; never start a tool call silently. Used as the citation in pattern files that don't need to specify a tier.

**T-latency-filler-audio** — the three-layer latency model. Three different things fill silence, and they are easy to blur; a well-tuned voice agent uses at least layers 1 and 3:

1. **Platform filler audio (non-verbal floor).** Agentforce Voice's `beepboop_config` plays a `.wav` after an action has been running for a configurable delay. **Platform default 6000ms; recommend 500ms.** Starting it at ~0.5s covers the whole 3–4s (sometimes 7–8s) latency band and reads as ambient "working"; starting it at 6s accentuates slowness and leaves most waits partly uncovered. The delay is authored **in-script** at `modality voice: → additional_configs: → beepboop_config: → max_wait_time_ms:` (500–60000ms) — the skill writes it directly (see `T-config` and H06). The `.wav` audio asset itself is platform-supplied.
2. **Spoken filler sentences (`outbound_filler_sentences`, agent-wide).** Flat syntax: `outbound_filler_sentences:` → `- waiting: ["…", "…"]`. Write them in the persona's voice; three variations of "Please wait." undo the persona work. See G01.
3. **Per-action `progress_indicator_message` (verbal, meaningful).** Authored conversational line voiced during the wait; prioritise on the long/slow actions. Requires `include_in_progress_indicator: True` on the same action definition or it never plays. See G01. Keep it conversational, not text-shaped ("Let me look that up…", not "Getting answers…"). Leave it empty (`""`) and the agent generates one at runtime in the caller's language; a fixed message also renders as text on web; several variants separated by `\n` rotate (Script view only). If the caller hears "let me check" over and over, trim the tool calls rather than rewording the line.

**Common mis-applications (optimize mode):**
- Pre-announce exists for slow operations but missing for medium ones (1–3s lookups).
- Same pre-announce string used regardless of expected duration ("Let me check…" for both 1s and 12s operations).
- Verbal fillers absent for >3s operations (silent processing).
- For >10s operations, no warning that it may take a while — the user starts wondering if the line dropped.

---

## T-config — In-script voice-channel configuration

Several timings, the STT bias list, the filler-word flag, and the custom-pronunciation dictionary are authored **in the `.agent` file**, inside the top-level `modality voice:` block — not in Workbench. The compiler enforces the ranges, so a design that needs a value outside them isn't expressible. Encode these directly (see H03, H04, H05, H06); reserve Layer E for what genuinely can't be scripted (TTS voice casting, SSML, ASR confidence thresholds, carrier/IVR). Note that `voice_id` + `outbound_*` run on the language **default model** (v3 Conversational for most languages), which honors only `outbound_stability`; selecting a Flash/other model to make speed/similarity/custom-pronunciation bite requires the emerging nested format (see H03).

| Citation ID | Key (path under `modality voice:`) | Range | Recommended | Governs |
|---|---|---|---|---|
| T-config-beepboop | `additional_configs → beepboop_config → max_wait_time_ms` | 500–60000ms | 500 | Filler-audio delay (P7 latency) |
| T-config-speakup | `additional_configs → speak_up_config → speak_up_first_wait_time_ms` / `…_follow_up_wait_time_ms` / `speak_up_message` | timers 10000–300000ms | 10000 + a holding token | No-input pursuit (P3) |
| T-config-keywords | `inbound_keywords → keywords` | list | predicted terms | STT key-term biasing (see H05) |
| T-config-filler-words | `inbound_filler_words_detection` | boolean | `False` (often `True` for telephony) | Strip um/uh/false starts from the transcript (see H05) |
| T-config-pronunciation | `pronunciation_dict` | list of {grapheme, phoneme, type: IPA\|CMU} | as needed | In-script custom pronunciation — **honored by Flash v2; likely inert on default v3** (see H04/H03) |
| T-config-voice | `voice_id`, `outbound_speed` (schema 0.5–2.0, usable 0.7–1.1), `outbound_stability`, `outbound_similarity`, `outbound_style_exaggeration` | see H03 | per persona | Voice selection & delivery — **speed & similarity are inert on the default v3 model; only stability is honored** (see H03) |

**Speak-up gotchas:** speak-up timers can't go below 10000ms. After three unanswered speak-ups the call ends with no closing line. Don't use "Are you still there?" as `speak_up_message` (H06). Leave `endpointing_config` at its default.

**Platform-default trap:** omit `beepboop_config` and the platform applies a 6000ms delay — most waits finish before the filler starts, so the caller hears raw silence. The 6000ms is a *platform* default, not a schema default; the value belongs in-script.

**Implication for encoding:** the skill writes these in Phase 7 with the recommended defaults and flags each `[review needed]`. `beepboop` is a low-risk latency win; `speak_up` changes no-input behavior and wants a listen before shipping.

## T-phrasebook — Spoken-function phrasebook scaffold

Rotating tokens prevent robotic repetition; recurring tokens give the agent a recognisable character. The phrasebook needs both, so it works as a **signature set** per function:

- **Seed from the Persona.** When `persona.md` is supplied, start from its Phrase Book's 2–4 alternatives. Expand only with variants a listener can tell apart by ear, preserving register, meaning, exact Never-Say constraints, immutable wording, Lexicon meaning, and Tone Flex boundaries. This is channel adaptation, not character redesign.
- **Set size by frequency.** Acknowledgment: **4–6** tokens (it's the most frequent function). Holding and tier-1 repair: 3–4. Resumption, pre-closing, terminal: 2–3.
- **Rotate within the set only.** Never the same token in adjacent turns. Never invent off-palette tokens at runtime: a new token the Persona didn't sanction is a small character change.

Without a Persona input, infer cautiously from the Script/sample and label the character evidence inferred.

| Function | Default tokens (rotate) |
|---|---|
| Acknowledgment | "Got it." / "Okay." / "Right." / "Sure." / "Thanks for that." / "Alright." |
| Holding | "One moment…" / "Let me check that…" / "Bear with me…" |
| Repair | "Sorry, I missed that. Could you say it again?" / "Just to be sure…" |
| Resumption | "Okay, where were we…" / "Right, so…" |
| Pre-closing | One specific, grounded next step: "Want me to check your other order too?" / "Should I text you the tracking number?" Or close if nothing useful is left. |
| Terminal | "Take care." / "Bye now." |

These are fallback starting points only. A completed Persona contract takes precedence; voice adaptation may not silently change its register or character.

**Acknowledgment rotation.** Acknowledgments are where repetition is most audible, so they get firm numbers (Voice Quality Heuristics v1.2):
- Rotate **4–6** acknowledgment tokens. Fewer than 4 can't avoid repeats over a normal call; more than 6 starts to mix registers.
- **Never the same token in adjacent turns.** (The Voice Quality Heuristics score a token repeated more than 3× in a row at the floor; the design rule is stricter on purpose.)
- Keep each acknowledgment short (**3–5 words**) and put it **before** the substance: "Got it. Your order shipped Tuesday.", not a closing "…, okay?".
- An acknowledgment isn't required on every turn. Skip it when the answer itself shows you heard.
- Write the rule into the instructions, not just the token list, or the model picks the same token every time: "Vary how you acknowledge. Rotate between [tokens]; never use the same one twice in a row."

Audit floor: the same acknowledgment token **8 or more times in one call** scores at the floor for that heuristic.

**Pre-closing is a specific offer, not "Anything else?"** After the task is resolved, offer **one** next step that follows from what just happened ("Want me to check your other order too?"), or close. Generic "Anything else I can help with?" is an open question the caller has to search memory to answer, it adds a turn to every call, and it reads as a script. Never re-offer something the caller already declined. If nothing useful is left, end after the answer. The Voice Quality Heuristics allow one proactive offer per resolved task; stacking offers scores at the floor.

**Common mis-applications (optimize mode):**
- Phrasebook defined but below the signature-set minimum (4 for acknowledgments, 3 for holding and repair, 2 for the rest): no real rotation possible.
- Tokens within a function mix registers (e.g., "Got it" + "Thank you so much" + "Right" — three different formality levels for the same purpose).
- Rotation defined but the LLM picks the same token every turn anyway because the instructions don't enforce variation.
- Phrasebook copied verbatim from the scaffold without adjustment to the agent's persona.

---

## T-opening — Two-voice opening structure

| Layer | Voice characteristics | Content |
|---|---|---|
| T-opening-system | Distinct TTS voice; formal, measured register | Brand, emergency redirect, recording and transcription disclosure, AI disclosure |
| T-opening-agent | The cast agent voice (H09), in the Persona's register; varied prosody, slightly slower than commercial baseline. *(No Persona: fall back to a warm, measured register, labeled inferred.)* | Self-identification, capability frame, first-topic question |
| T-opening-handover | 600–900ms pause; optional faint audio cue | — |

**Carrier branching:**
- **If IVR / carrier-side pre-call announcement is available** (modality trait): system layer plays before the agent connects. Agent layer is shorter, no disclosure repetition.
- **If not available**: agent voices both layers in sequence with the handover pause.

**Implication for Layer D:** The opening is split across artifacts. System-layer content may live in IVR / carrier configuration (Layer E), agent-layer content lives in the Agent Script welcome.

**Design default, not a client-specific choice.** Treat the IVR / Agentforce split as the recommended default for any voice engagement with disclosure requirements. Separating institutional/legal content (system layer) from the conversational welcome (agent layer) applies broadly — wherever recording, AI, or privacy disclosures are in play — not only where a particular customer happens to have an IVR.

### Worked example — IVR / carrier-side split (recommended)

When an IVR / carrier-side pre-call announcement is available, put the institutional disclosures in the IVR layer and keep the agent welcome to a single warm greeting. The call-routing step *is* the handover — there's no extra pause to engineer.

**IVR / carrier-side (system layer → Layer E):**
1. IVR welcome + recording & transcription notice: *"Thanks for calling Northwind Customer Experience. This call may be recorded and transcribed for quality and training."*
2. Language selection (if needed): *"For English, press one. Para español, oprima el dos. Pour le français, appuyez sur le trois."*
3. AI + privacy disclosure + hold: *"You'll be speaking with [Agent Name], our AI voice assistant. For our full privacy terms, visit northwind dot com. Please hold while we connect you."*
4. Route the call to Agentforce Voice.

**Agent layer (→ `messages.welcome`):**
> *"Hi, I'm [Agent Name], Northwind's AI assistant. I can help with your orders, deliveries, and returns. How can I help you today?"*

The agent layer is AI self-identification + a one-sentence capability frame + a "how can I help you?" variant. This split elegantly separates the institutional disclosures from the actual greeting, keeping the agent welcome short. ([Agent Name] and the brand are placeholders. Take both from the Persona, and give each a pronunciation entry (H04) and an STT keyword (H05). The Persona owns the welcome's wording; this skill owns its spoken structure; see B01.)

### Agent-layer structure — three recurring elements

Whether the system layer plays via IVR or the agent voices both layers in sequence, the agent layer stays short and conversational and carries three elements in order:

1. **AI self-identification.** *"Hi, I'm [Agent Name], Northwind's AI assistant."*
2. **Capability frame.** Set expectations up front — say what the agent can do — rather than an open-ended "ask me anything," which invites requests the agent can't handle and pushes callers to "human please." The frame takes different shapes depending on what the agent does:
   - *Scope:* *"I can help with your orders, deliveries, and returns."*
   - *Transactional:* *"I'll take a few details and log a case for the team to follow up by the next business day."*
3. **Turn-final CTA.** A *"How can I help you today?"* variant, placed last so it's what the caller acts on (P9 end-focus).

Keep the whole agent layer within the ~5–7s opening budget (P4, B01).

**Capability frame rules.** Name exactly three things the agent can do: three is the most a caller holds by ear, and it matches the three-item list cap. Don't pad with "and more" or "anything else", because a vague tail invites the requests the frame was meant to head off. Don't claim a feeling in the greeting ("I'm so happy to help!"); warmth comes from delivery, not from a stated emotion (A05). End on one invitation, not two questions. (Source: *Designing for the Ear* enablement deck; Voice Quality Heuristics v1.2, Approachability.)

### Static welcome vs. first-turn override

There are two places to author the agent's greeting, and they behave differently:

| Mechanism | When it plays | Can use runtime data? | Use it when |
|---|---|---|---|
| `system: → messages: → welcome:` | Before the caller speaks, the moment the call connects | No: static text only | The greeting is the same for every caller and the agent speaks first |
| First-turn conditional in each subagent's `reasoning.instructions` | On the caller's first turn, wherever it lands | Yes: caller name, account context from `before_reasoning` lookups | You want to greet by name, or the IVR has already spoken and the caller opens ("Hi there") |

The first-turn override needs a turn counter the router increments, checked in **every** subagent (the caller's first utterance can route anywhere):

```
variables:
    messageTurn: mutable number = 0
        description: "Count of caller turns so far."

start_agent router:
    before_reasoning:
        set @variables.messageTurn = @variables.messageTurn + 1

subagent sessions:
    reasoning:
        instructions: ->
            if @variables.messageTurn == 1:
                | This is the caller's first turn. Welcome them by name, name three things you can help with, and end with one short invitation to begin.
```

Without the counter, a lookup on turn one followed by a second welcome on turn two makes the agent sound like it forgot the call had started. Don't run both mechanisms with greeting content, or the caller is welcomed twice.

**T-opening-already-spoken — tell the model the welcome has played.** The platform voices a static `welcome:` before the first reasoning pass, and the model doesn't see it. Left alone, it greets and introduces itself again on turn one ("Hi, I'm Ava, Northwind's assistant…" after the caller has already heard exactly that). When the design uses a static welcome, or an IVR introduces the agent, add a rule to the global `system.instructions` that quotes what was said:

```
THE WELCOME LINE HAS ALREADY BEEN SPOKEN: "Hi, I'm Ava, Northwind's AI assistant. I can
help with your orders, deliveries, and returns. How can I help you today?"
Never greet the caller or introduce yourself again. Answer their first words directly.
```

Keep the quoted text in step with `messages.welcome`; a stale quote is worse than none. (Source: Agentforce Voice Agent Assessor, Personality, from a production prompt, Oct 2026.)

**Common mis-applications (optimize mode):**
- System and agent layers don't sound clearly different — same TTS voice, similar pacing, similar register — so the user doesn't perceive a layer change. The split exists on paper but not in the ear. (The exact register choice is flexible; what matters is contrast.)
- Agent layer is too long (notably >7s spoken length), defeating the split.
- System layer plays both via IVR / carrier AND agent (disclosure repetition), when an IVR / carrier-side announcement is available.
- Handover pause absent or too short (<300ms) — no perceptual gap between layers.
