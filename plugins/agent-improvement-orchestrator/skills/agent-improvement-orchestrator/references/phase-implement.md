# Phase: IMPLEMENT

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: IMPLEMENT

**Count the attempt.** On entering IMPLEMENT for the current batch, set `batches[].attempts` to `1` if it
is unset (first application), or increment it by `1` if the batch is being re-applied after a regression.
EVALUATE uses this counter to allow **up to 3 attempts** per batch before skipping it.

For each fix in the current batch:

1. **Read** the target file(s)
2. **Apply** the fix using Edit tool (prefer surgical edits over full rewrites)
3. **Verify** syntax: for `.agent` files, check for common DSL errors; for Apex, check compilation

After all fixes in the batch are applied:

4. **Deploy:** Show the diff and apply the authorization check in [Session Setup](session-setup.md). If deployment is not authorized, finish independent local preparation and report the pending deployment; do not claim live tests ran. Otherwise run:
   ```bash
   sf project deploy start --source-dir <modified-dirs> -o $ORG_USERNAME --json
   ```

5. **Handle deploy failure:**
   - If validation error: attempt auto-fix (1 retry max)
   - If still failing: revert the batch (per the `gitRevert` rule — git if granted, else ask), skip this batch, move to next
   - Log error in state

6. **Update state:** Record fixes applied, set `currentPhase: "TEST"`.
   - **Append (or update) this cycle's `iterations[]` entry.** Append a new entry keyed to the current
     iteration — `{ "iteration": <state.iteration>, "phase": "IMPLEMENT", "fixes": [ { "findingIds": [...], "summary": "..." }, ... ], "regressions": [], "commitSha": <set in step 7 if committed> }` — if no entry for
     `state.iteration` exists yet, otherwise update the existing one's `fixes`. Throughout the loop,
     **`iterations[current]` means the entry whose `iteration == state.iteration`** — TEST writes
     `testResults` onto this same entry and EVALUATE reads `state.iterations[current].testResults.passRate`
     from it (see TEST/EVALUATE). The shape matches `examples/loop-state-example.json`.
   - **Record the batch's file changes split into `added` (paths that did not exist before this batch) and `modified` (paths that existed and were edited)** — store them on the batch (`batches[].addedPaths`, `batches[].modifiedPaths`). The regression path in EVALUATE needs this split to undo new files correctly (see EVALUATE); a single combined list would either miss untracked additions or risk clobbering unrelated working-tree changes.
   - Persist `batches[].attempts` (set/incremented at the top of this phase).

7. **Git commit** — only if `GIT_AVAILABLE && consents.gitCommit`:
   ```bash
   git add <modified-files>
   git commit -m "improvement-loop iter $ITERATION: <Finding IDs> <fix summary>"
   # e.g. "improvement-loop iter 1: D3-H1,D2-M1 block invented discount + anti-jailbreak guard"
   ```
   The Finding IDs in the message keep git history on the traceability thread.

**IMPORTANT:** Reuse explicit deployment authorization only for the same project, org, agent, and permitted changes. A default flag, a local-edit request, or a saved state file without authorization evidence does not authorize deployment. A failed attempt permits a retry only within that same authorized scope.

---
