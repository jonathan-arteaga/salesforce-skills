# Audit rubric

Drives audit coverage. For each principle and pattern, defines what the audit must check, what triggers each tag, and how mode (migrate vs. optimize) affects the threshold.

Citation format in audit output: `why: P9-end-focus` or `why: T-translate-6 + P9-end-focus`. Always cite the most specific source.

---

## Coverage contract

The audit MUST visit each row below and produce one of:

| Tag | Meaning | Modes |
|---|---|---|
| `[changed]` | Voice principle violated or absent, rewrite applied | Both |
| `[ok]` | Principle respected (counts in summary, not surfaced inline) | Both |
| `[review needed]` | Principle violated AND intentionality signal present; preserve original, flag conflict | Both (threshold differs) |
| `[consider]` | Principle present but applied weakly; suggestion only — no rewrite, no preservation | **Optimize only** |
| `[out-of-scope]` | Pattern detected that source library doesn't cover | Both |

---

## Encoding surface (which layer a fix lands on)

Every fix the audit proposes lands on one of the three Agent Script surfaces (see SKILL.md Phase 5, "The encoding model"). Tag findings with the surface so the developer knows where the change goes:

| Surface | What lands here | Principles it typically serves |
|---|---|---|
| **Prose instructions (`\|`)** | Turn shape, end-focus, repair phrasing, grounding wording, sequential-gathering rules | P1, P2, P6, P8, P9, P10 |
| **Deterministic logic & variables** | Failure counters + `after_reasoning` escalation budget (J01), volunteered-slot capture (I02), `require_user_confirmation`, mandatory summaries | P3, P10 (guarantee), P2 (commit gate), P6 (never-re-ask) |
| **Voice channel config (`modality voice:`)** | `voice_id` + delivery (H03; on the default v3 model only `outbound_stability` bites — speed/similarity are Flash-only), `additional_configs` beepboop/speak-up (H06), `inbound_keywords` + `inbound_filler_words_detection` (H05), `pronunciation_dict` (H04) | P7 (latency), P3 (no-input), P10 (STT bias), P5 (pronunciation) |

Rule of thumb, from the paper: conversational behavior → prose; sequential guarantees → the deterministic blocks and variables; sound, timing, and wiring → voice channel config. A principle can touch more than one surface (e.g. P10 repair = prose ladder + deterministic budget + STT biasing).

## Persona precedence

When a completed `persona.md` or `persona-handoff.json` is supplied, treat it as the authoritative character contract. If both are supplied and the JSON's `source_persona.sha256` doesn't match the hash of `persona.md`, the handoff is stale: `[review needed]` before anything else. A Persona marked `draft` can be used, but every finding derived from it says so. Preserve exact Never-Say entries, immutable content and surrounding response shape, Lexicon meaning, explicit Guardrails, Identity, Register, Tone boundaries, and the semantic/lexical Tone Flex policy. The Script remains authoritative for business logic, actions, routing, and source-carried compliance. A conflict between those authorities is `[review needed]` and blocks the affected rewrite until a human resolves it.

Voice adaptation may change spoken turn shape and make wording listenable, but it may not silently redesign character. P5/A08 maps Persona Tone Flex triggers and resets to situational prosody. Layer C may expand 2–4 Persona alternatives into a signature set (4–6 for acknowledgments; T-phrasebook) only within the same register, meaning, prohibitions, and immutable constraints.

Two voice floors hold even against the Persona, and each conflict is surfaced, never resolved silently: **A10** (no first-person feelings; a Persona that licenses them → `[review needed]` with the amplification rationale) and **B02/Z05** (AI disclosure; no human impersonation). Persona owns the welcome's wording; this skill owns its spoken structure (B01). A structural edit that changes meaning is `[review needed]`.

## Principle-driven checks (presence checks)

Used in both modes. These check whether a principle is *present at all*. In migrate mode, absence dominates. In optimize mode, absence is rarer but still possible (script started voice-shaped but missed a category).

| ID | Check | Triggers `[changed]` if… | Notes |
|---|---|---|---|
| P1 | Long monologues | Any single utterance > 2 sentences (or > ~20s spoken) without a necessary caveat, a data read-back, or a pause point; or the answer isn't in the first sentence | Recommend chunking and answer-first; flag barge-in concern (Layer E) |
| P2 | Confirmation strategy | "Is that correct?" pattern OR explicit confirmation on low-stakes fields OR no confirmation on irreversible | Cross-reference T-grounding for field-type policy |
| P3 | No-input/no-match | Error messages blame the user OR don't vary across attempts OR no escalation path | Map to T-repair tier |
| P4 | Opening length | Agent-voiced welcome > 35 words, not counting required disclosure (Voice Agent Optimization Guide §2.3; B01) | Split or shorten; consider T-opening two-voice |
| P4 | Closing | Flow ends without pre-closing token before terminal | Insert pre-closing from T-phrasebook |
| P5 | Prosody | Numbers, names, irreversible terms not marked for stress (where SSML supported), OR no Persona-derived prosody strategy (base profile + situational shift) | Map supplied Persona Tone Flex to A08/A09 without redefining its lexical policy; SSML-level stress stays a Layer E recommendation |
| P6 | Sequential gathering | Two or more pieces of info requested in one turn | Split; re-order to natural narrative if data-schema order is unnatural |
| P7 | Latency | Action/tool call invoked without verbal pre-announce | Insert pre-announce per T-latency tier |
| P8 | Turn atomicity | Turn does framing + action + follow-up question in one breath | Split into atomic turns |
| P9 | End-focus | Question precedes context, OR critical info buried mid-turn | Reverse to put question/critical info last |
| P10 | Repair vocabulary | Same repair string used for tier 1, 2, 3 (no escalation) | Generate tiered variants |
| P11 | Phrasebook coherence | Acknowledgments mix registers OR exceed 6 unique tokens OR fewer than 4, OR no instruction enforces rotation (never the same token in adjacent turns), OR the agent may invent off-palette tokens, OR acknowledgments run longer than ~5 words or trail the substance | Derive spoken variants from supplied Persona per T-phrasebook; otherwise infer and label character evidence |
| P12 | Handoff | Tier 3 escalation drops state, OR no announcement of handoff target | Add what/where/why announcement; route per modality trait matrix |
| P13 | Emotional de-escalation | Auto-terminate path fires on frustration/negative sentiment (not Tier-4 explicit-threat), OR no distinct distress branch | Widen no-hangup rule to any distress; add distress branch that warm-transfers, not terminates. Couples with F01. Note: distress is detected from transcript text only — don't assume acoustic/prosodic signals exist (Layer E / v2) |
| H08 | Vocal Identity brief | No brief exists, OR the brief has no perceived-identity or must-not-sound-like fields, OR gender presentation was inferred rather than elicited | Write the brief (H08); label `inferred` without a Persona. `[review needed]` until a human confirms gender presentation, age band, and accent |
| H09 | Casting record | `voice_id` placeholder or set with no shortlist, casting sides, decision record, or runner-up | Run H09. Record the audition channel (phone recommended; Preview with caveat) and the listener tier (min 1; 3–5 recommended for go-live) |
| A11 | Unscripted commitments | Copy or instructions claim an action no action performs ("I've noted that"), OR a success line on a turn whose write runs after speech, OR no fail-safe rule in global instructions | Add the fail-safe rule; reword to what will happen (A11) |
| A12 | Times and dates | Digit-form times, timezone abbreviations, or ISO/slash dates in spoken copy or read-back variables | Add the spoken-form rule and companions (A12, I01) |
| T-opening-already-spoken | Re-greeting | Static `welcome:` (or IVR introduction) with no instruction telling the model it has already been spoken | Add the "welcome already spoken" rule quoting the welcome (T-opening) |
| Z06–Z08 | Silent script failures | Work after a `transition`; an empty check missing `None` or `""`; a generative stage told to output nothing | Auto-fix per Z06–Z08; Z06 and Z08 block hand-back until fixed |
| Z05 | Human impersonation | Any Z05 detection hit (identity claim, belief goal, disclosure dodge, likeness target, body-sound tags, scripted fillers) | Rewrite per Z05 and log each hit `[review needed]` with the rationale |
| P14 | Multi-intent | Multi-intent turns detected in sample with no handling, OR handling skips acknowledge/segment/verify steps, OR competing intents are sequenced without a stated reason when one is obviously time-sensitive, blocking, or ranked higher on the topic's priority list | Add acknowledge (with sequencing reason when the order matters — runtime signal or design-time priority list) → segment → verify pattern; each intent gets its own atomic turn (couples with P8); on escalation, forward all open intents (couples with P12) |

---

## Mis-application checks (optimize mode only)

Used in optimize mode to detect principles that are *present but applied wrong*. These triggered `[consider]` (or `[changed]` if the mis-application is unambiguous, e.g., a clear copy bug).

In migrate mode, these checks usually don't fire — the principle isn't present yet to be mis-applied. Run them anyway in case the source is partially voice-shaped (half-migrated script).

| ID | Mis-application | Detection signal | Default tag |
|---|---|---|---|
| P10-mis-1 | Repair tier 2 directive exists but rephrasing is identical/near-identical to tier 1 | String similarity between tier 1 and tier 2 prompts >70%, OR tier 2 lacks constrained vocabulary or candidate understanding | `[consider]` |
| P10-mis-2 | Repair tier 3 escalation defined but doesn't preserve state | Tier 3 prompt restarts the conversation OR doesn't reference collected fields | `[changed]` |
| P11-mis-1 | Phrasebook exists but is below the signature-set minimum | Fewer than 4 acknowledgment tokens, fewer than 3 holding or repair tokens, or fewer than 2 in any other function | `[consider]` |
| P11-mis-2 | Phrasebook tokens mix registers (formal + casual in same function) | Heuristic: contractions in some tokens but not others within the same function category; or one token uses "thank you" while another uses "thanks" | `[consider]` |
| P11-mis-3 | Acknowledgment tokens don't rotate | Same token in adjacent turns in the sample (`[consider]`); more than 3 in a row is the Voice Quality Heuristics floor (`[changed]`) | `[consider]` |
| P11-mis-4 | Acknowledgment overuse across the call | Same acknowledgment token 8+ times in one sample call (Voice Quality Heuristics floor) | `[changed]` |
| P2-mis-1 | Grounding policy exists but doesn't escalate on low ASR confidence, OR money/irreversible actions get only implicit echo | Phone/email skim past on implicit echo regardless of confidence; OR money/irreversible actions have no explicit summary + check | `[changed]` |
| P2-mis-2 | Grounding policy over-confirms low-stakes fields | Date, postcode, single name uses explicit "Is that correct?" pattern | `[consider]` |
| T-opening-mis-1 | Two-voice opening exists but system and agent layers don't sound clearly different | Same TTS voice used for both layers; or matching pacing/register such that the user can't perceive a layer change | `[changed]` |
| T-opening-mis-2 | Two-voice opening exists but agent layer is too long | Agent-layer utterance > 35 words (B01) | `[consider]` |
| T-latency-mis-1 | Pre-announce exists for some actions but not all | Subset of tool/action calls have verbal lead-in; others don't | `[changed]` |
| T-latency-mis-2 | Pre-announce exists but is identical for short and long operations | Same "Let me check…" used regardless of expected duration | `[consider]` |
| P6-mis-1 | Sequential gathering exists but order doesn't match natural narrative | Field order matches data-schema (e.g., DOB before name) rather than how a person would volunteer | `[consider]` |
| P3-mis-1 | Reprompt language exists but doesn't vary across attempts | Same reprompt string used for tiers 1 and 2 | `[changed]` |
| P12-mis-1 | Handoff announcement exists but doesn't include what/where/why | Announcement names the modality but not the reason or destination | `[consider]` |
| H03-mis-1 | Flat `outbound_speed`/`outbound_similarity` (or `pronunciation_dict`) set but no model selected | Block is flat (no nested `outbound: → model:`) → agent runs on the default v3 model, which ignores speed/similarity and doesn't do custom pronunciation → those settings are likely inert. Note it, don't auto-delete (harmless; live under a Flash model) | `[consider]` |
| H08-mis-1 | Brief restates Persona traits without sound-level description | Brief has adjectives but no perceived identity, voice quality, or must-not-sound-like | `[consider]` |
| H09-mis-1 | Voice approved from library sample or Preview only, or no runner-up | Casting record lacks casting sides, audition channel, or runner-up | `[consider]` |
| H09-mis-2 | "Deliberately ambiguous" brief with no listener validation | No perceived-gender answers in the audition scores | `[consider]` |
| H03-mis-2 | v3 agent with Flash-style stability | `outbound_stability` ≥ 0.8 on the default v3 model while A08 tags are in use | `[consider]` |
| A10-mis-1 | Persona-licensed feelings voiced on the phone | Persona Personification = Anthropomorphic with feelings licensed, and voice copy claims feelings | `[review needed]` |
| P12-mis-2 | Escalation from a multi-intent call only forwards state for the triggering intent | Handoff payload or rep-briefing turn references one intent while the sample shows multiple open intents in the same call | `[changed]` |

---

## Translation-rule checks (T-translate)

Used in both modes. In optimize mode these usually return `[ok]` for voice-source scripts, but catch text-shaped legacy regions in half-migrated scripts.

| ID | Trigger pattern (regex/heuristic) | Action |
|---|---|---|
| T-translate-1 | "reply with", "say yes or no", "type", "choose one" as default prompt | Strip; just ask |
| T-translate-2 | "click", "tap", "select", "submit", "press", "enter" as user-facing verb | Replace with conversational equivalent |
| T-translate-3 | "Please provide", "You must provide", "We require" | "What's your X?" / "I'll need" |
| T-translate-4 | Format prescriptions ("DD-MM-YYYY", "international format", "include @") in default prompts | Strip from default; allowed only in Tier 2 repair |
| T-translate-5 | "as shown", "see below", "listed are", "here are the options:" | Remove visual reference; rephrase |
| T-translate-6 | Numbered or bulleted menus in copy | Convert to "X, Y, or Z?" disjunction |
| T-translate-7 | Fixed acknowledgment template ("Thank you. Now please…") | Replace with rotating tokens from T-phrasebook |
| T-translate-8 | "and" / "also" / "as well as" joining two questions | Split into separate turns |

---

## Pattern checks (T-grounding, T-repair, T-latency)

Used in both modes.

| ID | Check | Action |
|---|---|---|
| T-grounding-low-stakes | Date / postcode / single name confirmed explicitly | Switch to implicit echo |
| T-grounding-phone | Phone number confirmed only via implicit echo even on low ASR confidence | Escalate to explicit digit-by-digit when ASR confidence is low |
| T-grounding-email | Email confirmed only via implicit echo even on low ASR confidence | Escalate to explicit char-by-char with improvised phonetics on the disputed segment when ASR confidence is low; type-don't-say screen handoff (D08) when char-by-char is impractical |
| T-grounding-money | Money/irreversible action without explicit summary | Add summary turn |
| T-repair-tier-1 | First-attempt repair language blames user | Replace with neutral open repair |
| T-repair-tier-2 | Second-attempt repair doesn't constrain or rephrase | Add constrained-vocabulary or candidate-understanding variant |
| T-repair-tier-3 | Third-attempt has no handoff or drops state | Add handoff per modality matrix; preserve state |
| T-latency-pre-announce | Tool/action call has no verbal lead-in | Insert "Let me check…" / "One moment…" per T-phrasebook |
| T-latency-long | Action expected to take >10s, no warning or filler | Add a "may take a while" warning before the action; verbal filler every 3–5s during processing |

### Voice latency triage (`[consider]` in both modes, never `[changed]`)

The skill flags these with the field cost and a snippet; it doesn't restructure routing, models or actions. Read them off the Phase 2 stage map. Costs: `T-latency-costs`.

| ID | Detection signal | Suggestion |
|---|---|---|
| L-router | Router runs an LLM reasoning pass when a phase variable could route it; or no catch-all final transition | Deterministic router branching on a phase variable (~0 s vs ~1 s), ending with a catch-all |
| L-classifier | Classification fork (yes/no, which-of-N) on a full LLM pass; OR HyperClassifier on a speaking or tool-calling stage | HyperClassifier on the fork only (~0.1 s) |
| L-model | Speaking stage on a large model, or no explicit `model_config` pin | Fast model, pinned (Sonnet → Haiku 4.5 cut 5.84 s to 3.20 s in the field) |
| L-parity | Prompt template on a different model from its stage | Match them (Guide §1.2) |
| L-guard | Model-callable tool with no `available when` guard, re-callable on later turns | Guard on the variable it sets (one re-call cost ~1.4 s) |
| L-after-speech | Fire-and-forget write (call result, case note) exposed as an LLM tool | `run` in `after_reasoning`; spoken line doesn't claim success (A11). Not for writes G02 covers |
| L-prefetch | Turn-one lookup of caller context | Pre-fetch onto VoiceCall in the inbound flow, read via `linked` variables (~0.6 s) |
| L-prompt | Global instructions over ~600 words, or a stage over ~800 | Condense; hide unneeded outputs (`filter_from_agent`) |
| L-passes | More than two back-to-back LLM passes on any turn | Name the passes and which of the above removes one |

---

## Conflict policy → `[review needed]`

Threshold differs by mode.

### Migrate mode (default conservative)

When the source script's behavior is voice-suboptimal AND there is a signal it's intentional, preserve the original. Surface as `[review needed]` with:
- The original directive (quoted)
- The voice principle it conflicts with (cite ID)
- A one-sentence recommendation
- The signal that suggested intentionality

**Strong intentionality signals (preserve in both modes):**
- Explicit compliance/regulatory language ("PCI", "GDPR consent", "must record", "required by")
- Comment or instruction text marking the directive as fixed
- Bundled question that asks for items legally bound together (e.g., consent + identification)

**Weak intentionality signals (preserve in migrate mode, surface as `[review needed]` or `[consider]` in optimize mode):**
- Repeated assertion of the same rule across multiple turns
- Pattern repeated across topics

Do not infer intentionality from a single occurrence of suboptimal copy in either mode.

### Optimize mode (lower bar)

The developer is asking for an opinion. Be more willing to challenge.

- Strong intentionality signals → preserve as `[review needed]` (same as migrate).
- Weak intentionality signals → flag as `[review needed]` with a stronger recommendation, OR as `[consider]`. Do not preserve silently.
- No intentionality signal → rewrite as `[changed]`.

The bar shift means: in migrate mode, "the designer probably knew what they were doing" is the working assumption. In optimize mode, "the designer wants my opinion" is the working assumption.

---

## Out-of-scope detection

If the audit finds these patterns, flag as `[out-of-scope]` rather than rewrite (gap in source library):

- Cascading error recovery (corrected field that has downstream impact)
- Multilingual / language-specific repair
- Agent-to-agent skill transfer

Surface in audit summary; do not block the rewrite.

---

## Mode-detection signals (for the extraction pass)

Used during automated extraction (Phase 3 of the intake flow) to infer mode. The extraction pass surfaces what it found and the proposed mode; the developer confirms in Phase 4.

### Text-shaped signals (suggests migrate mode)
- Interface verbs in copy ("click", "tap", "select", "submit") — T-translate-2
- Format prescriptions in default prompts ("DD-MM-YYYY", "international format") — T-translate-4
- Visual references ("as shown", "see below") — T-translate-5
- Numbered/bulleted menus in copy — T-translate-6
- Bundled questions joined by "and"/"also" — T-translate-8
- No repair tier directives in instructions
- No latency pre-announce patterns in instructions
- No phrasebook tokens defined
- No two-voice opening structure

### Voice-shaped signals (suggests optimize mode)
- Repair tier directives present (tier 1 / tier 2 / tier 3 referenced)
- Grounding-by-field-type policy present (different rules for phone vs. date)
- Latency pre-announce patterns present ("if X takes more than a second, say…")
- Phrasebook tokens defined (rotating acknowledgments)
- Two-voice opening structure present
- In-script voice-channel config present (`modality voice:` with `additional_configs` / `inbound_keywords`)
- Deterministic escalation guard present (`after_reasoning` failure budget forcing handoff)
- Absence of interface verbs in copy

### Mixed signals (half-migrated script)
If both signal sets are present (e.g., voice-shaped instructions but text-shaped copy strings), default the proposed mode to **optimize** and surface the mixed signals to the developer. Optimize mode's mis-application checks plus the T-translate checks will catch both shapes.
