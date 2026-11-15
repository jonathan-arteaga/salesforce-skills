# State File Management

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## State File Management

### State File Location

```
$PROJECT_ROOT/.agent-improvement/loop-state-$RUN_KEY.json
```

Collision-proof by construction: the **path** isolates the project (always under `$PROJECT_ROOT`, never the skill's possibly-shared install dir), and `$RUN_KEY` (`<AGENT_NAME>__<ORG_ID>`) isolates org + agent. Same agent on two orgs, or two same-named agents, get separate files.

Add `.agent-improvement/` to the project's `.gitignore` (local working data, not source).

### Identity Validation (on every state-file read)

Whenever the skill reads an existing state file — on `--resume` or before continuing any loop — it **must** validate the stored identity against the freshly-resolved Run Identity:

- `state.projectRoot == $PROJECT_ROOT`
- `state.orgId == $ORG_ID`
- `state.agentName == $AGENT_NAME`

If **any** mismatch:

> ⚠️ "This state file was created for a different project/org/agent:
> - Project: `<state.projectRoot>` → now `$PROJECT_ROOT`
> - Org: `<state.orgUsername>` (`<state.orgId>`) → now `$ORG_USERNAME` (`$ORG_ID`)
> - Agent: `<state.agentName>` → now `$AGENT_NAME`
>
> I will **not** reuse it, to avoid running against the wrong org. Start a fresh run for the current identity?"

**Never proceed on a mismatch by silently adopting the stored org.** This is the exact failure where a skill "runs on the first org after you switch projects" — the org must always come from the current Run Identity resolution, never from a carried-over state file.

### On Every Phase Transition

1. Update `currentPhase` in state
2. Update `lastUpdatedAt` to current ISO timestamp
3. Re-assert the identity fields (`projectRoot`, `orgId`, `orgUsername`, `agentName`) are still present and unchanged
4. Write state file atomically (write to a temp file in the same dir, then rename — never partial-write the live file)

### Resume Logic

When `--resume` is passed:
1. Resolve Run Identity first (project root + pinned org) — *do not* read the org from the state file
2. Locate the state file at `$PROJECT_ROOT/.agent-improvement/loop-state-$RUN_KEY.json`
   - If it doesn't exist: "No saved run found for agent `$AGENT_NAME` on org `$ORG_USERNAME` in this project. Start a new run?"
3. Run **Identity Validation** (above). Refuse on mismatch.
4. Validate it's not corrupted (valid JSON + has required fields). If corrupt, fall back to recovery (see Error Recovery).
5. Display current state summary to the user, including the org it will run against
6. Reconcile saved authorization with the current request using Session Setup. An explicit resume request needs no second resume confirmation when identity and scope match. Ask only for missing or changed permission; never infer permission from a legacy boolean alone.
7. Jump to the appropriate phase handler

### Pre-existing State Without `--resume`

If a non-corrupt state file for this exact `RUN_KEY` already exists and the user did *not* pass `--resume`, do not overwrite it blindly. Ask:

> "A previous run for `$AGENT_NAME` on `$ORG_USERNAME` exists (phase: `<currentPhase>`, last updated `<lastUpdatedAt>`). Resume it, or start fresh (archives the old state to `loop-state-$RUN_KEY.<timestamp>.bak`)?"

---
