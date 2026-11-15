# SOQL Queries for Org Metadata Fetching

This module contains all SOQL queries used in Phase 2 to fetch org routing metadata.

## 🎯 Agent-Centric Querying Strategy

**START FROM THE AGENT FILE, NOT FROM ALL POSSIBLE METADATA.**

### Core Principle
Query metadata **from the agent outward**. Don't query everything that COULD be related to escalation just because it has routing-related names. Only query what the agent actually references.

### When to Query Broadly

**DO broaden your queries if:**
- Agent file has NO connection blocks (malformed or incomplete agent)
- Connection blocks exist but targets are missing (e.g., queue name is null)
- User explicitly requests to "see all available queues/flows" for configuration purposes

**DO NOT query broadly if:**
- Agent has valid connection blocks with specific targets
- Targets exist in org (even if inactive)
- Agent is properly configured

### Query Strategy Flow

1. **Parse agent file FIRST** — Extract connection blocks and identify routing targets
2. **Query ONLY what's referenced** — Don't query all flows/Apex with routing-related names
3. **Validate what you found** — Check if referenced targets exist in org
4. **Broaden ONLY if agent configuration is incomplete** — Last resort, not default

---

## Step 1: Parse Agent File for Connection Blocks (DO THIS FIRST)

Before querying any org metadata, read the agent file and extract all `connection` blocks:

```yaml
connection:
  messaging:
    outbound_route_type: OmniChannelFlow
    outbound_route: Escalate_Messaging_To_Agent
  voice:
    outbound_route_type: Queue
    outbound_route: Customer_Support_Queue
```

**Extract and list:**
- Channel name (e.g., `messaging`, `voice`, `web`)
- Route type (`OmniChannelFlow`, `Queue`, `OmniChannelQueue`)
- Route target name (flow API name or queue developer name)

**Example output:**
```
Connection blocks found:
  1. messaging → OmniChannelFlow: Escalate_Messaging_To_Agent
  2. voice → Queue: Customer_Support_Queue
```

---

## Step 2: Query ONLY Referenced Routing Targets

### For Queue Targets

Query ONLY queues that are explicitly referenced in connection blocks:

```bash
# Query specific queues by DeveloperName
sf data query --json -q \
  "SELECT Id, Name, DeveloperName, QueueRoutingConfigId FROM Group \
   WHERE Type = 'Queue' \
   AND DeveloperName IN ('Customer_Support_Queue', '<other-queue-names>')" \
  -o <org-alias>
```

**Do NOT query all queues.** Only query the ones the agent references.

### For OmniChannelFlow Targets

Query ONLY flows that are explicitly referenced in connection blocks:

```bash
# Query specific flows by ApiName
sf data query --json -q \
  "SELECT Id, ApiName, Label, ProcessType, Status FROM FlowDefinitionView \
   WHERE ApiName IN ('Escalate_Messaging_To_Agent', '<other-flow-names>')" \
  -o <org-alias>
```

**Do NOT query all active flows.** Only query the ones the agent references.

**Do NOT** use LIKE clauses to find flows with "routing-related" names unless connection blocks are missing.

**IMPORTANT: Retrieve and Read Flow Definitions Immediately**

After querying flow metadata, retrieve the actual flow definition and read it:

```bash
# For each flow found, retrieve the flow definition
sf project retrieve start --metadata "Flow:<ApiName>" -o <org-alias>

# Read the flow XML file
# Path: force-app/main/default/flows/<ApiName>.flow-meta.xml
```

**Extract from flow definition:**
- Queue assignments (which queues does it route to?)
- ServiceChannel references
- Business hours checks (if any)
- Availability logic (how does it determine if agents available?)
- Fallback behavior (what happens if no agents available?)

---

### Step 2.5: Discover and Retrieve Flow Dependencies (Subflows)

**CRITICAL:** After retrieving each flow, parse its XML to discover subflow dependencies and retrieve them recursively.

**Why This Matters:**
During cross-device testing, one execution successfully retrieved subflows while another missed them, resulting in incomplete test coverage. Subflows often contain critical business logic (availability checks, capacity validation, SLA enforcement) that generate additional test scenarios.

**Dependency Resolution Algorithm:**

**1. Initialize tracking:**
```
FLOWS_TO_PROCESS = [<main-flow-api-names>]  # From connection blocks
FLOWS_RETRIEVED = []
SUBFLOWS_DISCOVERED = []
```

**2. For each flow in FLOWS_TO_PROCESS:**

```bash
# Extract subflow references from flow XML
grep -o '<flowName>[^<]*</flowName>' force-app/main/default/flows/<FlowApiName>.flow-meta.xml | sed 's/<flowName>//;s/<\/flowName>//' | sort -u
```

**Alternative method (if grep doesn't work):**
```bash
# Read flow file and look for <actionType>Flow</actionType> elements
# The <flowName> element that follows contains the subflow API name
cat force-app/main/default/flows/<FlowApiName>.flow-meta.xml | grep -A1 "actionType>Flow<" | grep flowName | sed 's/.*<flowName>//;s/<\/flowName>.*//'
```

**3. For each subflow found:**

Check if already retrieved:
```bash
if [[ ! " ${FLOWS_RETRIEVED[@]} " =~ " ${subflow_name} " ]]; then
  # Not yet retrieved, fetch it
  sf project retrieve start --metadata "Flow:${subflow_name}" -o <org-alias>
  
  # Add to retrieved list
  FLOWS_RETRIEVED+=("${subflow_name}")
  
  # Add to process queue for recursive discovery
  FLOWS_TO_PROCESS+=("${subflow_name}")
fi
```

**4. Repeat until FLOWS_TO_PROCESS is empty (all dependencies resolved)**

**5. Present dependency tree to user:**

```
Flow Dependencies Discovered:

Testing_Escalation_Queue (main)
  └─ Check_Agent_Availability (subflow)
     ├─ Query UserServicePresence for agent status
     ├─ Query AgentWork for capacity consumption
     └─ Returns: IsAgentAvailable (boolean)

All dependencies retrieved: ✅ (2 flows total)
```

**Example with nested subflows:**

```
Inbound_Routing_Flow (main)
  ├─ Check_Business_Hours (subflow)
  │  └─ Get_Current_Timezone (subflow)
  │     └─ (no further dependencies)
  │
  └─ Route_To_Queue (subflow)
     └─ Log_Routing_Decision (subflow)
        └─ (no further dependencies)

All dependencies retrieved: ✅ (5 flows total)
```

**Error Handling:**

**If subflow retrieval fails:**
```
⚠️  Subflow Retrieval Failed

Main flow: Testing_Escalation_Queue
Referenced subflow: Check_Agent_Availability
Error: Component 'Flow:Check_Agent_Availability' not found

This means:
  - Subflow was deleted or renamed in org
  - Flow XML references outdated subflow name
  - Subflow exists but is in different namespace

Impact on testing:
  ❌ Cannot analyze subflow-specific logic
  ⚠️  Test scenarios will be incomplete for this flow path

Recommendations:
  1. Update main flow to remove reference to deleted subflow
  2. Recreate missing subflow in org
  3. Continue with partial scenario generation (exclude subflow scenarios)

Continue with partial scenario generation? (yes/no)
```

**Best Practices:**

✅ **DO:**
- Retrieve all subflows recursively (subflows can call other subflows)
- Track what's already retrieved to avoid duplicate retrieval
- Parse each subflow for additional dependencies
- Present complete dependency tree before generating scenarios

❌ **DON'T:**
- Skip subflow retrieval (leads to incomplete test coverage)
- Assume no subflows exist without checking
- Stop at first level (miss nested subflows)
- Proceed to scenario generation with incomplete flow dependencies

### For Custom Apex (If Referenced)

Only if the agent file references custom Apex classes (e.g., `apex://CheckBusinessHours`):

```bash
# Query specific Apex classes by Name
sf data query --json -q \
  "SELECT Id, Name, ApiVersion FROM ApexClass \
   WHERE Name IN ('<ApexClassName1>', '<ApexClassName2>')" \
  -o <org-alias>
```

**Do NOT query all Apex classes with routing-related names** unless explicitly referenced.

**IMPORTANT: Retrieve and Read Apex Classes Immediately**

After querying Apex metadata, retrieve the actual Apex class and read it:

```bash
# For each Apex class found, retrieve the source
sf project retrieve start --metadata "ApexClass:<ClassName>" -o <org-alias>

# Read the Apex class file
# Path: force-app/main/default/classes/<ClassName>.cls
```

**Extract from Apex class:**
- **For Business Hours Apex:** Is it hardcoded (e.g., `if(Time.now() > 9 && Time.now() < 17)`) or does it query `BusinessHours` records?
- **If queries BusinessHours:** Extract the BusinessHours name/ID it queries (e.g., `WHERE Name = 'North America'`)
- **Availability logic:** How does it determine agent availability? Does it check capacity, presence status, or custom criteria?
- **Return values:** What does it return? Boolean? Queue name? Agent list?

**For Business Hours Apex specifically:**

If the class queries BusinessHours records:
```sql
-- Example pattern found in Apex: [BusinessHours bh] WHERE Name = 'North America'
-- Query that specific BusinessHours record:
SELECT Id, Name, IsActive, TimeZoneSidKey, 
       MondayStartTime, MondayEndTime, 
       TuesdayStartTime, TuesdayEndTime,
       ... 
FROM BusinessHours 
WHERE Name = 'North America' 
AND IsActive = true
```

Then present to user:
```
Apex class CheckBusinessHours queries BusinessHours: "North America"
  - Timezone: America/Los_Angeles (PT)
  - Hours: Mon 8am-7pm, Tue-Thu 7am-7pm, Fri 7am-5pm

Is this the BusinessHours configuration you want to test against? (yes/no)
```

---

## Step 3: Query Associated Metadata for Found Targets

Once you've queried the specific queues/flows referenced by the agent, query their associated metadata:

### For Each Queue Found: Query Routing Configuration

```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, MasterLabel, RoutingModel, CapacityPercentage, CapacityWeight \
   FROM QueueRoutingConfig \
   WHERE Id IN ('<QueueRoutingConfigId1>', '<QueueRoutingConfigId2>')" \
  -o <org-alias>
```

Use the `QueueRoutingConfigId` values from the queues found in Step 2.

---

## Step 4: Query Service Channels (For Channel-Linked Queues)

### Query: Business Hours with Timezone and Operating Hours
```bash
sf data query --json -q \
  "SELECT Id, Name, IsActive, IsDefault, TimeZoneSidKey, \
          MondayStartTime, MondayEndTime, \
          TuesdayStartTime, TuesdayEndTime, \
          WednesdayStartTime, WednesdayEndTime, \
          ThursdayStartTime, ThursdayEndTime, \
          FridayStartTime, FridayEndTime, \
          SaturdayStartTime, SaturdayEndTime, \
          SundayStartTime, SundayEndTime \
   FROM BusinessHours \
   WHERE IsActive = true" \
  -o <org-alias>
```

### Query: Service Channels Linked to Found Queues

```bash
# Query service channels for the specific routing configs found
sf data query --json -q \
  "SELECT Id, DeveloperName, MasterLabel, RelatedEntity, RoutingConfigurationId \
   FROM ServiceChannel \
   WHERE RoutingConfigurationId IN ('<QueueRoutingConfigId1>', '<QueueRoutingConfigId2>')" \
  -o <org-alias>
```

Use the `QueueRoutingConfigId` values from queues found in Step 2.

---

## Step 5: Query Business Hours (For Queues with BusinessHours)

### Query: Business Hours with Timezone and Operating Hours

Only query business hours if:
- User indicates routing uses business hours, OR
- Queues have BusinessHours associations

```bash
sf data query --json -q \
  "SELECT Id, Name, IsActive, IsDefault, TimeZoneSidKey, \
          MondayStartTime, MondayEndTime, \
          TuesdayStartTime, TuesdayEndTime, \
          WednesdayStartTime, WednesdayEndTime, \
          ThursdayStartTime, ThursdayEndTime, \
          FridayStartTime, FridayEndTime, \
          SaturdayStartTime, SaturdayEndTime, \
          SundayStartTime, SundayEndTime \
   FROM BusinessHours \
   WHERE IsActive = true" \
  -o <org-alias>
```

### Query: Queue-BusinessHours Associations (For Specific Queues Only)

```bash
# Only query for the specific queues found in Step 2
sf data query --json -q \
  "SELECT Id, Name, QueueRoutingConfigId, \
          (SELECT BusinessHoursId FROM QueueSobjects WHERE BusinessHoursId != null) \
   FROM Group \
   WHERE Type = 'Queue' \
   AND DeveloperName IN ('<queue1>', '<queue2>')" \
  -o <org-alias>
```

Use the queue DeveloperNames from Step 2.

---

## Step 6: Query MessagingChannel and EmbeddedServiceConfig (Deployment Surface)

### Query: MessagingChannel (If Routing Uses Messaging)

Query MessagingChannel to understand the deployment configuration:

```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, MasterLabel, MessagingChannelType, \
          SessionHandlerType, SessionHandlerFlow, SessionHandlerQueue \
   FROM MessagingChannel" \
  -o <org-alias>
```

**Match MessagingChannel to routing:**
- If SessionHandlerFlow matches a flow from Step 2, this is the relevant channel
- Note the SessionHandlerQueue (fallback queue if flow doesn't route)

### Query: EmbeddedServiceConfig (Deployment Details)

**IMPORTANT:** List ALL EmbeddedServiceConfig records, then filter by messagingChannel match.

```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, MasterLabel, SiteId, Site.Name, \
          EmbeddedServiceConfig.DeploymentType, \
          EmbeddedServiceMessagingConfiguration.MessagingChannelId \
   FROM EmbeddedServiceConfig" \
  -o <org-alias>
```

**Filter results:**
- Find the EmbeddedServiceConfig where `MessagingChannelId` matches the MessagingChannel from above
- **Do NOT guess the DeveloperName** - always list all and filter

**Extract from EmbeddedServiceConfig:**
- DeploymentType: Web (MIAW), Mobile, etc.
- Site: Experience Cloud site name
- MessagingChannel: Which channel it uses

**If Site is found, query Experience Cloud site details:**

```bash
sf data query --json -q \
  "SELECT Id, Name, Status, Subdomain, UrlPathPrefix \
   FROM Site \
   WHERE Id = '<SiteId>'" \
  -o <org-alias>
```

**Construct deployment URL:**
```
https://<Subdomain>.<domain>.force.com/<UrlPathPrefix>
```

**Present to user:**
```
EmbeddedServiceConfig found: <DeveloperName>
  - DeploymentType: Web (MIAW)
  - Site: <SiteName>
  - MessagingChannel: <ChannelName>
  - Deployment URL: https://example.my.site.com/eswClaudeTest

This is the deployment surface for triggering escalations in testing.
```

---

## Step 7: Fetch Presence Statuses (Generic - Always Query)

These are generic and don't depend on agent configuration:

### Query: Presence Statuses
```bash
sf data query --json -q \
  "SELECT Id, MasterLabel, DeveloperName FROM ServicePresenceStatus" \
  -o <org-alias>
```

### Query: Bot Dialog Intents (For the Selected Agent Only)

Only query intents for the selected agent:

```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, MasterLabel, Type FROM MlIntent \
   WHERE IsActive = true \
   AND BotVersionId = '<selected-bot-version-id>'" \
  -o <org-alias>
```

### Query: Bot Utterances (For the Selected Agent Only)

```bash
sf data query --json -q \
  "SELECT Id, Text, MlIntentId, MlIntent.DeveloperName FROM MlSlotClassUtterance \
   WHERE IsActive = true \
   AND MlIntent.BotVersionId = '<selected-bot-version-id>'" \
  -o <org-alias>
```

**Do NOT query all intents/utterances across all agents.** Only query for the agent being tested.

---

## Step 8: Service Channel Link Detection (For Found Queues Only)

For each queue found in Step 2, automatically determine whether it is **channel-linked** or **no-channel**.

**Relationship:**
`Group.QueueRoutingConfigId → QueueRoutingConfig.Id ← ServiceChannel.RoutingConfigurationId`

### Query: Check if ServiceChannel is Linked to Queue's Routing Config
For each queue:
```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, RelatedEntity \
   FROM ServiceChannel \
   WHERE RoutingConfigurationId = '<QueueRoutingConfigId>'" \
  -o <org-alias>
```

**Record the result for each queue as:**
- **channel-linked** — a `ServiceChannel` record was found; note its `DeveloperName` and `RelatedEntity`
- **no-channel** — no `ServiceChannel` points to this queue's routing config

**Impact on test case generation:**
- **channel-linked queues** → capacity-exceeded scenarios WILL be generated
- **no-channel queues** → capacity-exceeded scenarios will NOT be generated (capacity state not distinguishable from no-agents-online)

---

## Custom Business Logic Queries

When user describes business rules, generate custom queries based on their requirements.

### Example 1: VIP Customer Check
User says: "VIP customers have Account.VIP_Tier__c = 'Platinum' or 'Gold'"

Generate `queries/check-vip-status.soql`:
```sql
SELECT Id, Name, VIP_Tier__c, Type, OwnerId 
FROM Account 
WHERE Id IN (
  SELECT AccountId 
  FROM MessagingSession 
  WHERE CreatedDate = TODAY
)
AND VIP_Tier__c IN ('Platinum', 'Gold')
```

### Example 2: Verify Queue Assignment
User says: "VIP customers should route to 'Premium_Support' queue"

Generate `queries/verify-vip-queue-assignment.soql`:
```sql
SELECT Id, WorkItemId, Status, 
       OriginalQueue.Name, 
       OriginalQueue.Id,
       UserId, User.Name
FROM AgentWork 
WHERE WorkItemId IN (
  SELECT Id FROM MessagingSession WHERE CreatedDate = TODAY
)
AND OriginalQueue.Name = 'Premium_Support'
ORDER BY CreatedDate DESC
LIMIT 10
```

### Example 3: Escalation History Check
User says: "Check if customer escalated in last 24 hours"

Generate `queries/check-escalation-history-24h.soql`:
```sql
SELECT Id, CreatedDate, Status, EndTime, 
       MessagingEndUser.AccountId,
       MessagingEndUser.Account.Name
FROM MessagingSession 
WHERE MessagingEndUser.AccountId = '<account-id>'
AND CreatedDate >= LAST_N_DAYS:1
AND Status = 'Ended'
ORDER BY CreatedDate DESC
```

### Example 4: Business Hours + Custom Logic
User says: "VIP customers bypass business hours, standard customers respect them"

Generate `queries/verify-vip-business-hours-override.soql`:
```sql
SELECT Id, CreatedDate, Status,
       MessagingEndUser.Account.VIP_Tier__c,
       (SELECT Id, OriginalQueue.Name FROM AgentWork)
FROM MessagingSession 
WHERE CreatedDate = TODAY
AND HOUR_IN_DAY(CreatedDate) NOT IN (9,10,11,12,13,14,15,16,17)
ORDER BY CreatedDate DESC
```

---

## Tips for Custom Query Generation

When capturing user-described business rules:
- **Field names** they mention (e.g., "VIP_Status__c", "Customer_Tier__c", "Case_History__c")
- **Object names** involved (Account, Case, Contact, Custom Objects)
- **Values to check** (e.g., "Platinum", "Gold", TRUE, specific dates)
- **Relationships** between objects (Account → MessagingSession, Case → Account)

**Query best practices:**
- Always include `CreatedDate = TODAY` to limit results to test runs
- Use `LIMIT` clauses to avoid large result sets
- Include relationship queries (e.g., `MessagingEndUser.Account.Name`)
- Add comments in queries explaining what to look for
- Generate queries that can be run via SF CLI: `sf data query --query "$(cat queries/check-vip-status.soql)" --target-org <alias>`

---

## Fallback: Broad Metadata Queries (ONLY if Agent Config Incomplete)

**⚠️ USE THESE QUERIES ONLY IF:**
- Agent file has no connection blocks
- Connection blocks are malformed or missing targets
- User explicitly requests to see all available routing metadata

**DO NOT use these queries by default.** They create noise and return metadata unrelated to the agent.

### Fallback Query: All Queues
```bash
# Only use if agent has NO queue references
sf data query --json -q \
  "SELECT Id, Name, DeveloperName, QueueRoutingConfigId FROM Group \
   WHERE Type = 'Queue'" \
  -o <org-alias>
```

### Fallback Query: All Active Flows (with Routing Names)
```bash
# Only use if agent has NO flow references
sf data query --json -q \
  "SELECT Id, ApiName, Label, ProcessType FROM FlowDefinitionView \
   WHERE Status = 'Active' \
   AND (ApiName LIKE '%Escalat%' OR ApiName LIKE '%Route%' OR ApiName LIKE '%Handoff%')" \
  -o <org-alias>
```

### Fallback Query: All Apex Classes (with Routing Names)
```bash
# Only use if agent references availability logic but doesn't specify classes
sf data query --json -q \
  "SELECT Id, Name FROM ApexClass \
   WHERE Name LIKE '%Avail%' OR Name LIKE '%Route%' \
   OR Name LIKE '%Escalat%' OR Name LIKE '%Handoff%'" \
  -o <org-alias>
```

**After running fallback queries:**
- Present results to user
- Ask user to identify which queues/flows are actually used by the agent
- Update agent file connection blocks with correct targets
- Re-run skill with proper agent configuration
