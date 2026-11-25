# Flow Authoring Paths and Pre-Activation Testing

## Discover Available Tooling First

Salesforce supports multiple valid Flow authoring paths. Always inspect available tools before choosing, and never pretend an unavailable connector ran:

### Path A: Local Metadata API / SFDX Draft Path (Always Available Locally)

Use retrieved or project `.flow-meta.xml` files and the current Salesforce Flow Metadata API schema:
1. Ground every object, field, picklist value, and action against local SFDX metadata (`force-app/.../objects/`) or org describe output — never invent API names.
2. Author clean XML with `<status>Draft</status>`, meaningful element labels (never `Update Records 1`), Flow `<description>`, and `<processMetadataValues>` `CanvasMode`=`AUTO_LAYOUT_CANVAS` for canvas-based flows (non-canvas types like `CustomerLifecycle` omit it).
3. Generate only requested actions — never invent unrequested Chatter posts, emails, or side effects that reference undefined types.
4. Validate against the target sandbox/scratch org using `sf project deploy validate --source-dir <flow-path> --target-org <alias>` (or dry-run deployment).

### Path B: MCP Connector Pipeline (Only When Discovered)

Use this connector workflow **only** if `execute_metadata_action` is present with the 3-step actions:
1. **`fetchGroundedObjectMetadata`**: Pass single-flow `userPrompt` and `inflightMetadata` as a JSON **ARRAY** (`[]` if no local custom objects, or structured objects using exact keys `apiName`, `type`, `label`, `values`, `referenceTo` — never a string `"[]"` or prose descriptions).
2. **`flowElementSelection`**: Pass the exact same `userPrompt`, the raw `groundingMetadata` string from Step 1 (do not re-serialize), and `operationId: ""`.
3. **`flowElementGeneration`**: Loop with Step 2's `operationId` and `requestSource: "A4V"` until `isComplete` is `true` (never pause mid-loop; stop only on error). Extract XML from `result`.
- **Multi-flow requests**: Split into one focused `userPrompt` per Flow with its own scoped `inflightMetadata`, and run each 3-step pipeline **sequentially** (never interleaved or combined).
- **Returned XML integrity**: Preserve pipeline-returned XML as-is unless explicitly fixing a deployment/validation error; surface missing `AUTO_LAYOUT_CANVAS` as a pipeline gap instead of silently rewriting.

Example `inflightMetadata` entry (exact keys required):

```json
[
  {
    "type": "CustomObject",
    "apiName": "CustomerRequest__c",
    "label": "Customer Request",
    "fields": [{ "apiName": "Status__c", "type": "Picklist", "label": "Status", "values": ["New", "Closed"] }],
    "relationships": []
  }
]
```

## Pre-Activation Validation & Testing Gate

Never activate a Flow before executing and documenting these checks in a sandbox or scratch org:

| Test Category | What to Verify |
| --- | --- |
| Draft deployment | `sf project deploy validate` succeeds with dependencies (objects, fields, CMDTs, Apex Invocables, Subflows) deployed first |
| Bulk test (200+ records) | Mass insert/update of 200 records passes within SOQL/DML/CPU limits with no loop violations |
| Positive & Negative tests | Valid records trigger expected changes; non-matching records and unauthorized personas do not mutate protected data |
| Fault path test | Forced validation rule or DML failure routes cleanly through the Fault Connector and logs context |
| Recursion test | Updating a record twice or mutating the target field does not re-enter the Flow in a loop |
| Unified Logic / Flow Tests | Run native Flow Tests (`FlowTest` metadata) alongside Apex unit tests on the same object to verify combined automation safety |

## Deliverable Checklist

- Path to `.flow-meta.xml` (saved as `Draft`) and any supporting Subflow/CMDT references
- Authoring path used (Local Metadata API Draft vs MCP Connector) and schema grounding evidence
- Exact `sf project deploy validate` output (or explicit `unavailable: <reason>` if no org connection)
- Executed sandbox bulk/negative/fault/recursion test results vs remaining unverified checks before authorized activation
- Explicit confirmation that Flow activation requires authorized approval after Draft checks pass
