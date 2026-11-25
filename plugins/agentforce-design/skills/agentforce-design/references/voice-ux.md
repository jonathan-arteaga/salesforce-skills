# Voice UX & Telephony Design

Adapt existing chat agents or Agent Scripts into spoken interactions (`migrate` mode) or tune live voice agents (`optimize` mode). Produce a 5-layer rewrite bundle (Instructions, Copy, Phrasebook, Opening, Handoff notes), a Vocal Identity & Casting brief, and `modality voice:` specs for `agentforce-build`.

## Character vs. Voice Boundary

- **Persona owns WHO the agent is** (Never-Say list, immutable copy, Lexicon meanings, lexical Tone Flex, adjacent Guardrails).
- **Voice UX owns spoken realization** (vocal casting, light tuning, prosody, phrasebook rotation, pronunciation, STT key-term bias, latency masking, and `modality voice:`).
- Preserve supplied `persona.md` / `persona-handoff.json` contracts verbatim; mark any conflict with business logic or compliance `[review needed]` rather than deciding silently.
- Distinguish **multimodal** (voice + visual UI active simultaneously) from **crossmodal** (sequential voice-to-SMS/email/screen handoff for links, codes, or complex forms).

## Core Principles (P1-P14) & Chat-to-Voice Translation (`T-translate`)

Apply P1-P14 (P1 barge-in, P2 risk-stratified grounding, P3 no-input/no-match repair ladder, P4 two-voice opening/closing, P5 prosody, P6 one-question-per-turn sequencing, P7 silence/latency masking, P8 turn progressivity, P9 end-focus, P10 voice repair, P11 rotating phrasebook, P12 voice-to-screen handoff, P13 emotional de-escalation, P14 multi-intent).

- **8 Copy Rules (`T-translate-1..8`):** Strip input-shape prompts ("reply yes/no"), interface verbs ("click/tap/type"), transactional phrasing ("Please provide"), upfront format prescriptions ("DD-MM-YYYY" — repair tier 2 only), visual references ("see below"), numbered menus (use natural disjunctions "A, or B?"), repetitive acks, and bundled multi-part questions.
- **4 Grounded-Speech Rules:** Never speak internal plumbing (action/field names, IDs—recommend `filter_from_agent: True` on outputs); pronounce entities canonically from action data rather than ASR transcript text; explicitly state empty states instead of fabricating; apply caller corrections immediately without re-asking unchanged fields.
- **Risk-Stratified Grounding (`T-grounding`):** None for acks; implicit echo for low-stakes values; phonetic/digit-by-digit confirmation on low ASR confidence for names, phones, and emails (or crossmodal screen input); explicit summary + yes/no check ALWAYS before money or irreversible commits.

## Latency Heuristics (`T-latency`) & `modality voice:` Config (`T-config`)

Latency scales primarily with sequential generative LLM passes per turn (~0.85-1.4s fast model, up to ~2.8s large model, plus ~0.3-0.7s overhead; Trust Layer checks run async). Trim extra LLM passes before tweaking wording.

- **Three-layer filler model:**
  1. `additional_configs -> beepboop_config -> max_wait_time_ms`: set `500` (500-60000ms range; omitting falls back to 6000ms platform default, leaving raw silence).
  2. `outbound_filler_sentences`: persona-voiced rotating waiting phrases.
  3. Per-action `progress_indicator_message` paired with `include_in_progress_indicator: True` (for >1s waits; >3s requires periodic filler; >10s requires explicit wait warning).
- **In-script `modality voice:` keys:**
  - `speak_up_config`: timers 10000-300000ms (recommend `10000` + warm holding token, never "Are you still there?"; 3 unanswered prompts end the call silently). Leave `endpointing_config` at default.
  - `inbound_keywords` (STT key-term bias) and `inbound_filler_words_detection` (often `True` for telephony).
  - `voice_id`, `outbound_stability`, `outbound_speed` (usable 0.7-1.1), `pronunciation_dict` (IPA/CMU): note that default v3 Conversational honors `outbound_stability`, whereas `outbound_speed`, `outbound_similarity`, and `pronunciation_dict` require a Flash/nested model config to take effect.

## 2026 Compliance, Language & Validation Caveats

- **Call recording & consent:** Supported Real-Time Streaming setups can record agent call legs. Always inspect **Record Voice Calls with Agents**, per-agent Flow overrides, and participant notice/consent across every recorded leg—never auto-mark recording N/A.
- **Monolingual voice caveat:** Current Agentforce Voice guidance describes monolingual agents operating in the configured default language; text Allowed Languages is NOT evidence of multilingual voice support. Verify release/beta status in the target org.
- **Live test call requirement:** Static voice specs cannot verify barge-in, ASR accuracy, silence timeouts, latency, escalation, or recording—schedule real test calls in an authorized non-production environment via `agentforce-test`.
