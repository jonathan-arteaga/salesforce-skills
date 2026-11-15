## AUDIT DOMAINS

Evaluate every Flow across **all 8 domains**. Flag each finding as:

| Severity | Meaning |
| --- | --- |
| **CRITICAL** | Blocks activation / causes data loss or governor failures |
| **WARNING** | Degrades performance, maintainability, or security |
| **PASS** | Meets the standard |

---

### Domain 1: Flow Type & Trigger Selection — 15 pts

- Correct flow type for the use case?<br />*(Screen Flow, Record-Triggered, Schedule, Platform Event, Autolaunched)*
- Same-record field updates use **Before-Save** (NOT After-Save + Update Records)?<br />Before-Save consumes ZERO DML on the triggering record — 10x faster at scale.<br />After-Save must issue a separate UPDATE statement per transaction.
- After-Save used correctly **only** when record ID is needed?<br />*(e.g., creating child records, posting to Chatter, sending emails)*
- Combined Before-Save + After-Save on same object is acceptable and is the recommended<br />enterprise pattern — flag if execution order is unclear.
- Any legacy **Process Builder** or **Workflow Rules** in use?<br />*(End of official support: December 31, 2025. Bugs will not be fixed.)*
- HTTP callouts / outbound messages on a synchronous path? Must be async.

---

### Domain 2: Naming Conventions & Documentation — 5 pts

- Flow API Name follows: `[Object]_[Trigger]_[Purpose]`<br /><i>Examples: </i>*`Account_BeforeSave_SetOwnerTier`*<i>, </i>*`Lead_AfterSave_CreateFollowUpTask`*
- All elements use descriptive labels — NOT defaults like `"Update Records 1"`, `"Decision"`,<br />`"Get Records 2"`, `"Assignment 3"`, `"Loop 1"`
- Flow has a **Description** that explains purpose, trigger conditions, and last modified context
- Variable naming is meaningful (e.g., `varAccountId`, `colOpportunities`, `inpEmailAddress`) —<br />not `v1`, `v2`, `temp`, etc.
- **NO hardcoded Salesforce IDs** anywhere (RecordTypeId, UserId, QueueId, OwnerId, etc.) —<br />IDs change between sandbox and production environments
- **Custom Metadata Types (CMDT)** used for configuration values instead of hardcoded literals

---

### Domain 3: Bulkification & Governor Limits — 25 pts

> **HIGHEST PRIORITY** — most common cause of production failures

#### DML Inside Loops — CRITICAL if found

- Are **Create Records**, **Update Records**, or **Delete Records** elements placed **inside** a Loop element? Each execution = one DML statement per record. At 150 DML limit per transaction, this fails on any bulk operation.
- **Fix:** Use Assignment elements inside the loop to build a record collection, then place a single Update Records element **after** the loop ends.

#### SOQL Inside Loops — CRITICAL if found

- Are **Get Records** elements placed **inside** a Loop element? Each execution = one SOQL query per iteration. At 100 SOQL limit per transaction, this fails fast.
- **Fix:** Move Get Records before the loop, store results in a collection, loop over the<br />collection.

#### Bulk Volume

- Collections exceeding 2,000 records? Use Scheduled Path with batching.
- Is the flow designed to handle 200-record bulk saves correctly?

#### Governor Limits Reference (per transaction)

| Resource | Limit |
| --- | --- |
| SOQL | 100 queries max |
| DML | 150 statements max |
| CPU time | 10,000 ms (sync), 60,000 (async) |
| Heap size | 6 MB (sync), 12 MB (async) |

> Flows share these limits with **all** other automation in the same transaction (Apex triggers,<br />other Flows, Process Builder remnants).

---

### Domain 4: Error Handling & Fault Paths — 20 pts

- Does **every** Create Records, Update Records, Delete Records element have a **Fault Connector** attached? Unhandled faults become invisible data problems.
- Does **every** external callout (HTTP callout, Platform Event, external service) have a Fault Connector?
- Does the fault path surface meaningful information?
  - **Required:** Flow name, record ID, `{!$Flow.FaultMessage}`, relevant field values
  - **Not acceptable:** generic "An error occurred" screen with no context
- Is a **centralized error-handling Subflow** used to avoid duplicate fault logic?<br />*Pattern: every Flow's fault path calls the same error-handler Subflow*
- For enterprise orgs: are errors logged to a custom object for audit trail?
- Admin notification email includes: Flow name, record context, full error message (enough detail to diagnose without opening the flow)
- Try-catch retry pattern used for transient external callout failures?

---

### Domain 5: Security & Running Context — 15 pts

- Screen Flows: run in **User Context** by default? System context should **only** be elevated for specific privileged Subflows, never for the entire parent Screen Flow.
- **Hybrid pattern** for Screen Flows needing elevated access:<br />Parent Flow = User Context → privileged operations in System-Context Subflow
- Record-Triggered Flows always run in **System Context Without Sharing** — is access to<br />sensitive data fields justified and intentional?
- "Manage Flows" permission treated as sensitive admin permission? It grants ability to view and modify all data in the org.
- Apex Invocable Methods used in the Flow? User must have explicit access via Profile or<br />Permission Set (enforced since Summer '19).
- Experience Cloud flows reviewed for external user data exposure?
- Running context documented in Flow description?

---

### Domain 6: Design Architecture & Modularity — 10 pts

- **Single Responsibility:** Does each Flow focus on one object, one trigger event, one clear purpose?
- Reusable logic extracted into Subflows?<br />*(error handling, notifications, complex calculations, task creation)*
- Subflows used to promote consistency across multiple parent Flows?
- Business logic that changes frequently externalized to CMDT?<br />*(routing rules, threshold values, email templates, record type IDs)*
- Flow complexity: is the canvas readable without zooming out to 10%? If yes, consider breaking it into Subflows.
- "One Flow per object per trigger event" strategy documented for the org?
- **Note:** Subflows are NOT available in Before-Save Record-Triggered Flows<br />*(as of Summer '25 — verify for your release)*

---

### Domain 7: Entry Conditions & Performance Optimization — 8 pts

- Record-Triggered Flows have tight entry conditions to avoid firing on every record save when irrelevant fields change?
- Entry conditions use field-change detection correctly?<br />*(**`ISCHANGED`*<i>, specific field value checks, </i>*`{!$Record.FieldName}`*<i> comparisons)</i>
- Record Type filtering done at the **Start Element** (not via Decision after the flow starts executing) — this avoids unnecessary element traversal
- **Recursion prevention:** do entry conditions prevent the flow from triggering itself in a loop?<br />*Pattern: check if the field being updated was already set correctly*
- Tested against bulk scenarios (mass update of 200 records)?
- Scheduled Flows: time filter uses date formulas (not hardcoded dates)?
- Multiple Flows on same object: is the combined execution load profiled?

---

### Domain 8: Deployment & Version Management — 2 pts

- Flow developed and tested in sandbox or scratch org first?<br />**NEVER build or activate directly in production.**
- Flow status managed correctly: Active vs Draft vs Inactive during deployment?<br />Metadata API v44+ only fetches the latest version (active or draft).
- Dependencies deployed first?<br />*(custom objects, custom fields, other Flows, Apex classes, CMDTs)*
- Old inactive Flow versions cleaned up to avoid confusion?
- Flow XML tracked in source control?
- CI/CD pipeline includes static analysis of Flow XML before deployment?
- Deployment includes Flow Definition to control which version activates?

---
