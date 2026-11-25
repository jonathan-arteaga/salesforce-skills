---
name: salesforce-flow
description: "Design, generate, and audit Salesforce Flows (Record-Triggered, Screen, Scheduled, Autolaunched, Omni-Channel routing) for bulk safety, fault paths, and run-context security. Use salesforce-apex for Apex, agentforce-build for agent setup, and salesforce-devops-deploy for rollouts."
---

# Salesforce Flow

End-to-end skill for designing, generating, validating, and auditing Salesforce Flows, including Omni-Channel Agentforce routing flows and security run-context reviews.

## Mode Routing

Select the active mode first and read only the matching reference before proceeding:

| Mode | When to Use | Reference |
| --- | --- | --- |
| Design & Routing | Choose Before-Save vs After-Save, bulk/fault/recursion design, Omni-Channel Agentforce routing | [flow-design-and-routing.md](references/flow-design-and-routing.md) |
| Generate & Test | Author Flow XML via local Metadata API Draft path or MCP connector pipeline; run pre-activation tests | [authoring-paths-and-testing.md](references/authoring-paths-and-testing.md) |
| Audit & Security | Score existing `.flow-meta.xml` or design narratives across 8 domains; audit run-context security traps | [audit-rubric-and-security.md](references/audit-rubric-and-security.md) |

## Core 2026 Invariants

- **Before-Save vs After-Save**: Use Before-Save for same-record field updates (zero extra DML; no Subflows). Use After-Save only when saved record IDs, related-record DML, emails, Subflows, or async callouts are required. Process Builder and Workflow Rules reached end of support Dec 31, 2025.
- **Zero DML / SOQL in Loops**: Never place Get, Create, Update, or Delete Records inside a Loop. Query before the loop, build a record collection via Assignment inside the loop, and execute one bulk DML after the loop.
- **Entry Conditions, Recursion & Faults**: Filter at the Start element (`ISCHANGED`, Record Type, specific status transitions) to prevent wasted runs and recursive self-triggers. Attach Fault Connectors to every DML, Action, and Callout element; log Flow name, record ID, and `$Flow.FaultMessage` without swallowing errors.
- **System-Context Security Trap**: Inspect actual Flow run context. **System Context with Sharing still bypasses CRUD and FLS**; System Context without Sharing also bypasses record sharing. Agentforce action context does not automatically make a privileged Flow customer-safe.
- **Authoring Path Honesty**: Discover available tools first. Both local Metadata API Draft XML and a discovered MCP `execute_metadata_action` connector are valid paths; never fabricate an unavailable MCP pipeline.

## Hard Org & Safety Gates

- Always author and validate Flows as `Draft` in a sandbox or scratch org. Never build or activate directly in production.
- Never hardcode Salesforce Record IDs (RecordTypeId, QueueId, OwnerId, UserId); use Custom Metadata Types, Get Records by DeveloperName, or formulas.
- Before authorized activation, require 200-record bulk, negative/permission, fault-path, and recursion testing.
- For Omni-Channel Agentforce routing flows, verify fallback queue/agent ownership, Messaging Session input bindings, and non-privileged customer data boundaries.
- Never invent unrequested side-effect elements (e.g., unsolicited Chatter posts or emails) when generating Flow metadata.

## Required Deliverables & Verification Integrity

- **Generation output**: `.flow-meta.xml` saved as `Draft`, authoring path used (Local Metadata API vs MCP connector), schema grounding source, and pre-activation test plan/results.
- **Audit output**: 8-domain 100-point score + letter grade (A–F), prioritized findings (`CRITICAL -> WARNING -> IMPROVEMENT`) naming exact elements and XML evidence, plus run-context risk callouts.
- Separate **static XML/design audit findings** from **org-validated Draft checks** and **executed bulk/negative tests**. If org access or Flow test tooling is unavailable, label the draft as unvalidated and list exact missing checks.

## Draft Validation Commands

Validate Draft Flow metadata locally against an authorized sandbox or scratch org before any activation:

```bash
sf project deploy validate --source-dir force-app/main/default/flows/<FlowName>.flow-meta.xml --target-org <alias>
sf flow run test --class-names <FlowTestName> --target-org <alias>
```

## Cross-Skill Handoffs

- `salesforce-apex`: Apex triggers, `@InvocableMethod` classes, or complex bulk algorithms
- `salesforce-lwc`: custom Lightning Web Components embedded in Flow Screens
- `agentforce-build`: Agentforce topics, instructions, and Flow action bindings
- `salesforce-schema-data`: custom objects, fields, and Custom Metadata Types referenced by Flows
- `salesforce-security-access`: Permission Sets, Manage Flows governance, and Apex Invocable access
- `salesforce-devops-deploy`: CI/CD validation, Flow version activation, and org rollouts
