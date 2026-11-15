# Acceptance cases

## Realistic task

A support user needs Case read, Status update, no sensitive field access and only assigned-team records. Another direct permission set grants the sensitive field.

Acceptance: Find all grant paths; do not claim muting one group removes the direct grant. Draft the matrix and allow/deny tests without changing access.

## Route boundary

Request: Write an Apex trigger unit test. Route to `platform-apex-test-generate` when available; do not expand this skill into that workflow.

## Failure checks

- Missing tools: produce a useful draft and list unresolved target checks.
- Denied access: preserve the error distinction; never change identities/data spaces to bypass it.
- Partial results: mark evidence incomplete and avoid a success claim.
- Mutation outside the requested scope: prepare the artifact and obtain only the missing authorization.
- Sandbox execution: retain actual inputs/results and distinguish them from expected fixtures.
