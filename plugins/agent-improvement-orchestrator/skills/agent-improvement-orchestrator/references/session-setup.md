# Session Setup

Resolve Run Identity, then briefly show the project, stable org identity, agent, selected mode, and iteration limit. Infer settings from the current request and supplied flags; ask only about choices that block the next useful step. `full` requests an improvement workflow, not blanket permission for deployment, commits, or rollback.

## Reuse authorization within its scope

Current explicit user instructions take precedence over workflow defaults and saved state. Record permissions already granted in the conversation instead of asking again. A request to edit or produce local artifacts authorizes those local changes. An audit-only request does not authorize implementation. Deployment, commits, and destructive rollback require authorization for those actions and their actual targets.

Keep the existing `consents` booleans for compatibility, defaulting each to false until authorized. For each true value, record an `authorization` entry with the user instruction or approval that granted it, project root, org ID, agent, permitted changes/actions, and any limits or expiration. These records describe authorization; a file is not itself a new grant. Do not store credentials or unrelated correspondence.

```json
{
  "consents": {"deploy": false, "gitCommit": false, "gitRevert": false},
  "authorization": {}
}
```

| Permission | Required scope |
| --- | --- |
| `deploy` | Selected org and agent, permitted metadata changes or batches, and any limits on retries or environments. |
| `gitCommit` | Selected repository and the requested changes; never unrelated working-tree edits. |
| `gitRevert` | Exact run/batch changes that may be restored, including redeployment and deletion of newly added org components if needed. Protect pre-existing user work. |

Reports, plan, summary, and state live under `$PROJECT_ROOT/.agent-improvement/`. Requested local artifacts and contained helper files do not need a separate consent panel. Keep temporary helpers under `.agent-improvement/tmp/` and follow the cleanup rules.

## Before an external action

1. Show or summarize the concrete diff and target. Verify the current stable identity against the run identity.
2. Check that the current action, affected resources, and consequences fit the recorded user authorization. Honor a narrower or revoked instruction immediately.
3. Continue without another approval when the authorization still applies. Ask only for missing, ambiguous, expired, or materially changed scope. A changed org, new destructive deletion, or broader set of resources requires its own authorization.
4. If permission is missing, complete independent local preparation first and present the exact pending action. Do not run deployment or live tests that depend on it, and do not claim they passed.

## Resume

Re-resolve and validate project/org/agent identity using the state-file rules. Show the saved phase and settings, reconcile authorization with the current request, and continue an explicitly requested resume when scope matches. Do not ask the user to confirm the same resume or deployment permission again.

Legacy state with only `consents.deploy: true` is not proof of scoped authorization. Recover the actual approval from available conversation context; if unavailable, ask once for the specific pending action. Never infer permission from an example state file or a default checkbox.
