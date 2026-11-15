# Pre-Flight Checks

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Pre-Flight Checks
  - Check 1: Org Connectivity
  - Check 2: Agent File Exists
  - Check 3: Testing Skill Exists
  - Check 4: Config Review Skill Available
  - Check 5: Baseline Test Results
  - Check 6: Project Test Coverage
  - Check 7: Python Dependencies
  - Check 8: Git Availability
  - After All Checks Pass

## Pre-Flight Checks

Run these 8 checks in order. Stop on any hard failure. Warnings are logged but don't block.

### Check 1: Org Connectivity

The org was already resolved and pinned in **Run Identity & Org Resolution**. Re-confirm it is reachable using the pinned username:

```bash
sf org display -o $ORG_USERNAME --json
```

- PASS: JSON response contains `"status": 0`
- FAIL: "Cannot reach org `$ORG_USERNAME`. Run `sf org login web` and retry."

### Check 2: Agent File Exists

**First resolve the project's package directories** — don't assume `force-app/`. SFDX projects may use a different root or several package dirs. Read them from `sfdx-project.json` and save as `PACKAGE_DIRS` (every later filesystem search uses this, not a hardcoded path):

```bash
# PACKAGE_DIRS = the "path" of each entry in packageDirectories[]; fall back to force-app if the file is absent/empty
python3 -c "import json,os; p=os.path.join('$PROJECT_ROOT','sfdx-project.json'); d=json.load(open(p)) if os.path.exists(p) else {}; print(' '.join(e['path'] for e in d.get('packageDirectories',[])) or 'force-app')"
```

Then search for the agent across all of them:

```bash
for dir in $PACKAGE_DIRS; do find "$PROJECT_ROOT/$dir" -name "$AGENT_NAME.agent" -type f; done
```

- PASS: Exactly one file found. Save path as `AGENT_FILE_PATH`.
- FAIL: "Agent file `$AGENT_NAME.agent` not found in project `$PROJECT_ROOT` (searched: `$PACKAGE_DIRS`)."

### Check 3: Testing Skill Exists

```bash
grep -rl "$AGENT_NAME" .agents/skills/*/SKILL.md 2>/dev/null
```

Also check for `test-results.json` files referencing the agent:
```bash
grep -rl "\"agent\": \"$AGENT_NAME\"" .agents/skills/*/test-results.json 2>/dev/null
```

- PASS: Found a matching skill. Save the SKILL.md path as `TESTING_SKILL_PATH`, and its containing directory as `TESTING_SKILL_DIR` (e.g. `dirname $TESTING_SKILL_PATH`).
- FAIL: No testing skill found. **Trigger Testing Skill Bootstrap** (see below).

### Check 4: Config Review Skill Available

Look for `agentforce-config-review` in:
- `.agents/skills/agentforce-config-review/SKILL.md`
- The active personal Salesforce plugin; use the skill path provided by the host

- PASS: Skill located.
- SOFT FAIL: "Config review skill not available. Install the personal Salesforce plugin (it provides `agentforce-config-review`), or provide findings manually with `--findings <path>`."

### Check 5: Baseline Test Results

```bash
cat $TESTING_SKILL_DIR/test-results.json 2>/dev/null
```

- PASS: File exists, has `lastUpdated` set, **and passes the `test-results.json` validator** (see **Consumed JSON Contracts**: `passRate` a number in `[0,1]`, `passed`/`total` integers with `passed <= total`). Only then record `passRate`, `passed`, `total`, and `timestamp` into `state.baselineTestResults` — this is the baseline EVALUATE compares against. Running the same validator here, not just in TEST, stops a malformed-but-present baseline from seeding EVALUATE with invalid numbers.
- WARNING: "No baseline test results found. First iteration will establish baseline." Leave `state.baselineTestResults` as `null`; the first TEST result becomes the baseline. **Treat a present-but-invalid file the same way** — warn that the existing `test-results.json` failed validation (cite the detail), leave the baseline `null`, and let the first TEST re-establish it rather than trusting bad numbers.

### Check 6: Project Test Coverage

Run tests for project-local Apex classes only (ignore org-wide coverage):

```bash
# Find all test classes across the resolved package dirs (PACKAGE_DIRS from Check 2)
for dir in $PACKAGE_DIRS; do find "$PROJECT_ROOT/$dir" \( -name "*Test.cls" -o -name "*_Test.cls" \); done | \
  xargs -n1 basename | sed 's/.cls//' | paste -sd, -
```

```bash
sf apex run test --class-names <comma-separated-test-classes> --code-coverage -o $ORG_USERNAME --result-format json --wait 10
```

Evaluate coverage **only for classes that exist in the local project** (under `$PACKAGE_DIRS`). Ignore org-resident classes that are not part of this repo.

- PASS: All project test classes pass AND project class coverage averages >= 75%.
- WARNING: Tests fail or coverage is below 75%. Log details for the final report but **do not block** the loop. The agent file itself may still be improvable.

### Check 7: Python Dependencies

```bash
python3 -c "import docx" 2>&1
```

- PASS: No error.
- FAIL: "Missing Python packages. Run: `pip3 install python-docx`"

### Check 8: Git Availability

```bash
git --version 2>&1
```

- PASS: Set `GIT_AVAILABLE = true`. Whether the skill *uses* git is governed by the `gitCommit` / `gitRevert` consents from Session Setup — detection alone never authorizes a commit or revert.
- WARNING: "Git not available. Progress commits and auto-revert will be skipped." Set `GIT_AVAILABLE = false`.

### After All Checks Pass

Initialize the state file inside the **current project** (never the skill's install dir):
```
$PROJECT_ROOT/.agent-improvement/loop-state-$RUN_KEY.json
```

If a state file with this exact `RUN_KEY` already exists and `--resume` was *not* passed, do not silently overwrite it — see **Pre-existing State Without `--resume`** under State File Management.

Write initial state with `currentPhase: "REVIEW"` (or `"PLAN"` if `--skip-review` or `--findings`). The initial state **must** record the run identity so future reads can be validated:

```json
{
  "version": "1.3.0",
  "agentName": "$AGENT_NAME",
  "projectRoot": "$PROJECT_ROOT",
  "orgUsername": "$ORG_USERNAME",
  "orgId": "$ORG_ID",
  "orgAlias": "$ORG_ALIAS",
  "runKey": "$RUN_KEY",
  "currentPhase": "REVIEW",
  "settings": { "mode": "full_ownership", "maxIterations": 3 },
  "consents": { "deploy": false, "gitCommit": false, "gitRevert": false },
  "authorization": {},
  "gitAvailable": "<true|false from pre-flight Check 8>",
  "startedAt": "<ISO timestamp>",
  "lastUpdatedAt": "<ISO timestamp>",
  "iteration": 0,
  "baselineTestResults": null,
  "reviews": [],
  "batches": [],
  "iterations": [],
  "remaining": [],
  "errors": [],
  "outputs": []
}
```

`gitAvailable` is a literal JSON boolean (`true` / `false`), not the quoted string `"true"` — the `"<…>"` above is a fill-in placeholder, and every consumer (`GIT_AVAILABLE && consents.gitCommit`, the guardrails) reads it as a boolean.

Every array (`reviews`, `batches`, `iterations`, `remaining`, `errors`, `outputs`) is initialized **empty here**, and `iteration` starts at `0`, so the first cycle and any `--resume` never read `undefined`. EVALUATE's "Increment iteration" and the IMPLEMENT commit's `$ITERATION` both rely on this starting value. `personaRubric` is added later, only if a persona finding appears (see **Persona Rubric**). `remaining[]` collects findings known but not addressed this run — deferred LOW findings (PLAN) and the findings of any `skipped` batch (EVALUATE).

The top-level `"version"` field tracks the **state-file format** (currently `1.3.0`), independent of the plugin version in `plugin.json` — they version different things and are bumped on different occasions.

**Settings & consents.** These are captured in **Session Setup** and are the authoritative record
of what the user agreed to. The `--mode` flag maps to `settings.mode`: `full → "full_ownership"`,
`plan → "plan_only"`. Every git operation checks `consents.gitCommit` / `consents.gitRevert`;
deployment also requires a matching scoped `authorization` record (see Session Setup). On `--resume`, revalidate the identity and scope, carry forward still-valid explicit approvals, and honor any newer restriction. Legacy state without authorization evidence requires reconciliation with the user's actual request, not automatic approval.

**Baseline.** `baselineTestResults` starts `null` and is set by pre-flight Check 5 (or the first TEST
if no prior results exist). EVALUATE reads `state.baselineTestResults.passRate`.

**Output manifest.** `outputs[]` is the run's index of every artifact it produces, so the
user (or a `--resume`) can find everything in one place instead of hunting across `force-app/`,
the testing-skill dir, and `.agent-improvement/`. Append an entry the moment each deliverable is
written — review report, findings JSON, test report, `test-results.json`, improvement plan,
run summary. Each entry:

```json
{ "type": "config-review-report", "path": "<relative-to-projectRoot>", "phase": "REVIEW", "iteration": 0, "createdAt": "<ISO>" }
```

Use `type` values: `config-review-report`, `findings-json`, `test-report`, `test-results-json`,
`improvement-plan`, `run-summary`, `run-report-html` (the optional shareable HTML report from COMPLETE).

---
