# Acceptance cases

## Task

Revise a previously active prompt template, now deactivated, and compare candidate responses. There is no org connection. Do not activate.

Acceptance: Create a new version draft, regression fixtures and explicit binding unknowns; do not edit the immutable historical version.

## Routing boundary

Bind an already-active template as an agent action belongs to `agentforce-generate` when available. Preserve a handoff if unavailable.

## Failure evidence

Test missing tools, denied access, partial/asynchronous results and an operation outside authorization. Do not report expected outcomes as executed tests. Provide a useful draft when runtime validation is blocked.
