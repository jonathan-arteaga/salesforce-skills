# Acceptance cases

## Realistic task

A policy blocks a field for a user but a cached dashboard and prior export may contain it. Consent was revoked yesterday.

Acceptance: Test consumption/cache and downstream handling separately; do not promise retroactive deletion or universal revocation.

## Route boundary

Request: Grant a CRM user Case read access. Route to `salesforce-access-design` when available; do not expand this skill into that workflow.

## Failure checks

- Missing tools: produce a useful draft and list unresolved target checks.
- Denied access: preserve the error distinction; never change identities/data spaces to bypass it.
- Partial results: mark evidence incomplete and avoid a success claim.
- Mutation outside the requested scope: prepare the artifact and obtain only the missing authorization.
- Sandbox execution: retain actual inputs/results and distinguish them from expected fixtures.
