---
name: salesforce-industry-playbook
description: "Discover and tailor Salesforce or Agentforce builds to a customer’s industry, business model, and actual environment. Use for industry playbooks, brownfield discovery, existing-org readiness, reuse-versus-rebuild decisions, acquired or multi-org estates, and phased adoption. Return an evidence-backed discovery brief and implementation handoff. Not a substitute for a known scoped code fix, persona-only design, live deployment, or detailed agent architecture."
---

# Salesforce Industry Playbook

Use [current Salesforce guidance](references/current-salesforce/guide.md) for version-sensitive claims. For context-specific examples, read only the matching [industry and role patterns](references/shared/industry-patterns.md). For existing estates, read [customer environment discovery](references/customer-environment.md); use the [brief template](assets/discovery-brief.md) to structure the result inline or in the requested destination.

## Decision principle

Customer-specific evidence and agreed business outcomes outweigh generic industry patterns. Apply verified policy, contractual/security constraints, actual operating processes, and target-environment evidence before industry assumptions or feature novelty. Existing behavior is evidence of what happens, not proof of what should happen: surface conflicts between policy and implementation instead of blessing current defects. Do not assign arbitrary numeric weights that let commercial value average away an authorization or data-integrity blocker.

Own discovery, fit assessment, reuse decisions, and the handoff. Let persona own character, agent-architecture own detailed control/action design, and implementation skills own changes. Do not force a full discovery workshop for a small, already-understood fix.

## Workflow

1. **Scope the outcome and lane.** Infer greenfield, brownfield, or hybrid per capability, not per customer logo. A new agent on an established org is brownfield. An acquired org with unknown internals is not greenfield. Identify business sponsor, operational owner, job, pain, affected audience, baseline metric, target, deadline, and non-goals. Make reasonable explicit assumptions; ask a short set of high-value questions only where answers change decisions.
2. **Gather bounded evidence.** Reuse supplied diagrams, sanitized metadata, repository history, policies, incident summaries, and metrics. If org reads are authorized and available, confirm exact org/environment identity and use supported read-only tools scoped to the target domain. Never broaden permissions, enable features, retrieve all customer records, or expose secrets to complete discovery. Keep customer material in its authorized workspace; do not publish it with this public skill library.
3. **Map reality.** Record the current customer/employee journey, manual exceptions, operational owners, data authorities and freshness, automation entry points, integration contracts, access context, installed packages/versions, channels, and deployment process. Label each finding observed / stakeholder-reported / inferred / unknown, with source, date, environment, and confidence. A failed or unauthorized read means not observed, not absent. Do not treat sandbox observations as production parity.
4. **Test industry fit.** Use the playbook to propose useful questions and two plausible design options, then explicitly record which industry assumptions the customer evidence supports, changes, or rejects. Model brand, business model, franchise/partner arrangements, geography, contractual terms, accessibility, and channel expectations. Avoid invented regulations or demographic personality stereotypes.
5. **Choose the smallest useful intervention.** Compare no-agent/process improvement, existing configuration/automation, a narrowly scoped assistive agent, and autonomous action where justified. For each capability choose reuse / adapt / build / defer, with evidence, owner, dependencies, permissions, cost, and risk. Reuse proven interfaces where appropriate; do not expose a powerful screen flow or system-context operation merely because it already works for staff. Preserve the approved business rule in one owner rather than duplicate it in prompts.
6. **Assess change impact.** Trace touched records through active Flow/Apex, validation and duplicate rules, approvals, managed-package behavior, async jobs, external events, and downstream consumers. Identify recursion, duplicate notifications or writes, lock contention, capacity, eventual consistency, and partial failures. Propose an additive boundary or limited refactor before broad replacement. Record discovery coverage and unknown dependencies; metadata alone does not prove runtime behavior.
7. **Define progressive validation and adoption.** Establish baseline tests on existing critical paths and the proposed outcome. Plan a sanitized sandbox prototype, regression/permission/integration tests, limited cohort or channel only where supported, observable release, and explicit stop/rollback criteria. If rollback cannot undo external effects, specify reconciliation and compensation owners. Include human training, support staffing, handoff acceptance, and ongoing ownership. Reuse existing scoped authorization; discovery does not itself authorize deployment or production writes.
8. **Deliver the brief and handoff.** Return findings, decision table, narrow first release, blocked dependencies, success measures, and next steps with owners. Mark READY FOR DESIGN, CONDITIONAL, or BLOCKED per capability with evidence and the precise next proof needed; these are workflow labels, not certifications. Unknowns may block writes or release without blocking a useful provisional design. Scale the output to the requested scope; avoid an exhaustive questionnaire when existing evidence is enough.

## Handoff contract

Pass the exact target environment and inspected artifact revisions, evidence/conflict ledger, business outcomes, authoritative data, proposed capability boundaries, reuse choices, existing behavior to preserve, dependency risks, acceptance tests, release/rollback plan, and open decisions. Keep identifiers in the customer's authorized project only; do not include credentials.

- Existing agent inspection: agentforce-architecture-analyze, using available metadata evidence.
- Access/authority: salesforce-access-design; Data 360 governance: data360-governance.
- Detailed agent design: agent-architecture; character: persona; dialogue: conversation-design.
- Build: agentforce-generate for agents, automation-flow-generate or platform-apex-generate for automation changes.
- Test and rollout: agentforce-test, platform-metadata-deploy, agentforce-observe.

If a companion is unavailable, provide the bounded handoff and state the missing capability. Do not pretend it ran. Stop re-discovery once the necessary evidence is sufficient and current; reopen only decisions affected by new facts or scope changes.
