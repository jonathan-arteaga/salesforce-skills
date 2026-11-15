# Agent-Type Specific Review Variants

> **Version note:** Dimension 8 (Permissions, Identity & Access Control) was added in v1.7.0. The approach differs fundamentally by agent type — Service/SDR agents use a dedicated running user (audit their permission sets); Employee Agents run in the calling user's context (audit the instructions and action design instead). Voice adds a PSL license check. See each type's D8 block below.

For each agent type, these are the additional dimension-specific checks to layer on top of the base 7-dimension framework.

---

## SDR / Sales Development Agent

**Dimension 1 additions:**
- Are topics scoped to outreach and scheduling only? Flag any topic that could lead to autonomous deal-making or pricing decisions.
- Is the agent clearly framed as assistive (hands off to human rep) vs. autonomous?

**Dimension 3 additions:**
- Competitor mention handling (by name — e.g. [Competitor1], [Competitor2], named market rivals)
- CASL / CAN-SPAM opt-out compliance — is there a dedicated opt-out topic with auditable flow action?
- Bilingual handling if Canada deployment (English/French per Bill 101)
- No SLA, pricing, or contract commitment guardrail

**Dimension 6 additions:**
- CASL compliance for commercial electronic messages
- Canadian data residency if applicable (PIPEDA)
- LLM fallback to out-of-region endpoint risk

**Dimension 7 additions:**
- Email Activity logging (EmailMessage + Task on Lead/Contact)
- MAX_OUT_EMAIL_THREAD_RETRY error handling
- Lead deduplication — is duplicate email address handling addressed?

**Dimension 8 — Permissions (dedicated running user):**
- Retrieve action schemas first — confirm which objects/fields/classes the actions touch before checking permissions
- Priority Apex classes to verify: any invocable class backing email send, lead status update, or opt-out write
- Priority objects + required access:
  - Lead: Read required; Create/Edit only if actions write status or opt-out fields — confirm from schema
  - Contact: Read required; Edit on `HasOptedOutOfEmail`, `DoNotCall` if opt-out action present
  - Task: Create required if activity logging is in scope
  - EmailMessage: Create if email logging action is present
  - User: Read if seller lookup / calendar link action queries User records
- Custom fields: any sequence-state fields (e.g. `Outreach_Stage__c`, `Last_Contacted_Date__c`) appearing in action inputs/outputs — verify Read/Edit FLS per schema
- Named Credential: verify if any action makes an external callout (e.g. calendar API, sequencing tool)

---

## Service Agent (Customer-Facing Support)

**Dimension 1 additions:**
- Is the agent scoped to deflect/resolve only — not make service credits, refunds, or policy exceptions autonomously?
- Are topic handoff conditions to human agent clearly defined?

**Dimension 3 additions:**
- Sensitive complaint handling — legal threats, regulatory complaints, media escalation
- No autonomous credit/refund/exception decisions
- Data subject request handling (GDPR Article 17 / PIPEDA right of erasure)

**Dimension 4 additions:**
- Case ID null-check before case creation or update
- Dedup check — does creating a new case check for open duplicates?

**Dimension 5 additions:**
- Knowledge source scoped to approved support articles only — no access to internal policy docs
- Hallucination risk on technical troubleshooting steps

**Dimension 6 additions:**
- Minimize case input and verify data access. Einstein Trust Layer LLM masking is disabled for Agentforce agents, including prompt templates invoked as agent actions; do not count the global masking toggle as an agent control.
- No storage of sensitive personal data outside Salesforce

**Dimension 7 additions:**
- Case creation and update logging
- CSAT trigger after case resolution
- Escalation queue for failed resolutions

**Dimension 8 — Permissions (dedicated running user):**
- Retrieve action schemas first — confirm which objects/fields/classes the actions touch before checking permissions
- Priority Apex classes to verify: any invocable class backing case create/update, OTP/verification, or escalation routing
- Priority objects + required access:
  - Case: Read required; Create/Edit only if actions create or update cases — confirm from schema; do NOT assume CRITICAL if Create/Edit is absent without schema confirmation
  - CaseComment: Create only if a logging action writes comments — confirm from schema
  - Contact/Account: Read required for caller verification lookups
  - MessagingSession: Read + Edit on CaseId and status fields if Email2Case or messaging channel is in scope
  - KnowledgeArticleVersion: Read required if a knowledge action is present — verify FLS on Title and article body fields
- For Email2Case / voice channel: verify `MessagingSession.CaseId` Read FLS — frequently missing
- Named Credential: verify if any action calls an external verification service or ticketing system

---

## Field Service Agent

**Dimension 1 additions:**
- Is agent scoped to scheduling, status updates, and notifications only?
- Is technician dispatch out of scope (human-only decision)?

**Dimension 3 additions:**
- No SLA commitment or technician arrival time promise
- No autonomous rescheduling without customer confirmation
- Safety incident reporting escalation path

**Dimension 4 additions:**
- Work Order ID null-check
- Asset and location data typed correctly

**Dimension 5 additions:**
- Product/equipment knowledge scoped to field service catalogue
- No hallucination of technical specifications

**Dimension 6 additions:**
- Location data handling (GPS / address) — residency and retention
- Work order data classification

**Dimension 7 additions:**
- Work order write-back logging
- Technician notification delivery confirmation

**Dimension 8 — Permissions (dedicated running user):**
- Retrieve action schemas first before checking any permission
- Priority objects: WorkOrder, ServiceAppointment, Asset, Location — confirm Create/Edit only if schema shows DML
- Named Credential: verify if any action calls an external dispatch or scheduling API

---

## Employee Agent (Internal-Facing)

**Dimension 1 additions:**
- Is the agent scoped to a defined internal domain (HR, IT, Finance, Legal)?
- Are cross-domain requests explicitly deflected?

**Dimension 3 additions:**
- No HR or legal advice guardrail — must escalate to qualified professional
- No access to other employees' personal data
- No autonomous policy exceptions or approvals

**Dimension 4 additions:**
- Employee ID / user ID typed correctly
- Role/permission check before surfacing sensitive data

**Dimension 5 additions:**
- Internal knowledge scoped to approved policy documents
- No access to confidential documents outside the employee's entitlement

**Dimension 6 additions:**
- Internal data classification — must not expose confidential data to LLM
- Audit trail required for Finance and HR actions
- Data subject access rights if applicable

**Dimension 7 additions:**
- Audit log for all agent actions (approval requests, data lookups)
- Escalation path for policy ambiguity

**Dimension 8 — Running user context (NOT a dedicated user):**
Employee Agents run as the logged-in employee. There is no single running user to audit. The D8 check is fundamentally different:

- **Do not run permission set queries for Employee Agents.** The checks below apply instead.
- **Permission assumption check:** Do any topic instructions or actions assume access that a standard employee profile would not have? (e.g. reading another employee's compensation, querying HR records outside the caller's own data) → **HIGH** if yes
- **Graceful degradation check:** If an action returns null or throws `INSUFFICIENT_ACCESS` for a lower-privileged employee, does the planner handle it? Or does the agent silently fail / hallucinate? → **HIGH** if no fallback
- **Least-privilege scope check:** Are actions scoped only to objects/fields a typical employee should reach? Flag any action querying sensitive objects (Salary, Performance, Medical) without a documented access-gating mechanism → **HIGH**
- **No privilege escalation path:** Can the agent be prompted to access data the running user's own profile would block? (LLM-driven actions can sometimes bypass profile restrictions if the action runs in a different execution context) → **CRITICAL** if evidence of this
- **Admin-only action bleed:** Are any actions requiring elevated access (e.g. updating another user's record) present but ungated? These silently fail for standard employees with no useful error → **MEDIUM**
- Set permission readiness status to `NOT_APPLICABLE — Employee Agent (running user context)` in the scorecard.

---

---

## Voice Agent (`isVoiceAgent: true`)

This flag activates when the agent is deployed on a voice channel (Amazon Connect / Service Cloud Voice). It layers on top of the base agent type (e.g. Service Agent + Voice). All base dimension checks still apply — the additions below are voice-specific overrides and new mandatory checks.

---

### Token Budget — Mandatory rules for voice reviews

1. **Triage gate before analysis.** Run a silent PASS/CHECK/N/A scan across all voice checks before writing a single finding. Only CHECK items get written up. PASS items collapse to a one-line "Voice channel baseline verified" bullet per dimension.
2. **D8a is a binary table.** Output as `d8a_checklist` in the JSON — one row per check, `PASS/FAIL/N/A` + one-line note. No prose. Any FAIL escalates to a finding in D2 (timeouts/retries), D3 (consent/PCI), or D7 (logging) as appropriate.
3. **D7 voice findings are labelled by validatability.** `[METADATA]` = confirmable from config. `[REQUIRES LIVE TEST CALL]` = can only be confirmed by placing a call and querying VoiceCall records. Never mark `[REQUIRES LIVE TEST CALL]` items PASS — mark `[UNVERIFIED]` with a recommendation to validate.

---

### Dimension 1 additions — Persona, Tone & Topic Scope

- Voice persona name announced at call start (e.g. "Hi, I'm [PersonaName]")
- Voice persona and tone explicitly configured per agent — not inherited from a generic base config
- TTS voice engine documented (e.g. Amazon Polly neural voice model and voice ID)
- Verbosity guardrail — all agent responses must be speakable: no markdown, bullet lists, tables, or URLs returned as literal strings in voice output
  - *Source: General IVR UX research; Call Centre Helper — structured content is unrenderable in TTS*
- Welcome message concise — no verbose voice openers; target ≤2 sentences before first prompt
  - *Source: IVR UX research — callers abandon if opening message exceeds ~8 seconds*
- Opening message present and of appropriate length (absence = immediate call drop)
  - *Source: Salesforce Agentforce Voice — confirmed root cause of 3s call drops observed in sandbox testing May 2026*
- Voice consistency checked across all topics — tone, persona name, and verbosity guardrails apply to every topic, not just the opening topic
- Any topic whose default response renders structured content (numbered steps, links, tables) flagged as voice-incompatible without adaptation

---

### Dimension 2 additions — Instructions, Actions & Fallback

- Silence / no-input timeout configured (industry standard: 4–5 seconds)
  - *Source: Amazon Connect default `SpeechTimeout: 4s`; Twilio default `timeout: 5s` — both vendor docs*
- Max retries before escalation set to 2–3 maximum
  - *Source: Twilio Voice IVR best practices; Google Dialogflow CX no-input handling docs*
- Interruption / barge-in handling tested — caller can interrupt TTS mid-response and the agent processes the new utterance correctly without replaying the interrupted prompt
- Speech recognition no-match path configured (what happens when the agent cannot parse the utterance)
- DTMF fallback path exists — caller can press keys instead of speaking as an alternative input method
  - *Source: Amazon Connect contact flow design guide; general IVR accessibility best practice*
- Hyperlinks and URLs suppressed in voice responses — any action or knowledge response that may return a URL must have a voice-adapted fallback (e.g. "visit our website" not the full URL)
- Context handoff on transfer — VoiceCallId + conversation summary passed to live agent on escalation

**Platform limit checks (Agentforce Voice runtime — HIGH severity if breached):**
- **Response length** — no single agent turn should produce more than ~20 seconds of spoken audio. Action outputs, KB responses, and inline data blobs that return long text will be silently truncated mid-sentence in TTS. Flag any topic or action whose output can realistically exceed ~300 words.
  - *Source: Agentforce Voice operators-manual — 20s TTS ceiling enforced by platform*
- **LLM call ceiling per turn** — complex action chains must resolve within 6 LLM calls (Flash orchestrator) or 8 (Java planner). Workflows with more than 4 sequential tool calls are at risk; design them to resolve within budget or break across multiple user turns.
  - *Source: Agentforce Voice operators-manual — hard ceiling, no config override*
- **118-second LLM timeout** — any Apex action or external callout that can take longer than ~100 seconds in the worst case will timeout mid-call. Flag actions with unbounded SOQL queries, external API calls with no timeout set, or synchronous callouts without a fallback.
  - *Source: Agentforce Voice operators-manual — 118s is the hard LLM call timeout*
- **3000-token rolling context window** — long conversations silently drop leading context (earlier turns are truncated, not summarised). For multi-step verification or booking flows, confirm the agent does not rely on context from more than ~15–20 turns back.
  - *Source: Agentforce Voice operators-manual — applies to Unified Planner path*
- **TTS formatting instructions** — the platform's `NormalizationPreStep` automatically appends pronunciation guidance and TTS formatting rules (entity tagging, number/date expansion) to every system prompt. Do NOT duplicate these in topic instructions — duplication can cause conflicts. Flag any topic instruction that manually specifies "say numbers as digits", "expand abbreviations", or similar TTS directives.
  - *Source: Agentforce Voice v2-mgr-orchestration.md — NormalizationPreStep + NormalizationPostStep run automatically on ASA_VOICE profile*

---

### Dimension 3 additions — Guardrails, Safety & Compliance

**Platform escalation triggers — verify routing is configured for all of these:**

The Agentforce Voice platform will automatically escalate to a human agent when any of the following thresholds are hit. If escalation routing (flow_id / telephony transfer) is not configured, callers will receive a transfer message with nowhere to go — a silent failure. Check each trigger:

| Trigger | Threshold | Risk if unhandled |
|---|---|---|
| **Consecutive tool error** | 1 error | CRITICAL — a single Apex exception or failed callout immediately escalates the call. Any unreliable action is a direct escalation risk. |
| Safety violation | 2 instances | HIGH — inappropriate content detection fires escalation; ensure safety topics are tuned to avoid false positives on legitimate queries |
| Message limit | 400 messages per session | LOW for most deployments — but flag for long-running or looping flows |
| Human-machine rounds | 50 rounds | LOW for most deployments |
| Explicit user request | Any turn | Must have a valid transfer destination configured |

The `EscalateHandler` sends a GSM Hangup protobuf message to terminate the voice session and trigger telephony-level call transfer. If `flow_id` is not populated in the escalation tool definition (`atlas/voice/metadata/escalate_function.json`), the transfer will fail silently.
  - *Source: Agentforce Voice operators-manual.md; escalation.md — EscalateHandler + GSM Hangup flow*

- **Verbal abuse handling** — profanity or aggressive tone triggers a de-escalation response or routes to human transfer; agent does not continue resolving the original inquiry under abuse
  - *Source: Call Centre Helper industry blog; Amazon Comprehend + Azure Speech Services sentiment detection documentation*
- **Emotional distress / crisis language** — phrases indicating self-harm, severe distress, or crisis route to a crisis line or human, not a support ticket
  - *Source: NIST AI Risk Management Framework (AI RMF 1.0) — GOVERN 6.1 harm escalation; emerging responsible AI standard across CCaaS vendors*
- **Call recording notice/consent** — inspect the actual telephony path and settings. Supported Real-Time Streaming configurations can enable **Record Voice Calls with Agents**, with per-agent Flow overrides. Provider recording can cover other call legs. Verify notice, consent, access, and retention for every recorded leg; mark N/A only with evidence that recording is disabled. See the current Salesforce guidance reference.
  - *Source: Salesforce Agentforce Voice — calls are not recorded by the platform; confirmed 2026-05-21*
- **PCI-DSS voice ban** — no prompt, instruction, or action should ask a caller to speak a card number aloud; DTMF-only for any payment input
  - *Source: PCI DSS v4.0 Requirement 3.2 (data minimization); PCI SSC guidance on voice channel payment collection*
- **TCPA compliance** — if any outbound voice calls are in scope: do-not-call list adherence, consent logging, authentic caller ID (no spoofing)
  - *Source: FCC TCPA rules (47 CFR Part 64)*
- **TTY/TDD accessibility** — relay service option present or Amazon Connect TTY detection configured
  - *Source: ADA Title III (public accommodations); FCC relay service rules (47 USC 225)*

---

### Dimension 4 additions — Variable Typing & Data Integrity

- `VoiceCallId` context variable bound, non-null, and flowing into actions and logs
  - *Source: Salesforce Service Cloud Voice data model — VoiceCallId is the primary correlation key for Amazon Connect ↔ Salesforce*
- Speech confidence threshold configured — utterances below threshold re-prompt rather than act on a low-confidence interpretation

---

### Dimension 5 additions — Knowledge Grounding

- KB response length and format checked for voice suitability — responses that work in chat may be unspeakable at length (400-word articles, step lists, URLs)
  - *Source: Call Centre Helper; general IVR UX research*
- KB articles returning structured content (numbered steps, hyperlinks, tables) flagged — require voice-adapted variants or SSML wrapping before voice deployment

---

### Dimension 6 additions — Data Residency & AI Governance

- Call recording storage location and retention policy documented (e.g. Amazon S3 region, Salesforce Files)
  - *Source: GDPR Art.5(1)(e) storage limitation; PIPEDA principle 4.5*
- Sensitive data redacted — no verbal exposure of PII in TTS responses (account numbers, DOB, card details must not be read aloud)
- Voice transcript PII masking — card numbers, dates of birth, government IDs redacted from stored transcripts
  - *Source: PCI DSS v4.0 Req 3.2; GDPR Art.5 data minimization; PIPEDA principle 4.4*
- Language(s) configured for target user population — STT and TTS language models match the caller's expected language(s); mismatched language models degrade recognition accuracy
- If voice biometrics introduced in future: voiceprint consent, retention limits, and anti-spoofing controls documented

---

### Dimension 7 additions — CRM Integration & Logging

- VoiceCall record created in Salesforce for every call, including bot-only calls that never reach a human agent
  - *Source: Salesforce Service Cloud Voice reporting requirements; Amazon Connect CTI Adapter docs*
- Amazon Connect / CTI adapter health monitored — failure mode is silent (no records created, no error surfaced to agent)
- Post-call transcript synced to VoiceCall or Case record
  - *Source: Salesforce Service Cloud Voice transcript feature; Amazon Connect Contact Lens*
- Agentforce Observability enabled — session traces available for post-call RCA; without this, latency and routing failures are invisible
- Latency monitoring in place — target <2.5s end-to-end for complex requests; spikes indicate action timeout or STT processing delays
- Containment rate tracked as a primary operational metric — confirm the reporting mechanism is configured before go-live
- Feedback loop configured for incorrect or confusing responses — mechanism for callers or agents to flag bad responses feeding into a review queue

---

### Dimension 8a (new) — Voice Channel Configuration *(no chat equivalent)*

Mandatory block — check all of the following:

| Check | Standard / Source |
|---|---|
| Agent created in Agent Builder with topics & NL instructions | Salesforce Agentforce Voice setup |
| Actions configured (Flows / Apex / Prompts / external APIs) | Salesforce Agentforce Voice setup |
| **Voice architecture path identified: GSM Path or Realtime LLM Path** | GSM Path = production voice (GSM owns STT/TTS, Python Reasoner over WebSocket); Realtime LLM = direct OpenAI Realtime API or Gemini Live. Findings and KPIs differ — confirm before reviewing. *Source: Agentforce Voice voice-and-realtime.md* |
| Silence timeout configured (target: 4–5s) | Amazon Connect `SpeechTimeout` default; Twilio `timeout` default |
| Max speech duration limit set | Amazon Connect `MaxSpeechDuration` default: 15s |
| No-input re-prompt count set (max 2–3 before escalation) | Twilio IVR best practices; Google Dialogflow CX docs |
| Barge-in / interruption handling enabled | Amazon Connect Lex V2 `AllowInterrupt: true`; Twilio `<Gather>` docs |
| SSML enabled for TTS (numbers, dates, brand names) | Amazon Polly SSML; Twilio `<Say>` SSML; Google Dialogflow CX TTS config |
| STT / TTS settings validated (language model, voice ID, sampling rate) | Amazon Polly / Lex V2 config; Twilio Voice settings |
| DTMF fallback path exists | Amazon Connect contact flow guide; IVR accessibility best practice |
| Opening message present | Salesforce Agentforce Voice — confirmed root cause of call drops in sandbox testing, May 2026 |
| IVR channel capacity / throttle limit documented | Operational — specific to provisioned PSTN capacity (e.g. 300/month initial cap) |
| Speech recognition no-match path configured | Amazon Connect Lex V2 fallback intent; Twilio no-match handling |
| **Escalation flow_id configured** — telephony transfer target set in `escalate_function.json`; absent = silent transfer failure on any escalation trigger | *Source: Agentforce Voice escalation.md — EscalateHandler requires flow_id to route GSM Hangup* |
| **Topic instructions do not duplicate TTS formatting rules** — NormalizationPreStep handles this automatically; manual duplication can conflict | *Source: Agentforce Voice v2-mgr-orchestration.md — NormalizationPreStep + NormalizationPostStep run on all ASA_VOICE sessions* |
| **Session Redis TTL acknowledged** — sessions expire after 3 days (259,200s); TTL refreshed on every state update. Long-dormant sessions will lose context. | *Source: Agentforce Voice session-lifecycle.md* |

---

### Pre-Flight Testing Checklist (Voice) — Human Verification Required

These items cannot be auto-generated as test cases. They require manual verification before go-live. Include as a checklist table appended to the Dimension 8a block in the review doc (not a separate numbered section) — the FDE ticks each off and records notes.

| # | Check | How to verify | Result |
|---|---|---|---|
| 1 | Voice Preview tested in Agent Builder UI | Open agent in Builder → Voice Preview tab → run 3–5 representative utterances | ☐ |
| 2 | Multi-turn conversation tested via Testing Center | Upload voice test CSV → run suite → review turn-by-turn responses | ☐ |
| 3 | Audio playback reviewed for response quality | Play TTS output for at least one full conversation path — check for unnatural phrasing, mispronunciations, excessive length | ☐ |
| 4 | Task Resolution LLM Judge metric reviewed | Check Agentforce Observability → Task Resolution score for test sessions; target passing threshold set | ☐ |
| 5 | End-to-end: full session & intent resolution | Place a real test call through the configured channel (Amazon Connect / SCV); verify intent routing, actions fire, transfer works | ☐ |
| 6 | Benchforce `AgentforceVoice` metric run (if available) | Run Benchforce eval suite — check `is_tts_problematic` flag for any response containing literal punctuation, markdown, or URLs. Review stereo WAV recordings for TTS fidelity. Supports half-duplex and full-duplex modes. *Source: Agentforce Voice benchforce.md + operators-manual.md* | ☐ |
| 7 | Escalation transfer tested end-to-end | Trigger escalation deliberately (e.g. ask for human agent) — confirm telephony transfer completes, VoiceCall record updated, caller reaches correct queue | ☐ |

---

### Dimension 8 additions for Voice (`isVoiceAgent: true`)

Layer these on top of the base agent type's D8 checks (Service or SDR):

- **`ServicePlannerAgentUserPsl` license check (mandatory first step):**
  ```bash
  sf data query --query "SELECT PermissionSetLicense.DeveloperName \
    FROM PermissionSetLicenseAssign WHERE AssigneeId = '<userId>' \
    AND PermissionSetLicense.DeveloperName = 'ServicePlannerAgentUserPsl'" \
    --target-org <alias>
  ```
  - PSL present → VoiceCall object + FLS access confirmed. Mark PASS. Do not query ObjectPermissions or FieldPermissions for VoiceCall — they will always return zero rows and do not reflect actual access.
  - PSL absent → **CRITICAL** — running user lacks the Service Cloud Voice license entitlement entirely; no VoiceCall records will be created

- **VoiceCall object — never check via ObjectPermissions/FieldPermissions:** Access is license-controlled via `ServicePlannerAgentUserPsl`, not permission-set-controlled. Filing a gap finding based on absent ObjectPermissions rows is always a false positive for voice agents.

- **Dedicated voice permission set hygiene:** If a voice-specific permission set (e.g. `Restaurant_Agentforce_Voice_Permissions`) contributes zero Apex class entries, flag as **MEDIUM** — likely cloned from a chat or messaging agent without voice-specific curation. Retrieve action schemas to confirm which custom Apex classes are invoked before deciding severity.

- **CTI adapter Named Credential:** If the agent uses an external CTI adapter or makes outbound callouts during a voice session, verify the Named Credential is granted.

---

### KPI overrides for Voice (`isVoiceAgent: true`)

Replace or supplement the base KPI set with:

| KPI | Target (starting point) | Source |
|---|---|---|
| Call Completion Rate | > 70% | Call Centre Helper CCaaS benchmarks |
| Call Abandonment Rate | < 8% | Industry IVR average; Twilio operational benchmarks |
| Speech Recognition Accuracy | > 90% utterances correctly interpreted | Amazon Connect Lex V2 accuracy benchmarks |
| Barge-In Rate | < 20% (high = prompts too long) | Call Centre Helper; IVR UX research |
| Bot-to-Human Transfer Rate | < 30% | General CCaaS industry target |
| Average Handle Time (bot-only) | Baseline TBD by customer | Operational |

---

## Scoring Calibration by Agent Type

Some dimensions carry different weight depending on agent type:

| Agent Type | Most Critical Dimensions |
|---|---|
| SDR / Sales | D3 (Guardrails), D5 (Knowledge), D6 (Residency) |
| Service | D3 (Guardrails), D7 (CRM Logging), D4 (Variables) |
| Field Service | D7 (CRM Logging), D3 (Guardrails), D4 (Variables) |
| Employee | D6 (Governance), D3 (Guardrails), D5 (Knowledge) |
| Voice (channel modifier) | D3 (Safety/Compliance), D8a (Channel Config), D7 (CRM Logging) |
