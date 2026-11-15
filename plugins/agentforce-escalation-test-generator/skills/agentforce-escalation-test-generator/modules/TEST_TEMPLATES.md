# Test Scenario Templates

This module contains all test scenario templates for Phase 3 scenario generation.

Test scenarios are generated from three sources:
1. **Agent file structure** — escalation subagents, connection blocks, gating variables (agent-derived)
2. **Org routing metadata** — queues, service channels, business hours, flows (infrastructure validation)
3. **User-described business logic** — custom rules, SLA requirements, compliance needs (business validation)

Scenarios are organized into flexible categories. Only generate scenarios for categories that apply to this agent and org configuration.

---

## Category 1: Agent Behavior - Escalation Paths

Generate one test case per escalation path found in the agent file.

### Test Case Template: Escalation Path

```
Scenario [N]: Agent Behavior - [Path Name from subagent/action description]

**Category:** Agent Behavior - Escalation Path
**Source:** Derived from agent file escalation subagent '<subagent-name>'

**Preconditions:**
- Agent version <version> deployed
- [List any gating variables that must be set, e.g., "ready_to_escalate = True"]
- [If multi-turn: list conversation history requirements]

**Test Utterances:**
- [Placeholder - utterances will be customized in Step 7 after all scenarios are generated]
- Primary utterance will be synthesized from agent file action/subagent description
- Persona variations available if personas defined in Step 2
- User can provide custom utterances via file in Step 7

**Expected Path:**
- Agent should route to subagent: <escalation-subagent-name>
- [If pre-escalation exists: Agent should first route to <pre-escalation-subagent-name>, then <escalation-subagent-name>]

**Expected Actions:**
- <Level 2 invocation name from reasoning: actions:>
- [e.g., "transfer_to_human", "escalate_to_support"]

**Expected Outcome:**
- Agent response should match: "[from connection block escalation_message or subagent instructions]"
- Agent should indicate transfer is occurring
- Session should prepare for handoff

**Routing Basis:**
- Connection block: <channel> → <route_type>: <route_target>
- Confirmed in org: [✅ exists / ⚠️ mismatch - see Phase 2]

**Multi-turn:** [yes/no]
[If yes, include conversation history turns required to trigger gating variables]

**Verification:**
- Check agent response contains expected outcome text
- Check agent invoked expected action
- Check agent routed to expected subagent topic
```

### Generate Test Cases For:
1. User-requested escalation (from each user-requested trigger found)
2. Agent-initiated escalation (if agent-initiated trigger found with attempt threshold)
3. Verification-failure escalation (if verification-gated path found)
4. Pre-escalation context gathering (if pre-escalation subagent exists)
5. Cancel/abort path (if cancel action found)
6. Per-channel escalation (one test case per connection block found)
7. Context-switching escalation scenarios (see Category 2)

---

## Category 2: Agent Behavior - Context-Switching Scenarios

If context-switching scenarios were found in agent file analysis, generate test cases for each.

### Template: Knowledge Article-Triggered Escalation

```
Category: Agent Behavior - Context-Switching
Objective: Validate escalation triggered by knowledge article interaction

Preconditions:
- Agent has action to show knowledge article
- Escalation triggered after specific article is shown or dismissed

Conversation Flow:
1. User asks question that triggers knowledge article
2. Agent shows knowledge article [Article Name]
3. User responds with: "[dismissal phrase or follow-up question]"
4. Agent transitions to escalation subagent
5. Escalation fires

Test Utterances:
- Turn 1: "[Question that triggers article]" (from agent file or typical article trigger)
- Turn 2: "[Dismissal phrase]" (e.g., "That doesn't help", "I need more than this")

Expected Path:
- Agent shows article
- Agent detects article didn't resolve issue
- Agent routes to escalation subagent
- Escalation fires with context about article attempt

What This Tests:
- Service desk switch after knowledge attempt
- Context preservation (agent knows article was tried)
- Appropriate escalation routing based on article topic

Verification:
- Check agent showed article before escalating
- Check escalation message mentions article attempt
- Check context variable includes article ID or name
```

### Template: Data Retrieval-Triggered Escalation

```
Category: Agent Behavior - Context-Switching
Objective: Validate escalation triggered by data retrieval result

Preconditions:
- Agent retrieves data (order status, account info, case details)
- Escalation triggered based on retrieved data value

Conversation Flow:
1. User asks about their order/account/case
2. Agent invokes data retrieval action
3. Data shows triggering condition (e.g., order status = "delayed")
4. Agent transitions to escalation subagent with context
5. Escalation fires to appropriate specialist queue

Example:
- Turn 1: "Where is my order?"
- Agent retrieves order data
- Order status = "delayed" → triggers escalation to fulfillment team
- Agent: "I see your order is delayed. Let me connect you with our fulfillment specialist."

What This Tests:
- Service desk switch based on data condition
- Context preservation (order ID, status passed to human agent)
- Appropriate specialist queue selection

Verification:
- Check data retrieval action invoked
- Check escalation triggered by data condition
- Check context includes retrieved data
- Check routes to correct specialist queue
```

### Template: Multi-Turn Context Accumulation

```
Category: Agent Behavior - Context-Switching
Objective: Validate escalation after multiple conversation turns

Preconditions:
- Escalation requires context from multiple turns
- Agent accumulates information before escalating

Conversation Flow:
1. Turn 1: User describes issue
2. Turn 2: Agent asks clarifying question
3. Turn 3: User provides additional detail
4. Turn 4: Agent determines escalation needed based on accumulated context
5. Escalation fires with full conversation context

Example:
- Turn 1: "I have a problem with my account"
- Turn 2: Agent: "What type of account issue?"
- Turn 3: User: "I can't access it, and it involves financial data"
- Turn 4: Agent detects "financial data" → escalates to secure support team

What This Tests:
- Context accumulation across multiple turns
- Escalation decision based on conversation history
- Full context passed to human agent

Verification:
- Check escalation happens after required turns
- Check context includes conversation history
- Check routing based on accumulated context
```

---

## Category 3: Routing Infrastructure - Core Scenarios

Always include these core routing validation scenarios.

### Scenario R1: Agents Available → Successful Routing

```
Category: Routing Infrastructure - Core
Objective: Validate successful routing when agents are available

Preconditions:
- ≥1 agent set to "Available" in Omni-Channel
- Agent is member of target queue: <queue-name from connection block>
- [If channel-linked: Agent has available capacity on ServiceChannel <channel-name>]

Test Steps:
1. Set agent presence to "Available" via Omni-Channel widget
2. Verify agent capacity: Run queries/check-agent-presence.soql
3. Trigger escalation using utterance: [use primary utterance from agent behavior TC]
4. Observe Omni-Channel widget for incoming work

Expected Outcome:
- Work item (AgentWork) created
- AgentWork.Status = "Opened" (waiting for agent acceptance)
- AgentWork.OriginalQueue.Name = "<queue-name>"
- MessagingSession.Status = "Waiting"
- Agent can accept work and session becomes "Active"

Verification:
- Run: queries/verify-routing.soql — Check AgentWork created
- Run: queries/check-session-status.soql — Check MessagingSession status
- Compare results to expected outcome
- Record pass/fail in test log

Pass Criteria:
✅ PASS if: AgentWork created AND OriginalQueue correct AND agent can accept
❌ FAIL if: No AgentWork created OR wrong queue OR agent cannot accept

Troubleshooting:
- If no AgentWork: Check connection block target exists (Phase 2 cross-validation)
- If wrong queue: Review routing flow logic or queue assignment rules
- If agent can't accept: Check queue membership and service channel configuration
```

### Scenario R2: No Agents Available → Fallback Behavior

```
Category: Routing Infrastructure - Core
Objective: Validate fallback behavior when no agents are available

Preconditions:
- All agents in target queue set to "Busy" or "Offline"
- No agents available to accept work

Test Steps:
1. Set all agents to "Busy" or "Offline" via Omni-Channel widget
2. Verify no agents available: Run queries/check-agent-presence.soql
3. Trigger escalation using utterance: [use primary utterance from agent behavior TC]
4. Observe conversation transcript for fallback message

Expected Outcome (based on acceptance criteria from Phase 2b):
- [If message only: Agent sends fallback message, MessagingSession.Status = "Ended"]
- [If Case creation: Case record created, linked to MessagingSession]
- [If external callout: Platform event published or external system called]
- NO unintended actions (verify no Case if not expected, etc.)

Verification Queries:
- queries/check-session-status.soql — Verify session ended
- [If Case expected: queries/verify-case-created.soql]
- [If NO Case expected: queries/verify-no-cases.soql — Critical: confirm Case count = 0]

Pass Criteria:
✅ PASS if: Fallback behavior matches acceptance criteria AND no unintended side effects
❌ FAIL if: Unexpected behavior OR unintended actions occurred

Troubleshooting:
- If routing attempted despite no agents: Check availability check logic (Flow/Apex)
- If no fallback triggered: Review connection block fallback configuration
- If unintended Case created: Check automation rules, Process Builder, flows
```

### Scenario R3: MessagingSession Status Lifecycle

```
Category: Routing Infrastructure - Core
Objective: Validate session status transitions throughout escalation lifecycle

Preconditions:
- 1 agent available in target queue

Test Steps:
1. Trigger escalation: [use primary utterance]
2. Check initial status: Run queries/check-session-status.soql → expect "New" or "Waiting"
3. Agent accepts work via Omni-Channel widget
4. Check active status: Run queries/check-session-status.soql → expect "Active"
5. Agent ends conversation
6. Check ended status: Run queries/check-session-status.soql → expect "Ended"

Expected Outcome:
- Status transitions: New → Waiting → Active → Ended
- Each transition occurs within expected timeframe
- No stuck sessions in intermediate states

Verification Queries:
- queries/check-session-status.soql (run at each stage)

Pass Criteria:
✅ PASS if: All status transitions occur correctly in sequence
❌ FAIL if: Session stuck in any intermediate state OR skips a status

Troubleshooting:
- If stuck in "Waiting": Check if agent can see work in widget
- If never reaches "Active": Check agent acceptance flow
- If doesn't end: Check agent end-conversation configuration
```

---

## Category 4: Routing Infrastructure - Availability Model Scenarios

Generate scenarios based on the automatically detected availability model from Phase 2. Only generate scenarios for queues that match each model.

### For Channel-Linked Queues:

#### Scenario R4: Service Channel Capacity - Agent Available with Capacity

```
Category: Routing Infrastructure - Availability Model
Queue: <channel-linked-queue-name>
Service Channel: <service-channel-name> (<RelatedEntity>)

Objective: Validate routing when agent has available capacity on ServiceChannel

Preconditions:
- Agent has UserServicePresence.ConfiguredCapacity > current work count
- Agent is "Available"
- Agent is member of queue

Test Steps:
1. Query agent capacity: Run queries/check-channel-capacity.soql
2. Verify: ConfiguredCapacity > (number of active AgentWork records)
3. Trigger escalation: [use primary utterance]

Expected Outcome:
- Routes successfully
- AgentWork created for this agent

Verification:
- queries/check-channel-capacity.soql — before and after
- queries/verify-routing.soql

Pass Criteria:
✅ PASS if: Agent with capacity receives work
❌ FAIL if: Agent not routed despite having capacity
```

#### Scenario R5: Service Channel Capacity - All Agents at Capacity

```
Category: Routing Infrastructure - Availability Model
Queue: <channel-linked-queue-name>
Service Channel: <service-channel-name>

Objective: Validate behavior when all agents are at max capacity

Preconditions:
- All agents online and "Available"
- All agents at ConfiguredCapacity (no remaining capacity on ServiceChannel)

⚠️  **CAPACITY WEIGHT CONSIDERATION:**
If the queue's CapacityWeight is high (e.g., 5), it may be impractical to fill capacity during testing.

**Recommended Setup for High Capacity Weight:**
1. Temporarily lower the CapacityWeight to 1 in Setup:
   - Navigate to: Setup → Omni-Channel → Routing Configurations
   - Edit: <QueueRoutingConfig-name>
   - Set CapacityWeight: 1 (instead of 5)
   - Save
2. Run this test scenario with CapacityWeight = 1 (easier to fill capacity)
3. After testing, restore original CapacityWeight: 5

**Current Config:**
- CapacityWeight: <actual-value>
- Recommendation: [Lower to 1 for testing if value > 2]

Test Steps:
1. [If CapacityWeight > 2: Temporarily lower to 1 per above instructions]
2. Query all agents: Run queries/check-channel-capacity.soql
3. Verify all agents: CurrentLoad >= ConfiguredCapacity
4. Trigger escalation: [use primary utterance]

Expected Outcome:
- May queue (AgentWork.Status = "Waiting") OR trigger fallback (depends on routing config)
- Should NOT drop session silently

Verification:
- queries/verify-routing.soql — Check if AgentWork created
- queries/check-session-status.soql — Check session not dropped

Pass Criteria:
✅ PASS if: Session queues OR fallback triggers (as expected)
❌ FAIL if: Session dropped OR unexpected behavior

**Cleanup:**
- Restore CapacityWeight to original value: <actual-value>
```

### For No-Channel Queues:

#### Scenario R6: Queue Presence Only - Agent Available

```
Category: Routing Infrastructure - Availability Model
Queue: <no-channel-queue-name>

Objective: Validate routing based on queue presence only (no capacity check)

Preconditions:
- Agent status = "Available"
- Agent is member of queue
- No ServiceChannel linked to queue

Test Steps:
1. Verify presence: Run queries/check-queue-membership.soql
2. Trigger escalation: [use primary utterance]

Expected Outcome:
- Routes based on presence status alone (no capacity validation)
- AgentWork created

Verification:
- queries/verify-presence-status.soql
- queries/verify-routing.soql

Pass Criteria:
✅ PASS if: Presence = Available → routes successfully
❌ FAIL if: Routing fails despite Available status
```

---

## Category 5: Routing Infrastructure - Business Hours Scenarios

Generate scenarios based on business hours configuration detected in Phase 2.

### Scenario BH1: Well Within Business Hours

```
Category: Routing Infrastructure - Business Hours
Objective: Validate routing during normal business hours

Preconditions:
- Current time is well within business hours (e.g., 11:00am if hours are 9am-5pm)
- <Queue Name> uses <Business Hours Name>
- Agent available

Test Steps:
1. Verify current time: Run queries/check-business-hours-config.soql
2. Confirm time is within hours
3. Trigger escalation

Expected Outcome:
- Routes successfully (business hours check passes)

Verification:
- queries/verify-current-time-in-hours.soql
- queries/verify-routing.soql

Pass Criteria:
✅ PASS if: Routes successfully during business hours
❌ FAIL if: Routing blocked despite being within hours
```

### Scenario BH2: Opening Time Boundary

```
Category: Routing Infrastructure - Business Hours
Objective: Validate behavior at opening time boundary

Preconditions:
- Test scheduled for business hours opening time (e.g., exactly 9:00:00am)
- <Queue Name> uses <Business Hours Name> (timezone: <timezone>)
- Agent available

Test Steps:
1. Schedule test execution for opening time
2. Trigger escalation at exactly opening time
3. Also test edge case: 8:59:59am (just before opening)

Expected Outcome:
- At 9:00:00am: Routes successfully
- At 8:59:59am: Fallback behavior (outside hours)

Verification:
- queries/verify-current-time-in-hours.soql
- Compare HOUR_IN_DAY(CreatedDate) to business hours schedule

Pass Criteria:
✅ PASS if: Boundary time handled correctly (9:00:00 = in, 8:59:59 = out)
❌ FAIL if: Incorrect boundary behavior
```

### Scenario BH3: Closing Time Boundary

```
Category: Routing Infrastructure - Business Hours
Objective: Validate behavior at closing time boundary

Preconditions:
- Test scheduled for business hours closing time (e.g., exactly 5:00:00pm)
- <Queue Name> uses <Business Hours Name>
- Agent available

Test Steps:
1. Schedule test execution for closing time
2. Trigger escalation at exactly closing time
3. Also test edge case: 5:00:01pm (just after closing)

Expected Outcome:
- At 4:59:59pm: Routes successfully
- At 5:00:00pm or later: Fallback behavior (outside hours)

Verification:
- queries/verify-current-time-in-hours.soql

Pass Criteria:
✅ PASS if: Closing boundary handled correctly
❌ FAIL if: Routes after hours OR blocks before closing
```

### Scenario BH4: Outside Business Hours

```
Category: Routing Infrastructure - Business Hours
Objective: Validate fallback behavior outside business hours

Preconditions:
- Test scheduled outside business hours (e.g., 8:00pm if hours are 9am-5pm)
- <Queue Name> uses <Business Hours Name>

Test Steps:
1. Verify current time is outside hours
2. Trigger escalation

Expected Outcome:
- Fallback behavior (based on Phase 2b acceptance criteria)
- No routing attempted

Verification:
- queries/verify-current-time-in-hours.soql (should show false)
- queries/verify-no-routing.soql

Pass Criteria:
✅ PASS if: Fallback triggered, no routing attempted
❌ FAIL if: Routes outside business hours OR no fallback
```

### Scenario BH5: Timezone Cross-Boundary Testing

```
Category: Routing Infrastructure - Business Hours
Objective: Validate timezone handling when tester and queue are in different timezones

Preconditions:
- Tester timezone: <tester-timezone>
- Queue timezone: <queue-timezone>
- Test time: <time in tester timezone> = <time in queue timezone>

Test Steps:
1. Verify timezone conversion is correct
2. Trigger escalation at time that is within queue hours but may be outside tester's local hours

Example:
- Queue: America/New_York (EST) — hours: 9am-5pm EST
- Tester: America/Los_Angeles (PST) — 3 hours behind
- Test at 6:00am PST = 9:00am EST (should route)

Expected Outcome:
- Routing decision based on QUEUE timezone, not tester timezone

Verification:
- queries/check-business-hours-config.soql (shows queue timezone)
- queries/verify-routing.soql

Pass Criteria:
✅ PASS if: Routes correctly based on queue's timezone
❌ FAIL if: Uses wrong timezone for decision
```

---

## Category 6: Edge Cases - Full Escalation Stack

Generate comprehensive edge case scenarios that test the full stack.

### Subcategory: Pre-Escalation Edge Cases (Agent Behavior)

These test agent behavior edge cases before routing infrastructure.

#### Edge Case 1: Rapid Repeated Escalation Requests

```
Category: Edge Cases - Agent Behavior
Objective: Validate agent handling of rapid repeated escalation requests

Test Steps:
1. Trigger escalation: "I need to talk to someone"
2. Immediately (within 5 seconds) send: "Transfer me now"
3. Again: "Connect me to an agent"

Expected Outcome:
- Agent should not create multiple escalation attempts
- Agent should acknowledge first request and proceed with single escalation
- No duplicate AgentWork or MessagingSession records

Verification:
- queries/verify-routing.soql (count should be 1, not 3)
- Check conversation transcript for appropriate handling

Pass Criteria:
✅ PASS if: Single escalation created despite multiple requests
❌ FAIL if: Multiple escalation attempts OR agent confused
```

#### Edge Case 2: Mid-Conversation State Change

```
Category: Edge Cases - Agent Behavior
Objective: Validate agent handling when escalation conditions change mid-conversation

Test Steps:
1. Start conversation (do NOT trigger escalation)
2. Mid-conversation, have admin manually update a triggering field (e.g., Account.VIP_Status__c = true)
3. Continue conversation and trigger escalation

Expected Outcome:
- Agent recognizes updated state
- Routes based on current state, not initial state

Verification:
- queries/verify-routing.soql (check queue assignment matches current state)

Pass Criteria:
✅ PASS if: Routes based on current state
❌ FAIL if: Uses stale state from conversation start
```

### Subcategory: Post-Escalation Edge Cases (Routing Infrastructure)

These test routing infrastructure gotchas after agent fires escalation.

#### Edge Case 3: Agent Goes Offline Mid-Routing

```
Category: Edge Cases - Routing Infrastructure
Objective: Validate system behavior when agent goes offline during routing

Test Steps:
1. Set 1 agent to "Available"
2. Trigger escalation
3. Immediately set agent to "Offline" (before accepting work)

Expected Outcome:
- System should re-route to another available agent OR trigger fallback
- AgentWork should not remain stuck in "Opened" state indefinitely

Verification:
- queries/verify-routing.soql (check AgentWork status after 30 seconds)
- queries/check-session-status.soql

Pass Criteria:
✅ PASS if: Re-routes OR fallback triggers within reasonable time
❌ FAIL if: Work stuck indefinitely OR session dropped
```

---

## Category 7: Business Logic Scenarios (User-Described)

Generate scenarios for each custom business rule described by the user in Phase 2b. Reference BUSINESS_LOGIC_EXAMPLES.md for requirements gathering guidance.

### Example Scenario Template:

```
Scenario BL[N]: Business Logic - [Business Rule Name]

**Business Requirement:** [Why this rule exists — the business need]

**Preconditions:**
- [Set up business conditions, e.g., "Customer Account has VIP_Status__c = true"]
- [Agent/queue configuration, e.g., "VIP queue has 2 agents available"]

**Test Steps:**
1. [Set up test data]
2. [Trigger escalation]
3. [Observe routing behavior]

**Expected Business Outcome:**
- [Business result, e.g., "Routes to VIP Support Queue (not standard queue)"]
- [Timing requirement, e.g., "Agent accepts within 30 seconds"]

**Verification:**
- queries/[custom-business-logic-query].soql
- [Specific business outcome checks]

**Business Edge Case 1:** [What if condition X?]
**Business Edge Case 2:** [What if condition Y?]

**Technical Implementation Note:**
[Where implemented: Flow, Apex, agent file, etc.]

**Pass Criteria:**
✅ PASS if: [Business outcome achieved]
❌ FAIL if: [Business outcome not achieved]
```

Refer to BUSINESS_LOGIC_EXAMPLES.md for detailed examples of:
- VIP customer priority routing
- Repeat escalation routing
- SLA enforcement
- Compliance-based routing
- Geographic/language routing
- Product/service-based specialist routing

---

## Scenario Prioritization

After generating all scenarios, assign priority levels:

- **P0 (Critical):** Core routing scenarios (R1-R3), primary escalation paths
- **P1 (High):** Availability model scenarios, business hours boundaries, major business logic
- **P2 (Medium):** Context-switching scenarios, edge cases, persona variations
- **P3 (Low):** Stress testing, boundary conditions, exotic edge cases

Recommend execution order: P0 → P1 → P2 → P3 (stop at first category that reveals failures)
