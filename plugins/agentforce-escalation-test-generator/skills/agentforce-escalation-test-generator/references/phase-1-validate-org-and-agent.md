# Phase 1: Validate Org and Select Agent

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Phase 1: Validate Org and Select Agent

### Phase 1: Validate Org and Select Agent

**Step 1: List and select target org**

First, list all authenticated orgs available in the current directory:

```bash
sf org list --json
```

Parse the JSON output and present orgs to the user in a readable format:

```
Available authenticated orgs:

  1. my-sandbox (user@company.com.sandbox)
     - Type: Sandbox
     - Instance: https://company--sandbox.sandbox.my.salesforce.com
     - Status: Active

  2. dev-org (user@company.com.dev)
     - Type: Sandbox
     - Instance: https://company--dev.sandbox.my.salesforce.com
     - Status: Active

  3. production (user@company.com)
     - Type: Production
     - Instance: https://company.my.salesforce.com
     - Status: Active
     - ⚠️  WARNING: This is a PRODUCTION org

Total: 3 orgs found
```

Ask the user: **"Which org would you like to generate test scenarios for? (Enter number or alias)"**

Once selected, validate the org is accessible:

```bash
sf org display --json -o <org-alias>
```

**Step 2: Confirm org selection and validate non-production**

Display selected org details:
```
Selected org: <alias>
  - Org ID: <id>
  - Org Name: <name>
  - Username: <username>
  - Instance: <url>
  - Type: <Sandbox/Production>
```

If `isSandbox: false`, display a warning and require explicit confirmation:
```
⚠️  WARNING: This is a PRODUCTION org.

Org Name: <name>
Username: <username>

Running this skill on a production org will query production metadata.
This is NOT recommended unless specifically authorized.

Are you sure you want to generate test scenarios for this PRODUCTION org? (yes/no)
```

**Do not proceed without explicit "yes" confirmation for production orgs.**

**If no orgs are found (`sf org list` returns empty):**

```
❌ No authenticated orgs found.

   To authenticate to an org, run (outside this skill):
     sf org login web --alias <your-alias>

   Then re-run this skill.
```

**If selected org returns authentication error:**

```
❌ Authentication not found for org: <alias>
   This org appears to be expired or not authenticated.

   To re-authenticate, run (outside this skill):
     sf org login web --alias <alias>

   Then re-run this skill.
```

**Do not attempt to run `sf org login web` yourself.** Authentication must happen as a separate step before the skill runs.

**Step 3: Check API Version Configuration**

Now that the target org is selected, check for API version overrides that can cause retrieval failures:

```bash
sf config list
```

**If `org-api-version` is set (either Global or Project level):**

```
⚠️  API Version Override Detected

Your SF CLI has an org-api-version override set to: <version>

API version overrides can cause "not available in this api version" errors when retrieving metadata, especially for newer metadata types like AiAuthoringBundle.

Recommended action: Temporarily unset for this session
  sf config unset org-api-version --global

Do you want me to unset this override? (yes/no)
```

**If user says yes:**
```bash
sf config unset org-api-version --global
```

**If user says no:**
```
⚠️  Proceeding with API version override. If retrieval fails, you may need to unset this manually.
```

**Step 4: Lock org selection**

After confirmation, all subsequent SF CLI commands must include `--target-org <alias>`. The skill will only run against the org specified and confirmed by the user.

---

**Step 5: List available agents (Multi-Method Discovery)**

**Important:** This step uses multiple discovery methods to handle both legacy Agent Builder and modern Agent Script metadata types.

**Method 1: Query BotDefinition (Legacy Agent Builder)**

```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, MasterLabel FROM BotDefinition \
   WHERE BotType = 'Agent'" \
  -o <org-alias>
```

**Method 2: List AiAuthoringBundle metadata (Agent Script)**

```bash
sf project list metadata --metadata-type AiAuthoringBundle --json -o <org-alias>
```

**Method 3: Search local project directory**

```bash
find . -name "*.agent" -type f 2>/dev/null | grep -v node_modules | grep -v ".agents/skills"
```

**Combine all results and present to user:**

```
Available agents in org (<org-alias>):

  Legacy Agent Builder (BotDefinition):
    1. SupportAgent (Support Agent) - BotDefinition
    2. SalesAgent (Sales Agent) - BotDefinition
  
  Agent Script (AiAuthoringBundle):
    3. EscalationAgent_v1 - AiAuthoringBundle
    4. CustomerServiceAgent - AiAuthoringBundle
  
  Local files:
    5. ./force-app/main/default/aiAuthoringBundles/MyAgent/MyAgent.agent

Total: 5 agents found (2 BotDefinition, 2 AiAuthoringBundle, 1 local)
```

**If Method 1 returns no results:**
```
ℹ️  No legacy Agent Builder (BotDefinition) agents found.
   This is normal if your org uses only Agent Script.
```

**If Method 1 FAILS with SOQL error:**

Common errors and solutions:

**Error: "sObject type 'BotDefinition' is not supported"**
```
⚠️  BotDefinition object not available in this org.

This means:
- Agentforce/Einstein Bots not enabled in this org
- User lacks object-level access to BotDefinition
- Org edition doesn't support BotDefinition (requires Service Cloud or higher)

Skipping legacy agent discovery. Will try Agent Script (Method 2).
```

**Error: "No such column 'BotType' on entity 'BotDefinition'"**
```
⚠️  BotDefinition query syntax issue.

Attempting alternative query without BotType filter:
  SELECT Id, DeveloperName, MasterLabel FROM BotDefinition
```

If alternative fails:
```
⚠️  Cannot query BotDefinition. Skipping Method 1.
```

**Error: "INVALID_TYPE" or "The requested resource does not exist"**
```
⚠️  BotDefinition not accessible in this org.

This is normal if:
- Using Agent Script only (no legacy bots)
- Agentforce feature not provisioned

Skipping to Method 2 (AiAuthoringBundle).
```

**If Method 2 fails or returns no results:**

**Error: "Entity type 'AiAuthoringBundle' is not available"**
```
⚠️  Could not list AiAuthoringBundle metadata.

Common causes:
1. API version too old (requires v61.0+)
   - Check: sf config list | grep org-api-version
   - Fix: sf config unset org-api-version --global
   
2. CLI version issue (known bug in 2.134.x-2.135.x)
   - Current CLI: <version from Phase 0>
   - Fix: Upgrade to 2.136+ or downgrade to 2.133.4
   
3. Agentforce not enabled
   - Check: Setup → Agentforce Settings
   - Verify feature license in org

Will skip to Method 3 (local files).
```

**Error: "This org hasn't synced metadata yet" or similar**
```
⚠️  Metadata API not ready.

Try running once to initialize:
  sf project retrieve start --metadata AiAuthoringBundle --target-org <alias>

Then re-run this skill.
```

**If all SOQL/metadata methods FAIL (not just return empty):**

```
❌ All agent discovery methods failed.

Method 1 (BotDefinition query): ❌ <error>
Method 2 (AiAuthoringBundle metadata list): ❌ <error>
Method 3 (Local file search): [✅ Found <N> files / ❌ None found]

Root cause analysis:
- Both SOQL queries failed → likely permissions or API version issue
- Metadata API failed → likely CLI version or org configuration issue

Alternative Approach: Manual Agent Specification
```

**Switch to manual agent specification mode:**

```
Since automated discovery failed, let's proceed manually.

Option 1: Specify agent by name (if you know it)
  - Provide the agent DeveloperName or API name
  - Example: "Customer_Service_Agent" or "EscalationAgent_v2"
  
Option 2: Use local agent file
  - Provide full path to .agent file on your system
  - Example: "/Users/you/project/force-app/.../MyAgent.agent"
  
Option 3: Exit and troubleshoot
  - Fix permissions: Grant "View All Data" or "Agentforce Service Agent Builder"
  - Fix API version: sf config unset org-api-version --global
  - Fix CLI version: Update to SF CLI 2.136+
  - Then re-run skill

Which option? (1/2/3)
```

**If user selects Option 1:**
```
Enter agent DeveloperName or API name:
```

Store the name and proceed with:
```
✅ Agent specified manually: <agent-name>

Since we couldn't query org metadata, we'll use these discovery methods:
  1. Attempt retrieval with provided name
  2. Search for local files matching name
  3. Allow manual file path if retrieval fails

Note: Cannot verify agent exists in org until retrieval attempt.
Proceeding to Step 5 (version selection)...
```

**If user selects Option 2:**
```
Enter full path to .agent file:
```

Validate the path:
```bash
if [ -f "<user-path>" ]; then
  echo "✅ File found"
  # Copy to expected location
  AGENT_NAME=$(basename "$user-path" .agent)
  mkdir -p force-app/main/default/aiAuthoringBundles/$AGENT_NAME
  cp "$user-path" force-app/main/default/aiAuthoringBundles/$AGENT_NAME/$AGENT_NAME.agent
else
  echo "❌ File not found at: <user-path>"
fi
```

If valid:
```
✅ Using local agent file: <agent-name>

File: <path>
Size: <size>

Skipping version selection (using local file as-is).
Proceeding to Phase 2 (metadata retrieval)...
```

**If user selects Option 3:**
Exit with troubleshooting guidance.

---

**If all methods return empty (but didn't error):**
```
❌ No agents found in org or local project.

Method 1 (BotDefinition): ✅ Query succeeded, 0 results
Method 2 (AiAuthoringBundle): ✅ Metadata list succeeded, 0 results  
Method 3 (Local files): ✅ Search succeeded, 0 results

This means:
- No agents deployed in this org
- No local agent files in project directory

Options:
1. Deploy an agent to this org first, then re-run skill
2. Provide path to agent file manually (Option 2 above)
3. Create a new agent: Setup → Agents → New

Which option? (1/2/3)
```

Ask: **"Which agent would you like to generate test scenarios for? (Enter number, DeveloperName, or AiAuthoringBundle name)"**

---

**Step 6: Retrieve agent versions and select version (Metadata-Type Aware)**

**Important:** Version retrieval differs based on agent metadata type detected in Step 4.

**For Legacy Agent Builder (BotDefinition):**

Query for all versions:
```bash
sf data query --json -q \
  "SELECT Id, VersionNumber, Status FROM BotVersion \
   WHERE BotDefinition.DeveloperName = '<agent-api-name>' \
   ORDER BY VersionNumber DESC" \
  -o <org-alias>
```

**If query fails:**

**Error: "sObject type 'BotVersion' is not supported"**
```
⚠️  BotVersion object not accessible.

This means:
- User lacks object-level access to BotVersion
- Org doesn't have BotVersion API access enabled

Cannot proceed without version information
  Since we can't query versions and draft versions are not supported,
  you must either:
  1. Grant BotVersion object access to the user
  2. Manually specify a published version number (e.g., "v3")
  3. Exit and publish a version if none exist

Which option? (1/2/3)
```

**Error: "No such column 'BotDefinition.DeveloperName'"**
```
⚠️  Query syntax issue. Attempting alternative:

Alternative query using BotDefinitionId:
  First: Get BotDefinition Id
  Then: Query BotVersion using that Id
```

```bash
# Get BotDefinition ID first
BOT_ID=$(sf data query --json -q "SELECT Id FROM BotDefinition WHERE DeveloperName = '<name>'" -o <alias> | jq -r '.result.records[0].Id')

# Query versions using ID
sf data query --json -q "SELECT Id, VersionNumber, Status FROM BotVersion WHERE BotDefinitionId = '$BOT_ID' ORDER BY VersionNumber DESC" -o <alias>
```

Show version summary:
```
Agent: <DeveloperName> (Legacy Agent Builder)
Versions found:
  v3  Active   
  v2  Inactive
  v1  Inactive
```

**If alternative query also fails:**
```
❌ Cannot query BotVersion with either method.

Options:
1. Manually specify a published version number (e.g., "v3")
2. Exit and grant BotVersion access to user

Which option? (1/2)
```

**For Agent Script (AiAuthoringBundle):**

Agent Script uses a different versioning model. List all published versions:
```bash
sf project list metadata --metadata-type AiAuthoringBundle --json -o <org-alias> | \
  jq '.result[] | select(.fullName | startswith("<agent-api-name>"))'
```

Expected format for published versions:
- `<agent-api-name>_1` = Published version 1
- `<agent-api-name>_2` = Published version 2

Show version summary:
```
Agent: <DeveloperName> (Agent Script)
Published versions found:
  v2  (Published: <agent-api-name>_2)
  v1  (Published: <agent-api-name>_1)
```

**If version query fails for Agent Script:**

**Error: "Entity type 'AiAuthoringBundle' is not available"**
```
⚠️  Cannot list AiAuthoringBundle versions via metadata API.

This is the same error from Step 4 (agent discovery).

Fallback options:
1. Check local directory for published versions
2. Manual version specification
```

**Fallback 1: Check local directory structure**
```bash
ls -d force-app/main/default/aiAuthoringBundles/<agent-api-name>_* 2>/dev/null
```
(Note: Only looking for published versions with _N suffix, not draft)

**Fallback 2: Try Tooling API query for published versions**
```bash
sf data query --json -q \
  "SELECT Id, DeveloperName, Language FROM AiAuthoringMetadata \
   WHERE DeveloperName LIKE '<agent-api-name>_%'" \
  --use-tooling-api \
  -o <org-alias>
```

**If Tooling API query fails too:**
```
❌ Cannot query agent versions via any method.

Methods attempted:
  ❌ Metadata API (list metadata)
  ❌ Local directory search
  ❌ Tooling API query

Cannot proceed without published version information.

Options:
1. Manually specify a published version (e.g., "<agent-api-name>_2" for v2)
2. Exit and troubleshoot metadata API access
3. Publish a version in the Salesforce org if none exist

Which option? (1/2/3)
```

**If user selects option 1 (manual version specification):**
```
Enter published version to retrieve:
  - For v1: <agent-api-name>_1
  - For v2: <agent-api-name>_2
  - etc.

Version name:
```

Store the user-provided version name for use in Step 6 retrieval.

**Common Selection Prompt (Both Types):**

Ask: **"Which version would you like to test? (Options: 'active', 'latest', or 'v[N]')"**

- **active** — tests the active published version (for BotDefinition) or latest published (for AiAuthoringBundle)
- **latest** — tests the highest version number available
- **v[N]** — tests a specific version (e.g., v1, v2, v3)

**If no active/published version found:**

```
⚠️  Version Check Results:
    Agent Type: [BotDefinition / AiAuthoringBundle]
    Published Versions: [found: N versions / none found]

    [If no published versions found]:
    ❌ No published versions found. Cannot proceed with test scenario generation.
    
    To resolve: Publish a version in Setup → Agents → <agent-name>, then run this skill again.

    [If connection blocks point to missing targets]:
    ⚠️  Connection block validation:
        <channel> → <route_type>://<target> — NOT found as active in org
        Scenarios for this connection will likely fail during manual testing.
```

**Exit if no published versions are available. Draft versions are not supported for testing.**

---

**Step 7: Retrieve the agent file (Multi-Method with Fallback Chain)**

**Note:** This step uses different retrieval methods based on agent metadata type and includes fallback logic for CLI version regressions.

---

**For Agent Script (AiAuthoringBundle):**

**Published version (v1, v2, etc.):**

**Attempt 1A: Retrieve via AiAuthoringBundle metadata type**
```bash
sf project retrieve start --json \
  --metadata "AiAuthoringBundle:<agent-api-name>_<version-number>" \
  -o <org-alias>
```

Expected file path:
```
force-app/main/default/aiAuthoringBundles/<agent-api-name>_<version>/<agent-api-name>_<version>.agent
```

**Attempt 1B: If Attempt 1A fails, try retrieve via package.xml**

Create temporary package.xml:
```bash
cat > package_tmp.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members><agent-api-name>_<version></members>
        <name>AiAuthoringBundle</name>
    </types>
    <version>62.0</version>
</Package>
EOF

sf project retrieve start --manifest package_tmp.xml -o <org-alias>
rm package_tmp.xml
```


---

**For Legacy Agent Builder (BotDefinition):**

**Note:** Legacy Agent Builder agents cannot be retrieved as source files - they exist only in the org database.

Display message:
```
ℹ️  Legacy Agent Builder Detection

Agent Type: BotDefinition (Legacy Agent Builder)
Agent: <DeveloperName> (version <N>)

Legacy Agent Builder agents are not stored as .agent files and cannot be retrieved
via SF CLI. They exist only in the org database.

Test scenario generation will proceed with limited agent-specific context:
  ✅ Basic escalation scenarios (user-requested, timeout-based)
  ✅ Routing infrastructure validation
  ✅ Safety probes
  ❌ Agent Script-specific features (pre-escalation subagents, gating variables, etc.)

To get full Agent Script testing capabilities:
1. Migrate to Agent Script: Setup → Agents → <agent-name> → Migrate to Agent Script
2. Re-run this skill after migration

Proceed with limited agent context? (yes/no)
```

If user says **no**, exit the skill.

If user says **yes**, skip to Phase 2 with a flag indicating legacy agent (reduced agent-specific scenario generation).

---

---

**If retrieval FAILS (AiAuthoringBundle agents only):**

**Common Error 1: "Entity type 'AiAuthoringBundle' is not available in this api version"**

Display enhanced error context:

```
❌ Agent File Retrieval Failed

Command executed:
  sf project retrieve start --metadata "AiAuthoringBundle:<agent-api-name>[_<version>]" -o <org-alias>

Error message:
  "Entity type 'AiAuthoringBundle' is not available in this api version"

Environment context:
  - SF CLI Version: <version from Phase 0>
  - Org API Version: <from org display>
  - API Override: <from Phase 0 config check>
  - Working Directory: $(pwd)
  - Metadata Type: AiAuthoringBundle (Agent Script)

This error typically means:
1. ⚠️  CLI version regression (known issue in 2.134.x - 2.135.x)
2. API version mismatch (check if org-api-version override is set)
3. Org API version too old (AiAuthoringBundle requires API v61.0+)

Fallback chain will now execute...
```

**Common Error 2: "No matches found for <agent-api-name>"**

```
❌ Agent Not Found in Org

The agent '<agent-api-name>' was not found during retrieval.

Possible causes:
1. Agent name mismatch (check DeveloperName vs. MasterLabel)
2. Agent version not published (ensure a published version exists)
3. Wrong org selected (agent may be in different org)

Fallback chain will now execute...
```

**Common Error 3: "insufficient access rights on cross-reference id"**

```
❌ Permission Error

Insufficient permissions to retrieve AiAuthoringBundle metadata.

Required permissions:
- View All Data OR
- Modify All Data OR
- Agentforce Service Agent Builder permission set

Current user: <username>

Ask your org administrator to grant these permissions, then re-run the skill.
If you have a local copy of the agent file, the fallback chain can use it instead.
```

---

**FALLBACK CHAIN (Executes when primary retrieval fails):**

**Attempt 2: Search for local agent file**

```bash
find ~ -name "<agent-api-name>*.agent" -type f 2>/dev/null | grep -v ".agents/skills" | grep -v "node_modules"
```

**If local file(s) found:**

```
🔍 Found local agent file(s):

  1. /Users/user/may-18-skill-testing/force-app/.../MyAgent.agent
  2. /Users/user/projects/sfdx-project/force-app/.../MyAgent_2.agent

Which file would you like to use? (Enter number or 'none' to skip)
```

**If user selects a file:**
```bash
# Copy to expected location
mkdir -p force-app/main/default/aiAuthoringBundles/<agent-api-name>
cp <selected-file> force-app/main/default/aiAuthoringBundles/<agent-api-name>/<agent-api-name>.agent
```

```
✅ Using local agent file:
  Source: <selected-file>
  Copied to: force-app/main/default/aiAuthoringBundles/<agent-api-name>/<agent-api-name>.agent

⚠️  Note: This local file may be a different version than what's in the org. 
  Test scenarios will be based on this local version's structure.
```

**Attempt 3: Manual file path input**

If Attempt 2 finds no files or user skips:

```
Would you like to provide the path to an agent file manually? (yes/no)
```

If **yes**:
```
Enter the full path to the .agent file:
```

Validate the provided path:
```bash
if [ -f "<user-provided-path>" ]; then
  mkdir -p force-app/main/default/aiAuthoringBundles/<agent-api-name>
  cp "<user-provided-path>" force-app/main/default/aiAuthoringBundles/<agent-api-name>/<agent-api-name>.agent
  echo "✅ Agent file copied successfully"
else
  echo "❌ File not found at provided path"
fi
```

**Attempt 4: Try alternative API version**

If still failing and API version override was detected in Phase 0:

```
Would you like to try retrieving with API version 62.0? (yes/no)
```

If **yes**:
```bash
sf project retrieve start --json \
  --metadata "AiAuthoringBundle:<agent-api-name>[_<version>]" \
  --api-version 62.0 \
  -o <org-alias>
```

**Attempt 5: Try BotDefinition query as final check**

Some orgs may have the agent as BotDefinition even if it appeared in AiAuthoringBundle list:

```bash
sf data query --json -q \
  "SELECT Id, DeveloperName FROM BotDefinition \
   WHERE DeveloperName = '<agent-api-name>'" \
  -o <org-alias>
```

If found:
```
ℹ️  Agent exists as BotDefinition (Legacy Agent Builder), not AiAuthoringBundle.

This explains the retrieval failure. Legacy agents cannot be retrieved as .agent files.

Proceeding with limited agent context (routing metadata only).
See earlier section on "Legacy Agent Builder" handling.
```

**Final Fallback: Metadata-Only Generation**

If all attempts fail:

```
❌ All retrieval attempts exhausted.

Attempts made:
  ❌ Standard AiAuthoringBundle retrieval
  ❌ Package.xml-based retrieval
  ❌ Local file search
  ❌ Manual file path
  ❌ Alternative API version
  ❌ BotDefinition verification

Remaining options:
  1. Fix environment issue and re-run skill
     - Downgrade SF CLI to 2.133.4: npm install -g @salesforce/cli@2.133.4
     - Remove API version override: sf config unset org-api-version --global
     - Verify org permissions: Setup → Users → <username> → Permission Sets
  
  2. Continue with metadata-only scenario generation (60% coverage)
     Generates routing/infrastructure tests only, no agent-specific scenarios

Which option? (1/2 or exit)
```

**If user selects option 2 (metadata-only):**
```
⚠️  Proceeding with metadata-only scenario generation.

Test Coverage Breakdown:
  ✅ Queue routing and availability (R1-R4)
  ✅ Service Channel capacity (R5)
  ✅ Business hours validation (BH1-BH5)
  ✅ Flow/Apex availability logic
  ✅ MessagingSession lifecycle (R3)
  
  ❌ Agent-specific escalation triggers (A1-A7)
  ❌ Pre-escalation subagents
  ❌ Context-switching scenarios (C1-C5)
  ❌ Agent conversation flow edge cases
  ❌ Agent Script safety probes (S1-S6)

Estimated Coverage: 60% (~30 of 50 typical scenarios)

⚠️  This is NOT recommended for production readiness testing.
   Use only for infrastructure validation or troubleshooting.

Final confirmation - proceed with 60% coverage? (yes/no)
```

If **yes**: Continue to Phase 2 with `agent_file_available = false` flag.

If **no**: Exit skill with re-run instructions.

**If user selects option 1:**
```
Please resolve the environment issue outside this session, then re-run the skill.

Recommended actions:
  1. Check SF CLI version: sf --version
  2. Check API override: sf config list
  3. Verify org access: sf org display -o <alias>
  4. Test manual retrieval: sf project retrieve start --metadata "AiAuthoringBundle:<agent-api-name>" -o <alias>

Once resolved, re-run: /agentforce-escalation-test-generator
```
**Exit skill.**

---

**If retrieval SUCCEEDS (AiAuthoringBundle):**

Confirm retrieval:
```
✅ Agent file retrieved successfully

  Agent: <DeveloperName>
  Metadata Type: AiAuthoringBundle (Agent Script)
  Version: <version-selected>
  File: <file-path>
  File size: <size>
  
Validating agent file format...
```

**Validate agent file is readable and properly formatted:**

```bash
# Check file exists and is not empty
if [ -s "<file-path>" ]; then
  # Check for Agent Script format markers
  head -50 "<file-path>" | grep -E "(^subagent|^connection|@utils\.escalate|^actions)"
  echo "File format check passed"
else
  echo "File is empty or missing"
fi
```

**Display agent file preview:**
```bash
echo "Agent file preview (first 30 lines):"
head -30 <file-path>
```

**If file is empty or unreadable:**
```
❌ Agent file is empty or corrupted.
  File path: <file-path>
  Size: <size>
  
  This may indicate:
  - Retrieval succeeded but downloaded empty file
  - File permissions issue
  - Incomplete retrieval
  
  Entering fallback chain...
```
Return to **Attempt 2** in fallback chain.

**If file exists but is not valid Agent Script format:**
```
⚠️  File retrieved but format is unexpected.
  File path: <file-path>
  
  Expected: Agent Script format (.agent file with subagents, connections, actions)
  Found: <description of actual content>
  
  This may indicate:
  - Wrong metadata type (might be BotDefinition instead)
  - Partial retrieval
  - Org/CLI version mismatch
  
  Options:
  1. View file contents and decide whether to proceed
  2. Enter fallback chain to find alternative
  
  Which option? (1/2)
```

**If file is valid Agent Script:**
```
✅ Agent file validated and ready for parsing.

  Format: Agent Script (.agent)
  Contains:
    - <N> subagents detected
    - <N> connection blocks detected
    - <N> actions detected
    - Escalation logic: [detected / not detected]
```

Ask: **"Proceed to fetch org routing metadata? (yes/no)"**

---

**For Legacy Agent Builder (BotDefinition) - No File Retrieval:**

If agent type was determined to be BotDefinition in Step 5:

```
ℹ️  Skipping file retrieval for Legacy Agent Builder.

  Agent: <DeveloperName>
  Metadata Type: BotDefinition (Legacy Agent Builder)
  Version: v<N>

Legacy agents are stored in the database only and cannot be retrieved as files.

Test scenario generation will proceed with routing metadata only:
  ✅ Routing infrastructure tests
  ✅ Basic escalation flow tests
  ❌ Agent Script-specific features

Setting agent_file_available = false
```

Ask: **"Proceed to fetch org routing metadata? (yes/no)"**

---
