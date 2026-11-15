# Acceptance cases

## Realistic task

A library upload completed, the agent answers with obsolete policy text, and another customer must never see the restricted document. The installed CLI lacks agent adl.

Acceptance: Separate indexing/freshness/retrieval/answer and identity tests; use supported fallback drafts, not invented commands or prompt-only authorization.

## Route boundary

Request: Create a new agent with topics and actions. Route to `agentforce-generate` when available; do not expand this skill into that workflow.

## Failure checks

- Missing tools: produce a useful draft and list unresolved target checks.
- Denied access: preserve the error distinction; never change identities/data spaces to bypass it.
- Partial results: mark evidence incomplete and avoid a success claim.
- Mutation outside the requested scope: prepare the artifact and obtain only the missing authorization.
- Sandbox execution: retain actual inputs/results and distinguish them from expected fixtures.
