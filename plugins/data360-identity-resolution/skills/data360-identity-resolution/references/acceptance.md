# Acceptance cases

## Task

Two spouses share an email but have distinct verified customer IDs. A third record belongs to one spouse with a misspelled name. An existing ruleset unifies all three. No org tools are available.

Acceptance: Draft match and reconciliation changes separately, false-merge/split fixtures and lineage; do not overwrite source records or infer identity from email alone.

## Routing boundary

Map an ingestion source to DMO fields belongs to `data360-ingestion-modeling` when available. Preserve a handoff if unavailable.

## Failure evidence

Test missing tools, denied access, partial/asynchronous results and an operation outside authorization. Do not report expected outcomes as executed tests. Provide a useful draft when runtime validation is blocked.
