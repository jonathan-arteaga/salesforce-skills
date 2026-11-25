# Org Lifecycle Reference

Manage Salesforce scratch orgs, snapshots, org shapes, Dev Hub resolution, and safe target-org classification using Salesforce CLI v2 (`sf`).

## 1. Explicit Target Pinning & Dev Hub Resolution

Never rely on an ambient default org for mutations. Pin `--target-org <username-or-alias>` and `--target-dev-hub <username-or-alias>` explicitly.

Resolve Dev Hub in strict order:
1. User-specified Dev Hub username or alias (use verbatim).
2. Configured default via `sf config get target-dev-hub --json` (`result[0].value`).
3. All-bucket lookup via `sf org list --skip-connection-status --json` (a Dev Hub can appear in `devHubs`, `nonScratchOrgs`, `other`, `sandboxes`, or `scratchOrgs`):

```bash
sf org list --skip-connection-status --json \
  | jq -r '[.result.devHubs[]?, .result.nonScratchOrgs[]?, .result.other[]?, .result.sandboxes[]?, .result.scratchOrgs[]?] | map(select(.isDevHub == true).username) | unique | .[]'
```

- **Exactly 1 username**: use it via `--target-dev-hub <username>`.
- **0 usernames**: hard stop. Never fabricate a placeholder Dev Hub alias (`DevHub`, `my-dev-hub`). Advise `sf org login web --set-default-dev-hub`.
- **2+ usernames**: ask the user which Dev Hub to use; never pick arbitrarily.

## 2. Target Org Classification (Prod vs Non-Prod)

Classify every target org from `sf org list --skip-connection-status --json` (local read; avoids refreshing OAuth tokens for unrelated orgs). Do NOT classify from `sf org display`, which omits sandbox/scratch/trial booleans and misclassifies Sandbox-or-Demo Orgs (SDOs).

Match the record by `alias`, `username`, or `orgId` (first rule wins):
1. **Scratch**: `isScratch == true`.
2. **Sandbox**: `isSandbox == true`, or `instanceUrl` contains `--` or `test.salesforce.com`.
3. **Trial / Developer Edition**: `trailExpirationDate` (or `trialExpirationDate`) is in the future, or `instanceUrl` contains `orgfarm-`, `.develop.my.salesforce.com`, `.pc-rnd.`, or `.scratch.my.salesforce.com`. Ignore past dates (cached at login).
4. **Production**: anything else, including a Dev Hub (`isDevHub == true`) lacking non-prod signals.
5. **Unknown**: missing record or missing `instanceUrl` and flags -> stop and ask the user.

## 3. Creating Scratch Orgs

Choose **exactly one** creation source type (if two conflict, stop and ask):

```bash
# Definition file (preferred in DX projects with config/*scratch-def.json)
sf org create scratch --definition-file config/project-scratch-def.json \
  --target-dev-hub <devhub> --alias <alias> --duration-days 7 --json

# Edition only
sf org create scratch --edition developer \
  --target-dev-hub <devhub> --alias <alias> --duration-days 7 --json

# From Snapshot
sf org create scratch --snapshot <snapshot-name> \
  --target-dev-hub <devhub> --alias <alias> --json

# From Org Shape (--source-org takes 15-char 00D... org ID, NOT 3SR... shape record ID)
sf org create scratch --source-org <00D-15-char-id> \
  --target-dev-hub <devhub> --alias <alias> --json
```

Useful flags:
- `--duration-days <1..30>` (default 7, max 30).
- `--set-default` (only when requested by user).
- `--no-track-source` (recommended for CI/CD ephemeral scratch orgs).
- **Batch creation**: no native count flag; loop with collision-guarded aliases (`<base>-1` .. `<base>-N`), stopping cleanly on Dev Hub limit errors and reporting which orgs succeeded.

After successful creation, inspect the org entry from `sf org list --skip-connection-status --json` and report `alias`, `username`, `orgId`, `instanceUrl`, and `expirationDate`. Never un-redact `accessToken` or `sfdxAuthUrl`.

## 4. Snapshots & Org Shapes

```bash
# Create, inspect, list, and delete snapshots (requires Scratch Org Snapshots enabled on Dev Hub)
sf org create snapshot --name <snap-name> --source-org <scratch-alias-or-id> --target-dev-hub <devhub> --json
sf org get snapshot --snapshot <snap-name-or-id> --target-dev-hub <devhub> --json
sf org list snapshot --target-dev-hub <devhub> --json
sf org delete snapshot --snapshot <snap-name-or-id> --target-dev-hub <devhub> --json

# List available org shapes
sf org list shape --target-dev-hub <devhub> --json
```

If scratch creation fails with "Snapshot not found", direct the user to `sf org list snapshot --target-dev-hub <devhub>`.

## 5. Operating on Existing Orgs

```bash
# List active scratch orgs (use --all for expired/deleted, --clean only when requested)
sf org list --skip-connection-status --json

# Display org metadata (NEVER pass --verbose; it exposes sfdxAuthUrl refresh tokens)
sf org display --target-org <user-or-alias> --json

# Resume timed-out or --async scratch creation (exit code 69)
sf org resume scratch --job-id <job-id> --json

# Delete scratch org (DESTRUCTIVE: require explicit user confirmation first; flag if default org)
sf org delete scratch --target-org <user-or-alias> --no-prompt --json

# Open org in browser (NEVER pass --json or --url-only; they emit credential-equivalent frontdoor.jsp URLs)
sf org open --target-org <user-or-alias>
sf org open --target-org <user-or-alias> --path '/lightning/setup/SetupOneHome/home'
```

If the user explicitly requests an auth URL or login link, do **not** run `sf org display --verbose` or `sf org open --url-only`; instruct them to run those commands directly in their local terminal.
