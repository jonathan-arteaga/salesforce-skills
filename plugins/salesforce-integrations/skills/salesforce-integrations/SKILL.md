---
name: salesforce-integrations
description: "Configure Salesforce integrations: External Client Apps, Named/External Credentials, callouts, External Services, Pub/Sub API events, Agent API sessions, and Hosted MCP Servers. Use salesforce-apex for Apex logic, agentforce-build for agents, and salesforce-devops-deploy for rollouts."
---

# Salesforce Integrations

Unified skill for Salesforce inbound/outbound connectivity: External Client Apps, enhanced Named & External Credentials, REST/External Services, Pub/Sub API events & CDC, Agent API sessions, and Hosted MCP Servers.

## Mode Routing

Select the active mode first and load only the matching reference before authoring or troubleshooting:

| Mode | When to Use | Reference |
| --- | --- | --- |
| OAuth & ECA Apps | External Client Apps, OAuth flows, PKCE/JWT, Connected App migration | [eca-and-oauth-apps.md](references/eca-and-oauth-apps.md) |
| Credentials & Callouts | Enhanced Named/External Credentials, REST/SOAP callouts, External Services, CSP/Remote Sites | [named-credentials-and-callouts.md](references/named-credentials-and-callouts.md) |
| Pub/Sub, Events & CDC | Platform Events, CDC, Pub/Sub API 72h durability, opaque replay IDs, ManagedSubscribe | [pubsub-events-and-cdc.md](references/pubsub-events-and-cdc.md) |
| Agent API & Hosted MCP | Agentforce Agent API session lifecycle (sync/SSE/feedback) & Summer '26 Hosted MCP Servers | [agent-api-and-hosted-mcp.md](references/agent-api-and-hosted-mcp.md) |

## Core 2026 Invariants

- **External Client Apps First**: Prefer External Client Apps (ECAs) for all new integrations, including single-org apps. Connected App creation is restricted as of Spring '26; existing Connected Apps keep working, and unavoidable new creation requires Salesforce Support eligibility.
- **Enhanced Named + External Credentials**: Store all outbound auth in Named Credentials backed by External Credentials. Map principals to least-privilege Permission Sets and grant `User External Credentials` object access where required. Never hardcode secrets or execute synchronous callouts from triggers.
- **Pub/Sub API Durability & Replay**: Pub/Sub API retains events for **72 hours** with **opaque replay IDs** (never parse or increment numerically). Evaluate `ManagedSubscribe` (Beta) for server-managed durable checkpoints and enforce idempotent consumers.
- **Agent API & Hosted MCP**: Use ECA + JWT tokens against the documented public Agent API host (`api.salesforce.com`), model the full session state machine (start -> sync/SSE message -> feedback -> end), and verify Summer '26 Hosted MCP Server availability, auth scopes, and schemas before use.

## Hard Org & Safety Gates

- Never commit consumer secrets, API keys, private keys, or bearer tokens to source control, logs, or tool output.
- Preserve existing working Connected Apps and credentials while validating a migration; never revoke working credentials before cutover verification.
- Never trust a user-supplied customer ID as proof of authorization; verify explicit service/agent identity (`bypassUser` for Agent API) and least-privilege OAuth scopes (never `Full` by default).
- Distinguish a read-only Documentation MCP from an org-connected Salesforce Hosted MCP Server.

## Deterministic Scripts (Black-Box Usage)

Use the bundled scripts directly without rewriting internals:

```bash
# Score integration Apex, Named Credentials, or Platform Event metadata (120-pt rubric)
python3 scripts/validate_integration.py <path-to-file>

# Configure an External Credential principal API key interactively via ConnectApi
bash scripts/configure-named-credential.sh <external-credential-name> <principal-name> <org-alias>
```

See `scripts/README.md` for legacy `set-api-credential.sh` and `scripts/templates/setup-credentials-with-csp.sh`; `suggest_credential_setup.py` is an advisory hook helper.

## Required Deliverables & Verification Integrity

- **Report order**: Integration pattern & auth model -> Files created/updated -> Security & operational safeguards (scopes, retries, idempotency, timeouts, redaction) -> Local validation score -> Sandbox smoke-test status & next step.
- Separate **local metadata/mock/contract checks** from **executed sandbox smoke tests** and **untested production behavior**. Mocks prove client behavior, not live service compatibility.

## Cross-Skill Handoffs

- `salesforce-apex`: complex domain Apex services, retry handlers, or Apex unit tests
- `salesforce-flow`: declarative HTTP callout or Platform Event Flows
- `agentforce-build`: Agentforce agent authoring, topics, and actions
- `salesforce-security-access`: Permission Sets, integration users, and org RBAC
- `salesforce-devops-deploy`: validation deployments and CI/CD rollouts
