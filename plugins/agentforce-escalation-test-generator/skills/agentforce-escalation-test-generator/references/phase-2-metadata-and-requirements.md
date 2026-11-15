# Phase 2: Fetch Org Routing Metadata

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Phase 2: Fetch Org Routing Metadata
- Phase 2b: Gather Requirements
- Phase 2 Summary: Metadata Completeness Check
  - Present Metadata Completeness Matrix
  - Let User Decide
  - Document Gaps
- Phase 2c: Testing Setup Questions

### Phase 2: Fetch Org Routing Metadata

**📄 Load Module: `modules/SOQL_QUERIES.md`**

Before executing this phase, read the SOQL_QUERIES.md module to get all query definitions.

**🎯 IMPORTANT: Agent-Centric Querying Approach**

Start from the agent file and work outward. Only query metadata that is directly referenced by the agent's escalation configuration. Do NOT query all flows/Apex/metadata that COULD be related just because it has routing-related names.

**Querying Strategy:**

1. **Parse agent file FIRST** — Extract all connection blocks and their routing targets
2. **Query only what's referenced** — Fetch queues, flows, and Apex classes that the agent actually uses
3. **Broaden only if needed** — If connection blocks are missing or incomplete, then query broader metadata

Run all queries against the confirmed org. Surface results as readable summary tables — do not dump raw JSON.

**Execute queries in the following order:**

**Step 1: Parse agent file for connection blocks (DO THIS FIRST)**
- Extract all `connection` blocks from the agent file
- Identify routing targets: Queue names, Flow API names, Apex class references
- List what the agent actually references

**Step 2: Query ONLY referenced routing targets**
- **For Queue targets:** Query specific queues by DeveloperName
- **For OmniChannelFlow targets:** Query specific flows by ApiName
- **For custom Apex:** Query specific Apex classes referenced in agent file

**Step 3: Query associated metadata for found targets**
- For each queue found: Query its QueueRoutingConfig
- For each queue found: Query its ServiceChannel (if exists)
- For each queue found: Query its BusinessHours (if associated)

**Step 4: Query presence statuses and intents**
- Fetch presence statuses (generic, applies to all orgs)
- Fetch bot intents and utterances (for the selected agent only)

**Step 5: Service channel link detection**
- For each queue found in Step 2, determine if channel-linked or no-channel

**Step 6: Present metadata findings as a tree (from agent outward)**

Present metadata as a **tree structure** showing the chain from agent → connection blocks → routing targets → associated metadata.

**Tree Format Example:**

```
Agent: Robbie_Escalation_Agent (v3 Active)
│
├─ Connection: customer_web_client
│  ├─ Route Type: OmniChannelFlow
│  ├─ Route Target: Testing_Escalation_Queue ✅ (found, active)
│  │
│  └─ Flow: Testing_Escalation_Queue
│     ├─ Availability Check: Are_Agents_Available?
│     ├─ If Available → Routes to Queue: Test Admins ✅
│     │  │
│     │  ├─ Queue: Test Admins (00Gak00000SzrYkEAJ)
│     │  │  ├─ Routing Config: Test_Admins_RoutingConfig
│     │  │  │  ├─ Model: MostAvailable
│     │  │  │  └─ Capacity Weight: 5 ⚠️  (suggest lowering to 1 for testing)
│     │  │  │
│     │  │  └─ ServiceChannel: sfdc_livemessage ✅ (channel-linked)
│     │  │     ├─ Related Entity: MessagingSession
│     │  │     └─ Valid Presence Statuses:
│     │  │        • All - Available (All_Available)
│     │  │        • Messaging - Available (Available_LiveMessage)
│     │  │
│     │  └─ BusinessHours: ❌ (not configured for this queue)
│     │
│     └─ If NOT Available → Fallback Message: varFallbackMessage
│
├─ Pre-Escalation: check_availability subagent
│  ├─ apex://CheckBusinessHours ✅ (found, retrieved)
│  │  └─ Queries BusinessHours: "North America" ✅
│  │     ├─ Timezone: America/Los_Angeles (PT)
│  │     └─ Hours: Mon 8am-7pm, Tue-Thu 7am-7pm, Fri 7am-5pm
│  │
│  └─ apex://CheckAgentAvailability ✅ (found, retrieved)
│     └─ Logic: Checks Test Admins queue capacity
│
└─ Deployment Surface:
   ├─ MessagingChannel: Messaging_for_In_App_Web ✅
   │  ├─ Type: EmbeddedMessaging
   │  ├─ SessionHandlerType: Flow
   │  ├─ SessionHandlerFlow: Inbound_Routing_Flow
   │  └─ SessionHandlerQueue: SDO_Service_Messaging (fallback)
   │
   └─ EmbeddedServiceConfig: Claude_Escalation_Testing ✅
      ├─ DeploymentType: Web (MIAW)
      ├─ Site: ESW_Claude_Escalation_Test_17770532230421
      └─ URL: https://example.my.site.com/support
```

**Tree Structure Rules:**
- Start with Agent at the root
- Show connection blocks as first-level children
- For each connection, show the routing chain (flow → queue → ServiceChannel)
- Branch out to show associated metadata (BusinessHours, Apex, deployment)
- Use ✅ for found/valid, ❌ for not found, ⚠️ for warnings
- Indent consistently to show parent-child relationships

**After presenting tree, ask:**
```
Metadata chain traced from agent outward.

Key findings:
• Routing configured: ✅ Complete (queue + ServiceChannel + flow)
• BusinessHours: ❌ Not configured (skip business hours scenarios)
• Deployment surface: ✅ Found (can test end-to-end)
• Availability model: Channel-linked (capacity scenarios will be generated)

Proceed to generate test scenarios? (yes/no)
```

> 📦 **SOQL_QUERIES.md — done.** Its query templates and examples guided metadata retrieval above. Only the results (queue names, IDs, routing targets, business hours values) need to be carried forward — not the module's instructional content.

---

### Phase 2b: Gather Requirements

**📄 Load Module: `modules/BUSINESS_LOGIC_EXAMPLES.md`**

After metadata confirmation, ask the user additional questions to customize test scenario generation.

**1. Acceptance criteria for routing scenarios:**
- When agents available → expected behavior?
- When no agents → fallback behavior?
- Session status transitions expected?

**2. Business hours configuration (if BusinessHours found):**

Follow the guided interview process from BUSINESS_LOGIC_EXAMPLES.md:
- Does routing use business hours?
- Which configuration(s) to test?
- What timezone are you testing from?
- Do different queues use different hours?
- Test boundary conditions?
- Holiday/exception handling?

**3. Custom business logic and organization-specific processes:**

Use the workflow from BUSINESS_LOGIC_EXAMPLES.md:
- **Step 1:** Parse agent file for business logic indicators
- **Step 2:** Summarize findings to user
- **Step 3:** Conduct guided interview if needed (for each business rule)
- **Step 4:** Ask about cross-cutting concerns
- **Step 5:** Confirm all business rules before proceeding

For each business rule, capture:
- Business rule name
- Business requirement (WHY)
- Trigger conditions
- Expected behavior
- Where implemented
- Operational/capacity considerations
- Business edge cases
- Success criteria

**4. Other edge cases to include:**
- Skills-based routing? (if skills configured)
- Capacity overflow? (if capacity limits defined)
- Multiple channels? (if multiple ServiceChannels exist)

> 📦 **BUSINESS_LOGIC_EXAMPLES.md — done.** Its interview workflow and example rules (VIP, SLA, HIPAA, etc.) guided requirements gathering above. Only the confirmed business rules the user validated need to be carried forward — not the module's examples or process steps.

---

### Phase 2 Summary: Metadata Completeness Check

**📄 Load Module: `modules/GRACEFUL_DEGRADATION.md`**

**Tiered approach** — Only STOP if the agent file is missing and the user did not choose metadata-only generation in Phase 1 (Step 7, Final Fallback). If they chose it, skip agent-specific scenarios and proceed with routing and infrastructure scenarios (~60%). Otherwise WARN but PROCEED.

**Coverage tiers:**
- Missing Queue(s) → ~30% | Missing ServiceChannel → ~70%
- Missing BusinessHours → ~85% | Missing MessagingChannel/ESD → ~85-90%

#### Present Metadata Completeness Matrix

Show what was found and estimated coverage:

```
Metadata Completeness Check:
  ✅ Agent File: found (v<N> active)   [or ⚠️ not retrieved — metadata-only, confirmed in Phase 1]
  ✅ Connection Blocks: <N> found
  ✅ Queue(s): <N> found
  [✅/❌] ServiceChannel / BusinessHours / MessagingChannel / ESD
  ✅ Presence Statuses: <N> found

Estimated Test Coverage: [X]% (~[N] of 50 scenarios)

Scenarios that WILL be generated: [list]
Scenarios that will NOT be generated: [list with reasons]
```

**See GRACEFUL_DEGRADATION.md for complete examples at 100%, 70%, 30% coverage.**

#### Let User Decide

```
Options:
  1. Proceed with [X]% test plan
  2. Show details about what's missing
  3. Stop - configure metadata first
```

- **Option 1/yes** → Proceed to Phase 3
- **Option 2/show-details** → Display detailed gap analysis from module
- **Option 3/no** → Stop with re-run instructions

#### Document Gaps

Include "Scenarios NOT Generated" section in TEST_SCENARIOS.md with "Why Skipped", "To Enable", "Impact" notes. **Format details in GRACEFUL_DEGRADATION.md Step 4.**

---

### Phase 2c: Testing Setup Questions

**IMPORTANT: Ask these questions BEFORE generating scenarios to tailor test plan to available resources.**

**Question 1: How many human agent users are available for testing?**

```
How many human agent users do you have available for testing escalations?

Options:
  1. One agent user (me)
  2. Two agent users
  3. Three or more agent users

Enter number:
```

**Question 2: Can you run multiple simultaneous browser sessions?**

```
Can you open multiple browser sessions simultaneously? (e.g., incognito tabs, different browsers)

This is needed for scenarios like:
- Capacity-exceeded testing (multiple customers at once)
- Race condition scenarios (TOCTOU)
- Concurrent escalation testing

Options:
  yes - I can open multiple browser sessions
  no - I can only test with one session at a time

Enter choice:
```

**Use responses to tailor scenarios:**

If user has **1 agent** and **1 browser session:**
- Flag capacity-exceeded scenarios: "⚠️ Requires multiple sessions or temporarily lowering capacity weight to 1"
- Flag race condition scenarios: "⚠️ Requires multiple simultaneous sessions"
- Flag concurrent scenarios: "⚠️ Requires coordinated timing with multiple testers"

If user has **1 agent** and **multiple sessions:**
- Capacity scenarios: Possible with config change (lower capacity weight)
- Race conditions: Possible (open multiple customer sessions)

If user has **2+ agents**:
- All scenarios testable without config changes

**Store these responses for scenario preconditions.**

> 📦 **GRACEFUL_DEGRADATION.md — done.** Its coverage tiers and example matrices guided the completeness decision above. Only the coverage decision itself (e.g., "proceeding at 85%, skipping R5 and BH2-BH5") needs to be carried forward — not the module's tier definitions or example matrices.

---
