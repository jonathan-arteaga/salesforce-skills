# Phase: RE-REVIEW

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: RE-REVIEW

Run a final config review to measure improvement:

```
Agent({
  description: "Run final config review",
  prompt: "Run /agentforce-config-review on the agent file at $AGENT_FILE_PATH. Target org: $ORG_USERNAME. This is a re-review after improvements. Write findings with today's date (ensure filename doesn't conflict with existing). Return findings JSON path and composite score. Per the Sub-Agent Delegation Policy: write any helper/scratch file (e.g. a docx-builder) ONLY under $PROJECT_ROOT/.agent-improvement/tmp/ (never /tmp or outside the project), give it a descriptive <phase>-<AgentName>-<purpose> name, and report any you create."
})
```

**Persona final score (only if a persona/tone finding was in scope this run).** If
`personaRubric.baseline` was captured, score the *improved* `.agent` with the persona skill's
brownfield SCORE and store it as `personaRubric.final` (see **Persona Rubric**):

```
Agent({
  description: "Score persona rubric (final)",
  prompt: "Run the `persona` skill from the personal Salesforce plugin in BROWNFIELD mode, SCORE phase only, on the agent file at $AGENT_FILE_PATH. Target org: $ORG_USERNAME. Do not redesign or encode — only audit and score the persona on the 100-point rubric. Return three things in your result: the integer total score (0–100), the band label, and the path to the evaluation.md it wrote. Per the Sub-Agent Delegation Policy: write any helper/scratch file (e.g. the persona working dir) ONLY under $PROJECT_ROOT/.agent-improvement/tmp/ (never /tmp or outside the project), give it a descriptive <phase>-<AgentName>-<purpose> name, and report any you create."
})
```

(The same prompt, run in REVIEW/PLAN against the *original* `$AGENT_FILE_PATH`, produces
`personaRubric.baseline`.)

After completion:
1. **Validate** the re-review findings JSON against the consumed-schema contract (see **Consumed JSON Contracts**). If a persona final score was captured, also validate it against the persona-rubric Consumed Contract.
2. **Reconcile against the initial Finding IDs.** Match re-review findings to the originals by their description/dimension and classify each:
   - **Resolved** — an initial Finding ID no longer present
   - **Persisting** — an initial Finding ID still present
   - **New** — a finding with no prior ID (assign a fresh ID per the Finding IDs scheme)

   **Persona findings are reconciled by the rubric, not by config-review presence** — apply the resolution rule defined in **Persona Rubric** (the single source of truth: resolved on a strong-enough rubric score that also beats baseline; otherwise persisting, even if config-review still flags the dimension; *persisting* if the rubric was unavailable, with the gap reported). Non-persona findings reconcile exactly as above.
3. Compare new score vs initial score
4. Report delta to user, broken down by ID where useful:
   - "Config review score: X.XX → Y.YY (delta: +/-Z.ZZ)"
   - If a persona finding was in scope: "Persona rubric: NN → MM (band: <baseline band> → <final band>)"
   - "Resolved: D3-H1, D2-M1, …"
   - "Persisting: D7-M1, …"
   - "New: D4-L1, …"
5. Update state (store the reconciliation and `personaRubric` under the re-review entry), set `currentPhase: "COMPLETE"`
6. If `GIT_AVAILABLE && consents.gitCommit`: commit review artifacts

---
