# Existing-environment discovery validation — 2026-11-15

Two independent forward exercises used the new skill without supplied expected answers:

1. An eight-year-old manufacturing org with custom warranty objects, a system-context screen flow, ERP/email side effects, and a stale sandbox. The output treated facts as stakeholder reports, preserved the custom model, rejected wholesale exposure of the flow, proposed an authorized read-only first release, and required drift/access/regression evidence.
2. Two merged hotel brands with separate orgs and conflicting cancellation guidance. The output preserved brand-specific rules and systems, surfaced the policy conflict, separated customer experience from backend consolidation, proposed a limited rollout, and avoided full discovery for a typo-only edit.

Both outputs distinguished no org access from an empty environment, included a no-agent alternative, identified operational owners, and marked runtime tests NOT RUN. These are qualitative offline design checks, not proof of runtime security or customer deployment success.

Metadata and basic skill validation passed for the new package. Catalog, generated references, packaged links, 29 root tests and 164 persona tests passed after the extension. The preceding published export also passed 604 architecture and 407 Data 360 tests; GitHub CI reruns all suites on the final revision.
