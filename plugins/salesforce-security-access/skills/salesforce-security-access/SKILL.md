---
name: salesforce-security-access
description: "Design and audit Salesforce CRM access (permission sets, groups, muting, OWD, sharing), Agentforce runtime security, and org security posture (My Trust Center, file scanning, guest boundaries). Use salesforce-apex for Apex security or data360-activation-governance for Data 360."
---

# Salesforce Security & Access

Least-privilege CRM access design, Agentforce runtime authorization, and org security posture review. Select the mode below and load only its reference file first.

## Mode Routing

| Mode | When to use | Reference |
| --- | --- | --- |
| CRM Access Design | Permission Sets, Permission Set Groups, muting sets, OWD, sharing rules, access matrices, allow/deny user tests | [crm-access-design.md](references/crm-access-design.md) |
| Agentforce Runtime Security | Employee vs Service vs channel agent execution identity, backing-action authorization, Trust Layer masking vs trace/transcript controls | [agentforce-runtime-security.md](references/agentforce-runtime-security.md) |
| Org Security Posture | My Trust Center / Health Check triage, file upload malware scanning, Experience Cloud & guest user boundaries | [org-security-posture.md](references/org-security-posture.md) |

## Core 2026 Invariants

- **Layered authorization**: Object CRUD, Field-Level Security (FLS), and Record Sharing (OWD, hierarchy, sharing rules) are independent layers. Sharing alone never grants CRUD/FLS, and hiding UI elements is never security.
- **Additive grants and muting**: Permission sets are additive. A muting permission set only suppresses grants within its own Permission Set Group (PSG); it does NOT revoke grants from profiles, direct permission sets, or other PSGs. Wait for PSG recalculation (`Status = 'Updated'`) before evaluating tests.
- **Agent execution identity**: Employee agents run as the logged-in user; Service agents run as a designated agent user (`default_agent_user` under `access`) or verified site/channel user. A Contact ID in context never enforces record access; scope sensitive actions to a verified customer identity inside backing Apex/Flow/API.
- **Trust Layer masking boundary**: Einstein Trust Layer LLM data masking is disabled for Agentforce agents, including prompt templates invoked through agent actions. Provider zero retention does not prove zero stored Salesforce traces or transcripts.
- **Apex/Flow boundary**: API 67.0+ defaults Apex database operations to user mode and rejects `WITH SECURITY_ENFORCED`; API 66.0 and earlier differ. Configuration cannot compensate for `without sharing` or `SYSTEM_MODE` code.
- **Guest & upload boundaries**: Keep external OWD Private, guest sharing rules narrowly read-only, and treat uploaded files as untrusted (prompt-injection and malware risk; platform download settings do not replace dedicated malware scanning).

## Hard Org & Safety Gates

1. **Read-only by default**: A design, audit, or troubleshooting request authorizes read-only inspection and local drafts only. Never silently assign permission sets, edit OWD/sharing, or change org security settings without explicit authorization for the target org and scope.
2. **Explicit target identity**: Pin `--target-org <username-or-alias>` and inspect org type, release/API version, licenses, and effective running user before any check. Never print access tokens or raw auth payloads.
3. **No broad elevation shortcuts**: Never add `View All Data`, `Modify All Data`, `View All`, or `Modify All` to fix a single symptom. If elevated privileges are genuinely required, document affected scope, named owner, and rollback steps.
4. **No regulatory certification claims**: Never claim HIPAA, PCI-DSS, SOC 2, GDPR, or FedRAMP compliance or certification. Report concrete technical controls, verified boundaries, and remaining gaps.

## Execution & Deliverable Contract

1. Resolve target org, persona classes (employee, integration, agent, external/guest), and actual execution user.
2. Run read-only discovery (`PermissionSetAssignment`, `ObjectPermissions`, `FieldPermissions`, `SecurityHealthCheckRisks`, `Network`) or inspect local metadata when offline.
3. Deliver a desired-vs-effective matrix, minimal proposed diff (metadata XML only for verified API names), explicit rollback steps, and allow/deny sandbox test plan.

## Verification Integrity

- **Separate evidence tiers**: Explicitly distinguish (a) local drafts/static inspection, (b) executed sandbox allow/deny tests with synthetic records, and (c) untested production behavior.
- **Non-admin proof required**: An admin pass proves nothing about an employee, service agent, integration, or guest identity. Test allowed and denied paths, separate field read vs write, unrelated records, direct-grant-vs-muting, and cross-customer denial.
- **No org connection**: Produce an actionable local draft and list every unresolved live-org check explicitly. Do not invent API names, IDs, or test results.

## Companion Handoffs

- Apex `USER_MODE` / sharing / `stripInaccessible` code fixes: `salesforce-apex`
- Flow context and system-vs-user mode repairs: `salesforce-flow`
- Experience Cloud LWC implementation: `salesforce-lwc`
- Named/External Credential callout setup: `salesforce-integrations`
- Data 360 data spaces, masking, and policy enforcement: `data360-activation-governance`
- Agent authoring, static review, and behavioral tests: `agentforce-build`, `agentforce-review`, `agentforce-test`
- Metadata validation, deployment, and trace audits: `salesforce-devops-deploy`, `agentforce-observe`
