# Pub/Sub API, Platform Events, and Change Data Capture

## Choosing the Event Pattern

| Pattern | Source | Best Use Case |
| --- | --- | --- |
| **Platform Events (`__e`)** | Explicit Apex, Flow, or API publish | Domain business events, decoupled microservices, custom payloads |
| **Change Data Capture (CDC)** | Automatic on SObject DML (`*ChangeEvent`) | Replicating CRM record mutations downstream without custom trigger glue |
| **Pub/Sub API** | gRPC / HTTP2 with Apache Avro schemas | High-throughput external publish & subscribe replacing legacy CometD/Streaming API |

## 2026 Pub/Sub API Invariants

- **72-hour durability window**: High-volume Platform Events and CDC events are retained on the Salesforce event bus for **72 hours** (3 days). Consumers offline longer than 72 hours cannot replay missed events and must run a reconciliation backfill query (REST/Bulk API).
- **Opaque replay IDs**: Treat every `replay_id` as an **opaque binary/base64 token**. Never decode, increment, parse as an integer, or assume monotonic arithmetic across replay IDs — store the exact bytes/base64 returned by the server.
- **Subscription checkpointing**:
  - **Client-managed `Subscribe`**: Persist the last successfully processed `replay_id` durably only after committing side effects; reconnect with `ReplayPreset.CUSTOM` (use `LATEST` for fresh starts or `EARLIEST` only when full 72h replay is safe).
  - **`ManagedSubscribe` (Beta)**: Uses Salesforce server-managed durable checkpoints (`ManagedEventSubscription` metadata) to track subscriber progress and simplify consumer restarts. Verify org Beta availability, limits, and error-commit semantics before adopting in production.
- **Flow control & schemas**: Use gRPC `FetchRequest.num_requested` backpressure so consumers only pull batches they can commit safely. Cache Avro schemas by `schema_id` (`GetSchema`) and refresh automatically when an unknown `schema_id` arrives.

| Subscription Mode | Replay Behavior | Best Fit |
| --- | --- | --- |
| `Subscribe` + `ReplayPreset.CUSTOM` | Resumes from client-persisted opaque `replay_id` within 72h | Production external consumers with durable checkpoint store |
| `Subscribe` + `ReplayPreset.LATEST` | Receives only new events arriving after subscribe | Real-time telemetry or initial bootstrap |
| `Subscribe` + `ReplayPreset.EARLIEST` | Replays full 72-hour bus retention | Recovery after checkpoint loss with idempotent sink |
| `ManagedSubscribe` (Beta) | Server-managed durable checkpoint via `ManagedEventSubscription` | Managed restart recovery when org Beta limits fit |

## Publishing, Subscribing & Failure Recovery

- **Publish behavior**: Choose `Publish After Commit` (default, prevents phantom events on transaction rollback) vs `Publish Immediately` (error/audit logging that must survive rollback). Always inspect `Database.SaveResult` returned by `EventBus.publish(events)` and handle failures.
- **Idempotent consumers**: Salesforce provides **at-least-once** delivery. Deduplicate on `EventUuid` (or domain event ID) so replays never create duplicate orders or double-charge customers.
- **Apex event subscribers**:
  - Process events in bulk inside trigger handlers; keep SOQL and DML strictly outside loops.
  - Call `EventBus.TriggerContext.currentContext().setResumeCheckpoint(lastReplayId)` after each processed batch chunk so an unhandled exception or governor limit resumes cleanly rather than reprocessing up to 2,000 events.
  - Throw `EventBus.RetryableException` only for transient failures with an explicit retry cap (`EventBus.TriggerContext.currentContext().retries < maxRetries`) before routing failed payloads to a dead-letter custom object.
  - Configure `PlatformEventSubscriberConfig` metadata to control subscriber running user and batch size (`batchSize`) explicitly rather than defaulting blindly to Automated Process.

```apex
EventBus.TriggerContext ctx = EventBus.TriggerContext.currentContext();
for (Order_Event__e evt : Trigger.new) {
    processEventIdempotently(evt);
    ctx.setResumeCheckpoint(evt.ReplayId);
}
```

## CDC Channel Scoping & Testing

- **Channel membership edits**: When a request only adds or removes objects from a CDC channel, scope the change to `PlatformEventChannelMember` metadata without rebuilding unrelated triggers or classes.
- **Apex testing**: Call `Test.enableChangeDataCapture()` before DML and `Test.getEventBus().deliver()` inside `Test.startTest()` / `Test.stopTest()` to execute subscribers synchronously and assert side effects.
- **Local validation**: Run `python3 scripts/validate_integration.py <path-to-event-or-trigger>` to score Platform Event metadata and subscriber triggers before deployment.
