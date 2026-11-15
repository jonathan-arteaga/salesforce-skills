# Phase 5 — Write Output

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 5 — Write Output

Use `templates/rewrite-bundle.md` as the skeleton. Write to `artifacts/voice-ux/[agent-name]-voice-{migration,optimization}.md`.

The output frontmatter records the mode, the mode rationale (signals that drove the inference), and the developer's confirmation.

### The encoding model — three surfaces, one division of labor

Every voice behavior this skill encodes lands on one of **three surfaces in Agent Script**. Knowing which surface a fix belongs to is what keeps the rewrite from drifting into instructions the platform can't honor:

1. **Prose prompt instructions (`|`)** — conversational behavior: turn shape, end-focus, repair phrasing, grounding wording. Written as concrete turn rules ("Place the question at the very end"), not vague tone descriptors ("Be helpful"). The reasoning engine acts on these each turn.
2. **Deterministic logic & variables** — sequential *guarantees* that must hold every time: slot-filling variables, failure counters, mandatory summary confirmations, forced escalation. These live in variables and the blocks around the reasoning loop (`before_reasoning`, `after_reasoning`) — outside the LLM's judgement — plus `require_user_confirmation` on hard-to-reverse actions. See patterns **J01** (escalation budget) and **I02** (volunteered-slot capture).
3. **Voice channel configuration (`modality voice:`)** — sound and timing: `voice_id`, speed/stability/similarity + `pronunciation_dict` (H03/H04), the `additional_configs` latency/turn-timing block (H06), and `inbound_keywords` + `inbound_filler_words_detection` STT biasing (H05). In-script, written by the skill — not deferred to a human. One caveat carried by the underlying TTS model: the flat block runs on the language default (v3 Conversational for most languages), which honors only `outbound_stability` — `outbound_speed`/`outbound_similarity`/`pronunciation_dict` bite only under a Flash model, selected via the emerging nested format (H03).

The division of labor: **conversational behavior → prose; sequential guarantees → the deterministic blocks and variables; sound, timing, and wiring → voice channel config.** When voice best practice and business logic conflict, that's a `[review needed]`, not a silent override.

This describes *where a design lives*. The **Layers A–E below are the output-bundle shape** — how the rewrite is presented for review and handoff. The two are orthogonal: a single Layer A instruction rule is a prose-surface fix; a Layer E-adjacent config value is a voice-channel-config-surface fix now written into the file (see Layer A's voice-channel-config callout in the template).

**Layer A — Rewritten instructions (LLM-facing):** Voice best practices baked in as directives. Includes turn structure rules, grounding policy by field type, repair escalation ladder as conditional behavior, latency communication patterns, sequential gathering rules. Opinionated text the LLM acts on at runtime.

**Layer B — Rewritten user-facing copy:** Every changed string with original quote, rewritten quote, principle citation. In optimize mode, mostly short; in migrate mode, often substantial.

**Layer C — Spoken-function phrasebook:** a signature set per function: 4–6 tokens for acknowledgments, 3–4 for holding and repair, 2–3 for the rest. Never the same token in adjacent turns; rotate within the set only (T-phrasebook). When a Persona is supplied, derive these from Persona's 2–4 alternatives and preserve register, meaning, Never-Say constraints, immutable wording, and Tone Flex boundaries. Expanding the palette for spoken rotation is channel adaptation, not character redesign. In optimize mode without a Persona input, the existing phrasebook is the starting point; check coherence and completeness.

**Layer D — Opening sequence:** Two-voice structure if applicable. In optimize mode, audit the existing opening for system-layer contractions, agent-layer length, contrast, and handover pause.

**Voice channel configuration (in-script):** `voice-ux` designs and writes the `modality voice:` block: `voice_id` + delivery settings (H03), the `additional_configs` latency/turn-timing block (H06: `beepboop_config` 500ms, `speak_up_config`), `inbound_keywords` STT biasing + `inbound_filler_words_detection` (H05), and custom pronunciation via `pronunciation_dict` (H04). Each value is `[review needed]`. Active Agent Script tooling supplies current grammar, compilation, and validation authority. The target org determines valid voice IDs; the casting record (Phase 4b) supplies the `voice_id`; a human listening sign-off approves it. The three-layer latency model (`T-latency-filler-audio`: beepboop audio, spoken `outbound_filler_sentences`, per-action `progress_indicator_message` via G01) lives here. Preserve the Persona character baseline while adapting the progress line for spoken latency; never alter the action contract. This is not Layer E because it is config the skill emits. On delivery settings (`outbound_speed` / `outbound_stability` / `outbound_similarity`), recommended values are starting points to tune by ear. **Model caveat:** the emitted block is the flat/legacy format, which runs on the language default model (v3 Conversational for most languages). v3 honors only `outbound_stability`; `outbound_speed`, `outbound_similarity`, and `pronunciation_dict` take effect only under a **Flash** model. Selecting a non-default model requires the emerging nested format (`outbound: → model:`), which the offline validator does not yet recognize, so the skill documents it (H03) but still emits flat by default.

**Layer E — Out-of-Agent-Script notes:** Items that genuinely cannot be encoded in the `.agent` — recognizer-side ASR thresholds, the system/IVR-layer voice, SSML, carrier/IVR pre-call announcement (whose recording / AI / privacy disclosures are legal-owned and vary by market and language — flag a review whenever the engagement adds one), sensitive-digit privacy routing, utility-action Apex/Flow implementations. If it can go in `modality voice:`, it belongs in the voice channel configuration above, not here.

**Layer E — known platform gotcha to surface:** connected subagents currently play "Collaborating with other agents" on every turn, and `loading_text` doesn't suppress it (reported October 2026). If the design uses a `connected_subagent`, flag it so the team can test it on a real call before go-live.

**Layer E — voice latency triage (detect, `[consider]`, never refactor).** Latency tracks the number of LLM passes that run back-to-back in a turn, not the length of the reply. Speech starts when the final pass begins, so the caller waits for every pass before it. Read the stage map (Phase 2) and flag each item below as `[consider]`, with the field cost and a paste-ready snippet. The skill doesn't restructure routing, models or actions (see "What this skill does NOT do"); owners are in "Where neighbouring work goes". Field costs come from one Agentforce Voice + Amazon Connect build (Oct 2026, one live call per version), so treat them as directional (`T-latency-costs`). Sources: Voice Agent Optimization Guide §1.1–1.4; Agentforce Voice Agent Assessor.
- **Router passes.** A router that branches on a phase variable with no prompt costs about 0 s; HyperClassifier about 0.1 s; an LLM router about 1 s. End the router with a catch-all transition. Use HyperClassifier on classification forks (yes/no, which-of-three), never on a speaking or tool-calling stage.
- **Fast model on speaking stages.** In the field build, moving speaking stages from Sonnet to Haiku 4.5 cut average delay from 5.84 s to 3.20 s; Gemini 3.5 Flash measured on par with Haiku (the Guide advises against Gemini, so test on your own flows). Pin `model_config` explicitly. Pins on logic-only stages don't matter, because they never generate.
- **Model parity.** Use the same model at stage and prompt-template level. A mismatch adds a reasoning step (§1.2).
- **Tool re-calls.** A tool with no `available when` guard can be called again on a later turn. In the field one re-call added about 1.4 s. Guard on the variable the tool sets.
- **Writes after speech.** A fire-and-forget write (call result, case note) run as an LLM tool keeps the caller waiting. Running it with `run` in `after_reasoning` cut a final turn from 3.86 s to 1.53 s. The spoken line then mustn't claim success (A11). Writes whose outcome the caller has to hear (a booking, a payment) stay as G02: narrate, run, then confirm.
- **Pre-fetched context.** A turn-one lookup of caller context (account, open case) can move into the inbound flow, written onto the VoiceCall and read through `linked` variables. In the field this saved about 0.6 s on turn one.
- **Lean prompts.** Keep global instructions under about 600 words and each stage under about 800. Condensing the largest stage was worth 0.6–0.8 s in the field. Hide action outputs the model doesn't need (`filter_from_agent`; also a voice-floor issue, see `T-translate-plumbing`).
- **Dynamic progress indicator** on model-called actions (`include_in_progress_indicator: True` with an empty message, G01).

**Layer E — platform-latency checklist (handoff to the platform owner).** These are set outside the `.agent`. Include them when a sample call or the audit shows long waits, rather than covering the wait with more filler (Voice Agent Optimization Guide §1.1–1.4; *Designing for the Ear* enablement deck):
- **Call routing:** direct phone routing to the agent vs. an inbound Omni flow. An Omni flow holds the connection until the whole flow finishes (§1.1).
- **Lean inbound flow:** if an Omni flow is needed, avoid DML, index the fields used in reads, remove unused branches, and pass only the context the agent needs before it says hello (§1.1.1).
- **Model availability:** choose the model by testing your own call scenarios, and date the guidance ("as of October 2026"). Gemini 3.6 Flash retires on November 19, 2026.
- **Cache common answers:** refresh popular FAQ content into Platform Cache on a schedule and load it at setup, so common questions need no lookup (§1.4).
- **Tight retrieval:** chunk only the fields used for lookup, and use a retriever with filters (§1.4).
- **Light Apex and flows:** return only what the agent uses, and move non-blocking DML to async. Each Apex call carries about 0.25–0.35 s of fixed overhead (§1.4).
- **Don't tune Trust Layer checks for latency.** They run off the critical path.
- **Amazon Connect (DVR):** if the call arrives through Connect Dynamic Voice Routing, run the Assessor's telephony checklist (caller ID on the transfer, `reserveRoutableNumber`, `CONTACTFLOW_LOGS`, the route flow pointing at the active agent).

**Inline audit section:** Every `[changed]`, `[review needed]`, `[consider]`, and `[out-of-scope]` entry with citation. Top-level summary table with counts per category and tag.
