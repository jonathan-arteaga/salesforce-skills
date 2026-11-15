# History Cleanup

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## History Cleanup

**First, always sweep the sub-agent scratch dir.** Rename `$PROJECT_ROOT/.agent-improvement/tmp/`
aside — these are sub-agent helper/scratch files (see **Sub-Agent Delegation Policy**), pure
scaffolding that was announced as temporary at Session Setup. This is automatic and needs no prompt;
nothing in `tmp/` is ever a deliverable, and nothing in it is needed to `--resume` (resume keys off
the `loop-state-$RUN_KEY.json` state file, not `tmp/`). (If the run aborts before COMPLETE, the next
invocation's **On Every Invocation** step 3 sweeps it.)
```bash
DIR="$PROJECT_ROOT/.agent-improvement/tmp"
[ -d "$DIR" ] && mv -f "$DIR" "$DIR.discarded.$RUN_KEY"
```
Renaming (not deleting) keeps the prior scratch recoverable should a resume ever want it; the active
`tmp/` is always cleared before the next run ("never lingers"). The `tmp.discarded.*` copy is
gitignored scratch, listed in the cleanup **Prompt** below for opt-in removal.

Then handle the rest. A run leaves behind two kinds of files. At the end of a run (and on request
mid-run), ask the user what to do with the **working files** — never touch the deliverables without asking.

**Always keep (durable deliverables):**
- Config review reports (`.docx`) and findings JSON
- Test reports (`.html`) and `test-results.json`
- The improvement plan (Plan Only mode)
- The run summary (`run-summary-$RUN_KEY-<date>.md`) and the optional shareable HTML report (`improvement-report-$AGENT_NAME-<date>.html`, if produced)
- Git commits (the source-of-truth history; never auto-deleted)

**Working / intermediate files (candidates for cleanup):**
- The loop-state file `loop-state-$RUN_KEY.json` (only needed for `--resume`)
- Archived/superseded state: `*.bak`, `*.corrupt` backups
- Swept scratch dirs: `.agent-improvement/tmp.discarded.*` (renamed-aside `tmp/` from this or prior runs)
- Any scratch/temp files written under `.agent-improvement/`

### Prompt

Ask once via `AskUserQuestion` (**multi-select**) — this single panel both surfaces the optional
shareable HTML report (making it discoverable without the user knowing a magic phrase) and decides
the fate of the working files. List exactly what each choice writes or removes:

> "The run is complete. What would you like to do? (select any)
> - **Generate shareable HTML report** — renders the self-contained `improvement-report-$AGENT_NAME-<date>.html` into the agent's directory from reconciled state (see **Optional shareable HTML report**). *Omit this option entirely in Plan Only mode and if the report was already generated this run.*
> - **Clean up working files** — deletes the state file, any `.bak`/`.corrupt` backups, and `tmp.discarded.*` scratch dirs listed below; **keeps** all reports, the plan, the run summary, and git history
> - **Keep everything as-is** (default — selecting nothing) — leaves `loop-state-$RUN_KEY.json` so you can `--resume` or inspect later, and produces no extra report
>
> Files that would be removed if you clean up: `<explicit list>`"

Order of operations: if **Generate shareable HTML report** is selected, produce it (and append its
`run-report-html` entry to `outputs[]`) **before** any cleanup, so the cleanup file list reflects the
final set of artifacts.

Rules:
- **Default to keep, and to not generate.** Cleanup deletes only on explicit selection; the HTML report is produced only when explicitly selected (or requested earlier in the run).
- **Never delete a deliverable** in the `outputs[]` manifest other than the state file itself.
- List every file by path before deleting; delete only what was listed.
- If git is available, the deletion is recoverable anyway — mention that.
- If the user is mid-loop (not COMPLETE), warn that deleting the state file disables `--resume`.

---
