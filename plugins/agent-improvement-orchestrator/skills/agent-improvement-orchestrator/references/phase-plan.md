# Phase: PLAN

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: PLAN

**First, ensure Finding IDs exist.** If findings came from this run's REVIEW they are already assigned. On the skip path (`--findings` / `--skip-review`), REVIEW did not run — validate the supplied findings JSON against the **Consumed JSON Contracts**, then assign Finding IDs now (per the **Finding IDs** scheme) before doing anything else. No batch may be planned against an unidentified finding. On the skip path, also capture the **persona baseline** here if any persona/tone finding exists (REVIEW step 5 didn't run) — see **Persona Rubric** — storing it under `personaRubric.baseline`.

**Persona skill availability (only when a persona/tone finding exists).** Locate the `persona` skill via the usual lookup (`~/.agents/skills/persona/` → `~/.agents/skills/persona/` → project `.agents/skills/` or `.agents/skills/` → plugin cache). If it can't be found, say so once, then degrade gracefully: hand-edit the persona-bearing fields per `/agentforce-generate` conventions and skip rubric verification (the persona finding reconciles by config-review presence, like any other). Don't block the run.

Read the findings JSON and the agent file. Classify each finding into a fix pattern using the
**Pattern Library** in [`references/planning.md`](planning.md).

### Planning Algorithm

1. Filter findings to HIGH and MEDIUM severity only (LOW are noted but not fixed)
2. Score each finding by the **priority formula** in [`references/planning.md`](planning.md) (`severity_weight × determinism_impact × fix_confidence`, all derived from the findings JSON + the Pattern Library match — no new inputs) and sort descending; break ties by severity DESC. A high-severity, high-impact, clean-pattern fix outranks a marginal one of the same severity.
3. Group into batches of 2-4 related fixes (avoid giant monolithic changes)
4. For each batch, plan:
   - **The Finding ID(s) the batch addresses** (e.g. `D3-H1`, `D2-M1`) — every plan item must cite the IDs it resolves
   - Which files to modify (agent file, Apex, schemas, flows)
   - What the change looks like (old → new)
   - Expected test impact (which personas might be affected)

5. **Persist the batches to state** as `batches[]`, each with a `status` (`pending` | `applied` | `succeeded` | `reverted` | `skipped`), an `attempts` counter (starts unset; IMPLEMENT sets it to `1` on first application and increments on each re-application), and its Finding IDs. **PLAN is re-entered between iterations, so it must not re-derive batch 1 every time.** On entry:
   - If `state.batches[]` already exists, do **not** re-run the grouping. Select the **next `pending` batch** and proceed (Full Ownership) — the ranking/grouping above runs only on the *first* PLAN, when `batches[]` is empty.
   - A batch moves `pending → applied` in IMPLEMENT, `→ succeeded` when EVALUATE accepts it, `→ reverted` on regression, `→ skipped` when abandoned as unresolvable (after 3 attempts — see EVALUATE). "More HIGH/MEDIUM findings remain" (EVALUATE) means "a `pending` batch remains." A `skipped` batch's findings are recorded in `remaining[]` with a one-line reason.

6. **Record deferred findings in `remaining[]`.** The LOW-severity findings filtered out in step 1 are appended to `state.remaining[]` (each as `{ id, severity, finding, detail }` with a one-line reason for deferral), so the contract has a single home for "known but not addressed this run" — later joined by any batch EVALUATE marks `skipped`. This is the array the run summary and `--mode plan` deferral list read from.

### Mode Branch

- **Full Ownership (`MODE = full`):** Write plan to state, proceed to IMPLEMENT.
- **Plan Only (`MODE = plan`):** Write the plan to a dedicated file, then display its summary and **STOP** (set `currentPhase: "COMPLETE"`). This file is the entire deliverable of Plan Only mode, so it must be self-contained and actionable by someone who will implement the fixes by hand.
  ```
  $PROJECT_ROOT/.agent-improvement/improvement-plan-$RUN_KEY-<date>.md
  ```

  **Required structure** (see [`examples/sample-improvement-plan.md`](../examples/sample-improvement-plan.md)):

  1. **Header** — agent name, org username, composite score, date, finding counts by severity.
  2. **Summary** — 2–3 sentences: the score, the biggest gap, the expected outcome if the plan is followed.
  3. **Batches** — one `###` section per batch, in priority order. Each batch contains:
     - The **Finding ID(s)** it resolves and their severity
     - **Files to modify**
     - **Change** — a concrete old → new (code block or before/after prose), not a vague intent
     - **Expected test impact** — which personas/questions should flip
  4. **Deferred (not in this plan)** — LOW findings, each with its ID and a one-line reason for deferral.
  5. **Verification** — how to confirm the plan worked (run the testing skill; re-run the review and reconcile Finding IDs).

  Every fix and deferral **must cite its Finding ID** so the plan threads back to the review report.

### Reference Skills for Implementation

Before generating fix code, read the relevant skill content for conventions — the per-change skill map (`.agent`, Apex, Flow, deploy) and the **persona/tone delegation rule** are in the **Reference Skills for Implementation** section of [`references/planning.md`](planning.md). Persona/tone findings delegate to `persona` (brownfield mode), never hand-edited; the persona rubric (see **Persona Rubric** below) governs whether they count as resolved at RE-REVIEW.

---
