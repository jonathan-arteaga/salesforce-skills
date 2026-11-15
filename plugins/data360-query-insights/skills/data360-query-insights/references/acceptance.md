# Acceptance cases

## Realistic task

Orders 10 and 20 join to three contact points for customer A; a proposed total is 90. SQL execution is unavailable.

Acceptance: Explain fan-out, produce expected total 30 and a schema-conditional query draft; report offline arithmetic, not Salesforce execution.

## Route boundary

Request: Write SOQL for Account. Route to `platform-soql-query` when available; do not expand this skill into that workflow.

## Failure checks

- Missing tools: produce a useful draft and list unresolved target checks.
- Denied access: preserve the error distinction; never change identities/data spaces to bypass it.
- Partial results: mark evidence incomplete and avoid a success claim.
- Mutation outside the requested scope: prepare the artifact and obtain only the missing authorization.
- Sandbox execution: retain actual inputs/results and distinguish them from expected fixtures.
