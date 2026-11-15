# Phase: COMPLETE

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase: COMPLETE

**Write the summary to a durable file, then display it.** The headline result of the whole run
must not be terminal-only — once the console scrolls it would be lost. Write it to:

```
$PROJECT_ROOT/.agent-improvement/run-summary-$RUN_KEY-<date>.md
```

The `<date>` suffix matches the improvement plan and HTML report conventions, so a second run for the
same agent+org never overwrites a prior summary. Append a `run-summary` entry to the state `outputs[]` manifest.

This is the only deliverable meant to be read at a glance — the `.docx` review and `.html` test
reports are the detailed evidence. Three rules:
1. **Lead with a one-line verdict** — outcome + headline numbers.
2. **Put each improvement next to its evidence** — cite the Finding ID and where to verify it; don't split claims from proof.
3. **Reference, don't dump** — Evidence is a before/after artifact pair, not a file list.

The file uses this structure (the same content is echoed to the console):

```
## $AGENT_NAME — <Improved ✓ | Plan ready | No change> · $INITIAL_SCORE → $FINAL_SCORE · tests $BASELINE_RATE → $FINAL_RATE · $REGRESSION_COUNT regressions

<one-sentence "what happened": reviewed the agent, found N issues, fixed the M
priority ones in K iteration(s), re-tested with $REGRESSION_COUNT regressions.
Note any deferral in the same breath.>

### What improved   (evidence)
<!-- one line per fix: <plain-language outcome> (<Finding ID>, <SEV>)   <evidence refs> -->
- Stopped inventing discounts (D2-H1, HIGH)        review §3 · test P2-Q2 ↑
- Stays in role under jailbreak (D2-M1, MEDIUM)    review §3 · test P3-Q1 ↑
- Retries Knowledge fetch before failing (D3-M1, MEDIUM)   review §4
- Consistent, on-brand voice (D5-M1, MEDIUM)       persona rubric 62 → 88
→ Score $INITIAL_SCORE→$FINAL_SCORE, pass rate $BASELINE_RATE→$FINAL_RATE.
  Deferred: <Finding ID + one-line reason, or "none">.

### Evidence
- Before: <review report (score)> · <baseline test report (rate)>
- After:  <re-review report (score)> · <final test report (rate)>
- Persona: <baseline rubric NN (band)> → <final rubric MM (band)>   (only if a persona fix ran)
- Changes: <commit SHA(s), or "Plan Only — no changes applied">
- All artifacts: see `outputs[]` in loop-state-$RUN_KEY.json

Run: $ORG_USERNAME · $PROJECT_ROOT · iter $ITERATION/$MAX_ITERATIONS · $MODE · <ISO timestamp>
```

Keep the prose to one sentence; let the structure carry the rest. In **Plan Only** mode there is no
test/commit data — the verdict is "Plan ready", "What improved" becomes "What the plan will fix"
(citing review evidence only), and Evidence points to the review report and the improvement plan.

**Evidence references are best-effort.** The `.docx`/`.html` are owned by other skills, so cite what
you reliably know — the **Finding ID**, the **dimension** (e.g. "D3 → Guardrails"), and the
**persona/question label** from `test-results.json`. Never invent a section number; if no precise
anchor exists, reference the file + Finding ID. For a persona fix, the rubric before→after
(`personaRubric.baseline`/`final`) is the reliable evidence — cite it instead of a review section.

### Optional shareable HTML report

The markdown run summary above is **always** the canonical, at-a-glance deliverable. The shareable
HTML report is an *optional add-on* to it — never a replacement. It is produced when **either**:
- the user asks for something shareable at any point (e.g. "give me a report I can send", "make an HTML report"), **or**
- the user selects it from the **History Cleanup** multi-select at the end of the run (see below) — this is how a default run surfaces the option, so it's discoverable without the user having to know the phrase.

Skip it in **Plan Only** mode (there's no before/after to chart) — the cleanup multi-select omits the
option entirely in that mode. Generating it is never silent: it always comes from one of the two
explicit choices above, and default runs that decline it stay lean.

Write it to the agent's directory (the directory containing `$AGENT_FILE_PATH`, next to the
review/test artifacts so all evidence travels together), with today's date in the filename, and
append a `run-report-html` entry to `outputs[]`:

```
<agent directory>/improvement-report-$AGENT_NAME-<today's date>.html
```

Render **only from reconciled state** — the same numbers the markdown summary cites: `evaluations`
(composite before/after, per-dimension), the before/after finding-severity counts, the resolved
fixes with their **Finding IDs** and evidence refs, `personaRubric.baseline`/`final` (only if a
persona fix ran), `test-results.json` (per-persona pass rates), and `state.remaining[]`
(carry-forward). Don't invent data the run didn't produce — omit a section rather than fill it.

Three hard requirements (see `examples/sample-improvement-report.html` for the reference pattern):
1. **Single file, no external assets** — inline all CSS/JS so it opens and shares as one file.
2. **Print/PDF legibility** — include an `@media print` light-theme block (the dark screen theme
   must not render as an ink-heavy, unreadable PDF) and a `beforeprint` handler that expands any
   collapsed sections.
3. **Every claim threads to a Finding ID** — same rule as the markdown: each fix and carry-forward
   item cites its ID, so the HTML and the markdown tell the same story.

This is the orchestrator's own cross-skill synthesis rendered for sharing — distinct from the
testing skill's narrower per-persona HTML test report, which it does not replace.

After writing and displaying the summary, run **History Cleanup** (below) before exiting.

---
