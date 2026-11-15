# Run Identity & Org Resolution

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Run Identity & Org Resolution

**This is the first thing the skill does, before pre-flight, resume, or any org/file operation.** It exists to guarantee the loop always runs against the project the user is currently in and the org they actually intend — never a stale value carried over from a previous run in a different folder.

### Step A: Resolve the Project Root

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

Save as `PROJECT_ROOT` (absolute path). Everything the skill reads or writes is anchored to this path — never to the skill's own install directory, which may be global or symlinked and therefore shared across projects.

### Step B: Resolve and Pin the Target Org

Never trust a bare "default org" silently, and never carry an org over from a prior run. Resolve it fresh, here, every time:

1. If `--org <alias>` was passed, use that alias. Otherwise resolve the **project-local** default org from `PROJECT_ROOT`:
   ```bash
   sf config get target-org --json    # run with PROJECT_ROOT as cwd
   ```
2. Confirm the org and capture its stable identity:
   ```bash
   sf org display -o <alias-or-default> --json
   ```
   From the response, capture and pin:
   - `ORG_USERNAME` ← `result.username`
   - `ORG_ID` ← `result.id`
   - `ORG_ALIAS` ← the alias used (may be empty)

   **From this point on, every org command uses `-o $ORG_USERNAME`** (the resolved username, not the alias or "default"). Aliases and defaults are ambiguous across projects; the username is not.

Show the resolved identity in **Session Setup** and compare it with the user's selected target and recorded authorization. Ask only when the target is ambiguous or different. Read-only identity resolution is permitted; external mutations require authorization for the verified target.

### Step C: Compute the Run Key

```
RUN_KEY = "<AGENT_NAME>__<ORG_ID>"
```

Keys the state file so runs never collide (see State File Management for how it's used).

---
