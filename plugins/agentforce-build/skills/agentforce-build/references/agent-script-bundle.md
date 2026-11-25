# Agent Script & `aiAuthoringBundle` Lifecycle

Agent Script is Salesforce's declarative DSL for Hybrid Reasoning agents. Canvas, Script View, and DX author the same underlying `AiAuthoringBundle` metadata.

## Deployable Bundle Shape

Under `force-app/main/default/aiAuthoringBundles/<ApiName>/`, enforce the exact case-sensitive file pair:

- `<ApiName>.agent` — Agent Script source (4-space indentation for new files; preserve consistent legacy indentation on surgical edits).
- `<ApiName>.bundle-meta.xml` — descriptor XML (NEVER literal `bundle-meta.xml`). Preserve retrieved or CLI-scaffolded schemas (`<bundleType>AGENT</bundleType>` for new CLI scaffolds; do not mix with older `fullName`/`type`/`status` fields).

Verify config keys against the target release scaffold: `default_agent_user` belongs under `access`, and newer releases prefer `developer_name` over legacy `agent_name`. Never bulk-rewrite working bundles from overview snippets.

## Core Syntax & Control-Flow Rules

- **No nested `if` blocks:** Agentforce lint rejects nested conditionals; flatten into compound conditions or sequential single-level branches.
- **One pipe (`|`) per contiguous prompt block:** Repeated adjacent pipe markers do not create execution stages or priority.
- **No prompt impersonation:** Numbered steps or `ALWAYS` / `STOP` / `Call` inside `|` text are model guidance, not runtime scope. Enforce mandatory prerequisites with `available when`, `if`, `run`, `set`, and `transition to`.
- **Variable visibility:** Models cannot read stored state unless interpolated via `{!@variables.X}`. Interpolation reveals values but does not make LLM comparison deterministic—use runtime predicates for exact checks.
- **No `@utils.setVariables` turn hacks:** Never misuse `@utils.setVariables` to force extra reasoning iterations or turn boundaries.
- **Multi-turn routing state:** Check `config.runtime` (`runtime.reset_to_initial_node`) explicitly and verify continuation behavior with a two-turn preview trace rather than assuming every turn restarts at `start_agent`.

## Local Compilation, Preview & Gated Release

1. **Local compile first:** Run `node scripts/index-agent.mjs <path/to/Agent.agent>` before any org call (even in offline/non-interactive mode). If SDK setup is missing, run `node scripts/setup-agentscript-sdk.mjs` and retry. Fix all severity-1 diagnostics; local compile does NOT verify `<ApiName>.bundle-meta.xml`, so check XML pairing manually.
2. **Org validation & draft deploy:** Confirm `sf config get target-org --json`, then validate/deploy draft bundle metadata with `--json`. Keep surgical repairs minimal—inspect the final diff and revert unrelated hunks.
3. **Preview & traces:** Run `sf agent preview start --authoring-bundle <ApiName> --simulate-actions --json`, then `send` and `end` (mode flag belongs on `start` only). Use `--use-live-actions` ONLY with explicit approval, non-production sandbox confirmation, and synthetic test data.
4. **Explicit publish/activation gate:** Draft iteration ends at preview/validation. Obtain explicit user approval before running `sf agent publish authoring-bundle` or activating the agent for end users.
5. **Delete or rename safely:** Enumerate all references first, require explicit confirmation before deletion, and for renames create and validate the replacement bundle before removing the original.
