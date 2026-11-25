---
name: agentforce-observe
description: "Trace Agentforce sessions in Data 360, analyze production trends, diagnose voice latency and Flex Credit anomalies, and manage authorized AHM alerts. Use agentforce-build for agent edits, agentforce-test for test runs, or data360-activation-governance for masking policies."
---

# Agentforce Observability

Single-session Data 360 tracing, aggregate production trend analysis, voice latency and Flex Credit cost triage, and Agent Health Monitoring (AHM) alerts. Select the mode below and load only its reference first.

## Mode Routing

| Mode | When to use | Reference |
| --- | --- | --- |
| Single-Session Data 360 Tracing | Discover or trace one session (UUID or `0Mw...` MessagingSession), reconstruct STDM + GenAI timeline via bundled scripts | [session-tracing-d360.md](references/session-tracing-d360.md) |
| Production Trends & AHM Alerts | Aggregate STDM health metrics, issue classification, AHM data alerts (`tableau/dataAlerts`), notification history | [production-trends-alerts.md](references/production-trends-alerts.md) |
| Voice Latency & Cost Anomalies | Voice call latency/recording triage, Flex Credit & token/turn cost drivers, PII/PHI trace minimization | [voice-latency-cost.md](references/voice-latency-cost.md) |
| Voice Latency Heuristics | Field-verified voice latency anti-patterns and fix classifications (auto-instructional vs flag-only) | [voice-latency-heuristics.md](references/voice-latency-heuristics.md) |

## Resolving the script prefix

Resolve this skill's bundled `scripts/` directory before running any Data 360 session pipeline script (`discover_sessions.py`, `resolve_session.py`, `fetch_dc.py`, `assemble_dc.py`, `render_dc.py`):

```bash
_skill=agentforce-observe
for _c in "${SKILL_ROOT:-}" "${SKILL_DIR:-}" \
          "${VIBES_SKILLS_DIR:+$VIBES_SKILLS_DIR/$_skill}" \
          "$PWD/.agents/skills/$_skill" "$HOME/.agents/skills/$_skill" \
          "${PLUGIN_ROOT:-$HOME/.vibe/skills}/$_skill"; do
  [ -n "$_c" ] || continue
  for _r in "$_c" "$_c/artifacts"; do
    [ -f "$_r/scripts/fetch_dc.py" ] && { SKILL_ROOT="$_r"; break 2; }
  done
done
[ -f "${SKILL_ROOT:-}/scripts/fetch_dc.py" ] || { echo "$_skill: scripts not found — set SKILL_ROOT to this skill's directory" >&2; exit 1; }
prefix="$SKILL_ROOT/scripts"
```

Treat scripts as black boxes — invoke via CLI (`--help` for full flags):
- Discover sessions: `python3 "$prefix/discover_sessions.py" [--org <alias>] [--since "last 2 hours"] [--agent <name>] [--outcome ESCALATED]`
- Trace one session (fetch -> assemble -> render): `python3 "$prefix/fetch_dc.py" --session <uuid-or-0Mw> [--org <alias>] [--data-dir <path>]`
- Opt-in prompt rendering (PII-sensitive, suppressed by default): `python3 "$prefix/render_dc.py" --session <uuid> [--org <alias>] --show-prompts`

## Core 2026 Invariants

- **STDM readiness & ingestion lag**: Verify tracing enablement, Standard Data Model version (minimum **1.130**), selected data space, permissions, and materialization lag before concluding zero sessions exist. Changing the tracing data space does not migrate historical data.
- **Never fall back to `default` data space on error**: If data-space discovery fails (404, permission denied), keep the data space unresolved and report the exact failure. An access error is never evidence of an empty space or disabled tracing.
- **DC-only blind spot**: Data 360 traces show what ran (steps, messages, generations, gateway requests, audit 1:1 chain) — NOT which topics/actions were eligible or why the planner skipped an action. Do not fabricate root causes beyond trace evidence.
- **PII/PHI trace minimization**: Einstein Trust Layer LLM masking is disabled for agents and does NOT sanitize stored STDM/audit traces. Keep `--show-prompts` off by default and minimize exported trace artifacts.

## Hard Org & Safety Gates

1. **Read-only investigation by default**: Inspecting traces or metrics does NOT authorize deploying `AgentforceOptimizeService`, running live actions in preview, enabling tracing, creating/updating/deleting AHM alerts, or editing/publishing `.agent` files. Require explicit user authorization for any mutation.
2. **Safe AHM mutations**: Use `sf api request rest` with `0600` `mktemp` body files (never fixed `/tmp/*.json`), never interpolate untrusted usernames into SOQL, and always pass `X-UNS-Type-Filter: all` when reading notifications.
3. **Verification integrity**: State the exact org, data space, time window, agent/version filter, STDM/gateway coverage, and missing evidence in every report. With no live Data 360 access, analyze supplied logs/exports and list missing trace gaps explicitly.

## Companion Handoffs

- Editing `.agent` files or publishing fixes: `agentforce-build`
- Static pre-release safety and architecture review: `agentforce-review`
- Live preview reproduction and Testing Center regression suites: `agentforce-test`
- Data 360 masking, retention, and data-space governance: `data360-activation-governance`
- Runtime identity and backing-action authorization: `salesforce-security-access`
