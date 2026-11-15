# Business Logic Requirements Gathering

This module provides guidance for gathering custom business logic requirements from users in Phase 2b.

## Workflow Overview

**Approach:** Start smart (parse agent file) → Present findings → Fill gaps (guided interview) → Confirm before generating scenarios

---

## Step 1: Parse Agent File for Business Logic

Before asking the user, analyze the retrieved agent file for business logic indicators.

### Look For:
- Conditional routing based on variables (e.g., `if @context.customer_tier == 'VIP'`)
- Queue selection logic with conditions (e.g., different queues for different customer types)
- SLA/timing requirements in instructions (e.g., "premium customers within 2 minutes")
- Compliance mentions (e.g., HIPAA, PCI, GDPR)
- Customer segmentation (e.g., tier, priority, region, language)
- Historical checks (e.g., "check if customer escalated before")
- External data references (e.g., callouts, external system checks)
- Field references that suggest business rules (e.g., Account.VIP_Status__c, Contact.Region__c)
- Multi-queue routing with business logic conditions
- Apex/Flow invocations with business-sounding names (e.g., "CheckVIPStatus", "RoutePremiumCustomers")

---

## Step 2: Summarize Findings to User

Present what you found in the agent file:

```
I analyzed the agent file and found these potential business rules:

1. **VIP Customer Routing** (derived from connection block condition)
   - Trigger: When @context.account.vip_tier__c IN ('Platinum', 'Gold')
   - Behavior: Routes to 'Premium_Support_Queue'
   - Implementation: Conditional routing in connection block

2. **SLA Requirement** (derived from agent instructions)
   - Trigger: All premium customers
   - Behavior: "Connect within 2 minutes"
   - Implementation: Mentioned in agent instructions

3. **Compliance Routing** (derived from Apex invocation)
   - Trigger: Apex class 'CheckHIPAACompliance' is called
   - Behavior: Unknown - appears to check compliance status
   - Implementation: Apex invocation before escalation

Are these business rules correct? Are there additional business rules not captured in the agent file?
(confirm/add-more/correct)
```

---

## Step 3: Conduct Guided Interview if Needed

If user says "add-more" or "correct", conduct a guided interview to gather missing details.

### For Each Business Rule (Found or New), Ask:

#### a) Business Rule Name
Example: "VIP Customer Fast-Track"

#### b) Business Requirement
**Question:** What business need does this fulfill?
- Example: "VIP customers must receive priority routing to reduce wait time and churn"
- Guide user: "Why does this rule exist? What business problem does it solve?"

#### c) When This Applies
**Question:** What triggers this business logic?
- Example: "When customer has 'VIP' flag on Account record"
- Guide user: "What conditions must be true for this rule to activate?"
- Ask about field values: "What field determines this? What values trigger the rule?"

#### d) Expected Behavior
**Question:** What should happen?
- Example: "Route to VIP Support Queue, skip standard queue, agent must accept within 30 seconds"
- Guide user: "Walk me through what happens step-by-step when this rule triggers"
- Ask specific questions:
  - "Which queue should they route to?"
  - "Should they skip any queues?"
  - "Is there a time requirement (SLA)?"
  - "What happens if the preferred queue is unavailable?"

#### e) Where Implemented (Technical Implementation)
**Options:** Flow, Apex, validation rule, queue routing config, agent file, external system
- Guide user: "Where does this logic live? Is it in the agent file, a Flow, Apex, or external system?"
- This helps generate verification queries

#### f) Operational/Capacity Questions
Guide user through scenarios:
- "Do you anticipate multiple customers triggering this rule at the same time?"
- "If yes, and there are more customers than available agents, what should happen?"
  - Should they wait in queue?
  - Should they get fallback message?
  - Should they route to alternative queue?
- "What's the maximum acceptable wait time for this customer type?"
- "Should this rule work 24/7 or only during business hours?"

#### g) Business Edge Cases
**Question:** What special situations should we test?

Guide user through edge cases:
- "What if the target queue has no agents available?"
- "What if the customer's status changes mid-conversation?" (e.g., becomes VIP during chat)
- "What if the customer escalates outside business hours?"
- "What if multiple business rules conflict?" (e.g., VIP + HIPAA)
- "What if the external system providing data is down?"
- "What if the required field is null/empty?"

#### h) Success Criteria
**Question:** How do we know this business rule is working?
- Example: "VIP customer connects to agent within 30 seconds, routes to VIP queue only"
- Guide user: "What does success look like? What will you check to confirm it worked?"

---

## Step 4: Ask About Cross-Cutting Concerns

After gathering individual business rules, ask:

### a) External Data Dependencies
**Question:** Do any business rules depend on external data or systems?
- Customer tier from external CRM
- Account status from billing system
- Compliance flags from external database
- Real-time data that might change during escalation
- Guide: "If the external system is slow or unavailable, what should happen?"

### b) Rule Conflicts and Priority
**Question:** Do any business rules conflict or have priority order?
- Example: "VIP customers override business hours (always route), but HIPAA compliance overrides VIP (must wait for certified agent)"
- Guide: "If two rules both apply, which one wins?"

### c) Hidden Business Rules
**Question:** Are there any business rules NOT visible in the agent file?
- Pre-routing logic (runs before agent)
- Post-routing logic (runs after agent handoff)
- Queue assignment rules
- Platform events that trigger routing changes
- Guide: "Is there any routing logic that happens before or after the agent conversation?"

---

## Step 5: Confirm All Business Rules Before Proceeding

Present complete summary:

```
I've identified the following business rules for testing:

1. **VIP Customer Fast-Track**
   - Why: Reduce churn for high-value customers
   - Trigger: Account.VIP_Tier__c IN ('Platinum', 'Gold')
   - Behavior: Route to Premium_Support queue, connect within 30 seconds
   - Implementation: Conditional routing in agent connection block
   - Capacity: If Premium_Support full, hold in queue (don't fallback)
   - Edge cases: Test null VIP_Tier__c, mid-conversation tier change, outside business hours
   - Success: Routes to Premium_Support AND connects within 30 seconds

2. **HIPAA Compliance Routing**
   - Why: Legal requirement for healthcare data
   - Trigger: Apex class CheckHIPAACompliance returns TRUE
   - Behavior: Route only to HIPAA-certified agents (HIPAA_Certified__c = TRUE on User)
   - Implementation: Apex invocation + queue filter
   - Capacity: Hold until HIPAA-certified agent available (never route to non-certified)
   - Edge cases: All HIPAA-certified agents offline, external compliance check fails
   - Success: Routes ONLY to agents with HIPAA_Certified__c = TRUE

3. **Rule Priority:** HIPAA Compliance > VIP Status (compliance always wins)

Is this correct? Should I proceed to generate test scenarios for these business rules?
(yes/modify/add-more)
```

Only proceed after user confirms "yes".

---

## Scenario Generation Guidelines

For each business rule described, generate:
- A dedicated test scenario in the "Business Logic" category
- Business-focused test objective (validates the business requirement, not just the automation)
- Preconditions that set up the business conditions (customer tier, account type, etc.)
- Test steps that exercise the business process
- Verification that confirms the business outcome (not just technical execution)
- Business edge cases (null values, conflicting rules, external system failures)
- **Custom SOQL queries specific to this business rule**

---

## Example Business Logic Scenarios

### Scenario 37: Business Logic - VIP Customer Priority Routing
- **Business Requirement:** VIP customers receive priority support to reduce churn
- **Preconditions:** Customer Account has VIP_Status__c = true, VIP queue has 2 agents available
- **Test Steps:** Trigger escalation from VIP customer account
- **Expected Business Outcome:** Routes to VIP Support Queue (not standard queue), agent accepts within 30 seconds
- **Verification:** Check queue assignment is VIP queue, measure time-to-accept
- **Business Edge Case 1:** VIP queue has no agents → should system hold or fallback to standard?
- **Business Edge Case 2:** Customer loses VIP status during conversation → does routing change?
- **Technical Implementation Note:** Implemented via Flow "Route_VIP_Customers" (queries Account.VIP_Status__c)

### Scenario 38: Business Logic - Repeat Escalation Routing
- **Business Requirement:** Customers escalating multiple times get escalated to management for service recovery
- **Preconditions:** Customer has MessagingSession created in last 24 hours with Status = 'Ended'
- **Test Steps:** Trigger second escalation from same customer within 24h
- **Expected Business Outcome:** Routes to Tier 2 Management Queue (bypasses Tier 1)
- **Verification:** Check queue assignment, verify MessagingSession history query
- **Business Edge Case 1:** What if first escalation is still active (not ended)?
- **Business Edge Case 2:** What if 24h1m passes (just outside window)?
- **Business Edge Case 3:** What counts as an "escalation" vs normal inquiry?
- **Technical Implementation Note:** Implemented via Apex class "EscalationHistoryChecker"

---

## Common Business Logic Categories

Use these as prompts if user is unsure what business rules to test:

1. **Customer Tier/Priority Routing**
   - VIP, Premium, Standard customer tiers
   - Priority-based queue assignment
   - SLA requirements by tier

2. **Case History-Based Routing**
   - Repeat escalations
   - Previous case volume
   - Customer sentiment/satisfaction scores

3. **Product/Service-Based Routing**
   - Different queues for different products
   - Specialist routing by product line
   - Technical vs billing inquiries

4. **Compliance Requirements**
   - HIPAA-certified agents
   - PCI-compliant routing
   - GDPR data handling
   - SOX audit requirements

5. **Geographic/Language Routing**
   - Region-based assignment
   - Language preference matching
   - Timezone-aware routing

6. **Account Relationship Logic**
   - Partner vs customer routing
   - Account size/revenue-based priority
   - Strategic account flagging

7. **SLA-Based Requirements**
   - Time-to-connect targets
   - Response time guarantees
   - Escalation timing rules

8. **Escalation Chain Logic**
   - Tier 1 → Tier 2 → Management progression
   - Automatic escalation on time thresholds
   - Management override paths
