# Persona Rubric

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Persona Rubric

The `persona` skill carries its own **100-point persona rubric** (its SCORE
phase, brownfield mode). The orchestrator uses it for one purpose: to judge whether a persona/tone
fix actually landed. It is **supplementary** — it never touches the loop's continue/stop/regression
spine (that stays pass-rate + config-review composite), and it is **authoritative only inside the
persona lane**: it governs whether a *persona* Finding ID counts as resolved, nothing else.

This is the single source of truth for how the rubric is used; REVIEW/PLAN, RE-REVIEW, and COMPLETE
all gate on it.

**When it runs.** Only when the run contains at least one persona/tone finding (the Persona / tone
weakness pattern). If there is no such finding, no rubric work happens — there is no overhead on runs
that don't touch persona.

**Capturing a score.** Delegate a brownfield SCORE via sub-agent (see the delegation prompt under
**Phase: RE-REVIEW**). The persona skill writes its evaluation to `persona/<agent>/evaluation.md` as
prose plus a percentage — **not** machine-readable JSON — so capture the number from the sub-agent's
**returned result**, exactly the way REVIEW captures `composite_score` and TEST captures `passRate`
(see the persona-rubric **Consumed Contract**). Store:

```json
"personaRubric": {
  "baseline": { "score": 62, "band": "needs revision", "evaluationPath": "<rel-path>" },
  "final":    { "score": 88, "band": "strong foundation", "evaluationPath": "<rel-path>" }
}
```

- **baseline** — scored on the *original* `$AGENT_FILE_PATH`, captured in REVIEW step 5 (or at the
  start of PLAN on the skip path), before any fix.
- **final** — scored on the *improved* `.agent` in RE-REVIEW, after the persona fix deployed.

**Resolution rule (persona Finding IDs only).** At RE-REVIEW, a persona finding is **resolved** iff
`final.score >= 75` **and** `final.score > baseline.score` (the skill's own "strong foundation" band,
and a real improvement over baseline). Otherwise it is **persisting**. This rule *replaces*, for
persona findings, the default "resolved if the ID is no longer present in config-review" — the rubric
governs the persona lane even if config-review still flags the dimension. **Non-persona** findings
reconcile exactly as before, by Finding ID presence in config-review output.

**Bands** (from the persona skill): ≥90 production-ready, ≥75 strong foundation, 50–74 needs revision,
<50 significant gaps.

**Degraded path.** If a rubric score can't be captured or fails validation (see Consumed Contracts),
treat the persona finding as **unresolved**, report that the rubric was unavailable, and continue the
rest of the loop — never block on it.

---
