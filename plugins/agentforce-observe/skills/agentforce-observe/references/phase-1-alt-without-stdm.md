# Phase 1-ALT: Observe Without STDM (Fallback Path)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 1-ALT: Observe Without STDM (Fallback Path)

When STDM is not available, use test suites and `sf agent preview --authoring-bundle` with local trace analysis.

| Data source | When to use | Pros | Cons |
|---|---|---|---|
| STDM (Phase 1) | Historical production analysis | Real user data, volume | Requires Data Cloud, 15-min lag |
| Test suites + local traces (Phase 1-ALT) | Dev iteration, orgs without STDM | Instant, full LLM prompt, variable state | Preview only, no real user data |

### 1-ALT.1 Run existing test suite (if available)

```bash
sf agent test list --json -o <org>
sf agent test run --json --api-name <TestSuiteName> --wait 10 --result-format json -o <org> | tee /tmp/test_run.json
JOB_ID=$(python3 -c "import json; print(json.load(open('/tmp/test_run.json'))['result']['runId'])")
sf agent test results --json --job-id "$JOB_ID" --result-format json -o <org>
```

### 1-ALT.2 Derive test utterances from .agent file (if no test suite)

If no test suite exists, derive utterances: one per non-entry subagent (from `description:` keywords), one per key action, one guardrail test, one multi-turn test.

### 1-ALT.3 Preview with `--authoring-bundle` (local traces)

Run each test utterance through preview to generate local trace files:

```bash
sf agent preview start --json --authoring-bundle <BundleName> --simulate-actions -o <org> | tee /tmp/preview_start.json
SESSION_ID=$(python3 -c "import json; print(json.load(open('/tmp/preview_start.json'))['result']['sessionId'])")

sf agent preview send --json --session-id "$SESSION_ID" --authoring-bundle <BundleName> \
  --utterance "$UTT" -o <org> | tee /tmp/preview_response.json

sf agent preview end --json --session-id "$SESSION_ID" --authoring-bundle <BundleName> -o <org>
```

**Trace file location:** `.sfdx/agents/{BundleName}/sessions/{sessionId}/traces/{planId}.json`

### 1-ALT.4 Local trace diagnosis

| Issue type | Trace command |
|---|---|
| Subagent misroute | `jq -r '.plan[] \| select(.type=="NodeEntryStateStep") \| .data.agent_name' "$TRACE"` |
| Action not called | `jq -r '.plan[] \| select(.type=="EnabledToolsStep") \| .data.enabled_tools[]' "$TRACE"` |
| LOW adherence | `jq -r '.plan[] \| select(.type=="ReasoningStep") \| {category, reason}' "$TRACE"` |
| Variable capture fail | `jq -r '.plan[] \| select(.type=="VariableUpdateStep") \| .data.variable_updates[]' "$TRACE"` |
| Vague instructions | `jq -r '.plan[] \| select(.type=="LLMStep") \| .data.messages_sent[0].content' "$TRACE"` |

**DefaultTopic trace quirk:** With `--authoring-bundle`, the root `.topic` field often shows `"DefaultTopic"` even when routing works. Always use `NodeEntryStateStep.data.agent_name` for the real subagent chain.

**Entry answering directly (SMALL_TALK pattern):** If `start_agent` trace shows `SMALL_TALK` grounding and transition tools visible but none invoked, add "You are a router only. Do NOT answer questions directly." to `start_agent` instructions.

### 1-ALT.5 Classify and present

Classify issues using the categories in `references/issue-classification.md`. After presenting findings, automatically proceed to agent config evidence analysis.

---
