# Agent Health Monitoring (AHM)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Agent Health Monitoring (AHM)

> Full AHM alert procedures -- POST schema, enums, SDM/metric/agent discovery, thresholds, metric verification, troubleshooting: see `references/ahm-alerts.md`

Proactive complement to the reactive Observe phases: **AHM data alerts** fire when an agent metric (escalation, deflection, etc.) crosses a threshold. Driven through `sf api request rest` against `tableau/dataAlerts` (`dataAlertType: "agenthealthmonitoring"`) -- there is no `sf agent alert` subcommand yet. Reuse **Phase 0** for `dataspace`. Build the POST body and discover the SDM, its `_mtc` metric id, and the agent filter value **per the reference first**, then:

```bash
# List/describe -- resolve owner id first (required); single-alert GET is 405 => list + filter client-side
USER_ID=$(sf org display user --target-org <org> --json | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["id"])')
sf api request rest "/services/data/v66.0/tableau/dataAlerts?ownerId=$USER_ID" -o <org>
# Create / PUT update-in-place / delete (204). PUT & DELETE are addressed by $ALERT_ID in the path; PUT takes the full POST-style body. Bodies per reference into a 0600 mktemp file.
sf api request rest "/services/data/v66.0/tableau/dataAlerts" -X POST -H "Content-Type: application/json" -b "@$body" -o <org>
sf api request rest "/services/data/v66.0/tableau/dataAlerts/$ALERT_ID" -X PUT -H "Content-Type: application/json" -b "@$body" -o <org>
sf api request rest "/services/data/v66.0/tableau/dataAlerts/$ALERT_ID" -X DELETE -o <org> --include
# Notifications REQUIRE header X-UNS-Type-Filter: all (else custom-types-only => AHM empty = false 0). Report status + list.
sf api request rest "/services/data/v66.0/connect/notifications/status" -H "X-UNS-Type-Filter: all" -o <org>
sf api request rest "/services/data/v66.0/connect/notifications"        -H "X-UNS-Type-Filter: all" -o <org>
# AHM notifications: type=templatized_data_alert; no per-alert endpoint. Attribute by alertId in targetPageRef.state.c__alertId (15/18-char-safe), NOT metricId (collides).
```

**Three silent-failure traps to carry into any alert work:**
- **Thresholds are raw 0-1 ratios**, not display percentages -- 5% is `"0.05"`, `"1"` means 100%.
- **POST field names/casing differ from GET** -- POST uses `utterance` (not `alertName`) and PascalCase `type` discriminators, so copying a GET response back into a POST fails.
- **Notifications need `X-UNS-Type-Filter: all`** -- without it `connect/notifications*` returns custom types only, so AHM notifications (type `templatized_data_alert`) come back empty; an empty list is a false negative, not "never fired."

---
