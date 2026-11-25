---
name: salesforce-discovery
description: "Discover customer context, run Agentforce workshops, assess brownfield readiness, test industry fit, and scope Well-Architected solutions. Use agentforce-design for agent specs, agentforce-build for code, salesforce-security-access for RBAC, or salesforce-devops-deploy for rollout."
---

# Salesforce Discovery

Own customer discovery, Agentforce workshop facilitation, brownfield readiness, industry fit testing, reuse-versus-build decisions, and lightweight Well-Architected solution scoping. Produce evidence-backed discovery briefs, workshop artifacts, and bounded handoffs without forcing full discovery on a small, already-understood fix.

## Mode & Reference Routing

Select only the reference(s) needed for the active task and skip unrelated phases:

| Task / Mode | Load Reference |
| --- | --- |
| Brownfield/greenfield readiness, reuse-vs-build, Well-Architected scoping, discovery brief | [brownfield-and-solution-scoping.md](references/brownfield-and-solution-scoping.md) |
| Agentforce workshop prep, question bank, RACI map, use-case capture, branded output doc | [workshop-facilitation.md](references/workshop-facilitation.md) |
| Industry vertical hypotheses (12 verticals), cross-industry roles (7), situation overlays | [industry-patterns.md](references/industry-patterns.md) |
| Canonical sibling handoff payload and downstream delegation map | [handoff-contracts.md](references/handoff-contracts.md) |

## Execution Spine

1. **Scope outcome and lane:** Classify `greenfield`, `brownfield`, or `hybrid` per capability—never per customer logo. Confirm business sponsor, operational owner, target metric, deadline, and non-goals; ask only questions whose answers change a decision.
2. **Gather bounded evidence:** Inspect supplied diagrams, sanitized metadata, repo history, and policies first. Run read-only org discovery only with explicit authorization and confirmed org identity.
3. **Test fit and choose smallest intervention:** Record which industry assumptions customer evidence supports, changes, or rejects. Compare no-agent remediation, existing config reuse/adaptation, narrow assistive agent, and autonomous action.
4. **Trace impact and phased rollout:** Map touched Flows, Apex, validation/duplicate rules, integrations, and downstream consumers; define baseline tests, limited cohort, stop criteria, and rollback/reconciliation owners.
5. **Deliver brief and hand off:** Emit a discovery brief or workshop deliverable with per-capability readiness labels and route implementation to the owning sibling skill.

## Core 2026 Invariants

- **Evidence over stereotypes:** Customer facts, verified policies, and operating processes outrank generic industry patterns. Existing behavior shows what happens, not what should happen—surface defects instead of blessing them.
- **Five-pillar Well-Architected lens:** Evaluate cross-platform trade-offs using Salesforce's current five quality dimensions: **Trust**, **Reliability**, **Operational Excellence**, **Resource and Cost Optimization**, and **Fairness**. Never cite the retired three-pillar layout.
- **Single rule owner:** Preserve each approved business rule in one authoritative enforcement point rather than duplicating policy logic in prompts or exposing bundled staff screen flows directly to agents.
- **Non-compensable blockers:** Never assign numeric weights that average away an authorization gap, missing consent, compliance risk, or unbounded external mutation.
- **Customer-facing workshop standards:** Use current Agentforce terms (Service Agent, Topic, Action, Einstein Trust Layer), exclude internal metadata jargon, auto-add Compliance for FinServ/Healthcare/Government, and brand deliverables to the customer first.

## Hard Org & Safety Gates

- **Strictly read-only:** Discovery never mutates org metadata, deploys packages, enables features, broadens permissions, or exports bulk customer records.
- **Explicit authorization for org reads:** Confirm exact org identity, release, and sandbox-versus-production status before any read-only tool call.
- **Zero fabrication & data boundary:** Never invent regulations, customer names, metrics, logos, brand hex codes, or Salesforce API names. Keep customer identifiers and secrets in authorized project workspaces—never in public doc searches or this public library.
- **Bounded scope:** Solution scoping produces architecture trade-offs and delegates execution; never turn discovery into an all-Salesforce build monolith.

## Verification Integrity

- Tag every finding `observed`, `stakeholder-reported`, `inferred`, or `unknown` with source, date, and environment. Mark unexecuted tests or checks `Not verified`.
- A failed or unauthorized org read means `not observed`, never `absent`. Sandbox metadata alone does not prove production parity or runtime behavior.
- Mark capability readiness `READY FOR DESIGN`, `CONDITIONAL`, or `BLOCKED` strictly as workflow labels paired with the exact next proof required—never as compliance or deployment certifications.

## Delegate Outside Discovery

Stop re-discovery once evidence is sufficient and hand off via [handoff-contracts.md](references/handoff-contracts.md):

- **Agent specs, persona & dialogue:** `agentforce-design`
- **Agent code, flows, Apex, LWC, integrations:** `agentforce-build`, `salesforce-flow`, `salesforce-apex`, `salesforce-lwc`, `salesforce-integrations`
- **Existing agent review, testing & telemetry:** `agentforce-review`, `agentforce-test`, `agentforce-observe`
- **Access, Data 360, schema & analytics:** `salesforce-security-access`, `data360-data-pipeline`, `data360-activation-governance`, `salesforce-schema-data`, `salesforce-analytics`
- **Deployment & enablement guides:** `salesforce-devops-deploy`, `salesforce-tutorial-builder`
