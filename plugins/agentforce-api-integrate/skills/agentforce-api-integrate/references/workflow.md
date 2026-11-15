# Session and transport decisions

| Event | Client behavior to design/test |
| --- | --- |
| Session start fails | No fictitious active session; preserve useful redacted error |
| Partial stream data | Buffer and parse documented event framing; no premature completed answer |
| Disconnect after send | Mark outcome unknown; do not automatically replay an action-bearing message |
| Token/session expires | Follow documented refresh/session semantics; avoid cross-user recovery |
| Two concurrent sends | Serialize or use explicitly supported ordering; don't invent sequence rules |
| User cancels | Distinguish local UI cancellation from confirmed server cancellation |
| End session | Mark ended only with evidence; clean client resources and prevent accidental reuse |

The official lifecycle is start session, send synchronous or streaming messages, then end session; feedback is a separate operation. Inspect the current API reference for exact headers, payloads, event types and status semantics. Do not claim transport cancellation cancels a Salesforce business action.

Sources fetched 2026-11-15: [Session Lifecycle](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-lifecycle.html); [Agent API Reference](https://developer.salesforce.com/docs/ai/agentforce/references/agent-api). Generic state handling here is an implementation design recommendation, not a claim of server-side exactly-once behavior.

## Empty session errors

OAuth token success does not prove agent/session readiness. For an empty 404, preserve redacted status, endpoint, timestamp and correlation evidence; verify current public API host, configured org domain, agent ID/type, client connection and execution identity separately. Do not infer entitlement failure from an empty error, expose the token, try undocumented internal hosts or broaden privileges as a diagnostic shortcut.

## Verified setup baseline

As reviewed 2026-11-15, the official setup uses External Client Apps and JWT-based access tokens. Agentforce (Default) agents are not supported. Use the documented public Agent API host (`api.salesforce.com`, or its Government Cloud variant where applicable); My Domain serves a separate org/authentication role. Inspect `bypassUser`: true selects the agent-assigned user, false the token-associated user. Choose this explicitly for the intended authorization model; neither value authenticates a customer supplied in message text. Fetch the current request schema and setup requirements before implementing.

Source: [Get Started with Agent API](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-get-started.html), fetched 2026-11-15.
