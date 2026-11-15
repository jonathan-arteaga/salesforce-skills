# Async Decision Matrix

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Async Decision Matrix

| Scenario | Default | Key Traits |
|---|---|---|
| Standard async work | **Queueable** | Job ID, chaining, non-primitive types, configurable delay (up to 10 min via `AsyncOptions`), dedup signatures |
| Very large datasets | **Batch Apex** | Chunked processing, max 5 concurrent; use `QueryLocator` for large scopes |
| Modern batch alternative | **CursorStep** (`Database.Cursor`) | 2000-record chunks, higher throughput, no 5-job limit |
| Recurring schedule | **Scheduled Flow** (preferred) or **Schedulable** | Schedulable has 100-job limit; use only when chaining to Batch or needing complex Apex logic |
| Post-job cleanup | **Finalizer** (`System.Finalizer`) | Runs regardless of Queueable success/failure |
| Long-running callouts | **Continuation** | Up to 3 per transaction, 3 parallel |
| Delays > 10 minutes | `System.scheduleBatch()` | Schedule a Batch job at a specific future time |
| Legacy fire-and-forget | `@future` | **Do not use in new code** — see Hard-Stop Constraints; replace with Queueable + Finalizer |

---
