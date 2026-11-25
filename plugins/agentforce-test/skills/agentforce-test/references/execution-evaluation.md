# Test Execution, Voice Heuristics & Evaluation

Execute authorized test runs cleanly across preview smoke tests, Testing Center batches, isolated REST action checks, and live voice validation while preserving strict evidence boundaries.

## Mode A: Ad-Hoc Preview Smoke Testing (`sf agent preview`)

Requires `sf` CLI **2.131.0+** (`plugin-agent` 1.32.16+) inside an SFDX project (`sfdx-project.json`). Pass `--simulate-actions` (default) or `--use-live-actions` (explicit opt-in + sandbox only) on `start` ONLY:

```bash
sf agent preview start --json --authoring-bundle <ApiName> --simulate-actions -o <org>
sf agent preview send --json --session-id <ID> --utterance "<msg>" --authoring-bundle <ApiName> -o <org>
sf agent preview end --json --session-id <ID> --authoring-bundle <ApiName> -o <org>
```

For Mode C2 adversarial probing, use one fresh session per payload under `--simulate-actions` to isolate state and avoid unintended writes.

## Mode B: Testing Center Batch Execution (`sf agent test`)

```bash
sf agent test create --json --spec tests/<Agent>-testing-center.yaml --api-name <SuiteApiName> -o <org>
sf agent test run --json --api-name <SuiteApiName> --wait 10 --result-format json -o <org>
```

- **Cost & mutation reminder:** Testing Center runs consume requests/Flex Credits and can mutate CRM records without automatic rollback. Verify `SELECT IsSandbox FROM Organization` and synthetic fixtures before running.

## Direct Flow / Apex Action Isolation (REST API)

Before invoking any action directly via REST (`/services/data/v63.0/actions/custom/flow/<ApiName>` or `/actions/custom/apex/<ClassName>`), enforce the 3-part safety gate: (1) verify non-production sandbox, (2) warn on any CREATE/UPDATE/DELETE DML, and (3) require synthetic inputs with zero real PII. Never print raw access tokens in reports or logs.

## Voice Latency & Live-Call Evaluation Heuristics

Text preview and Testing Center suites CANNOT prove voice UX outcomes. For voice agents, schedule real test calls in an authorized sandbox and evaluate:

- **Latency pass budget:** Floor is ~1.3s (1 fast LLM pass 0.85-1.4s + 0.3-0.7s overhead; large model up to ~2.8s; Apex ~0.25-0.35s; Trust Layer runs async). Count back-to-back LLM passes first when diagnosing slow turns.
- **Filler & silence verification:** Confirm `beepboop_config` (`max_wait_time_ms: 500`), spoken filler rotation, per-action `progress_indicator_message` (>1s lookups; periodic filler >3s; explicit wait notice >10s), and `speak_up_config` (>=10000ms, 3-strike behavior).
- **Live telephony checks:** Verify barge-in recovery, ASR misrecognition repair tiers, digit/phonetic grounding, escalation transfer, `VoiceCall` record creation, and Real-Time Streaming recording/consent behavior.

## Scoring, Reporting & Exit Codes

Report subagent routing %, action invocation %, grounding %, safety %, response quality %, safety verdict (`SAFE`/`UNSAFE`/`NEEDS_REVIEW`), and OWASP A-F grade (Mode C2). Always include target org, agent version, suite path, execution mode (`simulated` vs. `live`), and explicit separation of simulated vs. live proof:

- **Exit 0:** All tests passed — eligible for next gate.
- **Exit 1:** Non-critical failures — review before deploy.
- **Exit 2:** Critical/security failure — block deployment.
- **Exit 3:** Execution/CLI error (e.g., CLI < 2.131.0 missing `--simulate-actions`, session timeout) — fix harness and rerun.
