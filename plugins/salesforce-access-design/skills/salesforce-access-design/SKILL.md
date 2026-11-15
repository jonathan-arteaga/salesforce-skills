---
name: salesforce-access-design
description: "Design or troubleshoot Salesforce CRM access using permission sets, permission set groups, object and field permissions, and record sharing. Use for access matrices, least-privilege plans and allowed/denied user tests. Not Data 360 policy configuration or a full adversarial security audit."
---

# Salesforce Access Design

## Operating contract

Read [current Salesforce guidance](references/current-salesforce/guide.md) before making product claims. Discover available tools and inspect their schemas or CLI help; do not assume a connector or command exists. Use the Salesforce Docs MCP search and fetch when available, otherwise official Salesforce documentation. Verify target org, release/API version, licenses, feature availability and effective execution identity. Never print tokens or raw auth payloads.

Use existing task context before asking for missing information. With no org connection, produce a useful local draft and mark unknowns explicitly. Do not invent API names, IDs, success results or deployed resources. A review or design request authorizes read-only inspection and drafts; mutations require authorization for the intended org and scope. Continue already-authorized work without repeated confirmations. Use synthetic records in tests and preserve prior configurations for rollback.

Read [the workflow reference](references/workflow.md) for decisions and failure handling. Copy [the deliverable template](assets/workbook.md) into the project, fill it with evidence, and keep it outside the installed skill. Read [acceptance cases](references/acceptance.md) before finishing. Report draft checks, executed sandbox checks and untested production behavior separately.

## Workflow

1. Establish the business operations per persona: object, field, create/read/update/delete, record population and sensitive fields. Identify employee, integration, agent and external users separately. Resolve the actual running user for each action; a successful admin test proves little about another identity.
2. Read current assignments, profiles, permission sets/groups, object/field grants, org-wide defaults, hierarchy and relevant sharing/restriction settings through available read-only tools. Record unavailable evidence. Distinguish missing permissions, record filtering, license limits and session/context differences.
3. Build a desired-versus-effective matrix. Account for additive grants from other assignments: muting a permission within one group does not revoke grants from elsewhere. Object access, field access and record access are separate layers; sharing alone does not grant CRUD/FLS.
4. Propose focused permission sets and persona groups, plus the narrow record-sharing changes needed. Avoid broad View All/Modify All grants to fix a single symptom. If those privileges are actually required, document the affected scope and rationale. Delegate code security to platform-apex-generate/review tooling; do not assume configuration compensates for system-mode code.
5. Produce deployment-ready metadata only for supported types and known API names; otherwise produce an explicit configuration draft with unresolved fields. Delegate deployment to platform-metadata-deploy when available, or give a validated manual handoff. Do not silently assign permissions during design.
6. Run authorized sandbox allow/deny cases as the intended identities. Check field read and write separately, unrelated records, alternate permission assignments and agent execution contexts. Verify permission-group recalculation has completed before treating results as final.
7. Deliver the matrix, proposed diff, evidence and rollback steps. Route Data 360 policies to data360-governance; route agent behavior verification to agentforce-test. If a companion is unavailable, preserve the handoff artifact and state the limitation.
