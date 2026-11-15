# Phase: EVALUATE

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: EVALUATE

Compare test results against baseline:

```
currentPassRate = state.iterations[current].testResults.passRate
baselinePassRate = state.baselineTestResults.passRate
```

**First-iteration baseline:** if `state.baselineTestResults` is `null` (no prior results existed at
pre-flight), this iteration's result *establishes* the baseline — set `state.baselineTestResults`
from it, treat the iteration as successful, and skip the regression branch this once.

### Decision Tree

**If `currentPassRate >= baselinePassRate`:**
- Tests pass. This iteration is successful. Mark the current batch `succeeded` in `state.batches[]`.
- If a `pending` batch remains AND `iteration < maxIterations`:
  - Increment iteration, set `currentPhase: "PLAN"` (PLAN advances to the next `pending` batch — it does not re-derive)
- Else:
  - Set `currentPhase: "RE_REVIEW"`

**If `currentPassRate < baselinePassRate` (regression):**
- Identify which personas regressed
- **Revert the last fix batch — restore *both* the files and the org.** A regressed batch is already
  **deployed and live**; restoring only the working tree leaves the bad metadata in the org, and the
  next batch would deploy on top of it. Reverting therefore has two parts, in order:

  1. **Restore the working tree** — **only if `GIT_AVAILABLE && consents.gitRevert` and the scoped authorization record covers this rollback:** Verify the user approval and affected batch paths before any deletion or restoration; never use a legacy flag alone.
     ```bash
     git checkout -- <batch.modifiedPaths>          # undo edits to files that existed before the batch
     rm -rf <batch.addedPaths>                        # remove files the batch newly created (git checkout can't:
                                                      # they're untracked). Delete only these recorded paths —
                                                      # never a broad `git clean -fd`, which would also wipe
                                                      # unrelated untracked working-tree files.
     ```
  2. **Re-sync the org so the live agent matches the restored files** (show the diff and check scoped deployment and rollback authorization from Session Setup, including deletion of newly added components; ask only for permission not already granted):
     - **Modified files** — re-deploy the restored versions:
       ```bash
       sf project deploy start --source-dir <dirs covering batch.modifiedPaths> -o $ORG_USERNAME --json
       ```
     - **Added files** — these were *new* components, so a constructive deploy won't remove them;
       delete them from the org explicitly (a plain `deploy start` of the restored tree leaves the
       added components live):
       ```bash
       sf project delete source --source-dir <batch.addedPaths> -o $ORG_USERNAME --no-prompt --json
       ```
       If a component can't be cleanly removed (dependency, packaging), say so explicitly rather than
       leaving the org dirty.

  **The regression is only marked handled once step 2 succeeds.** If the re-deploy fails, stop and
  tell the user the org is in a mixed state and name the files, rather than silently proceeding.

  If `gitRevert` was declined (or no git): **do not discard edits silently, and do not pretend the org
  is clean.** Stop and tell the user the org *and* the working tree both still hold the regressed change:
  > "Iteration $ITERATION regressed the pass rate ($BASELINE_RATE → $currentPassRate). This batch is **still deployed and live in `$ORG_USERNAME`**, and these working-tree paths still hold it — modified: `<batch.modifiedPaths>`; newly added: `<batch.addedPaths>`. I won't discard your changes or redeploy without permission. To fully undo this you must revert the files **and** redeploy the clean state to the org. Revert + redeploy manually, or enable auto-revert to let me handle both?"
- Log regression in state; mark the batch `reverted`
- **Count this as a used attempt on the batch.** `batches[].attempts` was set to `1` when the batch was
  first applied in IMPLEMENT and is incremented on every re-application, so after this regression it equals
  the number of times the batch has been tried. A batch gets **up to 3 attempts**:
  - If `batches[].attempts < 3`: try an alternative fix pattern for the same findings — the batch returns to
    `pending` for re-application (IMPLEMENT will increment `attempts` again) and the loop re-enters IMPLEMENT.
  - If `batches[].attempts >= 3` (third regression): mark the batch `skipped` (unresolvable after 3 attempts),
    record its findings in `remaining[]` with a one-line reason, and move to the next `pending` batch, or
    RE-REVIEW if none remain.

  This per-batch attempt cap (3) is **independent** of the whole-run `--max-iterations` cycle cap — see
  Guardrails.

**If `iteration >= maxIterations`:**
- Stop regardless of remaining findings
- Set `currentPhase: "RE_REVIEW"`
- Report: "Max iterations reached. N findings remain unaddressed."

---
