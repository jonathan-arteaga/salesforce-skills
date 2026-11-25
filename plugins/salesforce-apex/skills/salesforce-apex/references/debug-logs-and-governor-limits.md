# Debug Logs and Governor-Limit Diagnosis

## Retrieving & Capturing Logs

```bash
# List recent logs, fetch a specific log, or stream live logs
sf apex list log --target-org <alias>
sf apex get log --log-id <logId> --target-org <alias> --output-dir ./logs
sf apex tail log --target-org <alias> --color
```

- **2 MB truncation trap**: If a log truncates, lower verbose categories (set `ApexCode: INFO`, `ApexProfiling: FINE`, `Database: INFO`, `System: INFO`) and recapture.
- **Missing logs**: Verify the `TraceFlag` targets the exact running user (or Automated Process / Guest User) and has a future `ExpirationDate`.

## Six-Step Evidence Analysis Order

Always read logs in this sequence and ground every finding in actual log events:

1. **Entry point & transaction context**: Identify Sync vs Async (`EXECUTION_STARTED`, trigger, Aura/LWC, Batch, Queueable, Flow) — limits differ sharply.
2. **Exceptions & fatal errors**: Scan `EXCEPTION_THROWN`, `FATAL_ERROR`, and walk up the call stack past trigger frameworks to the originating user code.
3. **Governor limits**: Inspect `LIMIT_USAGE_FOR_NS` and `CUMULATIVE_LIMIT_USAGE` — never assume limits are safe without reading them.
4. **Repeated SOQL / DML**: Count `SOQL_EXECUTE_BEGIN` and `DML_BEGIN` signatures inside repeated method frames or trigger re-entry.
5. **CPU & heap hotspots**: Check `METHOD_ENTRY`/`METHOD_EXIT` durations, `HEAP_ALLOCATE` spikes, and `CODE_UNIT_FINISHED` deltas.
6. **Callout timing**: Inspect `CALLOUT_REQUEST`/`CALLOUT_RESPONSE` latency and HTTP error statuses.

## Governor Limits Quick Reference

| Resource | Synchronous Limit | Asynchronous Limit |
| --- | --- | --- |
| SOQL queries | 100 | 200 |
| SOQL rows returned | 50,000 | 50,000 |
| DML statements | 150 | 150 |
| DML rows | 10,000 | 10,000 |
| Apex CPU time | 10,000 ms | 60,000 ms |
| Apex heap size | 6 MB | 12 MB |

## High-Signal Issue Patterns

| Pattern | Log Signal | Root-Cause Fix |
| --- | --- | --- |
| SOQL in loop | Repeating `SOQL_EXECUTE_BEGIN` in same method; often causes secondary CPU spike | Fix SOQL-in-loop first: hoist query, index into `Map<Id, SObject>` |
| DML in loop | Repeating `DML_BEGIN` in loop or recursive trigger | Accumulate into `List<SObject>`, single bulk DML + recursion guard |
| Non-selective query | High rows scanned, `QueryException`, or slow `SOQL_EXECUTE_END` | Filter on indexed fields (`Id`, lookups, `ExternalId`, custom index) + `LIMIT` |
| Heap pressure | High `HEAP_ALLOCATE` on large result sets | Stream with SOQL `for (List<SObject> chunk : [...])` or Apex Cursors |
| API 67+ permission failure | `QueryException` / `DmlException` on inaccessible field/object | Grant least-privilege Permission Set or review intentional `SYSTEM_MODE` path |
| Null pointer | `System.NullPointerException` after `map.get()` or empty query | Add guard clauses, `containsKey()`, safe navigation `?.`, empty list checks |

## Required Diagnosis Output

For every finding, report all six fields:
- **Issue**: Concise failure summary
- **Location**: Class, method, line number, and transaction stage
- **Root cause**: Traceable log evidence (not symptom restatement)
- **Severity**: `Critical` (runtime failure / limit hit / corruption risk), `Warning` (near-limit / non-selective / slow path), or `Info` (hygiene)
- **Fix**: Smallest bulk-safe, testable change
- **Verify**: Exact test command or log-recapture check to confirm resolution
