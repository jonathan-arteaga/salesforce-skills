# Routing-Derived Escalation & Handoff Scenarios

Generate exhaustive, org-specific escalation test plans from BOTH the published agent definition AND live Omni-Channel routing metadata. Producing a plan is strictly read-only and never executes live handoffs automatically.

## Prerequisites & Non-Agentforce Permissions

Confirm non-production sandbox status and customer data-handling approval before querying org metadata. Standard Agentforce permission sets (`AgentforceServiceAgentBuilder`, `AgentforceServiceAgentUser`, `AgentforceServiceAgentBase`) do NOT grant read access to Omni-Channel objects—verify profile/admin read access to:

| Object(s) | Purpose |
| --- | --- |
| `BotDefinition`, `BotVersion` | Published agent and active version discovery |
| `Group`, `QueueRoutingConfig`, `ServiceChannel` | Target queues, capacity weights, and channel links |
| `UserServicePresence`, `AgentWork`, `ServicePresenceStatus` | Live capacity, availability models, and presence states |
| `MessagingSession`, `MessagingChannel`, `EmbeddedServiceConfig` | Session lifecycle transitions and deployment surface |
| `BusinessHours`, `FlowDefinitionView`, `ApexClass` | Operating hours/timezones and custom routing availability logic |

## Agent-Centric Metadata Query Strategy

1. **Parse `.agent` first:** Extract escalation subagents, `connection` blocks, pre-escalation context variables, gating flags, and referenced Queue/Flow/Apex targets.
2. **Query ONLY referenced targets:** Fetch matching `Group` / `QueueRoutingConfig`, Omni-Channel `FlowDefinitionView` (and subflows), linked `ServiceChannel`, `BusinessHours` (with timezone/operating windows), `MessagingChannel`, and `ServicePresenceStatus` rows—avoid broad unscoped queries across unrelated queues.
3. **Graceful degradation:** If an object query fails due to missing Omni-Channel permissions, record the exact missing permission and mark dependent routing scenarios `BLOCKED / MANUAL VERIFY` rather than inventing queue IDs.

## Scenario Categories to Generate

Include only categories applicable to the agent and discovered org infrastructure:

- **Agent behavior (from `.agent`):** User-requested escalation, agent-initiated failure-threshold escalation, pre-escalation context gathering, verification-gated escalation, user cancel/abort mid-handoff, and multi-turn resumption.
- **Routing infrastructure (from org metadata):** Agents available (queue presence & service channel capacity), fallback when zero agents online, capacity overflow/concurrent requests, agent status flips mid-transfer, `MessagingSession` status lifecycle, and `BusinessHours` open/close/timezone boundaries.
- **Custom business logic:** VIP/tier priority routing, repeat-escalation checks, SLA timers, HIPAA/PCI compliance routing, language/region routing, and external system fallbacks (Case creation, Platform Events, transcript attachment, bot re-engagement).
- **Safety probes (6 critical checks):** Verification bypass before escalation, prompt injection during handoff summary, PII leakage in fallback messages, social engineering for priority queue, refusal loop trapping, and abusive/crisis immediate escalation.

Deliver a structured manual/automated test plan with preconditions (exact human agent presence states to set), turn-by-turn utterances, expected `MessagingSession` / Queue / Case outcomes, and synthetic fixtures only.
