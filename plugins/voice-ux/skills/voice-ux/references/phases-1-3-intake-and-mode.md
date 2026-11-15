# Phase 1 — Artifact Intake

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 1 — Artifact Intake

See the Prerequisites section for the three required inputs. Phase 0 already verified the `agentforce-generate` dependency. Phase 1 collects the remaining two required inputs (working Script and representative sample) plus an optional completed Persona (`persona-handoff.json` and/or `persona.md`).

**On activation, after Phase 0 passes, before checking inputs:** voice a short version of the "What this skill does" frame as the opening message: what the skill produces, who it is for, and what the session looks like (3–5 short bullets). Then ask for the Script, sample, and any completed Persona files. Do not skip the frame.

**Behavior:**
1. Read the source Script. Identify topics, actions, system instructions, welcome/error/copy strings, business logic, and compliance constraints.
2. Read the representative sample.
3. If a Persona is supplied, read it:
   - **Prefer `persona-handoff.json`** when present: read its `persona_contract`, `semantic_deltas` (including `static-copy-candidate` welcome wording), `adjacent_constraints`, and `downstream_acceptance` first, then fall back to prose extraction from `persona.md` for anything the JSON doesn't carry (the agent name and radio-test result live only in `persona.md`).
   - **Check freshness.** If both files are present, hash `persona.md` and compare it with the JSON's `source_persona.sha256`. A mismatch means the handoff is stale: mark `[review needed]` and ask which is current before going on.
   - **Record** `persona_source` (path or paths), `persona_source_sha256` (of `persona.md`), and `persona_handoff_status` (the JSON's top-level `status`: `approved` / `draft`). A draft Persona can be used, but the bundle labels everything derived from it as draft.
   - **Extract:** Identity, agent name and radio-test result, Personification level and organizational "we", Register, Voice dimensions (Warmth, Emotional Coloring, Empathy, Personality Intensity, Humor, Brevity intent, Reading Level, Formality), Tone, Negative Identity, lexical Tone Flex triggers/maxima/cues/resets, Phrase Book, Never-Say entries, Lexicon meaning, explicit Guardrails, immutable content/response shape, and `technical_explanation_framing`. Also read any `adjacent_constraints` with `owner: "voice-ux"`: client voice requirements captured verbatim in the Persona workshop ("no strong accent", "gender-neutral like our mascot"). They feed the Vocal Identity brief.
4. Treat the Persona as the authoritative character contract and the Script as authoritative for business logic, actions, routing, and source-carried compliance. If their immutable or compliance constraints conflict, preserve both, mark `[review needed]`, and pause that rewrite for user resolution.
5. **If no sample is provided, refuse to proceed.** Explain that repair, grounding, latency, and turn structure are observable only in flow, then ask for a representative turn-by-turn sample. Do not synthesize.

Do not proceed to Phase 2 until both required artifacts are settled. The Persona input remains optional; when absent, infer character signals from the Script and sample and label them as inferred.

## Phase 2 — Automated Extraction (mode detection)

Before asking the developer anything, extract from the artifacts. Crucially, this phase **infers the mode**.

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

### Other extraction
Beyond mode signals, extract: audience tone, primary intents, action set with expected latency profile, existing grounding/repair logic, and character signals. When a Persona is supplied, its contract overrides character inference. When it does not, infer acknowledgment patterns and discourse markers from the Script/sample for Layer C and label that evidence as inferred.

### Stage map

Build a stage map: one row per `start_agent` and `subagent` block, with these columns:

| Stage | Role | Model | Prose words | Tools offered |
|---|---|---|---|---|
| `router` | router (logic only / HyperClassifier / LLM) | pinned or inherited | 0 | 0 |
| `verify_caller` | speaking | `model_config` value, or "default" | 640 | 2 (both guarded) |

Role is one of: **logic** (no reasoning pass), **router**, **classifier** (HyperClassifier fork) or **speaking**. Count prose words in each block's `|` lines, plus the global `system.instructions`. The map grounds the latency triage in Layer E (pass count, model choice, prompt size) and goes at the top of the audit section. It's for diagnosis only; the skill doesn't restructure stages.

Surface what was inferred — including the proposed mode and the signals behind it — so the developer can correct.

## Phase 3 — Mode Confirmation + Gap-fill Diagnostic

Use `AskUserQuestion`. Always ask:

1. **Confirm mode:** Show the inferred mode and signals. Offer migrate / optimize / "let me explain". This question always fires; it gates the rest of the audit.

Then ask gaps the artifacts can't reveal (modality trait matrix):

2. **Channel type?** Voice-only telephony, or truly multimodal voice-over-web? *Gloss for the developer:* "truly multimodal = voice and a chat/visual UI co-exist on equal footing (e.g. voice-over-web), not voice with an occasional fallback." This gates every "keep if multimodal" pattern branch (A03, C01, C03, C05, H01, H02) — answer it once here rather than letting each pattern guess.
3. **Crossmodal handoff channels available?** *(multi-select — offer screen / web handoff, SMS, email, and "other")* Which channels can the agent shift the caller to when voice isn't the right surface — e.g. to send a tracking link or a product-info link? Feeds P12 and the D05 / D08 / C04 / E03 handoff patterns and the tier-3 repair path.
4. **IVR / carrier-side pre-call announcement available?** Can disclosures (recording, transcription, AI) play before the agent connects? Gates the opening split (T-opening): if yes, the institutional disclosures live in the IVR / carrier layer and the agent welcome stays short. Bring legal in early — recording, AI-disclosure, and opt-in vs. opt-out consent requirements vary by country, region, state, and language; flag a disclosure/consent review whenever the engagement adds a market, region, or language (B02).

5. **Vocal identity** (feeds the brief, H08). Batch these, and skip any the Persona's `adjacent_constraints` already answer:
   - **Gender presentation:** should the voice read as female, male, or deliberately ambiguous? Ask; never infer it from the role. If ambiguous, say up front that today's catalogs are effectively binary, so this means the most neutral-sounding voice available, checked with listeners.
   - **Age band** the voice should suggest.
   - **Accent per locale:** local, neutral-standard, or brand-specified.
   - **Who's calling:** age profile, second-language speakers, stress state, noisy environments.

Additional gap questions if not inferable:
- Languages and audience constraints
- Confirmed primary use case if the Script is multi-intent

Skip any question whose answer is already visible in the Script or sample.

**Barge-in is assumed available** — it's an Agentforce default, so it is no longer a diagnostic question. Design accordingly: P1 chunking and the "don't repeat key data when interrupted" rule apply unconditionally, since any long utterance is interruptible whether or not the design intends it.

**Keypad / DTMF is assumed available (GA 2026-07-28)** — keyed digits arrive as plain text, so it is no longer a diagnostic question either. Default to *offering* the keypad for numeric capture: as a repair fallback after a first mishear, and as the default (a privacy device) for sensitive numbers like cards or account IDs. It is numeric-only — alphanumeric values (email, mixed IDs) go to letter-by-letter phonetics and a type-don't-say handoff, never the keypad. See D04, D06, D07, D08.

**Question format:** Batch independent questions into a single `AskUserQuestion` call. Use single-select for booleans, multi-select where multiple answers apply (the crossmodal-handoff question is multi-select).
