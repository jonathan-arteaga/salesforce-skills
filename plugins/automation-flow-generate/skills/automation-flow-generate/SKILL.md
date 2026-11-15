---
name: |-
  automation-flow-generate
description: |-
  Create Salesforce Flow metadata from a Salesforce process and trigger. Return a Flow definition. Use salesforce-flow-auditor to assess an existing Flow.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## Goal

Generate Salesforce Flow metadata grounded in the target schema and validate it. When the connected generator is available, use its 3-step pipeline (fetchGroundedObjectMetadata → flowElementSelection → flowElementGeneration).

## When to Use This Skill

Use this skill when you need to:

- Create any type of Flow (Screen, Autolaunched, Record-Triggered, Scheduled)
- Generate Flow metadata XML
- Automate business processes without code
- Build user-guided workflows or background automation
- Troubleshoot deployment errors related to Flows

## Specification

# Flow Metadata Specification

Use this workflow for Salesforce Flow requests. Discover available tools first. If the generator below is unavailable, use existing project/retrieved Flow metadata and the current Metadata API Flow schema for a local draft, then validate with the available CLI/org tools. If schema or validation is unavailable, provide a clearly labeled unvalidated draft or design and identify the missing inputs.

## Overview

Salesforce Flows are powerful automation tools that enable complex business process automation without code. Flows can collect and process data through interactive screens, execute logic and calculations, manipulate records, call external services, and trigger based on various events. Flow types include Screen Flows (user-guided), Autolaunched Flows (background processing), Record-Triggered Flows (database events) and Scheduled Flows (time-based).

## Flow Generation Pipeline

**Connector-specific path:** If the discovered `execute_metadata_action` tool supports these actions, follow its schema and the three steps in order. The following payloads describe that connector, not a universal Salesforce API. Do not invent this capability when it is absent. For the local metadata path, validate against the current Flow metadata schema and target org instead.

### MCP Connection Details

**When using this connector, all 3 pipeline steps use:**

- **MCP Tool Name:** `execute_metadata_action`
- <b>The </b>**`action`**<b> parameter</b> selects which pipeline step to run: `"fetchGroundedObjectMetadata"`, `"flowElementSelection"`, or `"flowElementGeneration"`

This connector uses a **strict 3-step pipeline**. Call each step in order when this path is available. The local metadata path uses its own validation instead.

### Step 1 (REQUIRED): Fetch Grounded Object Metadata (`fetchGroundedObjectMetadata`)

Fetches org schema metadata relevant to the flow generation request. This step is **mandatory** and must always be called first.

**Inputs (all required):**

- **userPrompt** (STRING, REQUIRED): The user's natural language request
- **inflightMetadata** (ARRAY, REQUIRED): Custom objects/fields from local sfdx project. Use empty array `[]` if none needed.

**Outputs:**

- **groundingMetadata** (STRING): Grounded object metadata for org schema relevant to the request, returned as a JSON string. **You must pass this directly to Step 2 — it is already a string and does not need to be serialized again.**

### Step 2 (REQUIRED): Flow Element Selection (`flowElementSelection`)

Selects flow elements (assignments, decisions, record ops, etc.) and their connections based on the user prompt and grounded metadata. This step is **mandatory** and must be called after Step 1.

**Inputs (all required):**

- **userPrompt** (STRING, REQUIRED): The user's natural language request (**must be the same value as Step 1**)
- **groundingMetadata** (STRING, REQUIRED): Org schema metadata (**must be the exact string returned from Step 1 output** — pass it directly, do NOT serialize it again)
- **operationId** (STRING, REQUIRED): Operation ID (use empty string `""` for first call)

**Outputs:**

- **operationId** (STRING): Operation ID. **You must pass this to Step 3.**
- **userOutput** (STRING): Reasoning for next steps. You can show this to the user.

### Step 3 (REQUIRED): Flow Element Generation (`flowElementGeneration`)

Generates flow metadata element by element. This step is **mandatory** and must be called after Step 2. <b>Must be called repeatedly in a loop until </b>**`isComplete`**<b> is </b>**`true`****.**

**Inputs (all required):**

- **operationId** (STRING, REQUIRED): Operation ID **from Step 2 output**
- **requestSource** (STRING, REQUIRED): The source of the request. Use **`"A4V"`** to get flow metadata in XML format.

**Outputs:**

- **isComplete** (BOOLEAN): Indicates if the flow generation is complete. **You must check this value.**
- **result** (STRING): Result of the flow element generation. Contains the final flow metadata <b>only when </b>**`isComplete`**<b> is </b>**`true`**.

**MANDATORY: Loop until complete. NEVER pause or ask the user to confirm continuation.**

- A flow can have **any number of elements**. Each call generates one element at a time, so you may need **many** iterations.
- Call `flowElementGeneration` with the `operationId` from Step 2 and `requestSource` (use `"A4V"` for XML output, empty string or other value for JSON).
- Check the `isComplete` output and the `result` field after each call.
- If `isComplete` is `false` **and no errors are returned**, you **MUST** call `flowElementGeneration` again with the <b>same </b>**`operationId`** from Step 2. **Do NOT ask the user if they want to continue. Do NOT pause. Do NOT summarize progress mid-loop. Just keep calling** — there is **no maximum** number of iterations.
- When `isComplete` is `true`, extract the flow metadata from the `result` field.
- If errors are returned, stop the loop and surface the error to the user.

**STRICT CONSTRAINTS (CRITICAL) — These rules apply to the XML returned by the generation pipeline:**

- DO NOT modify the content, values, or child nodes inside any block.
- DO NOT add new nodes, tags, attributes, or text (do not add missing labels, X/Y coordinates, etc.).
- DO NOT remove any existing nodes.

**Canvas mode.** A net-new canvas-based flow needs a `<processMetadataValues>` `CanvasMode`=`AUTO_LAYOUT_CANVAS` entry (independent of `BuilderType`) or it opens in **Free-Form**. STRICT CONSTRAINTS forbid hand-editing the XML, so this must come from the generation pipeline — if the returned XML lacks it, surface a pipeline gap; do NOT hand-edit. (Non-canvas types like `CustomerLifecycle` carry none — don't flag those.)

## inflightMetadata Format

**DATA TYPE: ARRAY (not string)**

**STRICT NAMING CONVENTION - MUST FOLLOW EXACTLY:**

| Property | Correct Name | Do NOT Use |
| --- | --- | --- |
| Object API name | `apiName` | `objectApiName`, `name`, `objectName` |
| Field API name | `apiName` | `fieldApiName`, `name`, `fieldName` |
| Field type | `type` | `fieldType`, `dataType` |
| Lookup target | `referenceTo` | `relatedTo`, `lookupTo`, `reference` |

When custom objects are needed (sample format showing multiple field data types):

```json
[
  {
    "type": "CustomObject",
    "apiName": "CustomerRequest__c",
    "label": "Customer Request",
    "fields": [
      {
        "apiName": "Status__c",
        "type": "Picklist",
        "label": "Status",
        "values": ["New", "In Progress", "Completed"]
      },
      {
        "apiName": "Priority__c",
        "type": "Number",
        "label": "Priority"
      },
      {
        "apiName": "AssignedTo__c",
        "type": "Lookup",
        "label": "Assigned To",
        "referenceTo": "User"
      },
      {
        "apiName": "Description__c",
        "type": "Textarea",
        "label": "Description"
      },
      {
        "apiName": "Email__c",
        "type": "Email",
        "label": "Contact Email"
      },
      {
        "apiName": "DueDate__c",
        "type": "Date",
        "label": "Due Date"
      },
      {
        "apiName": "IsUrgent__c",
        "type": "Boolean",
        "label": "Is Urgent"
      },
      {
        "apiName": "Amount__c",
        "type": "Currency",
        "label": "Amount"
      }
    ],
    "relationships": []
  }
]
```

**Supported field types**: Text, Textarea, Number, Picklist, Lookup, Email, Phone, URL, Date, Datetime, Boolean, Checkbox, Currency, Percent

When no custom objects needed:

```json
[]
```

### MANDATORY Decision Logic for inflightMetadata (DATA TYPE: ARRAY)

1. **REQUIRED - First**: Scan the local sfdx project for custom objects and fields that are relevant to the user's flow request.
2. **If relevant custom objects ARE found**: You MUST extract and pass them as an array of structured objects (see format above)
3. **If NO relevant custom objects found**: You MUST pass an empty array `[]` (NOT the string `"[]"`)
4. **NEVER**: Pass text descriptions, instructions, or string representations in inflightMetadata
5. **MANDATORY**: The data type MUST be ARRAY, not STRING

**Instructions for Vibes when custom objects ARE relevant:**

- Extract the object metadata and map to JSON properties:
  - `apiName`: The object's API name (with `__c` suffix for custom objects)
  - `label`: The object's display label
  - `type`: Set to `"CustomObject"`
  - `fields`: Array of field objects, each containing:
    - `apiName`: The field's API name (with `__c` suffix for custom fields)
    - `type`: The field type (Text, Number, Picklist, Lookup, etc.)
    - `label`: The field's display label
    - `values`: (Picklist only) Array of picklist values
    - `referenceTo`: (Lookup only) The target object API name
- Include only objects and fields that are relevant to the flow being generated

## Mandatory Enhancement Rules

- **userPrompt**: REQUIRED.
  - If the user requests a **single flow**: use the user's prompt as-is.
  - If the user requests **multiple flows**: you MUST **split** the request and write a <b>separate, focused </b>**`userPrompt`**<b> for each individual flow</b>. Each `userPrompt` must describe only ONE flow. Do NOT pass the entire multi-flow request as a single `userPrompt`. See the multiple flows section below for examples.
- **inflightMetadata**: REQUIRED. Always use ARRAY data type.
  - MUST use `[]` (empty array) when no custom objects needed
  - MUST use structured array of objects when custom objects are relevant
  - NEVER use string `"[]"` - this is incorrect
  - NEVER use text descriptions - only structured object metadata

## Flow Pattern Guidance

Consult [`references/flow-pattern-guidance.md`](references/flow-pattern-guidance.md) before Step 2 (element selection) for every flow, including scheduled flows and requests for multiple flows.

## Example Tool Calls

**Example 1: Standard objects only (no custom objects)**

**Step 1 - fetchGroundedObjectMetadata:**

```json
{
  "userPrompt": "Create a scheduled-triggered Flow named Daily_Good_Morning that runs daily at 6:00 AM and sends an email to the running user saying good morning.",
  "inflightMetadata": []
}
```

**Step 2 - flowElementSelection:**

```json
{
  "userPrompt": "Create a scheduled-triggered Flow named Daily_Good_Morning that runs daily at 6:00 AM and sends an email to the running user saying good morning.",
  "groundingMetadata": "<groundingMetadata string from Step 1 — pass directly, do not serialize again>",
  "operationId": ""
}
```

**Step 3 - flowElementGeneration (call in a loop):**

```json
{
  "operationId": "<operationId from Step 2>",
  "requestSource": "A4V"
}
```

Loop as in Step 3 (same `operationId`, `requestSource: "A4V"`) until `isComplete` is `true` or errors return; extract the XML from `result` then.

**Example 2: With custom objects from local sfdx project**

**Step 1 - fetchGroundedObjectMetadata:**

```json
{
  "userPrompt": "Create a flow that updates the status of a Customer Request when it's assigned",
  "inflightMetadata": [
    {
      "type": "CustomObject",
      "apiName": "CustomerRequest__c",
      "label": "Customer Request",
      "fields": [
        {
          "apiName": "Status__c",
          "type": "Picklist",
          "label": "Status",
          "values": ["New", "In Progress", "Completed"]
        },
        {
          "apiName": "AssignedTo__c",
          "type": "Lookup",
          "label": "Assigned To",
          "referenceTo": "User"
        }
      ],
      "relationships": []
    }
  ]
}
```

**Step 2 - flowElementSelection:**

```json
{
  "userPrompt": "Create a flow that updates the status of a Customer Request when it's assigned",
  "groundingMetadata": "<groundingMetadata string from Step 1 — pass directly, do not serialize again>",
  "operationId": ""
}
```

**Step 3 - flowElementGeneration (call in a loop):**

```json
{
  "operationId": "<operationId from Step 2>",
  "requestSource": "A4V"
}
```

Loop exactly as in Example 1's Step 3.

## CRITICAL Verification Checklist (MUST VERIFY BEFORE AND AFTER EVERY FLOW GENERATION)

**Failure to follow this checklist exactly will result in broken or missing flow metadata.**

- [ ] **Pipeline**: ALL 3 steps are called in strict order (fetchGroundedObjectMetadata → flowElementSelection → flowElementGeneration). No step is skipped, combined, or replaced by another tool/API. This pipeline is the ONLY way to generate flow metadata.
- [ ] **No manual metadata**: Flow metadata is NOT created, modified, or generated outside the pipeline, and no elements/attributes were added to the returned XML (no `<label>`, `<description>`, or any other node). The final XML must be identical to what the pipeline returned. **Exception:** if the user explicitly requested fixes to validation/deployment errors in already-generated XML, targeted manual edits are permitted.
- [ ] **userPrompt** contains a **single** flow prompt (multi-flow requests are split, one `userPrompt` each), holds the flow requirements (NOT `inflightMetadata`), and is passed identically to Step 1 and Step 2.
- [ ] **inflightMetadata** is ARRAY data type (NOT the string `"[]"`), is `[]` when no custom objects are needed, and otherwise holds structured object/field metadata scanned from the local sfdx project — never text descriptions.
- [ ] **groundingMetadata** from Step 1 output is passed directly to Step 2 input (already a string — do NOT serialize it again).
- [ ] **Step 3** is called in a loop with the same `operationId` from Step 2, `requestSource` always `"A4V"`, until `isComplete` is `true` or errors are returned — no pausing, no asking the user to continue, no matter how many iterations. Extract the XML from `result` only when `isComplete` is `true`.
- [ ] **Multi-flow**: Each flow's full pipeline is completed before starting the next, SEQUENTIALLY (never in parallel, never interleaved), and ALL requested flows are generated — do NOT stop after the first.
- [ ] **Canvas mode (read-only)**: a canvas-based net-new flow's XML carries a `<processMetadataValues>` `CanvasMode`=`AUTO_LAYOUT_CANVAS` entry. If absent, surface a pipeline gap — do NOT hand-edit (STRICT CONSTRAINTS forbid it). Non-canvas types like `CustomerLifecycle` carry none — don't flag those.
