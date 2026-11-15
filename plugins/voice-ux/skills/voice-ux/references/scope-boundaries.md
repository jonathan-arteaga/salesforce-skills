# What this skill does NOT do

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## What this skill does NOT do

- **Build a voice agent from scratch** (no source Agent Script) — start with `agentforce-generate` to scaffold one, then come back. This skill works on an *existing* Script.
- **Character design or lexical Tone Flex policy** — use `persona`. If extraction reveals no coherent character contract, recommend that skill first. When a Persona is supplied, consume it as authoritative input; do not redesign it. (Interpreting that character for the ear, through the Vocal Identity brief, casting and light tuning, *is* this skill's work.)
- **Topic / action / tool restructuring** — preserved as-is. If the audit reveals a topic structure that fundamentally fights voice (e.g., a single mega-topic that should be three), surface as `[review needed]` with a recommendation, do not refactor.
- **Acoustic/prosodic distress detection** — de-escalation *policy* is in scope (see P13) and multi-intent handling is covered (P14); but sentiment is inferred from STT transcript text only, so paralinguistic cues (tone, pace, volume) are not available to the reasoning engine — a known platform limitation, tracked for v2
- **Multilingual generation** — flag languages in audit; do not generate non-English copy
- **Telephony-platform / recognizer setup** — TTS / IVR / ASR vendor settings — surfaced as Layer E for human handoff. (Casting the agent voice is in scope, Phase 4b; only the pick in the org voice library and the listening sign-off are human steps.) (In-script `modality voice:` config — including `pronunciation_dict` and `inbound_filler_words_detection` — *is* in scope; this skill writes it. Selecting a non-default voice *model* is Agent-Script-only via the emerging nested format — documented in H03, not emitted by default.)
- **Voice agent QA / testing** — use `agentforce-test`. For production session traces, use `agentforce-observe`.

### Where neighbouring work goes

The enablement material around voice agents covers more than the `voice-ux` lane. Route it rather than absorbing it:

| If the work is… | Route to | Examples |
|---|---|---|
| Agent structure and routing | `agent-architecture` | Subagent count (aim for five or fewer, as guidance), init-once setup, subagent `system:` overrides, disabling chit-chat, `filter_from_agent` vs `is_used_by_planner` |
| Voice latency architecture | `agentforce-generate` (`references/voice-latency-heuristics.md`) | Deterministic and HyperClassifier routing, model pins, `available when` tool guards, after-speech writes, pre-fetched context, prompt budgets. This skill flags them as `[consider]` in Layer E with field costs; the owner makes the change |
| Scoring voice quality on real calls | Not installed (`voice-evaluation` lives in designing-agentforce-labs); tell the user | Voice Quality Heuristics (VQH) scoring, the 20-point voice-readiness scorecard from the Agentforce Voice Implementation Playbook, naturalness rubrics |
| Scoring text transcripts | Not installed (`evaluating-conversations` lives in designing-agentforce-labs); tell the user | JTBD × severity matrices, emerging intents |
| Test suites and live monitoring | `agentforce-test` / `agentforce-observe` | Regression tests, session traces |
| Character and word choice | `persona` | The persona framework (Personification plus 13 dimensions), never-say lists, Tone Flex word choice, the Phrase Book |
| What the character sounds like | this skill (Phase 4b) | Vocal Identity brief, casting and audition, light tuning (H08, H09, H03) |
| Platform latency outside the script | Layer E checklist, handed to the platform owner | Omni flow routing, Platform Cache, retrievers, Apex, Connect DVR |
