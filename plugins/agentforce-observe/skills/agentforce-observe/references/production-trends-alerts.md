# Production Trends & AHM Alerts Reference

Investigate aggregate Agentforce production behavior across STDM sessions and manage authorized Agent Health Monitoring (AHM) data alerts via `sf api request rest`.

## 1. Resolve Agent Identity & Data Space (Read-Only Preflight)

Always resolve the exact agent identifiers and active Data Space before running aggregate queries:

```bash
# Resolve MasterLabel (STDM display name) and DeveloperName (strip _vN for sf agent --api-name)
sf data query --target-org <org> --json \
  --query "SELECT Id, MasterLabel, DeveloperName FROM GenAiPlannerDefinition WHERE MasterLabel LIKE '%<name>%' OR DeveloperName LIKE '%<name>%'"

# Discover active Data Spaces (do NOT pass --json to sf api request rest)
sf api request rest "/services/data/v66.0/ssot/data-spaces" -o <org>
```

**Data Space rules**:
- Filter to `status: "Active"`. If 1 active space exists, confirm it explicitly; if multiple exist, ask the user which space to query.
- **NEVER fall back to `default` on discovery error** (404 / permission denied). Keep the data space unresolved and report the exact access/configuration error.

## 2. Aggregate STDM Investigation & Issue Taxonomy

### Querying STDM Safely
- Prefer existing read-only Data 360 query access (`ConnectApi.CdpQuery.queryAnsiSqlV2` or Data 360 Query REST `/services/data/v66.0/ssot/query`) against core STDM DMOs:
  - `ssot__AiAgentSession__dlm` -> `ssot__AiAgentSessionParticipant__dlm` (`ssot__AiAgentApiName__c`)
  - `ssot__AiAgentInteraction__dlm` (`ssot__TopicApiName__c`) -> `ssot__AiAgentInteractionMessage__dlm` & `ssot__AiAgentInteractionStep__dlm` (`TOPIC_STEP`, `LLM_STEP`, `ACTION_STEP`, `TRUST_GUARDRAILS_STEP`, `SESSION_END`)
  - `ssot__AiAgentMoment__dlm` -> `ssot__AiAgentTagAssociation__dlm` -> `ssot__AiAgentTag__dlm` (1–5 quality scores + `ssot__AssociationReasonText__c`)
  - `AiRetrieverQualityMetric` (RAG retrieval/relevancy scores)
- **Helper Apex class gate**: The optional helper `assets/apex/AgentforceOptimizeService.cls` is bundled for authorized orgs that want batched STDM aggregation helpers (`findSessions`, `getAggregatedMetrics`, `getMomentInsights`, `runObservabilityQuery`). Check `SELECT Id FROM ApexClass WHERE Name = 'AgentforceOptimizeService'` first; **NEVER deploy it during a read-only investigation without explicit user authorization**.

### Root-Cause Priority Classification

| Priority | Observed Patterns | Evidence & Next Handoff |
| --- | --- | --- |
| P1 (Critical) | Action runtime errors (`ssot__ErrorMessageText__c`), subagent misroutes, LOW instruction adherence, safety/authorization boundary violations | Correlate with `.agent` bundle & backing action permissions (`agentforce-review`, `salesforce-security-access`) |
| P2 (High) | Missing/uninvoked actions, variable capture failures (`pre_vars` vs `post_vars`), RAG knowledge gaps / hallucinations | Confirm with single-session trace (`session-tracing-d360.md`), then reproduce via `agentforce-test` |
| P3 (Medium) | Slow actions, abandoned sessions, dead subagents / dead-hub routing, publish drift (org metadata vs local `.agent`), voice UX/latency anti-patterns | Flag architectural changes; route `.agent` edits to `agentforce-build` |

**Authorization boundary**: Read-only observation NEVER authorizes running live actions in `sf agent preview`, editing `.agent` files, publishing/activating agents, or enabling tracing. Hand off reproduction/regression suites to `agentforce-test` and bundle repairs to `agentforce-build`.

## 3. Agent Health Monitoring (AHM) Data Alerts

AHM alerts monitor aggregate agent metrics (escalation rate, deflection rate, latency, etc.) via `/services/data/v66.0/tableau/dataAlerts` (`dataAlertType: "agenthealthmonitoring"`). There is no `sf agent alert` subcommand; use `sf api request rest`.

### Authorization Gate
- **List alerts & inspect notifications**: Read-only (allowed during investigation).
- **Create (`POST`), Update (`PUT`), Delete (`DELETE`)**: State-changing mutations — **require explicit user authorization** for the target org, metric, threshold, and scope before executing.

### Safe Owner User ID Resolution (Prevent SOQL/Shell Injection)

```bash
# Preferred: current authenticated user (no user-supplied input)
USER_ID=$(sf org display user --target-org <org> --json \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["id"])')
```

If targeting another user, prefer a validated 15/18-character Salesforce User ID (`^[a-zA-Z0-9]{15,18}$`). Never interpolate untrusted free-text usernames directly into double-quoted `--query` strings.

### AHM REST Operations

Use a private `0600` temp file (`body=$(mktemp) && chmod 600 "$body"; trap 'rm -f "$body"' EXIT`) for POST/PUT bodies — never a fixed `/tmp/*.json` path.

```bash
# List alerts for owner (ownerId required; single-alert GET returns 405 -> filter client-side)
sf api request rest "/services/data/v66.0/tableau/dataAlerts?ownerId=$USER_ID" -o <org>

# Create alert (AUTHORIZED ONLY)
sf api request rest "/services/data/v66.0/tableau/dataAlerts" \
  -X POST -H "Content-Type: application/json" -b "@$body" -o <org>

# Update alert in place (AUTHORIZED ONLY; takes full POST-style body)
sf api request rest "/services/data/v66.0/tableau/dataAlerts/$ALERT_ID" \
  -X PUT -H "Content-Type: application/json" -b "@$body" -o <org>

# Delete alert (AUTHORIZED ONLY; returns 204)
sf api request rest "/services/data/v66.0/tableau/dataAlerts/$ALERT_ID" \
  -X DELETE -o <org> --include

# Inspect triggered alert notifications (MUST include X-UNS-Type-Filter: all)
sf api request rest "/services/data/v66.0/connect/notifications/status" \
  -H "X-UNS-Type-Filter: all" -o <org>
sf api request rest "/services/data/v66.0/connect/notifications" \
  -H "X-UNS-Type-Filter: all" -o <org>
```

### Three Silent-Failure Traps in AHM

1. **Thresholds are raw 0–1 ratios**: `5%` is `"0.05"`, not `"5"`; `"1"` means `100%`.
2. **POST/PUT field names and casing differ from GET**: POST/PUT uses `utterance` (not `alertName`) and PascalCase `type` discriminators. Never paste a raw GET payload back into POST/PUT.
3. **Mandatory notification header `X-UNS-Type-Filter: all`**: Without this header, `connect/notifications*` returns custom notification types only, causing AHM notifications (`type: templatized_data_alert`) to appear empty (false zero). Attribute notifications to a specific alert via `targetPageRef.state.c__alertId` (15/18-char safe), NOT `metricId` (which collides across alerts on the same metric).

## 4. Reporting Standard

Every trend or alert report must explicitly state:
- Target org, resolved agent (`MasterLabel` / `DeveloperName`), Data Space, and lookback window.
- Sample size (sessions/moments analyzed) and any STDM/DMO gaps or permission errors.
- Confirmed findings vs hypotheses, prioritized P1/P2/P3, and explicit companion handoffs (`agentforce-test`, `agentforce-build`, `agentforce-review`).
