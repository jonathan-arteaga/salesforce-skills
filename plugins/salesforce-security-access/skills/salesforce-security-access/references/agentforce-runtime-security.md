# Agentforce Runtime Security Reference

Secure Agentforce execution identity, backing-action authorization, deterministic guardrails, Trust Layer boundaries, trace/transcript governance, file uploads, and memory.

## 1. Execution Identity by Agent Type and Channel

Always resolve the **agent type, builder generation, channel, release, and effective execution user** before assessing data access:

| Agent Type | Typical Execution User | Primary Risk |
| --- | --- | --- |
| Employee Agent | Logged-in Salesforce user | Inherited over-privileged user permissions or `without sharing` backing actions |
| Service Agent (unauthenticated / Messaging / Voice / Web) | Designated Agent User (`default_agent_user` under `access`) | Shared agent user can query across all customers if backing actions do not filter by verified identity |
| Service Agent (authenticated Experience Cloud / verified site channel) | Verified site user or Agent User (verify per channel setup) | Assuming site login or a Contact ID in context automatically enforces record isolation |

Key invariants:
- **A Contact ID or variable in conversation context does NOT enforce record access.**
- **Verify `default_agent_user` placement**: In current Agent Script bundles, `default_agent_user` belongs under `access`; inspect the org's actual agent user profile, permission sets, and licenses rather than assuming defaults.
- **Test as the effective identity**: An admin preview proves nothing about the agent user or external site user's runtime permissions.

## 2. Backing-Action Authorization (Apex, Flow, External APIs)

Natural-language prompts, subagent descriptions, and action visibility filters are **UX/routing controls, never authorization boundaries**:

- **Enforce authorization inside every backing action**: For Service agents running as a shared agent user, bind queries and mutations to a **verified customer identity** obtained from a trusted verification action or authenticated channel claim — never from a free-text customer assertion or an LLM-populated variable.
- **Explicit CRUD/FLS and sharing in Apex**: Enforce `with sharing` and `WITH USER_MODE` / `AccessLevel.USER_MODE` (API 67.0+ defaults to user mode and rejects `WITH SECURITY_ENFORCED`; API 66.0 and earlier differ). If a narrow system-mode lookup is required for unauthenticated identity verification, justify it explicitly, return minimal fields via `Security.stripInaccessible`, and never expose unverified records. Delegate code edits to `salesforce-apex`.
- **Flow execution context**: Verify whether invoked autolaunched Flows run in User Context vs System Context with or without Sharing; never leave a Service agent action in `System Context Without Sharing` without explicit verified-identity scoping. Delegate Flow edits to `salesforce-flow`.
- **Re-check before consequential actions**: Re-validate eligibility and ownership immediately before DML, refunds, cancellations, or external callouts; use idempotency keys and reconcile uncertain outcomes before retrying.
- **Mandatory cross-customer denial test**: Every Service agent security review must include a synthetic test where verified Customer A attempts to read or mutate Customer B's record ID/order/case and is deterministically denied.

## 3. Deterministic Script Controls vs Prompts

- **Never rely on prompt wording ("always", "first", "STOP")** to enforce verification, eligibility, or sequencing. Use deterministic Agent Script transitions/conditions backed by trusted action outputs.
- **Subagent `system` overrides**: A subagent `system` block **replaces** (does not append to) global `system.instructions`. Audit every override so safety, privacy, and escalation rules are not silently dropped.
- **Lifecycle hook limits**: `after_reasoning` runs after the reasoning loop per turn, but is **skipped when a subagent transitions mid-execution** and is **unsupported with EinsteinHyperClassifier**. Never place required security checks, audit writes, or cleanup solely in `after_reasoning`.
- Delegate `.agent` authoring edits to `agentforce-build` and static bundle audits to `agentforce-review`.

## 4. Einstein Trust Layer Masking vs Stored Traces & Transcripts

A common production security misconception is assuming Einstein Trust Layer masks all agent PII/PHI:

- **LLM data masking is disabled for Agentforce agents**, including prompt templates invoked through agent actions. Do not design compliance controls that depend on Trust Layer LLM masking for agents.
- **Provider zero retention is NOT zero Salesforce storage**: Even when an external LLM provider enforces zero data retention, Session Tracing Data Model (STDM) DMOs (`ssot__AiAgentInteractionMessage__dlm`, `ssot__AiAgentInteractionStep__dlm`, `GenAIGatewayRequest__dlm`, `GenAIGeneration__dlm`), Messaging transcripts, and Voice recordings/transcripts can store PII, PHI, payment details, prompts, and raw action outputs inside Salesforce / Data 360.
- **Defense-in-depth controls**:
  1. **Data minimization**: Strip unnecessary sensitive fields before returning action payloads to the reasoning loop.
  2. **Trace & Data 360 access controls**: Restrict who can query STDM and Einstein Audit & Feedback DMOs, configure authorized Data 360 data-space governance and masking policies via `data360-activation-governance`, and keep prompt dumps gated (`--show-prompts` off by default in `agentforce-observe`).
  3. **Voice recording governance**: Verify telephony architecture, Real-Time Streaming recording settings, per-agent Flow overrides, and participant notice/consent on every recorded leg.

## 5. File Uploads, Memory, and Context Boundaries

- **Uploaded files (`config.file_upload`)**: Treat all user attachments as untrusted input capable of carrying prompt injection, malware, or another customer's records. Restrict file upload capability to specific subagents that genuinely require it, and validate file type/size/scanning upstream.
- **Agent memory & user-profile context**: Memory is **never** identity verification or authorization. Enforce cross-user isolation, explicit consent, data minimization, and deletion workflows. Note that disabling memory does not automatically delete previously stored memories.
- **Grounding & retrievers**: Ensure Data Library / custom retrievers enforce persona-appropriate document visibility; verify unauthorized-content denial cases via `agentforce-test`.

## 6. Security Review Output Contract

Report findings in four clear buckets:
1. **Verified org/bundle facts** (agent type, channel, execution user, permission sets, action targets).
2. **Blocking security gaps** (cross-customer access paths, unverified gates, dropped `system` overrides, exposed sensitive payloads).
3. **Sandbox verification evidence** (allowed + cross-customer denied runs with synthetic data — distinct from simulated action passes, which do not validate live permissions or DML).
4. **Untested / out-of-scope items** and companion handoffs (`salesforce-apex`, `salesforce-flow`, `agentforce-build`, `agentforce-test`, `data360-activation-governance`).

## Sources Verified

- Agent Execution Context and Data Access by Type: `https://help.salesforce.com/s/articleView?id=ai.agent_execution_data.htm&release=264.0.0&type=5`
- Data Masking Limitations in Agentforce: `https://help.salesforce.com/s/articleView?id=ai.agent_trust_data_masking.htm&release=264.0.0&type=5`
- Agent Script Blocks, Overrides & Hooks: `https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-blocks.html`
- Agentforce Session Tracing: `https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace.htm&release=264.0.0&type=5`
