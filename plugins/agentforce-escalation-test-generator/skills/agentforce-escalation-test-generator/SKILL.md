---
name: |-
  agentforce-escalation-test-generator
description: |-
  Use Agentforce routing metadata to author escalation scenarios and expected outcomes. Return a test plan and fixtures. Use agentforce-test for execution.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# Agentforce Escalation Test Generator

This skill generates comprehensive test scenarios for Agentforce escalation testing based on **published agent versions** and live org metadata. It does NOT execute tests - it produces detailed test plans for manual execution.

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## Recent Updates

Read [`references/changelog.md`](references/changelog.md) for release notes and version history.

## Purpose

Generate exhaustive, org-specific test scenarios for validating:

**Agent Behavior (derived from agent file):**

- User-requested escalation paths
- Agent-initiated escalation (failure threshold)
- Pre-escalation context gathering
- Verification-gated escalation
- Cancel/abort paths
- Multi-turn conversation flows
- Safety validation (6 critical security probes)

**Routing Infrastructure (derived from org metadata):**

- Escalation routing logic (agents available) - supports multiple availability models
- Service Channel capacity validation (for channel-based routing)
- Queue presence validation (for simple queue-based routing)
- Custom Flow/Apex availability logic testing
- Fallback behavior (no agents available)
- Business hours boundary testing (opening/closing times, timezones)
- Edge cases (capacity overflow, concurrent requests, agent status changes)
- Status lifecycle tracking (MessagingSession transitions)

**Business Logic (user-described custom rules):**

- Customer tier/priority-based routing (VIP, Premium, Standard)
- Escalation history checks (repeat customers)
- SLA enforcement and timing requirements
- Compliance-based routing (HIPAA, PCI)
- Geographic/language preference routing
- Product/service-based specialist routing
- External system dependencies

**Integration Points:**

- Case creation on fallback
- Platform event publishing
- External callouts
- Transcript attachment
- Bot re-engagement after agent handoff

---

## Prerequisites

- Salesforce org (non-production) with Agentforce + Omni-Channel configured
- SF CLI installed and authenticated to target org
- User access to set agent presence states manually

### Required Permissions

This skill queries objects that are **not covered by Agentforce permission sets** (`AgentforceServiceAgentBuilder`, `AgentforceServiceAgentUser`, `AgentforceServiceAgentBase`). Those sets carry no explicit object permissions on Omni-Channel objects — access is profile-level only. On a customer org, request the following from the Salesforce admin before running:

| Object | Why needed | Minimum access required |
| --- | --- | --- |
| `BotDefinition` / `BotVersion` | Agent discovery | Agentforce Builder permission set or System Administrator |
| `QueueRoutingConfig` / `ServiceChannel` | Routing metadata | Service Cloud permission set or System Administrator |
| `UserServicePresence` / `AgentWork` | Capacity/availability data | Omni-Channel Supervisor permission set or System Administrator |
| `MessagingSession` | Session status tracking | Messaging User permission set or System Administrator |
| `FlowDefinitionView` / `ApexClass` | Availability logic detection | View Setup and Configuration or System Administrator |
| `Group` / `BusinessHours` | Queue and business hours config | Read-only System Administrator or View Setup |

> If you receive permission errors during Phase 2, this is the likely cause — not a configuration problem.

---

<quote>
⚠️ **DATA NOTICE**

This skill queries org metadata (queues, routing configs, agent structure) via SF CLI. Results are processed by the current ChatGPT or Codex session.

Before running on a customer org, ensure you have:

- Customer consent for their org config to be processed by the current host
- Compliance approval per your engagement's data handling policy
</quote>

---

## Skill Execution Flow

### Phase 0: Pre-Flight Environment Validation

Consult [`references/phase-0-preflight.md`](references/phase-0-preflight.md) before Phase 0.

### Phase 1: Validate Org and Select Agent

Consult [`references/phase-1-validate-org-and-agent.md`](references/phase-1-validate-org-and-agent.md) before Phase 1.

### Phase 2: Fetch Org Routing Metadata

Consult [`references/phase-2-metadata-and-requirements.md`](references/phase-2-metadata-and-requirements.md) before Phase 2. Covers: Phase 2b: Gather Requirements; Phase 2 Summary: Metadata Completeness Check; Phase 2c: Testing Setup Questions.

### Phase 3: Parse Agent File & Generate Test Scenarios

**📄 Load Modules:**

- `modules/TEST_TEMPLATES.md` — All test scenario templates
- `modules/SAFETY_PROBES.md` — Security testing scenarios

Test scenarios are generated from three sources:

1. **Agent file structure** — escalation subagents, connection blocks, gating variables (agent-derived)
2. **Org routing metadata** — queues, service channels, business hours, flows (infrastructure validation)
3. **User-described business logic** — custom rules, SLA requirements, compliance needs (business validation)

Scenarios are organized into flexible categories. Only generate scenarios for categories that apply to this agent and org configuration.

---

## Step 1: Extract Escalation Elements from Agent File

Consult [`references/phase-3-steps-1-7-test-cases.md`](references/phase-3-steps-1-7-test-cases.md) before Phase 3 Step 1. Covers: Step 2: Gather Persona Information for Stress Testing; Step 3: Generate Agent Behavior Test Cases (Derived from Agent File); Step 4: Generate Safety Validation Test Cases; Step 5: Generate Routing Infrastructure Test Cases (Based on Org Metadata); Step 6: Generate Business Logic Test Cases (User-Described Custom Rules); Step 7: Utterance Customization (Optional).

## Step 8: Present Complete Test Plan to User

Consult [`references/step-8-and-phase-4-documentation.md`](references/step-8-and-phase-4-documentation.md) before Step 8 and Phase 4.

## Module Loading Protocol

When entering each phase, explicitly load the relevant modules:

**Phase 2:**

```javascript
📄 Loading module: modules/SOQL_QUERIES.md
[Read the module file]
```

**Phase 2b:**

```javascript
📄 Loading module: modules/BUSINESS_LOGIC_EXAMPLES.md
[Read the module file]
```

**Phase 3:**

```javascript
📄 Loading modules:
  - modules/TEST_TEMPLATES.md
  - modules/SAFETY_PROBES.md
[Read the module files]
```

**Phase 4:**

```javascript
📄 Loading module:
  - modules/OUTPUT_FORMATS.md
  [- modules/EXECUTION_SUMMARY.md (only if user requested execution summary)]
[Read the module file(s)]
```

This ensures the skill has access to the detailed guidance only when needed, keeping the main context window lean.

---

## Version 4.0 Improvements

Read [`references/changelog.md`](references/changelog.md) for release notes and version history. Covers: Migration from v3.0.

## Support and Troubleshooting

**Common Issues:**

**"Module file not found"**

- Ensure you're running the latest version of the skill
- Modules are loaded from within the plugin package (relative path `modules/`)

**"Skill taking too long"**

- V4.0 loads modules on-demand, which may appear slower initially
- Overall execution time should be similar to v3.0
- Large orgs (many queues/business rules) will take longer regardless of version

**For all other issues:**

- Refer to the skill documentation
- Check Phase 2 permissions if queries fail
- Ensure SF CLI is properly authenticated
