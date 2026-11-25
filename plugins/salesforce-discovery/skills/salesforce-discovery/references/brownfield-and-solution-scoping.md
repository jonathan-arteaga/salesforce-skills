# Brownfield Discovery & Well-Architected Scoping

Start with one business domain and its critical journey. Gather only the evidence that changes a decision—not an exhaustive org inventory.

## 10-Area Bounded Evidence Checklist

| Area | Inspect | Decision Informed |
| --- | --- | --- |
| Operating model | Brands, B2B/B2C, roles, regions, approval authority, support hours | Pattern fit and human accountability boundaries |
| Process | Steps, handoffs, workarounds, reopen rates, exception volume | True bottleneck; whether an agent is warranted |
| Org topology | Prod/sandbox map, acquired orgs, repos, deployed revisions, package namespaces | Target identity, drift, cross-org boundaries |
| Data | System of record per field/event, keys, freshness, quality, retention, consent, residency | Trustworthiness of answers/actions; prerequisite data work |
| Automation | Active Flow versions/types, Apex triggers/entry points, approvals, validation rules, async jobs | Reuse boundary, recursion, order-of-execution risk |
| Integrations | Contracts/versions, auth principal, timeout/retry, idempotency, event consumers | Safe execution, transaction truth, compensation needs |
| Access | Agent/user identity, sharing, CRUD/FLS, perm sets, guest/portal bounds, verified customer link | Whether staff automation is safe for external callers |
| Experience | Existing agents/bots, Omni-Channel routing, locales, Knowledge audience, live-agent capacity | Coexistence and genuine escalation paths |
| Nonfunctional | Volumes, peak concurrency, latency, API/credit/compute budgets, SLOs | Feasible scope and operating cost |
| Delivery | Test coverage, release windows, CI/CD pipeline, runbooks, operational owners | Reversible rollout and ongoing ownership |

Never infer possession of an industry cloud from the customer's vertical; an installed feature may also be unlicensed, inactive, or configured differently in production.

## Reuse vs. Adapt vs. Build vs. Defer

Evaluate each capability by stating current behavior, authoritative business rule, enforcement point, execution context, and side effects (record writes, external calls, emails, events, financial commitments). Neither system mode nor user mode alone proves business authorization.

- **Screen flow with bundled side effects:** Do not expose a staff UI flow combining lookup, approval, email, and ERP write as one agent action; start with read-only status and isolate writes cleanly.
- **Franchise or partner models:** Brand return rules do not establish franchise refund authority—verify seller-of-record, payment owner, and local policy first.
- **Merged/acquired orgs:** Duplicate names or Data 360 identity matches are not cross-org authorization; scope one approved domain before copying data.
- **Custom objects over industry clouds:** Reuse authoritative custom scheduling/case contracts instead of migrating data solely to fit a packaged template.
- **Legacy agents with working escalation:** Preserve proven routes while testing new Builder/Agent Script paths separately.

## Lightweight Well-Architected Scoping (5 Pillars)

Trace cross-platform decisions against Salesforce's five current quality dimensions before delegating builds:

1. **Trust:** Execution identity, least-privilege CRUD/FLS, verified customer linkage, consent, residency, and auditability.
2. **Reliability:** Change-impact tracing (recursion, lock contention, partial failures, idempotency, retries, queue unavailability) and regression coverage for original callers.
3. **Operational Excellence:** Named owners, observation windows, stop/rollback criteria, reconciliation owners for irreversible external effects, training, and support handoff.
4. **Resource & Cost Optimization:** Existing license/automation reuse, metered vs. unmetered usage, API/compute/credit budgets, and narrow first release sizing.
5. **Fairness:** Consistent policy enforcement across segments, accessibility, and zero demographic or unverified-sentiment bias.

## Discovery Brief Structure

Scale length to scope and deliver inline or in the approved workspace:

1. **Header:** Date, customer/project, target environment & inspected revisions, lane per capability (`greenfield`/`brownfield`/`hybrid`), business & operational owners.
2. **Outcome & Journey:** Job, audience, current process/exceptions, baseline metric & target, non-goals, release window.
3. **Evidence & Conflict Ledger:** Finding, status (`observed`/`stakeholder-reported`/`inferred`/`unknown`), source/date/env, confidence, conflict or next proof/owner.
4. **Fit & Capability Decisions:** Industry assumption vs. customer evidence (`keep`/`change`/`reject`), plus capability table (`reuse`/`adapt`/`build`/`defer`/`no-agent`, side effects, dependencies, `READY FOR DESIGN`/`CONDITIONAL`/`BLOCKED` + next proof).
5. **First Useful Release & Validation:** Preserved behaviors, narrow scope (explain/draft/execute/escalate), blocked effects + safe alternative, baseline & negative/failure scenarios (`NOT RUN` until executed), cohort limits, stop criteria, rollback/reconciliation, and sibling handoff.
