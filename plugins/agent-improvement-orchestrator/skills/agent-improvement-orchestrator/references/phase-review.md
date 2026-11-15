# Phase: REVIEW

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: REVIEW

**Skip if:** `--skip-review` is set or `--findings <path>` is provided.

Invoke `/agentforce-config-review` via sub-agent to avoid context exhaustion:

```
Agent({
  description: "Run config review",
  prompt: "Run /agentforce-config-review on the agent file at $AGENT_FILE_PATH. Target org: $ORG_USERNAME. Write findings to the agent directory with today's date in the filename. Return the findings JSON file path and composite score when complete. Per the Sub-Agent Delegation Policy: write any helper/scratch file ONLY under $PROJECT_ROOT/.agent-improvement/tmp/ (never /tmp or outside the project), give it a descriptive <phase>-<AgentName>-<purpose> name, and report any you create."
})
```

After the sub-agent completes:
1. Read the findings JSON file path from the result
2. **Validate** the findings JSON against the consumed-schema contract (see **Consumed JSON Contracts**). If required fields are missing, stop and surface the problem rather than planning against a malformed file.
3. Parse `composite_score`, then flatten `sections[].findings[]` across all sections and count by severity
4. **Assign a stable Finding ID to every finding** (see **Finding IDs** below), using each finding's parent `sections[].number` as the `D<n>` dimension. These IDs are the traceability thread that links REVIEW → PLAN → IMPLEMENT → RE-REVIEW. Store the assigned IDs in state under `reviews[].findings[]` so later phases reference the same identifiers.
5. **Persona baseline (only if a persona/tone finding exists).** If any finding matches the Persona / tone weakness pattern, capture the baseline persona rubric *now*, before any fix — see **Persona Rubric**. Store it in state under `personaRubric.baseline`. If no persona finding is present, skip this step entirely (no rubric work happens this run).
6. Update state: add to `reviews[]`, set `currentPhase: "PLAN"`
7. If `GIT_AVAILABLE && consents.gitCommit`: commit review artifacts

### Finding IDs

Every finding gets a stable ID of the form **`D<dimension>-<SEV><n>`**:

- `D<dimension>` — the scorecard dimension number the finding belongs to (e.g. `D2` = Instructions/Actions, `D3` = Guardrails). Use `D0` if a finding maps to no specific dimension.
- `<SEV>` — `H`, `M`, or `L` for HIGH / MEDIUM / LOW.
- `<n>` — a 1-based counter within that dimension+severity, in the order findings appear.

Examples: `D3-H1` (first HIGH guardrail finding), `D2-M1`, `D1-L2`.

Rules:
- IDs are assigned **once**, when findings first enter the run, and never reused or renumbered within a run. Normally that is REVIEW; on the skip path (`--findings` / `--skip-review`, where REVIEW doesn't run) they are assigned at the start of PLAN instead. Either way, every finding has an ID before any batch is planned.
- The RE-REVIEW reconciles against these IDs (see RE-REVIEW): a finding is *resolved* if its ID is no longer present, *persisting* if still present, *new* if it has no prior ID (assign a fresh one).
- Every plan item, commit message, and report row that refers to a finding **must cite its ID**, so a reader can follow one issue across all deliverables.

---
