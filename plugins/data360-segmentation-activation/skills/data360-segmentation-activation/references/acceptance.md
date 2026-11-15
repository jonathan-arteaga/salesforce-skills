# Acceptance cases

## Task

Preview an email audience where one member opted out, one has unknown consent and one has two contact points. A target already has a publishing schedule. Do not publish.

Acceptance: Provide owner-dependent consent handling and deterministic fixture counts; keep activation local and identify save/schedule side effects.

## Routing boundary

Resolve duplicate unified profiles belongs to `data360-identity-resolution` when available. Preserve a handoff if unavailable.

## Failure evidence

Test missing tools, denied access, partial/asynchronous results and an operation outside authorization. Do not report expected outcomes as executed tests. Provide a useful draft when runtime validation is blocked.
