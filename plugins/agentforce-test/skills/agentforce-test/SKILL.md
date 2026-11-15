---
name: |-
  agentforce-test
description: |-
  Author, run, or analyze structured Agentforce test suites in an authorized environment. Return test specifications or results. Use agentforce-generate for authoring changes.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.

For industry-specific agents, cross-industry ideation, or role/personality choices, read the selected patterns in [industry and role design](references/shared/industry-patterns.md). Use them within this skill’s ownership; distinguish documented capabilities from proposed designs.


# ADLC Test

Automated testing for Agentforce agents with smoke tests, batch execution, and iterative fix loops.

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## Overview

This skill provides comprehensive testing capabilities for Agentforce agents, including automated utterance derivation from agent subagents, preview-based smoke testing, trace analysis, an iterative fix loop for identified issues, and **security testing** (OWASP LLM Top 10). It bridges the gap between initial development and production deployment.

**Security testing is part of the ADLC, not a separate skill.** Functional correctness (right topic, right action) and security posture (resists attacks) are two dimensions of the same test suite. Treat adversarial coverage as part of the test flow and the Agent Spec — when you plan tests for an agent, plan its security tests too. Security test-case generation is **gated on explicit user confirmation** (see Mode C).

## Platform Notes

- Shell examples below use bash syntax. On Windows, use PowerShell equivalents or Git Bash.
- Replace `python3` with `python` on Windows.
- Replace `/tmp/` with `$env:TEMP\` (PowerShell) or `%TEMP%\` (cmd).
- Replace `jq` with `python -c "import json,sys; ..."` if jq is not installed.
- `find ... | head -1` -> `Get-ChildItem -Recurse ... | Select-Object -First 1` in PowerShell.

## Usage

This skill uses `sf agent preview` and `sf agent test` CLI commands directly.<br />There is no standalone Python script.

**Quick smoke test (Mode A):**

```bash
# Start preview, send utterance, end session (--authoring-bundle generates local traces).
# Run from inside the Salesforce project directory (the CLI requires sfdx-project.json).
# With --authoring-bundle, `start` REQUIRES an action mode: --simulate-actions or
# --use-live-actions. The mode flag belongs on `start` only — `send` and `end` reject it.
sf agent preview start --json --authoring-bundle MyAgent --simulate-actions -o <org-alias>
sf agent preview send --json --session-id <ID> --utterance "test" --authoring-bundle MyAgent -o <org-alias>
sf agent preview end --json --session-id <ID> --authoring-bundle MyAgent -o <org-alias>
```

**Batch testing (Mode B):**

```bash
# Deploy and run test suite
sf agent test create --json --spec test-spec.yaml --api-name MySuite -o <org-alias>
sf agent test run --json --api-name MySuite --wait 10 --result-format json -o <org-alias>
```

**Security testing (Mode C — confirm with the user before generating):**

```bash
# You read the .agent file and write the security cases yourself — same as
# Mode B, with security-specific guidance in references/security-test-design.md.

# C1: deploy the security suite you authored (identical to Mode B)
sf agent test create --json --spec /tmp/MyAgent-security-spec.yaml --api-name MyAgent_Security -o <org-alias>

# C2: live adversarial probing (identical to Mode A, one fresh session per case).
# --simulate-actions is the C2 default: probe the agent's reasoning without firing
# real Apex/Flow writes. Only substitute --use-live-actions on explicit user opt-in.
sf agent preview start --json --authoring-bundle MyAgent --simulate-actions -o <org-alias>
sf agent preview send --json --session-id <ID> --utterance "<payload>" --authoring-bundle MyAgent -o <org-alias>
sf agent preview end --json --session-id <ID> --authoring-bundle MyAgent -o <org-alias>
```

**Action execution:**

```bash
# Execute a Flow or Apex action directly via REST API
TOKEN=$(sf org display -o <org-alias> --json | jq -r '.result.accessToken')
INSTANCE_URL=$(sf org display -o <org-alias> --json | jq -r '.result.instanceUrl')
curl -s "$INSTANCE_URL/services/data/v63.0/actions/custom/flow/Get_Order_Status" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"inputs": [{"orderId": "00190000023XXXX"}]}'
```

## Testing Workflow

This skill supports three testing modes plus direct action execution:

- **Mode A: Ad-Hoc Preview Testing** -- Quick smoke tests during development using `sf agent preview`. No test suite deployment needed (org authentication still required). Best for iterative development and fix validation.
- **Mode B: Testing Center Batch Testing** -- Persistent test suites deployed to the org via `sf agent test`. Best for regression suites, CI/CD, and cross-skill integration with /agentforce-observe.
- **Mode C: Security Testing (OWASP LLM Top 10)** -- Adversarial testing across 7 OWASP categories. You write the cases yourself by reading the agent's own `.agent` script and business domain, using the neutral technique catalog in `assets/payloads/` as a coverage checklist. Two sub-modes over the same authored case set: **C1** deploys them as a Testing Center security suite (`AiEvaluationDefinition`, mechanically identical to Mode B); **C2** probes them live via `sf agent preview` (mechanically identical to Mode A) with A–F severity grading. **Generating security test cases requires explicit user confirmation.**
- **Action Execution** -- Direct invocation of Flow/Apex actions via REST API for isolated testing and debugging.

**When to use which:**

| Scenario | Mode |
| --- | --- |
| Quick smoke test during authoring | Mode A |
| Validate a fix from /agentforce-observe | Mode A |
| Build a regression suite for CI/CD | Mode B |
| Deploy tests to share with the team | Mode B |
| Persistent, re-runnable security regression suite | Mode C1 |
| Deep security assessment / red-team with A–F grade before sign-off | Mode C2 |
| Test a single Flow or Apex action in isolation | Action Execution |

---

## Mode A: Ad-Hoc Preview Testing

Consult [`references/mode-a-preview-testing.md`](references/mode-a-preview-testing.md) before Mode A.

## Mode B: Testing Center Batch Testing

Consult [`references/mode-b-testing-center.md`](references/mode-b-testing-center.md) before Mode B.

## Mode C: Security Testing (OWASP LLM Top 10)

Consult [`references/mode-c-security-testing.md`](references/mode-c-security-testing.md) before Mode C.

## Test environment and evidence

Testing Center can modify CRM data and consume credits. Run Testing Center suites in a sandbox with synthetic fixtures. Record the agent version, suite, test data, and simulated versus live-action mode. Do not assume a test run rolls back changes or a simulation proves runtime permissions, integration, or handoff behavior. Use existing authorization for the same target/scope; a request to author a plan is not a request to run live actions.

## Action Execution

> Full reference: `references/action-execution.md`

Execute individual Flow and Apex actions directly via REST API, bypassing the agent runtime.

### Safety Gate (Required)

Before executing ANY action:

1. **Org check**: `sf data query -q "SELECT IsSandbox FROM Organization" -o <org> --json` -- warn and require confirmation for production orgs
2. **DML check**: Warn if action performs write operations (CREATE, UPDATE, DELETE)
3. **Input validation**: Use synthetic test data only (`test@example.com`, `000-00-0000`). Warn if user provides real PII.

### Execution

```bash
TOKEN=$(sf org display -o <org> --json | jq -r '.result.accessToken')
INSTANCE_URL=$(sf org display -o <org> --json | jq -r '.result.instanceUrl')

# Flow action
curl -s "$INSTANCE_URL/services/data/v63.0/actions/custom/flow/{flowApiName}" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"inputs": [{"param": "value"}]}'

# Apex action
curl -s "$INSTANCE_URL/services/data/v63.0/actions/custom/apex/{className}" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"inputs": [{"param": "value"}]}'
```

See `references/action-execution.md` for integration testing patterns, debugging, and error handling.

---

## Test Report Format

> Full reference: `references/test-report-format.md`

Reports include: subagent routing %, action invocation %, grounding %, safety %, response quality %, overall score, and status (PASSED / PASSED WITH WARNINGS / FAILED). Safety verdict (SAFE/UNSAFE/NEEDS\_REVIEW) is always included. **Security runs (Mode C2)** additionally produce an OWASP A–F grade with per-category subtotals and per-failure remediation.

### Test File Location Convention

```txt
<project-root>/tests/
  <AgentApiName>-testing-center.yaml  # Full smoke suite (Mode B)
  <AgentApiName>-regression.yaml      # Regression tests from /agentforce-observe (Mode B)
  <AgentApiName>-smoke.yaml           # Ad-hoc smoke tests (Mode A)
  <AgentApiName>-security.yaml        # OWASP security suite (Mode C1)
```

---

## Troubleshooting

> Full reference: `references/troubleshooting.md`

| Issue | Solution |
| --- | --- |
| Session timeout | Split into smaller batches |
| Trace not found | Update to sf CLI 2.131.0+ |
| `Nonexistent flag: --simulate-actions` | CLI older than 2.131.0 — update; the flag does not exist below it |
| `jq` parse error | Use Python `re.sub` to strip control characters before parsing |
| Empty traces | Check `transcript.jsonl` or use Mode B instead |
| Security-specific issues | See `references/security-troubleshooting.md` (sessions, rate limits, INCONCLUSIVE) |

## Dependencies

- `sf` CLI **2.131.0+** (plugin-agent 1.32.16+). This is the floor for the flow this skill documents: `preview start`/`send`/`end` as separate subcommands arrived in plugin-agent 1.28.0, and `--simulate-actions` — which `start --authoring-bundle` requires — arrived in 1.32.16, first shipped in CLI 2.131.0. Below that, `start` accepts only `--use-live-actions`, so every simulated-action example fails with `Nonexistent flag`. Check with `sf --version` and `sf plugins --core | grep agent`.
- `jq` (system) -- JSON processing
- `python3` -- For result parsing snippets
- `pyyaml>=6.0` -- Only for the optional local spec-shape check in `references/security-test-design.md`. Nothing in the skill flow requires it: you author the YAML and the CLI validates it.

## Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | All tests passed -- safe to deploy |
| 1 | Some tests failed -- review before deploying |
| 2 | Critical failure -- block deployment |
| 3 | Test execution error -- fix infrastructure |
