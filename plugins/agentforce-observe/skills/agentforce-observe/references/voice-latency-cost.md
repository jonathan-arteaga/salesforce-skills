# Voice Latency, Cost Anomalies & PII Trace Minimization Reference

Diagnose Agentforce Voice latency and recording issues, identify Flex Credit / LLM / action cost drivers from STDM + Gateway traces, and enforce PII/PHI trace minimization.

## 1. Voice Latency & Quality Diagnosis

Voice callers tolerate under ~2 seconds between end-of-speech and agent response start; every extra second feels broken. Cross-reference trace step durations (`ACTION_STEP`, `LLM_STEP`, `TOPIC_STEP` in `dc._session_tree.json` or STDM `ssot__AiAgentInteractionStep__dlm`) against [voice-latency-heuristics.md](voice-latency-heuristics.md):

| Signal in Trace / Bundle | Likely Anti-Pattern | Action Class |
| --- | --- | --- |
| Slow `ACTION_STEP` (> 500ms) on write/insert/update/log action | Synchronous DML or trigger cascade on live-call path | Flag-only (move to Platform Event/Queueable via `salesforce-apex`) + ack phrase |
| Slow retrieval `ACTION_STEP` + bloated `prompt_tokens` on next `LLM_STEP` | Large raw RAG/KB payloads with no `limit`/`top_k` | Flag-only (summarize/page action) + ack phrase |
| Multi-second `ACTION_STEP` calling external APIs | Chained external HTTP callouts | Flag-only (consolidate or parallelize server-side via `salesforce-integrations`) |
| Multiple `TOPIC_STEP` / `LLM_STEP` hops before answering | Over-decomposed subagent routing / dead hub | Flag-only (flatten subagents or evaluate EinsteinHyperClassifier — note: hooks unsupported with HyperClassifier) |
| Agent output > 3 sentences (~30 words) or markdown/lists | Long turn tripping Speak-Up nudge timer / bad speech UX | Instructional fix via `agentforce-build` |
| Raw `$172,576.81`, phone numbers, or record IDs in output | TTS garble (missing spoken-form rule) | Instructional fix via `agentforce-build` |
| Truncated user transcripts on PSTN/SIP calls | Aggressive STT endpointing under ambient noise | Flag-only (channel/org STT threshold ~300–900ms) + ASR repair prompt |

### Voice Recording & Telephony Checks
- Inspect the telephony architecture and enabled settings before evaluating recording. Supported **Real-Time Streaming** configurations can record agent calls; check **Record Voice Calls with Agents** and per-agent Flow overrides.
- Verify participant notice/consent on every recorded call leg — never automatically mark voice recording N/A.
- Verify language/persona support and beta status against the target release (text `Allowed Languages` is not proof of multilingual voice).
- Static metadata cannot prove interruption, silence, recognition failure, latency, escalation, or recording behavior; validate with real test calls in an authorized sandbox (`agentforce-test`).

## 2. Flex Credit & Cost Anomaly Triage

Use trace evidence (`dc._session_tree.json`, `dc.gateway_requests.json`, `dc.steps.json`, and STDM aggregates) to isolate **observed consumption multipliers** driving unexpected Flex Credit or LLM spend:

1. **Action invocation fan-out**: Count `ACTION_STEP` executions per turn and per session. Flag retry loops (repeated identical tool calls after malformed inputs or transient errors) and unnecessary actions triggered on every greeting/routing turn.
2. **Subagent hop & planner multiplication**: Count `LLM_STEP` and `TOPIC_STEP` rows per user turn. Dead-hub routing or ping-pong transitions multiply planner calls per utterance (2x–4x cost + added latency).
3. **Prompt & RAG token inflation**: Inspect `prompt_tokens`, `completion_tokens`, and `total_tokens` in `dc.gateway_requests.json` / `dc._session_tree.json`. Spikes typically come from unpaginated retrieval payloads, oversized `system.instructions`, or long unpruned multi-turn histories.
4. **Session volume / bot traffic spikes**: Segment session counts by channel, agent version, and `end_type` (`TIMEOUT`, `ESCALATED`, `USER_ENDED`) to distinguish legitimate traffic growth from runaway loops, automated probing, or misconfigured retries.
5. **Pricing & contract boundary**: Report observed counts (sessions, turns, actions, LLM calls, tokens) accurately, and **never quote or fabricate dollar/Flex Credit billing totals** without verifying the org's current Salesforce Flex Credit consumption card and contract rates.

## 3. PII / PHI Trace Minimization & Governance

Stored traces and voice transcripts are a high-sensitivity data store:

- **No Trust Layer LLM masking for agents**: Einstein Trust Layer LLM data masking is disabled for Agentforce agents (including prompt templates called by agent actions). Provider zero retention does NOT remove PII, PHI, or payment data from Data 360 STDM DMOs, Einstein Audit & Feedback tables, or Voice transcripts.
- **Minimize what enters traces**: Strip sensitive fields in backing Apex/Flow action outputs before returning results to the agent (`salesforce-apex`, `salesforce-flow`, `salesforce-security-access`).
- **Minimize what leaves the org**: Keep `--show-prompts` disabled by default in `render_dc.py`; redact sensitive excerpts before pasting trace summaries into tickets or chat; delete temporary scratch artifacts when an investigation closes.
- **Governance handoff**: Route Data 360 data-space access restrictions, field masking policies, retention rules, and deletion workflows to `data360-activation-governance`.

## Sources Verified

- Turn on Voice Call Recording and Transcription (Real-Time Streaming): `https://help.salesforce.com/s/articleView?id=ai.agent_record_voice_calls_realtime_streaming.htm&release=264.0.0&type=5`
- Agentforce Voice Considerations: `https://help.salesforce.com/s/articleView?id=ai.agentforce_voice_considerations.htm&release=264.0.0&type=5`
- Data Masking Limitations in Agentforce: `https://help.salesforce.com/s/articleView?id=ai.agent_trust_data_masking.htm&release=264.0.0&type=5`
- Agentforce Session Tracing: `https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace.htm&release=264.0.0&type=5`
