# Acceptance cases

## Realistic task

Two sources use CustomerId 42 for different people. One batch has null keys, and a second run repeats rows. No connector is available.

Acceptance: Draft namespaced key/mapping decisions, reject handling and repeat-run reconciliation; do not claim provisioning or identity unification.

## Route boundary

Request: List fields in a DMO. Route to `data360-schema-get` when available; do not expand this skill into that workflow.

## Failure checks

- Missing tools: produce a useful draft and list unresolved target checks.
- Denied access: preserve the error distinction; never change identities/data spaces to bypass it.
- Partial results: mark evidence incomplete and avoid a success claim.
- Mutation outside the requested scope: prepare the artifact and obtain only the missing authorization.
- Sandbox execution: retain actual inputs/results and distinguish them from expected fixtures.
