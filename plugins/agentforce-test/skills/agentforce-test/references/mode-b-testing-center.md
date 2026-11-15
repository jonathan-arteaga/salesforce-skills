# Mode B: Testing Center Batch Testing

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Mode B: Testing Center Batch Testing

> Full reference: `references/batch-testing.md`

### Test Spec YAML Format

```yaml
name: "OrderService Smoke Tests"
subjectType: AGENT
subjectName: OrderService          # BotDefinition DeveloperName (API name)

testCases:
  - utterance: "Where is my order #12345?"
    expectedTopic: order_status
    expectedOutcome: "Agent checks order status"

  - utterance: "I want to return my order"
    expectedTopic: returns
    expectedActions:
      - lookup_order              # Use Level 2 INVOCATION names, NOT Level 1 definitions

  - utterance: "What's the best recipe for chocolate cake?"
    expectedOutcome: "Agent politely declines and redirects"
```

**Key rules:**
- `expectedActions` is a **flat string array** with **Level 2 invocation names** (from `reasoning: actions:`), NOT Level 1 definition names (from `subagent: actions:`)
- Action assertion uses **superset matching** -- test PASSES if actual actions include all expected
- **Always add `expectedOutcome`** -- most reliable assertion type (LLM-as-judge)
- For guardrail tests, omit `expectedTopic` and use `expectedOutcome` only. Filter out `topic_assertion` FAILURE for these (false negatives from empty assertion XML).

### Deploy and Run

```bash
# Deploy test suite
sf agent test create --json --spec /tmp/spec.yaml --api-name MySuite -o <org>

# Run and wait
sf agent test run --json --api-name MySuite --wait 10 --result-format json -o <org> | tee /tmp/run.json

# Get results (ALWAYS use --job-id, NOT --use-most-recent)
JOB_ID=$(python3 -c "import json; print(json.load(open('/tmp/run.json'))['result']['runId'])")
sf agent test results --json --job-id "$JOB_ID" --result-format json -o <org> | tee /tmp/results.json
```

### Parse Results

```bash
python3 -c "
import json
data = json.load(open('/tmp/results.json'))
for tc in data['result']['testCases']:
    utterance = tc['inputs']['utterance'][:50]
    results = {r['name']: r['result'] for r in tc.get('testResults', [])}
    topic = results.get('topic_assertion', 'N/A')
    action = results.get('action_assertion', 'N/A')
    outcome = results.get('output_validation', 'N/A')
    print(f'{utterance:<50} topic={topic:<6} action={action:<6} outcome={outcome}')
"
```

### Topic Name Resolution

Topic names in Testing Center may differ from `.agent` file names. If assertions fail on subagent routing:
1. Run test with best-guess names
2. Check actual: `jq '.result.testCases[].generatedData.topic' /tmp/results.json`
3. Update YAML with actual runtime names and redeploy with `--force-overwrite`

**Topic hash drift**: Runtime hash suffix changes after agent republish. Re-run discovery after each publish.

See `references/batch-testing.md` for full YAML field reference, multi-turn examples, known bugs, and auto-generation from `.agent` files.

---
