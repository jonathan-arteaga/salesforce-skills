# Agentforce Agent API and Summer '26 Hosted MCP Servers

## Agentforce Agent API Setup & Security Baseline

- **Authentication**: Configure an **External Client App** with **JWT-based access tokens** (server-to-server). Keep client secrets, private keys, and bearer tokens strictly server-side — never expose them to browsers or print raw auth payloads.
- **Host & Agent Eligibility**: Call the documented public Agent API host (`api.salesforce.com`, or its Government Cloud equivalent) — My Domain serves a separate org/token role. Verify the target agent type is supported (**Agentforce (Default)** employee copilot agents are not supported by Agent API).
- **Explicit execution identity (`bypassUser`)**: Choose `bypassUser` deliberately (`true` executes as the agent-assigned user; `false` executes as the token-associated user). Neither value authenticates an end customer supplied in message text — validate application-level user ownership before forwarding a session.

## Agent API Session Lifecycle & State Machine

Model an explicit client state machine isolated per authenticated application user (never share sessions across users):

`not_started -> starting -> active -> sending/receiving -> ending -> ended` (with explicit `failed` and `unknown` states).

| Lifecycle Event | Required Client Behavior |
| --- | --- |
| Start session | Capture real server `sessionId`; on failure (including empty `404`), preserve redacted status, endpoint, timestamp, and correlation ID — never fabricate an active session or broaden privileges |
| Sync message | Send against fetched current schema; serialize concurrent sends per session unless parallel ordering is explicitly documented |
| SSE streaming message | Buffer chunks and parse documented SSE event framing and completion signals; never assume one network chunk equals one complete message |
| Disconnect after send | Transition to `unknown` outcome; **never blindly replay** a message that may execute an agent action without verified server idempotency |
| Token/session expiry | Follow documented refresh/restart semantics without leaking state across users |
| User cancellation | Distinguish local UI abort from confirmed server cancellation (transport cancel does not roll back a Salesforce action) |
| Feedback | Submit separately using documented response/message identifiers (never mixed into the message turn) |
| End session | Call end-session endpoint, clean client state, prevent session reuse, and mark ended only on confirmed response |

## Empty 404 Diagnosis & Contract Testing

- **OAuth success does not prove session readiness**: On an empty `404`, inspect public API host, configured org domain, agent ID/type, client app connection, and execution identity separately without trying undocumented internal hosts or broadening permissions.
- **Mock/contract tests**: Cover start failure, identity isolation, partial SSE frames, malformed/error events, duplicate callbacks, disconnect-after-send, cancellation, feedback, and end-session cleanup. Never log full sensitive transcripts by default.
- **Sandbox smoke test**: Run a bounded authorized smoke test against a non-destructive test agent using synthetic records; report local contract tests, sandbox smoke results, and untested production behavior separately.

## Summer '26 Salesforce Hosted MCP Server Integration

- **Verify before authoring**: Confirm target org release (Summer '26+), Hosted MCP Server feature availability, endpoint URL, and live tool schemas before writing client adapters.
- **Documentation MCP vs Hosted Org MCP**: A Salesforce Documentation MCP provides read-only documentation search/fetch — it is **not** a live org connector. Treat org-connected Hosted MCP Servers as privileged data/action surfaces.
- **Auth & least-privilege scoping**: Connect via External Client App / OAuth 2.0 with minimal scopes, explicit user or integration-user identity, and clear read vs write tool boundaries.
- **Operational guardrails**: Enforce timeouts, idempotency, retry caps, and human-in-the-loop approval for mutating MCP tool calls; redact all bearer tokens and sensitive CRM records from client logs.

## Required Config Variables & Delivery Hygiene

Deliver integration adapters with environment variable names only — never inline secret values:

| Config Variable | Purpose | Logging / Redaction Rule |
| --- | --- | --- |
| `SF_API_HOST` / `SF_MY_DOMAIN` | Public Agent API host vs org My Domain | Safe to log hostnames |
| `SF_ECA_CLIENT_ID` / `SF_AGENT_ID` | External Client App & target Agent ID | Safe to log non-secret IDs |
| `SF_JWT_PRIVATE_KEY` / `SF_ACCESS_TOKEN` | Signing key & bearer token | **NEVER log, commit, or return to browser** |
| `SF_MCP_SERVER_URL` | Verified Summer '26 Hosted MCP endpoint | Log endpoint & correlation ID only |
