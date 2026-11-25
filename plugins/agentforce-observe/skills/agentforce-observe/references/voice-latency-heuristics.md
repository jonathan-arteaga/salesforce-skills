# Voice Latency Heuristics

Voice agents live and die on latency. Under ~2 seconds between "caller stops speaking" and "agent starts speaking" feels natural; every additional second erodes conversational flow. Text agents can hide a slow tool behind a spinner — voice agents cannot. This reference encodes field-verified latency anti-patterns worth catching at authoring time (`agentforce-build`) and diagnosing from traces (`agentforce-observe`).

Each pattern has three parts: **detection** (how to spot it in the `.agent` bundle or a trace), **impact** (typical cost), and **fix** (instructional patch, action/tool change, or flag-for-human).

> **Fix classification**: Only *purely instructional* fixes (adding an ack phrase, tightening turn length, adding a spoken-form rule) are safe to apply automatically via `agentforce-build`. Anything that changes an action's implementation, its synchronicity, or an org/channel-level setting is **flag-only** — surface it with the specific object/action named and let a human decide.

## 1. Synchronous Writes on the Live-Call Critical Path

Any write (DML, external callout, trigger cascade) running inside the live turn between caller-speaks and agent-speaks adds directly to perceived response time.

- **Detection**: Action performs a write synchronously in the reasoning turn (`update`, `insert`, `log`, `commit`, `save`, `record`, `create`, `submit`), or a trigger fires on the target object.
- **Impact**: Simple insert with trigger ~300–800ms; managed-package trigger cascade multiple seconds; chained callout inside trigger +1–3s per hop.
- **Fix**:
  - Preferred (flag-only): move write post-call via Platform Event or async Queueable (`salesforce-apex`).
  - Instructional: add an ack phrase before invoking the action ("One moment while I get that on file.").
  - Flag for human: if the write must occur mid-turn (authentication, payment auth), name the object and trigger rather than rewriting.

## 2. Large Result Sets Returned Raw to the Reasoning LLM

Returning full bodies of every matching article/record slows retrieval and bloats LLM reasoning context.

- **Detection**: Retrieval action (`search`, `retrieve`, `knowledge`, `articles`, `documents`) returns > ~5 items or > ~2KB raw text with no `limit` / `top_k` / `max_chars` parameter.
- **Impact**: Seconds per call, slower reasoning turns, degraded accuracy, and inflated prompt tokens.
- **Fix**:
  - Action change (flag-only): summarize first (title + 1–2 sentence excerpt), page detail via follow-up action, and add a low default `limit` (3–5) with allowed values documented in the parameter description.
  - Instructional: if bulky retrieval must stay, add an ack phrase.

## 3. Chained External Callouts

Every external HTTP hop adds tail latency; two chained hops push p95 across several seconds.

- **Detection**: Single action makes 2+ external HTTP calls, or a trigger on the target object fires an external webhook.
- **Impact**: ~200–800ms typical per hop, multiple seconds at p95.
- **Fix**: Flag for human with exact hops named; propose server-side consolidation or parallel pre-fetch (`salesforce-integrations`).

## 4. Over-Decomposed Multi-Subagent Routing

Each planner turn costs ~1–2s; deep trees of routing-only subagents ("dead hubs") multiply turns, latency, and Flex Credit consumption.

- **Detection**: Multiple subagents whose only role is routing to one child subagent, or a classifier/guardrail subagent intercepting every utterance.
- **Impact**: Extra planner round-trips per turn.
- **Fix**:
  - Flag for human: flatten multi-subagent hierarchy (`agentforce-design`, `agentforce-build`).
  - Where genuine domain boundaries remain and the entry router only selects transitions, evaluate Einstein HyperClassifier (do NOT use it when the router must answer, clarify, run other actions, inspect images, or use lifecycle hooks).
  - Where hops remain, add an ack phrase or fold lightweight guardrails into global `system:` instructions.

## 5. Long Agent Turns Trip the Silence/Nudge Timer

Long spoken turns can trigger the platform Speak-Up ("are you still there?") nudge prematurely, causing overlap or dead air.

- **Detection**: Responses over ~30 words / 2–3 sentences (~10s speech), or welcome greeting > 1–2 sentences.
- **Fix**:
  - Instructional: enforce concise <= 2-sentence turns and a 1-sentence greeting (`agentforce-build`).
  - Flag for human: legally required disclosures require tuning org-level silence/nudge timing, not the `.agent` bundle.

## 6. TTS Number, Currency, and ID Garble

TTS engines garble raw strings like `$172,576.81` or `+14155551212` unless pre-formatted into spoken form.

- **Detection**: Action outputs or instructions surface prices, phone numbers, dates, or record/account IDs without a spoken-form instruction rule.
- **Fix**: Instructional — add a spoken-form rendering rule in `system:` instructions (`agentforce-build`); note weak TTS locale normalization when applicable.

## 7. Premature End-of-Turn Under Noise (STT Endpointing)

Callers in noisy environments (telephony PSTN/SIP, retail, auto, home services) get cut off when STT endpointing fires too early.

- **Detection**: Telephony deployment in noisy domain with default endpointing silence threshold; traces show truncated caller utterances and repeated clarifications.
- **Fix**:
  - Flag for human (org/channel setting): raise endpointing silence threshold (~300–900ms range; higher when noisy).
  - Instructional: add an ASR mishearing repair rule so truncated utterances recover gracefully.

## 8. Telephony Transport Hops (SIP / Multi-Region)

Multiple SIP trunks, third-party telephony proxies, or non-local regions add fixed network latency outside the `.agent` bundle. Flag for human telephony/platform owners.

## Automatable Trace & Bundle Checks

| Pattern | Meaning | Severity | Fix Class |
| --- | --- | --- | --- |
| Mutating action runs synchronously inside turn | Sync write on critical path | High | Flag-only (+ ack phrase) |
| Retrieval action returns > ~5 items / > ~2KB without `limit` | Bulky retrieval | High | Flag-only |
| Action makes 2+ external HTTP calls | Chained callout | Medium | Flag-only |
| Routing-only subagent chains | Over-routing / dead hub | Medium | Flag-only |
| Responses > ~30 words or greeting > 1–2 sentences | Nudge / long-turn risk | Medium | Instructional |
| Prices / phones / IDs without spoken-form rule | TTS garble | Medium | Instructional |
| Slow action (SOQL, HTTP, RAG) without ack phrase | Missing filler | High | Instructional |
