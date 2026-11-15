---
name: |-
  agent-improvement-orchestrator
description: |-
  Coordinate an Agentforce review, improvement plan, and authorized validation. Return an advisory plan or evidence-backed result. Use agentforce-config-review for a one-off review.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# agent-improvement-orchestrator

Orchestrate structured improvement loops for any Agentforce agent.

---

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

## Execution Cheat Sheet

Quick orientation — each line points to the section that owns the detail.

- **Flow:** Run Identity → Session Setup → Pre-Flight (8 checks) → `REVIEW → PLAN → IMPLEMENT → TEST → EVALUATE` (loop, max `--max-iterations`) → `RE-REVIEW → COMPLETE`. Plan Only mode stops after PLAN.
- **Consents** (Session Setup; the source of truth): `deploy` (off until explicitly authorized for a bounded scope) · `gitCommit` (off) · `gitRevert` (off). Detection never equals authorization. (Writing reports/state under the project is intrinsic to the skill — not a consent.)
- **Finding IDs** `D<dim>-<SEV><n>` (e.g. `D3-H1`) thread one issue across all phases; assigned when findings first enter the run (REVIEW, or PLAN on the skip path).
- **State:** `$PROJECT_ROOT/.agent-improvement/loop-state-$RUN_KEY.json`, `RUN_KEY = <AgentName>__<OrgId>`. Validate identity on every read; never adopt a stored org.
- **Org:** pinned by `$ORG_USERNAME` (never alias/default). **Deploy:** show the diff and verify it remains within the recorded authorization; ask only for missing or changed scope. **Delegated** to other skills: config review, testing, persona, deploy.

---

## On Every Invocation

1. Parse arguments from the user's invocation
2. **Establish Run Identity** (see below) — resolve the project root and pin the target org *before* anything else. This must happen on every invocation, including `--resume`.
3. **Sweep a stale scratch dir.** Once `$PROJECT_ROOT` is known, if `$PROJECT_ROOT/.agent-improvement/tmp/` exists (left by a prior run that aborted before COMPLETE), rename it aside now using the sweep command in **History Cleanup**. This is the next-run sweep that keeps the "tmp/ never lingers" invariant true; it's automatic and needs no prompt.
4. Show the concise **Session Setup** summary of identity, settings, and scoped permissions (see below). On `--resume`, validate identity and authorization scope, show the saved settings, and continue when the current request already authorizes resuming.
5. If `--resume` is set, locate the state file for *this project + org + agent*, validate it matches the current identity, then jump to the saved `currentPhase`
6. Otherwise, run pre-flight checks, then enter the loop

---

## Session Setup

Consult [`references/session-setup.md`](references/session-setup.md) before Session Setup at the start of a run.

## Run Identity & Org Resolution

Consult [`references/run-identity-and-org.md`](references/run-identity-and-org.md) before resolving the project root, target org, or run key.

## Argument Parsing

Extract from the user's invocation:

| Arg | Variable | Required | Default |
| --- | --- | --- | --- |
| First positional | `AGENT_NAME` | Yes | — |
| `--mode` | `MODE` | No | Chosen in Session Setup |
| `--max-iterations` | `MAX_ITERATIONS` | No | 3 |
| `--org` | `ORG_ALIAS` (input) | No | Project-local default org |
| `--resume` | `RESUME` | No | false |
| `--skip-review` | `SKIP_REVIEW` | No | false |
| `--findings` | `FINDINGS_PATH` | No | — |

If `MODE` is not provided on the command line, infer it from the request in **Session Setup**; ask only if the intended mode is ambiguous. The two modes:

<quote>
<p />

1. **Full Ownership** — review, plan, implement fixes, test, and iterate autonomously
2. **Plan Only** — review and produce a detailed fix plan for you to implement
</quote>

---

## Pre-Flight Checks

Consult [`references/pre-flight-checks.md`](references/pre-flight-checks.md) before Pre-Flight Checks.

## Phase: REVIEW

Consult [`references/phase-review.md`](references/phase-review.md) before the REVIEW phase.

## Phase: PLAN

Consult [`references/phase-plan.md`](references/phase-plan.md) before the PLAN phase.

## Persona Rubric

Consult [`references/persona-rubric.md`](references/persona-rubric.md) whenever a phase scores or plans persona findings.

## Phase: IMPLEMENT

Consult [`references/phase-implement.md`](references/phase-implement.md) before the IMPLEMENT phase.

## Phase: TEST

Consult [`references/phase-test.md`](references/phase-test.md) before the TEST phase.

## Phase: EVALUATE

Consult [`references/phase-evaluate.md`](references/phase-evaluate.md) before the EVALUATE phase.

## Phase: RE-REVIEW

Consult [`references/phase-re-review.md`](references/phase-re-review.md) before the RE-REVIEW phase.

## Phase: COMPLETE

Consult [`references/phase-complete.md`](references/phase-complete.md) before the COMPLETE phase.

## History Cleanup

Consult [`references/history-cleanup.md`](references/history-cleanup.md) before any history cleanup.

## Testing Skill Bootstrap

Triggered when pre-flight check #3 fails (no testing skill found) — the common case is that a testing<br />skill already exists, so this flow is the exception, not the rule. When it fires, <b>read and follow<br />the full interactive flow in </b>[**`references/testing-skill-bootstrap.md`**](references/testing-skill-bootstrap.md):<br />confirm org/agent → read the agent config → develop personas conversationally → generate the<br />`<agent-name>-testing` skill (`SKILL.md` + `personas.md` + empty `test-results.json`) → offer a first<br />baseline run. After bootstrap completes, save `TESTING_SKILL_PATH` and `TESTING_SKILL_DIR`, then<br />continue pre-flight from check #4.

---

## Sub-Agent Delegation Policy

Delegated sub-agents (REVIEW, TEST, RE-REVIEW) choose their own mechanics and often need scratch<br />files — a wrapper around repeated `sf agent preview` calls, a Python helper to build the `.docx`,<br />etc. That's legitimate. But those files must be **contained, visible, and temporary**, never dropped<br />in `/tmp` unannounced. Every `Agent({...})` delegation prompt must carry this policy:

> **Note:** The one-line version of this policy is repeated verbatim inside each delegation prompt<br />(REVIEW, TEST, RE-REVIEW, persona SCORE). That duplication is **intentional, not a DRY violation** —<br />sub-agents run in their own context and never see the rest of this `SKILL.md`, so the rule has to travel<br />inside each prompt. This section is the canonical statement they restate.

1. **Confined to the project.** Any helper/temp/scratch file goes under<br />`$PROJECT_ROOT/.agent-improvement/tmp/` (create it if missing). **Never** write to `/tmp`, the<br />home directory, or anywhere outside `$PROJECT_ROOT`.
2. **Descriptive names.** Name scratch files for what they do, scoped to the phase and agent —<br />`<phase>-<AgentName>-<purpose>.<ext>` (e.g. `rereview-Local_Info_Agent-docx-builder.py`,<br />`test-Local_Info_Agent-preview-wrapper.sh`). Not `doc_helpers.py` or `lia_ask.sh`.
3. **Announced.** When a sub-agent creates such a file, it states the path and purpose in its result<br />so nothing appears unexpectedly to the user.
4. **Temporary.** These are scaffolding, not deliverables. The whole `tmp/` folder is swept aside at<br />COMPLETE (see History Cleanup). Real outputs still go to their normal locations and the<br />`outputs[]` manifest — never under `tmp/`.

Add `.agent-improvement/tmp/` and `.agent-improvement/tmp.discarded.*` to the project `.gitignore` alongside the state dir.

---

## Consumed JSON Contracts

This skill **does not own** the findings JSON, `test-results.json`, or the persona rubric — they are produced by the delegated `/agentforce-config-review` skill, the project testing skill, and `persona`. To avoid silently breaking when a delegated skill changes its output (or a different skill is swapped in), the orchestrator depends on only a **minimal set of fields** and **validates their presence** the moment a sub-agent returns. Treat extra fields as opaque; treat a missing required field as a hard stop — *except* the persona rubric, which degrades gracefully.

The exact required/optional fields, the snake\_case→internal field mapping, and the precise validation assertions + stop messages for all three contracts are in [**`references/consumed-contracts.md`**](references/consumed-contracts.md). Read it at the validation step of REVIEW, PLAN (skip path), TEST, RE-REVIEW, and the persona SCORE return. When a delegated skill renames or removes a field, fix the mapping there in one place rather than scattering field names through the phases.

---

## State File Management

Consult [`references/state-file-management.md`](references/state-file-management.md) when loading state or changing its format. Apply its identity checks on reads and atomic-write rules on phase transitions without rereading unchanged guidance.

## Error Recovery

| Error | Recovery |
| --- | --- |
| Deploy fails | Show error, attempt auto-fix once, then ask user |
| Test timeout | Retry the timed-out persona once, then skip with warning |
| Sub-agent fails | Retry once, then surface raw error to user |
| Org auth expired | Pause, tell user to re-auth: `sf org login web -a $ORG_ALIAS` (or `sf org login web` if no alias), then re-resolve Run Identity |
| State file corrupt | Archive the bad file to `loop-state-$RUN_KEY.<timestamp>.corrupt`, warn the user that previous progress is lost, and start fresh for the current Run Identity. Never silently delete it. |
| State identity mismatch | Refuse to reuse the file; offer to start a fresh run for the current project/org/agent (see Identity Validation) |
| Unknown fix pattern | Ask user for guidance, apply their approach |

---

## Guardrails

- **Carry authorization forward within its scope.** Session Setup records permission for deployment, commits, and rollback from the user's request or prior approval. A true flag alone is insufficient without its target and scope. Recheck the diff before each external action; ask only when authorization is missing, revoked, ambiguous, or the target, scope, or consequences materially change. Local edits and reports requested by the user do not require a separate permission round.
- **Max 3 fix attempts on the same batch.** If a batch regresses the pass rate on 3 attempts (`batches[].attempts == 3`), mark it `skipped` and move on (see EVALUATE). This per-batch cap is a **separate counter** from `--max-iterations`, which bounds the number of whole REVIEW→…→EVALUATE *cycles* across the run (default 3) — the two limits are unrelated and can be hit independently.
- **Never discard working-tree edits silently, and never leave the org out of sync.** On regression, a granted auto-revert restores the batch's files (edits *and* added files) **and** re-deploys the clean state to the org, so the live agent matches; it's marked handled only once that redeploy succeeds. If `gitRevert` is declined, stop and tell the user both the working tree and the org still hold the bad change — never imply the org is clean when only files were touched.
- **Versioned outputs.** Never overwrite existing review, test, or run-summary files — they all carry a `<date>` (or version) suffix so repeat runs accumulate rather than clobber.
- **Testing ownership.** The orchestrator delegates testing entirely. It never manages `sf agent preview` sessions directly.
