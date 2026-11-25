# Flow Architecture, Bulk Safety, and Omni-Channel Routing

## Choosing the Right Flow Type

| Flow Type | Best Use Case | Key Guardrails |
| --- | --- | --- |
| Record-Triggered (Before-Save) | Fast same-record field defaults and derivations | Zero extra DML; no Subflows; no related-record DML or callouts |
| Record-Triggered (After-Save) | Child/related records, emails, Subflows, async paths | Requires saved IDs; move HTTP callouts to async path |
| Screen Flow | Guided user experiences and LWC screen embedding | Default to User Context; isolate elevated ops in narrow Subflow |
| Scheduled Flow | Recurring batch jobs on filtered records | Put cadence on `<start><schedule>` and record filters on `<start>` so `$Record` runs per match without a manual Loop |
| Autolaunched (No-Trigger) | Reusable Subflows, Agentforce actions, Apex/API invoked | Literal no-trigger start; explicit input/output contracts |
| Platform Event-Triggered | Decoupled event-driven automation | Idempotent updates; watch Automated Process user context |
| Omni-Channel Flow | Routing Messaging, Chat, Voice, and Agentforce Service Agents | Explicit `Route Work` target, fallback queue, and `recordId` input |

## Naming, Modularity, and Legacy Sunset

- **Naming convention**: Name Flows `[Object]_[Trigger]_[Purpose]` (e.g., `Account_BeforeSave_SetOwnerTier`), label every element descriptively (never `Update Records 1`), name variables clearly (`varAccountId`, `colCases`), and populate the Flow `<description>` with purpose, trigger, and run context.
- **Single responsibility**: Keep each Flow focused on one object and trigger event; extract shared logic (notifications, error logging, calculations) into reusable Subflows, and externalize mutable thresholds/mappings into Custom Metadata Types (CMDT).
- **Legacy migration**: Process Builder and Workflow Rules reached end of support December 31, 2025; migrate remaining legacy rules to Record-Triggered Flows rather than extending them.

## Bulkification, Entry Conditions, and Recursion Guards

Flows share these per-transaction governor limits with Apex triggers and all other automation on the same object:

| Resource | Synchronous Limit | Asynchronous Limit |
| --- | --- | --- |
| SOQL queries | 100 | 200 |
| DML statements | 150 | 150 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap size | 6 MB | 12 MB |

- **No DML or SOQL in loops**: Hoist Get Records before the Loop; accumulate mutated records via Assignment into a collection variable; run a single Update/Create/Delete after the Loop. For collections exceeding 2,000 records, use Scheduled Paths or Apex batching/cursors.
- **Counting records cleanly**: Use a single Assignment with `<operator>AssignCount</operator>` from a Get Records collection into a Number variable — never emit duplicate assignment names or loop-increment counters.
- **Selective entry conditions**: Put Record Type, status, and `ISCHANGED` filters on the Start element (never in a downstream Decision after unnecessary traversal).
- **Recursion prevention**: Guard entry conditions so an update does not re-trigger the same Flow (check prior value or verify target field is not already set to the target state).
- **No hardcoded IDs**: Resolve RecordTypeId, QueueId, and thresholds via Custom Metadata Types (CMDT) or DeveloperName lookups.

## Fault Paths & Error Observability

- Attach a **Fault Connector** to every Create, Update, Delete, Get (when critical), Apex Action, and HTTP Callout element.
- Route faults to a centralized **Error-Handling Subflow** that records Flow API name, `$Record.Id` (or `recordId`), running user, and `{!$Flow.FaultMessage}` to a custom error log object and notifies admins.
- Never silently swallow faults with empty connectors or vague "An error occurred" screens; for transient external callouts, add bounded retry or async queuing.

## Omni-Channel Agentforce Routing Flows

- Accept `recordId` (the Messaging Session or work item ID) and any channel context variables (`input_record`) cleanly as input-only variables.
- Resolve customer/contact context safely before routing; handle null/unmatched records gracefully without exposing other customers' data.
- Configure the **Route Work** action to route to the intended **Agentforce Service Agent** (or Service Channel / Queue) with a verified **Fallback Queue** and **Routing Configuration** so unhandled escalations never strand customers.
- Document escalation triggers (human handoff intent, agent error, offline hours) and verify the Agentforce Service Agent is active and linked before activating the routing Flow.
