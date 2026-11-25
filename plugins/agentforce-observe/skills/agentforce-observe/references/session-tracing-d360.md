# Single-Session Data 360 Tracing Reference

Hierarchical single-session reconstruction from Data 360 Session Trace Data Model (STDM) + Einstein Audit & Feedback GenAI DMOs using the bundled Python pipeline in `scripts/`.

## 1. Prerequisites & STDM Readiness

Before concluding that a session does not exist or tracing is disabled:
- **CLI & Python**: `sf` CLI authenticated against the target org (supporting `sf org auth show-access-token`), Python 3.10+.
- **STDM minimum version**: Documented minimum Standard Data Model version is **1.130**.
- **Data Space resolution**: Discover active data spaces via `sf api request rest "/services/data/v66.0/ssot/data-spaces" -o <org>` (do NOT add `--json` to `sf api request rest`).
  - **NEVER silently fall back to `default` on error**: If discovery returns 404 or permission denied, keep the data space unresolved and report the exact cause. Missing permissions, wrong data space, incompatible schema, and disabled tracing are distinct conditions.
  - Changing the tracing data space does **not** migrate historical trace rows.
- **Ingestion / materialization lag**: Fresh sessions may initially report `interactions_not_materialized_yet` or render via the `gateway_direct` branch until STDM catches up. Re-run after 1–2 minutes before treating missing rows as permanent.

## 2. Inputs & Session ID Forms

| Form | Example | Resolution |
| --- | --- | --- |
| Agent Session UUID | `019dface-0000-7000-8000-000000000002` | Pass-through to `fetch_dc.py` |
| MessagingSession ID (`0Mw` prefix, 15/18 chars) | `0MwTESTMSG12345AAA` | Resolved via `resolve_session.py` (live DC lookup on first fetch, disk-first thereafter) |

**Multi-match handling**: One `MessagingSession` ID can map to multiple Agent Session UUIDs. On multi-match, `resolve_session.py` prints every candidate and exits non-zero; ask the user to choose a specific UUID.

If the user provides neither a session ID nor discovery filters, ask for:
1. Session ID (Agent Session UUID or `0Mw...` MessagingSession ID) OR discovery criteria (time window, agent, channel, outcome, or conversation phrase).
2. Target org alias (if no CLI default target org is set).

## 3. Running the Bundled Scripts (Black-Box CLI)

Resolve `"$prefix"` using the `## Resolving the script prefix` block in `SKILL.md`, then invoke scripts via CLI:

### Step A: Discover Sessions (when no ID is known)

```bash
python3 "$prefix/discover_sessions.py" [--org <alias>] \
  [--since "last 2 hours"] [--agent <api-name>] \
  [--channel Messaging|Builder|Voice] \
  [--outcome USER_ENDED|ESCALATED|TRANSFERRED|TIMEOUT|NOT_SET] \
  [--grep "<substring>"] [--tz <IANA>] [--limit 20]
```

Prints a numbered markdown table (`#`, `UUID`, `Start (UTC)`, `Agent`, `Channel`, `Duration`, `Outcome`). Have the user pick a row, then trace that UUID.

### Step B: Three-Stage Reconstruction Pipeline

```text
fetch_dc.py     -> 24 dc.<name>.json + dc._session_manifest.json   (5-wave DC Query REST waterfall)
assemble_dc.py  -> dc._session_tree.json                           (in-memory hierarchical join)
render_dc.py    -> dc._session_summary.md                          (human summary, up to 11 sections)
```

`fetch_dc.py` chains all three stages automatically unless `--no-assemble` or `--no-render` is passed:

```bash
python3 "$prefix/fetch_dc.py" --session <uuid-or-0Mw> [--org <alias>] [--verbose] [--data-dir <path>] [--cache-dir <path>]
```

- `--org` is optional for read-only discovery/tracing: omitting it uses `sf config get target-org`. If unset, `fetch_dc.py` exits with `DC_ACCESS_DENIED` (`reason: no_org`); ask the user for an explicit alias.
- `--show-prompts` on `render_dc.py` is **opt-in and suppressed by default** to minimize PII/PHI exposure. Re-render with `--show-prompts` only when explicitly requested for authorized prompt debugging:
  ```bash
  python3 "$prefix/render_dc.py" --session <uuid> [--org <alias>] --show-prompts
  ```

## 4. Artifact Layout & Read Order

Artifacts land under `<data-root>/<org_id15>/<agent>__<ver>/<session_id>/` (override root with `--data-dir <path>`). Read in order:

1. **`dc._session_summary.md`**: Top-to-bottom narrative (Session identity, bootstrap variables, ID reference, transcript, hierarchical trace `Interaction -> Step -> Generation -> GatewayRequest`, per-turn summary, opt-in LLM prompts, visual Gantt, manifest counts, empties diagnostics, session-filtered tag catalog).
2. **`dc._session_tree.json`**: Single source of truth for deep dives, token counts, step durations, and action inputs/outputs.
3. **`dc._session_manifest.json`**: Per-DMO row counts, classified `session_shape`, `counts.audit_chain_1to1_ok` (GatewayRequest vs GatewayResponse 1:1 integrity), and `_unavailable_reason` for empty DMOs.
4. **`dc.<name>.json`**: Raw DMO rows (`sessions`, `interactions`, `messages`, `steps`, `participants`, `generations`, `gateway_requests`, `gateway_responses`, `gateway_request_metadata`, `content_quality`, `content_category`, `moments`, `feedback`, etc.).

## 5. DC-Only Blind Spot & Caveats

- **What DC proves**: What ran (steps, order, timestamps), what the user saw (transcript), LLM generations/tokens/Trust Layer quality & toxicity scores, tool inputs/outputs/errors, feedback, and 1:1 gateway audit integrity.
- **What DC CANNOT prove**: Which topics/subagents were eligible for the classifier on a given turn, which declared actions survived rule expressions, or why the planner did not pick an unused action. Tell the user explicitly that eligibility/availability questions require runtime planner telemetry outside Data 360.
- **`planner_ran_no_gateway_logs` (`gateway_requests_dropped_by_stdm`)**: Zero `gateway_requests` rows cannot distinguish STDM exporter drops from logging disabled at source; state that ambiguity explicitly.
- **Timestamp caveat**: `GenAIGeneration` and `GenAIGatewayRequest` carry single-write timestamps (serialization order, not true start/end LLM wall-clock duration).
- **PII/PHI minimization**: Einstein Trust Layer LLM masking is disabled for agents and does NOT sanitize stored STDM/audit traces. Keep exported summaries minimal, suppress `--show-prompts` unless needed, and hand off Data 360 masking/access policies to `data360-activation-governance`.

## Sources Verified

- Set Up Agentforce Session Tracing: `https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_setup.htm&release=264.0.0&type=5`
- Agentforce Session Tracing: `https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace.htm&release=264.0.0&type=5`
