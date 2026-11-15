# Phase: TEST

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: TEST

Delegate entirely to the project's testing skill via sub-agent:

```
Agent({
  description: "Run agent tests",
  prompt: "You are running tests for the $AGENT_NAME agent. Read the testing skill at $TESTING_SKILL_PATH and follow its instructions to run ALL personas. Use org $ORG_USERNAME. Write results to the test-results.json file as specified by the skill. Return the overall pass rate and any failures. Per the Sub-Agent Delegation Policy: write any helper/scratch file (e.g. a preview-call wrapper) ONLY under $PROJECT_ROOT/.agent-improvement/tmp/ (never /tmp or outside the project), give it a descriptive <phase>-<AgentName>-<purpose> name, and report any you create."
})
```

After the sub-agent completes:
1. Read `test-results.json` from the testing skill directory
2. **Validate** it against the consumed-schema contract (see **Consumed JSON Contracts**). If `passRate`/`passed`/`total` are missing or inconsistent, stop and surface the problem — EVALUATE compares against these numbers and must not run on a malformed file.
3. Extract overall pass rate and per-persona results
4. **Write the results onto `iterations[current]`** — set `testResults` (`{ passRate, passed, total }`, plus
   per-persona detail if available) on the entry whose `iteration == state.iteration` (the one IMPLEMENT
   created this cycle). This is exactly what EVALUATE reads back as `state.iterations[current].testResults.passRate`.
5. Set `currentPhase: "EVALUATE"`

**Report shareability:** any HTML test report produced for sharing must include a print/PDF
path — an `@media print` light-theme block and a `beforeprint` handler that expands collapsed
sections — so a dark-theme screen report doesn't render as an unreadable, ink-heavy PDF. See the
sample reports under `examples/` for the pattern.

---
