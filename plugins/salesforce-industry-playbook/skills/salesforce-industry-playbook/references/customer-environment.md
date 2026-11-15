# Customer environment discovery

## Evidence before recommendations

Start with one business domain and its critical journey. Gather what changes the decision, not a complete org inventory. Use this checklist selectively; record unknowns and a named way to resolve them.

| Area | Evidence to inspect | Decision it informs |
| --- | --- | --- |
| Operating model | Brands, B2B/B2C, employee/customer/partner roles, regions, exceptions, approval authority, support hours | Whether the industry pattern fits; where humans remain accountable |
| Process | Current steps, handoffs, workarounds, reopen rates, time spent, exception volume | Actual bottleneck; whether an agent is the appropriate intervention |
| Org topology | Production/sandbox mapping, acquired orgs, source repositories, deployed revisions, package namespaces and versions | Target identity, drift, cross-org boundaries, deployment constraints |
| Data | System of record per field/event, identifier semantics, ownership, freshness, quality, retention, consent, residency | Whether answers and actions can be trusted; what data work precedes the agent |
| Automation | Active Flow versions and type, Apex entry points, triggers, approvals, validation rules, scheduled jobs | Reuse boundary, side effects, order-of-execution and regression risk |
| Integrations | Contract/version, authentication principal, timeout/retry behavior, idempotency, event consumers, external commitments | Safe execution and recovery; source of transaction truth |
| Access | Agent/user identity, sharing, CRUD/FLS, permission sets, portal/guest boundaries, verified customer linkage | Whether an employee process is safe for customer-facing invocation |
| Experience | Existing agents/bots, routing, channels/locales, Knowledge publishing/audience, live-agent capacity | Coexistence and real escalation options; avoid competing routes |
| Nonfunctional needs | Transaction volumes, peak concurrency, latency, API/compute/credit budgets, reliability targets | Feasible scope and expected operating cost |
| Delivery | Test coverage, release windows, pipeline, environment configuration, runbooks and owners | Reversible rollout and operational readiness |

Do not infer possession of a specific cloud from the customer's industry. A manufacturer may use custom objects without Manufacturing Cloud; a bank may have both managed-package and standard-object implementations. An installed feature may be unlicensed for the intended user, unused, inactive, or configured differently in production.

## Reuse decision examples (synthetic)

- **Manufacturer with an established warranty process:** inspect its authorization and input/output contract. If the UI flow combines lookup, approval, email, and ERP submission, do not expose the whole process as one agent action. Consider a read-only status capability first; treat isolation of an approved business function as a separate implementation change. Keep existing human workflow operational and regression-tested.
- **Retailer with a franchise model:** brand-level return patterns do not establish each franchise's refund authority. Trace seller-of-record, payment owner, local policy, and customer identity before proposing shared automation.
- **Merged business with two orgs:** match identity and field semantics explicitly; duplicate customer names or an identity-resolution match are not cross-org authorization. Start in one approved domain rather than copying data or merging access by default.
- **Healthcare scheduling on custom objects:** reuse the existing authoritative scheduling contract when suitable. Do not prescribe a new industry cloud or migrate data solely because a current Salesforce template uses it.
- **Legacy agent with working escalation:** preserve proven routes while testing any new Builder/Agent Script path separately. Inspect compatibility and migration support; a new feature announcement is not a mandate to replace a functioning deployment.

## Decision and validation rules

For each candidate, state current behavior, intended change, authoritative business rule, enforcement point, and evidence. Mark side effects explicitly: record updates, external writes, emails, events, entitlement changes, or financial commitments. Determine whether the existing execution context fits the new caller; neither system mode nor user mode alone proves the business authorization requirement is met.

No unknown authority, missing required consent, or unbounded external mutation may be averaged into a favorable readiness score. A credible alternative is read-only assistance, human-reviewed drafts, data/process remediation, or no agent. Propose a measurable prototype rather than endless discovery, but keep blocked effects unavailable.

Before changing shared automation, test original callers as well as the agent caller. Include negative access tests, cross-customer/tenant separation, duplicate invocation, changed data between read and write, downstream timeout, queue unavailability, and rollback/reconciliation. Select only scenarios relevant to the change. Preserve baselines and versioned evidence; a metadata review or mock is not proof of runtime success.

For rollout, define an owner, observation window, stop condition, customer/support communication, and how the previous working path stays available. Example thresholds are proposals until the operational owner agrees them. Turning off an agent does not reverse a payment, cancel an emitted event, or restore changed data.

## Sources checked 2026-11-15

These sources support the discovery approach, not customer-specific facts. Recheck target feature documentation for implementation details.

- [Architect the Right Solution](https://trailhead.salesforce.com/content/learn/modules/agentforce-agent-planning/architect-the-right-solution): plan the journey, information, channels, access, and escalation; refine through prototypes.
- [Make Your Existing Automation Agent-Ready](https://www.salesforce.com/blog/agent-ready-automation/): assess bounded existing automation before exposing it to agents. This library's reuse/adapt/build/defer decision table is our synthesis, not an official Salesforce score.
- [Well-Architected Framework](https://architect.salesforce.com/docs/architect/well-architected/guide/framework.html): current quality dimensions are Trust, Reliability, Operational Excellence, Resource and Cost Optimization, and Fairness. Do not hard-code the retired three-pillar layout as the current framework.
- [Operational Excellence](https://architect.salesforce.com/docs/architect/well-architected/guide/operational-excellence.html): plan operational ownership, observability, safe releases and recovery.
- [Resource and Cost Optimization](https://architect.salesforce.com/docs/architect/well-architected/guide/resource-and-cost-optimization.html): evaluate existing investments, full cost and capacity before adding capabilities.
