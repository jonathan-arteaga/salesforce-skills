# Acceptance cases

## Task

The stream disconnects after an agent message that may create a Case; app wants to retry automatically. No current API schema is available.

Acceptance: Mark outcome unknown, prevent blind replay and cross-user session reuse, draft transport/state tests; do not invent supported idempotency keys.

## Routing boundary

Build agent topics and actions belongs to `agentforce-generate` when available. Preserve a handoff if unavailable.

## Failure evidence

Test missing tools, denied access, partial/asynchronous results and an operation outside authorization. Do not report expected outcomes as executed tests. Provide a useful draft when runtime validation is blocked.
