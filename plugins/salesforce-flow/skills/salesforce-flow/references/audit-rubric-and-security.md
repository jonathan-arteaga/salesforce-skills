# Flow Security Traps and 8-Domain Audit Rubric

## Execution Context & Security Traps (Critical Review)

Inspect `<runInMode>` and trigger type on every Flow — never assume "with sharing" enforces object or field security:

| Flow Run Mode | Record Sharing | Object CRUD & Field FLS | Security Implication |
| --- | --- | --- | --- |
| User Context (`DefaultMode`) | Enforced | Enforced | Default for Screen Flows; safest baseline for interactive UI |
| System Context with Sharing (`SystemModeWithSharing`) | Enforced | **BYPASSED** | Still leaks restricted fields or objects unless guarded manually |
| System Context without Sharing (`SystemModeWithoutSharing`) | **BYPASSED** | **BYPASSED** | Full org data access; default for Record-Triggered Flows |

- **Hybrid Screen Flow pattern**: Keep parent Screen Flows in **User Context**; delegate only tightly scoped privileged operations to a dedicated System-Context Subflow with explicit input validation.
- **Agentforce & Experience Cloud trap**: Invoking an Autolaunched Flow as an Agentforce action does **not** automatically make a privileged Flow customer-safe. Verify the agent's effective execution identity, check external/guest user data exposure, and never trust customer-supplied IDs without ownership verification.
- **Apex Invocable & Manage Flows**: Users invoking Flows that call `@InvocableMethod` Apex must have explicit Apex class access via Permission Set. Treat `Manage Flows` as a high-privilege admin permission.

## 8-Domain 100-Point Audit Rubric

Evaluate `.flow-meta.xml` (or design narrative, labeling unverified XML details) across all 8 domains:

| # | Domain | Max Pts | Critical Checks |
| --- | --- | --- | --- |
| 1 | Flow Type & Trigger Selection | 15 | Before-Save for same-record updates; async path for callouts; no Process Builder/Workflow remnants |
| 2 | Naming & Documentation | 5 | `[Object]_[Trigger]_[Purpose]`, descriptive element labels, Flow description, zero hardcoded IDs |
| 3 | Bulkification & Governor Limits | 25 | Zero DML or SOQL inside Loops; collection Assignment + post-loop DML; 200-record bulk safe |
| 4 | Error Handling & Fault Paths | 20 | Fault Connector on every DML/Callout/Action; centralized error Subflow logging `$Flow.FaultMessage` |
| 5 | Security & Running Context | 15 | Explicit `<runInMode>` review; hybrid Screen Flow pattern; Agentforce/Experience Cloud exposure check |
| 6 | Design Architecture & Modularity | 10 | Single responsibility, Subflow extraction, CMDT externalization, readable canvas |
| 7 | Entry Conditions & Performance | 8 | Tight Start filters (`ISCHANGED`, Record Type at Start), recursion guard, date formulas on schedules |
| 8 | Deployment & Version Management | 2 | Draft-first validation, dependencies ordered, XML in source control, inactive version hygiene |

- **Deductions**: `CRITICAL` deducts 50–100% of domain points; `WARNING` deducts 20–40%; `PASS` awards full points.
- **Grades**: `90–100` = **A** (Production Ready), `75–89` = **B** (Minor Improvements), `60–74` = **C** (Fix Before Activating), `40–59` = **D** (Major Rework), `0–39` = **F** (Do Not Activate).

## High-Priority Anti-Pattern Triggers

Immediately flag as `CRITICAL` (blocks activation):
- Any `recordCreates`, `recordUpdates`, `recordDeletes`, or `recordLookups` reachable inside a `loops` path
- Missing `faultConnector` on DML, Apex Action, or HTTP Callout elements
- After-Save Flow executing an Update Records on `$Record` for simple same-record field changes
- Hardcoded 15- or 18-character Salesforce Record IDs in filters, formulas, or assignments
- Synchronous HTTP callout without an asynchronous path

## Multi-Flow Audit & Report Format

- For multi-flow repositories, scan `*.flow-meta.xml` in scope, score each Flow individually, and produce a combined Project Summary highlighting average health score and cross-flow contention on the same object (shared DML/SOQL budgets, conflicting triggers).
- Order every report's findings **CRITICAL -> WARNING -> IMPROVEMENT**, naming the exact element API name/label, quoting relevant XML when present, stating the concrete failure risk, and providing the exact remediation.
