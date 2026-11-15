# Graceful Degradation Guide

This module explains how the skill handles incomplete metadata and generates partial test plans.

---

## Philosophy: Never Block Unnecessarily

This skill uses a **tiered approach** to test generation. Only STOP if agent file is missing and the user did not choose metadata-only generation in Phase 1. Otherwise, WARN but PROCEED with whatever metadata is available.

**Stopping Criteria:**
- ❌ **STOP** if agent file is completely missing and the user did not choose metadata-only generation in Phase 1 (Step 7, Final Fallback)
- ⚠️ If the user chose metadata-only → ~60% coverage (routing and infrastructure only, no agent-specific scenarios)

**Warning but Proceed Criteria:**
- ⚠️ Missing Queue(s) → ~30% coverage (agent behavior + safety only)
- ⚠️ Missing ServiceChannel → ~70% coverage (skip capacity scenarios)
- ⚠️ Missing BusinessHours → ~85% coverage (skip business hours scenarios)
- ⚠️ Missing MessagingChannel/ESD → ~85-90% coverage (skip deployment guidance)

---

## Step 1: Show Metadata Completeness Matrix

Present findings in a visual matrix format showing what was found and what's missing.

### Example: 100% Complete

```
Metadata Completeness Check:

  ✅ Agent File: found (v3 active)
  ✅ Connection Blocks: 2 found
  ✅ Queue(s): 2 found
  ✅ Routing Flows: 1 found
  ✅ ServiceChannel: 2 found
  ✅ BusinessHours: 1 found
  ✅ MessagingChannel: 1 found
  ✅ EmbeddedServiceConfig: found
  ✅ Presence Statuses: 3 found
  ✅ Business Logic Rules: 2 captured

Estimated Test Coverage: 100% (~50 typical scenarios)
```

### Example: 70% Coverage (Missing ServiceChannel + Deployment Config)

```
Metadata Completeness Check:

  ✅ Agent File: found (v3 active)
  ✅ Connection Blocks: 2 found
  ✅ Queue(s): 2 found (Customer_Support_Queue, Premium_Support_Queue)
  ✅ Routing Flows: 1 found (Escalate_Messaging_To_Agent)
  ❌ ServiceChannel: not found
  ✅ BusinessHours: 1 found (North America Support Hours)
  ❌ MessagingChannel: not found
  ❌ EmbeddedServiceConfig: not found
  ✅ Presence Statuses: 3 found
  ⚠️ Business Logic Rules: none captured

Estimated Test Coverage: 70% (~35 of 50 typical scenarios)

Scenarios that WILL be generated:
  ✅ Agent Behavior (all) - utterance handling, context switching
  ✅ Basic Routing (R1-R4) - agents available, no agents, queue assignment
  ✅ Business Hours (R6-R8) - in-hours vs out-of-hours routing
  ✅ Safety Probes (S1-S6) - security testing
  ✅ Edge Cases (partial) - real-world gotchas

Scenarios that will NOT be generated:
  ❌ Capacity-Exceeded (R5) - requires ServiceChannel
  ❌ Deployment Guidance - requires MessagingChannel/EmbeddedServiceConfig
  ❌ Business Logic - no custom rules captured
```

### Example: 30% Coverage (Agent File Only, No Routing Config)

```
Metadata Completeness Check:

  ✅ Agent File: found (v2 active)
  ⚠️ Connection Blocks: none found (agent not configured for escalation)
  ❌ Queue(s): none referenced
  ❌ Routing Flows: none found
  ❌ ServiceChannel: not applicable
  ❌ BusinessHours: not applicable
  ❌ MessagingChannel: not found
  ❌ EmbeddedServiceConfig: not found
  ✅ Presence Statuses: 3 found
  ⚠️ Business Logic Rules: none captured

Estimated Test Coverage: 30% (~15 of 50 typical scenarios)

Scenarios that WILL be generated:
  ✅ Agent Behavior (partial) - utterance handling, context switching
  ✅ Safety Probes (S1-S6) - security testing

Scenarios that will NOT be generated:
  ❌ All Routing Infrastructure scenarios - no queues configured
  ❌ Capacity scenarios - no ServiceChannel
  ❌ Business Hours scenarios - no BusinessHours
  ❌ Deployment Guidance - no MessagingChannel/EmbeddedServiceConfig
  ❌ Business Logic - no custom rules captured

⚠️ WARNING: Agent has no connection blocks configured.
Recommendation: Configure escalation routing before proceeding.
```

---

## Step 2: Let User Decide

Ask the user how to proceed:

```
You can proceed with limited test coverage, or stop to configure missing metadata.

Options:
  1. Proceed with [X]% test plan (recommended if testing basic routing)
  2. Show details about what's missing and how to enable
  3. Stop - I want to configure missing metadata first

Your choice? (1/2/3 or yes/no/show-details)
```

### If user chooses "show-details" (or option 2):

Display detailed gap analysis using the format from Step 4 below.

### If user chooses "yes" or option 1:

Proceed to Phase 3 (scenario generation).

### If user chooses "no" or option 3:

```
Stopping test generation.

To complete metadata configuration:
  1. Configure missing ServiceChannel (for capacity testing)
  2. Deploy MessagingChannel + EmbeddedServiceConfig (for deployment guidance)
  3. Re-run this skill after configuration

Re-run command:
  /agentforce-escalation-test-generator
```

---

## Step 3: Generate What's Possible

When proceeding with incomplete metadata:
- Generate ALL scenarios that metadata supports
- Add placeholder sections for missing categories with "Why Skipped" notes
- Document gaps in final output (see Step 4 format)

---

## Step 4: Document Gaps in Generated Output

When test plan is generated with missing metadata, include a section in TEST_SCENARIOS.md:

### Template Format:

```markdown
## Scenarios NOT Generated (Missing Metadata)

This section documents test scenarios that could NOT be generated due to missing metadata configuration.

### [Category Name] Scenarios

**Scenario IDs:** [List IDs that would have been generated, e.g., R5, E3]

**Why Skipped:**
[Specific metadata that is missing, e.g., "No ServiceChannel found linking queues to capacity tracking"]

**To Enable:**
1. [Step 1 to configure missing metadata]
2. [Step 2 to configure missing metadata]
3. Re-run skill to regenerate scenarios

**Impact:**
[What cannot be tested without these scenarios, e.g., "Cannot test capacity overflow behavior or queue fallback when capacity exceeded"]

**Typical Scenarios in This Category:**
- [Description of scenario type 1]
- [Description of scenario type 2]
```

### Example: Missing Capacity Scenarios

```markdown
### Capacity-Exceeded Scenarios

**Scenario IDs:** R5, E3

**Why Skipped:**
No ServiceChannel found linking queues to capacity tracking. Without ServiceChannels, the system cannot distinguish between "no agents available" and "agents available but at capacity."

**To Enable:**
1. Create ServiceChannel record for your messaging deployment
2. Link ServiceChannel to QueueRoutingConfig via `RoutingConfigurationId` field
3. Verify link: `sf data query -q "SELECT Id, DeveloperName, RoutingConfigurationId FROM ServiceChannel WHERE RoutingConfigurationId = '<queue-routing-config-id>'" -o <alias>`
4. Re-run this skill to regenerate scenarios

**Impact:**
Cannot test capacity overflow behavior or queue fallback when all available agents are at capacity. This is a critical production scenario where agents are online but cannot accept additional work items.

**Typical Scenarios in This Category:**
- Agent at max capacity → new escalation waits in queue
- Multiple agents at capacity → escalation routes to fallback queue
- Capacity weight exceeded → work rejected until capacity frees up
```

### Example: Missing Deployment Guidance

```markdown
### Deployment Guidance

**Scenario IDs:** N/A (affects test execution, not specific scenarios)

**Why Skipped:**
No MessagingChannel or EmbeddedServiceConfig found in org. Cannot determine deployment surface (web chat URL, MIAW deployment, mobile app config).

**To Enable:**
1. Configure MessagingChannel for your deployment surface
2. Create EmbeddedServiceConfig linking to MessagingChannel
3. Deploy to Experience Cloud site (for web) or mobile app
4. Re-run this skill to include deployment URLs in test scenarios

**Impact:**
Test scenarios will not include deployment surface URLs. You must manually navigate to your chat/messaging interface to execute tests. This increases setup time and risk of testing wrong deployment.

**Workaround:**
Manually provide your deployment URL when executing scenarios. Example:
- Web: `https://yoursite.my.site.com/chat`
- MIAW: `https://yoursite.force.com/embeddedservice`
```

### Example: Missing Business Logic Scenarios

```markdown
### Business Logic Scenarios

**Scenario IDs:** BL1-BLn (varies based on org)

**Why Skipped:**
No custom business rules were captured during requirements gathering phase. Agent may have business logic implemented, but it was not documented for testing.

**To Enable:**
1. Document your org-specific routing logic (VIP customer handling, tier-based routing, time-based rules, etc.)
2. Re-run this skill and describe business rules when prompted in Phase 2b
3. OR provide business rule documentation for skill to parse

**Impact:**
Custom org-specific routing logic will not be tested. Business rules may fail in production without validation (e.g., VIP customers routed to wrong queue, tier-based routing broken, business hours exceptions not handled).

**Common Business Logic to Test:**
- VIP/priority customer routing
- Account tier-based queue assignment
- Case history-based routing decisions
- Time-sensitive routing rules
- Geographic/language-based routing
- Product/service-specific queues
```

---

## Coverage by Missing Metadata

Quick reference table showing expected coverage based on what's missing:

| Missing Metadata | Coverage | What's Available | What's Missing |
|------------------|----------|------------------|----------------|
| None | 100% | Everything | Nothing |
| EmbeddedServiceConfig only | 85-90% | All scenarios | Deployment URLs |
| ServiceChannel | 70% | Agent behavior, basic routing, safety | Capacity scenarios |
| BusinessHours | 85% | All except time-based | Business hours scenarios |
| Queue(s) | 30% | Agent behavior, safety | All routing |
| Agent file, metadata-only chosen in Phase 1 | ~60% | Routing, business hours, availability, session lifecycle | Agent-specific scenarios |
| Agent file, metadata-only not chosen | 0% | STOP | Everything |

---

## Decision Tree for Users

```
Is agent file present?
├─ NO, metadata-only chosen in Phase 1 → WARN (~60% coverage, no agent-specific scenarios), continue
├─ NO, otherwise → STOP (0% coverage, nothing to test)
└─ YES → Continue

Are connection blocks configured?
├─ NO → WARN (30% coverage, routing unavailable)
│   └─ Offer: Agent behavior + safety only
└─ YES → Continue

Are queues/flows found?
├─ NO → WARN (30% coverage, routing targets missing)
│   └─ Offer: Agent behavior + safety only
└─ YES → Continue

Is ServiceChannel configured?
├─ NO → WARN (70% coverage, capacity testing unavailable)
│   └─ Offer: Basic routing + behavior + safety
└─ YES → Continue

Is BusinessHours configured?
├─ NO → WARN (85% coverage, time-based testing unavailable)
│   └─ Offer: All except business hours scenarios
└─ YES → Continue

Is MessagingChannel/ESD configured?
├─ NO → WARN (85-90% coverage, deployment URLs missing)
│   └─ Offer: All scenarios, manual navigation required
└─ YES → 100% coverage, proceed
```
