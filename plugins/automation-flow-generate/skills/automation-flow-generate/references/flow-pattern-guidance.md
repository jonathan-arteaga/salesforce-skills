# Flow Pattern Guidance

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Flow Pattern Guidance

The pipeline selects flow elements from your `userPrompt`. Vague prompts lead the pipeline to pick wrong structures, producing metadata that fails deployment. When the request matches one of the patterns below, make the intent explicit in the `userPrompt` you pass to Step 1 and Step 2 so the pipeline selects the correct elements.

### Scheduled flows ("daily", "weekly", "every Sunday", "runs once a week at 10PM")

A recurring, time-based flow is a **Scheduled** flow. The schedule lives on the **start element**: `triggerType` is `Scheduled` and a `<schedule>` block holds `<frequency>` (e.g. `Weekly`), `<startDate>`, and `<startTime>`. Do NOT expect `startDate`/`startTime` on a `FlowScheduledPath` element — a scheduled flow's cadence is on `<start><schedule>`, not a scheduled path.

To select records for a scheduled flow, put the record criteria in the **start element's filters** (with `<object>` and `<filters>` on `<start>`), which runs the flow once per matching record with `$Record` bound to each. Prefer this over adding a Loop that re-queries and iterates the same object — a start-filtered scheduled flow does not need a Loop to walk the triggering object's records.

When the prompt says "runs once a week / every Sunday / daily at a time", the `userPrompt` should state: scheduled trigger, the frequency, the start time, and the record filter on the triggering object.

### "Autolaunched" is literal

An **"autolaunched"**/"no-trigger" request builds a **no-trigger** flow (no `triggerType`, `object`, or `<schedule>` on start) — put "for each…/when X"/timing intent in the **body**, not the trigger; add one only if asked.

### Counting related records ("count all related X", "number of X")

To store a count of records, use a **single** assignment element with `<operator>AssignCount</operator>`, assigning from the collection (the record-lookup result) into a Number variable. Do NOT emit two assignment elements for one count, and do NOT give two assignment elements the same `name` — duplicate assignment names, or two assignments doing one logical count, fail deployment. One lookup → one `AssignCount` assignment → one record update.

### Do not invent actions the prompt did not request

Generate only the elements the prompt asks for. If a prompt names a trigger but not an action (e.g. "create a flow for when a record is created" with no stated behavior), do NOT add a Chatter post, email, or other action that was not requested. An unrequested action such as a `chatterPost` produces metadata that references undefined types and fails deployment. When the requested behavior is genuinely absent, generate the minimal valid trigger without inventing side effects.

### MANDATORY: Multiple Flows = Multiple Separate Pipelines

**FIRST: Before calling any pipeline step, check if the user's request contains multiple flows. If it does, you MUST split it into separate single-flow prompts. Each flow gets its own 3-step pipeline with its own `userPrompt` that describes ONLY that one flow.**

**NEVER pass a multi-flow request as a single `userPrompt` field. NEVER club multiple flow descriptions into one `userPrompt`.**

When the user requests multiple flows (e.g., "Create flows for my app: 1) ... 2) ... 3) ..."), you MUST:
1. **Split** the request into separate individual flow descriptions.
2. **Run a separate 3-step pipeline for each flow**, using a `userPrompt` that describes ONLY that one flow.
3. **Execute ALL pipelines SEQUENTIALLY** — one after another, NEVER in parallel. Do NOT stop after the first flow. Do NOT wait for the user to ask you to continue. Do NOT summarize and stop. Keep going until every requested flow has been fully generated.

**WRONG - Multiple flows clubbed into one userPrompt:**
```json
{
  "userPrompt": "Create flows for the app: 1) Record-Triggered Flow on ResourceAllocation__c to update Resource__c. 2) Screen Flow to allocate resources. 3) Record-Triggered Flow on Supply__c to auto-flag Low_Stock__c.",
  ...
}
```

**CORRECT - Separate call for EACH flow:**

**Flow 1 - Step 1 (fetchGroundedObjectMetadata):**
```json
{
  "userPrompt": "Create a Screen Flow named Tenant_Onboarding that captures tenant details, selects a Unit__c with Status__c = 'Vacant', creates Lease__c...",
  "inflightMetadata": [...]
}
```
Then call Step 2 (`flowElementSelection`) with the `groundingMetadata` from Step 1, then Step 3 (`flowElementGeneration`) with the `operationId` from Step 2.

**Flow 2 - Step 1 (fetchGroundedObjectMetadata):**
```json
{
  "userPrompt": "Create an Autolaunched Flow named Generate_Onboarding_Checklist that given a Lease__c Id input, queries OnboardingTask__c...",
  "inflightMetadata": [...]
}
```
Then call Step 2 and Step 3 for this flow.

**Flow 3 - Step 1 (fetchGroundedObjectMetadata):**
```json
{
  "userPrompt": "Create a Record-Triggered Flow named Sync_Unit_On_Lease_Changes that on insert and update of Lease__c...",
  "inflightMetadata": [...]
}
```
Then call Step 2 and Step 3 for this flow.

**Mandatory Rules:**
- Complete every requested Flow. When using the MCP generator, run one three-step pipeline per Flow. For the local metadata path, validate each Flow against the schema and target-org checks; do not claim an unavailable pipeline ran.
- **You MUST fully complete the current flow's 3-step pipeline (including looping Step 3 until `isComplete` is `true` or errors are returned) BEFORE starting the next flow's pipeline.** Do NOT interleave or parallelize pipelines across flows. **Everything is SEQUENTIAL — NEVER parallel.**
- After completing a flow's pipeline, **immediately start the next flow's pipeline**. Do NOT pause, summarize, or wait for user confirmation between flows.
- For each flow, you MUST scan the local sfdx project to populate `inflightMetadata` with custom objects/fields **specific to that flow prompt**.
- Each flow pipeline MUST have its own `inflightMetadata` containing only the objects/fields relevant to that particular flow.
