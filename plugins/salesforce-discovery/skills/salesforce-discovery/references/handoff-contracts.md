# Handoff Contracts & Sibling Routing

Discovery ends when evidence is sufficient for the next bounded step. Reopen discovery only when new facts, release changes, or scope shifts invalidate prior decisions.

## Standard Handoff Payload

Pass only sanitized, decision-relevant facts inside the customer's authorized project workspace (never credentials, session tokens, or bulk PII):

1. **Target Identity:** Exact org/environment ID or alias, Salesforce release/API version, inspected artifact revisions, and sandbox-versus-production parity notes.
2. **Evidence & Conflict Ledger:** Observed, stakeholder-reported, inferred, and unknown facts with source, date, environment, and any policy-versus-implementation conflicts.
3. **Outcomes & Scope:** Agreed job, affected audience, baseline metrics, proposed targets, narrow first release, and explicit non-goals.
4. **Capability & Reuse Decisions:** Per-capability lane (`greenfield`/`brownfield`/`hybrid`), intervention choice (`no-agent`/`reuse`/`adapt`/`build`/`defer`), authoritative data owners, and existing behaviors to preserve.
5. **Risk, Validation & Rollout:** Side effects, dependency risks, acceptance and negative test scenarios, readiness label (`READY FOR DESIGN`/`CONDITIONAL`/`BLOCKED`) with next proof, stop/rollback criteria, and reconciliation owners.

## Canonical Sibling Routing Map

Route downstream execution strictly to the owning sibling skill:

| Downstream Need | Owning Sibling Skill |
| --- | --- |
| Agent architecture, persona, conversation design, voice UX, topics/actions spec | `agentforce-design` |
| Agent Script, Builder metadata, Prompt Builder templates, grounding/retrievers | `agentforce-build` |
| Existing agent configuration or architecture review | `agentforce-review` |
| Agent test plans, escalation/regression/runtime test execution | `agentforce-test` |
| Agent telemetry, session analytics, quality/latency/cost observability | `agentforce-observe` |
| Permission sets/groups, CRUD/FLS, sharing, agent user identity, RBAC | `salesforce-security-access` |
| Data 360 ingestion, DLO/DMO modeling, identity resolution, SQL/calculated insights | `data360-data-pipeline` |
| Data 360 data spaces, policy enforcement, consent, segmentation, activation | `data360-activation-governance` |
| Core CRM schema, custom objects/fields, SOQL/DML data operations | `salesforce-schema-data` |
| Reports, dashboards, CRM Analytics | `salesforce-analytics` |
| Apex classes, triggers, batch/queueable logic | `salesforce-apex` |
| Record-triggered, autolaunched, or screen Flows | `salesforce-flow` |
| Lightning Web Components and Experience Cloud UI components | `salesforce-lwc` |
| REST/SOAP, Named Credentials, Platform Events/CDC, Agent API integration | `salesforce-integrations` |
| Metadata packaging, CI/CD pipelines, safe sandbox/prod deployment | `salesforce-devops-deploy` |
| Standalone interactive HTML or print/PDF setup tutorials and enablement guides | `salesforce-tutorial-builder` |

## Freshness, Reopen & Unavailable Sibling Rules

- **Stop re-discovery:** Once target identity, evidence ledger, reuse choices, and acceptance criteria are current, move directly to the receiving sibling rather than repeating workshops.
- **Targeted reopen:** Reopen only affected decisions when an org upgrade, new managed-package version, policy change, or discovered side effect invalidates an assumption.
- **Authorization boundary:** A discovery handoff authorizes planning or drafting only—never production writes, feature activation, or deployment.
- **Unavailable sibling:** If a receiving sibling skill is unavailable in the active runtime, emit the complete bounded handoff payload above, explicitly name the missing capability, and stop without pretending the downstream skill ran.

## Pre-Handoff Verification Gate

Before transferring control to a downstream sibling skill, confirm:

- Target org/environment identity, release, and inspected artifact revisions are recorded (or explicitly marked `Not verified`).
- Every finding carries its provenance tag (`observed`, `stakeholder-reported`, `inferred`, or `unknown`) and zero secrets appear in the payload.
- Each capability has an explicit readiness label (`READY FOR DESIGN`, `CONDITIONAL`, or `BLOCKED`), next proof, and named operational owner.
