---
name: agentforce-api-integrate
description: "Build or troubleshoot an application integration with the Salesforce Agent API: authentication, session creation, synchronous or streaming messages, feedback and session end. Use for application-to-agent lifecycle and failure recovery. Not agent authoring, generic REST integrations, or voice-channel configuration."
---

# Agentforce API Integration

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Capture application platform, agent type/version, org/environment, intended authenticated users, channel and synchronous/streaming UX. Fetch current Agent API setup, lifecycle and API reference; verify the selected agent is supported. Do not assume every Agentforce channel/type is available through this API.
2. Discover existing OAuth/client configuration and current authorization requirements. Reuse integration-connectivity-connected-app-configure for client setup. Keep client secrets/tokens server-side, redact logs, and verify the actual service/agent identity plus end-user authorization. A user-supplied customer ID is not proof of access.
3. Specify a session state machine: not started → starting → active → sending/receiving → ending → ended, with explicit failure/unknown states. Map application conversations to sessions without sharing them across users. Capture actual API session/message identifiers; do not invent sequence, endpoint or idempotency behavior.
4. Build a client adapter only against the fetched current schema and available runtime. Separate transport/auth from conversation state and UI rendering. Choose synchronous responses or supported stream events; parse the documented framing and completion signals rather than assuming network chunks equal complete messages.
5. Define timeouts, cancellation, expired token/session, disconnect and retry behavior. A lost response can leave server processing state unknown. Do not blindly resend a message that might execute an action; verify documented replay/idempotency support or surface uncertainty with a controlled recovery path. Protect against concurrent sends/order races according to supported semantics.
6. Write mock/contract tests for session start failure, authorized identity isolation, partial stream frames, malformed/error events, duplicate callbacks, disconnect after send, cancellation, feedback and end-session cleanup. Mocks prove client behavior, not service compatibility. Never log full sensitive transcripts as default diagnostics.
7. Run a bounded authorized sandbox smoke test with a non-destructive test agent and synthetic data. Verify actual start/message/completion/end behavior, reconnect policy and conversation isolation; preserve request IDs/status without secrets. Feedback submission is separate from a message and must use the documented response identifiers.
8. Deliver implementation or, if required schema/runtime is unavailable, a concrete interface/state/test draft with blockers. Include configuration variable names without secret values, evidence and operational recovery. Agent edits/deployment and production messages are outside a read-only integration review.
