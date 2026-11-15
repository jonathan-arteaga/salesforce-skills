# Offline validator setup

The skill's mandatory Phase 7 self-heal loop (see SKILL.md) needs an offline `.agent` validator to call between every Edit batch. The canonical validator is `@agentscript/agentforce` from the official Salesforce repo `salesforce/agentscript`.

This guide documents how to set it up locally. The skill **does not embed** the validator because the upstream repo evolves quickly — embedding would go stale within weeks.

## Status of `@agentscript/agentforce` on npm

As of 2026-05-19, the package is **not yet published to npm** (the package metadata in `salesforce/agentscript` declares it as `@agentscript/agentforce` v2.5.31 but it's a workspace dependency, not on the public registry). Until it ships, the workflow below clones and builds the monorepo.

**Once it ships to npm**, the preferred path is one line:

```bash
pnpm add @agentscript/agentforce
```

(Or `npm install @agentscript/agentforce`.) Update this guide when the package becomes available.

## One-time setup (current path: clone + build)

### Prerequisites

| Tool | Version | Install |
|---|---|---|
| Node.js | ≥ 18 (22 recommended) | `nvm install 22` or use existing |
| pnpm | 10+ | `npm install -g pnpm@10` |
| tree-sitter CLI | 0.25.x | `npm install -g tree-sitter-cli@0.25` |
| git | any recent | system |
| gh | any recent (for version checks) | `brew install gh` |

> **macOS note:** `brew install tree-sitter` installs only the C library, not the CLI. For the CLI use `npm install -g tree-sitter-cli@0.25` (above) or `brew install tree-sitter-cli`.

### Clone and build

```bash
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/salesforce/agentscript.git
cd agentscript
pnpm install     # ~45s — pulls deps, builds the parser-tree-sitter native binding
pnpm build       # ~1m30s — builds all 12 workspace packages
```

Verify the build:

```bash
ls ~/dev/agentscript/packages/agentforce/dist/index.js
# expect: file exists
```

### Write the validator script

Create `validate-agent.mjs` in your working project (e.g., `~/Desktop/Voice Skills/validate-agent.mjs`):

```javascript
#!/usr/bin/env node
// Offline AgentScript validator using @agentscript/agentforce.
// Usage: node validate-agent.mjs <path-to-.agent>

import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { compileSource } from "/Users/<YOU>/dev/agentscript/packages/agentforce/dist/index.js";

const file = process.argv[2];
if (!file) {
  console.error("Usage: node validate-agent.mjs <path-to-.agent>");
  process.exit(2);
}

const path = resolve(file);
const source = readFileSync(path, "utf8");

console.log(`Validating: ${path}`);
console.log(`(${source.split("\n").length} lines, ${source.length} chars)\n`);

const result = compileSource(source);
const diags = result.diagnostics;

const errors = diags.filter((d) => d.severity === 1);
const warnings = diags.filter((d) => d.severity === 2);
const info = diags.filter((d) => d.severity === 3 || d.severity === 4);

const fmt = (d) => {
  const r = d.range?.start ?? { line: 0, character: 0 };
  const sev = ["", "ERROR", "WARN ", "INFO ", "HINT "][d.severity] ?? "??";
  const code = d.code ? ` [${d.code}]` : "";
  return `  ${sev} ${r.line + 1}:${r.character + 1}${code}  ${d.message}`;
};

if (errors.length) {
  console.log(`ERRORS (${errors.length}):`);
  errors.forEach((d) => console.log(fmt(d)));
  console.log("");
}
if (warnings.length) {
  console.log(`WARNINGS (${warnings.length}):`);
  warnings.forEach((d) => console.log(fmt(d)));
  console.log("");
}
if (info.length) {
  console.log(`INFO (${info.length}):`);
  info.forEach((d) => console.log(fmt(d)));
  console.log("");
}

if (!diags.length) console.log("Clean — no diagnostics.");

console.log(
  `Summary: ${errors.length} error(s), ${warnings.length} warning(s), ${info.length} info`,
);
process.exit(errors.length ? 1 : 0);
```

Replace `<YOU>` with your username, or templatize via env var:

```javascript
import { compileSource } from `${process.env.AGENTSCRIPT_HOME ?? `${process.env.HOME}/dev/agentscript`}/packages/agentforce/dist/index.js`;
```

### Test it

```bash
node validate-agent.mjs path/to/your.agent
```

Expected on a clean `.agent`:

```
Summary: 0 error(s), N warning(s), N info
```

(Deprecation warnings on `topic` keyword are expected — see Z02 in the skill's pattern catalog. Info-level `unused-variable` is normal for variables introduced in early Phase 7 batches but referenced later.)

## Version-staying-current

Repo evolves — keep your clone fresh.

### Check upstream latest tag

```bash
gh api repos/salesforce/agentscript/releases/latest --jq '.tag_name'
# 2026-05-18 example output: v2.5.31
```

### Check your local

```bash
cd ~/dev/agentscript
git describe --tags --abbrev=0
```

If they don't match:

```bash
cd ~/dev/agentscript
git pull
pnpm install
pnpm build
```

The skill's Phase 7 setup step should prompt you to run this if the local clone is older than 30 days, OR if local tag doesn't match upstream latest.

### When `@agentscript/agentforce` ships to npm

Replace this whole flow with:

```bash
pnpm add @agentscript/agentforce
```

Update `validate-agent.mjs` import path:

```javascript
import { compileSource } from "@agentscript/agentforce";
```

Delete the local clone if you want; no longer needed.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `pnpm install` fails on parser-tree-sitter | Missing tree-sitter CLI | `npm install -g tree-sitter-cli@0.25` |
| `pnpm build` fails on tree-sitter generate | tree-sitter CLI version too new (0.26.x+) | Use 0.25.x — `npm install -g tree-sitter-cli@0.25.10` |
| `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING` from corepack | Old Node + corepack mismatch | `npm install -g pnpm@10` directly, skip corepack |
| Validator runs but every file shows 1500+ errors | Wrong import — pointed at source `.ts` instead of built `dist/index.js` | Verify import path includes `/dist/index.js` |
| Validator says "compileSource is not a function" | Build incomplete or stale | `cd ~/dev/agentscript && pnpm build` again |

## Why not embed the validator in the skill

Embedding pinned to a specific upstream commit would:

1. Go stale within weeks as `salesforce/agentscript` evolves.
2. Bloat the skill with ~1GB of `node_modules` and built artifacts.
3. Hide where the validator is actually coming from — bad for trust and debugging.
4. Make skill version bumps painful (every commit on upstream forces a skill release).

Cloning and building locally:
- Keeps users aware of where the dependency lives.
- Lets users update on their own cadence.
- Will be obsoleted cleanly when the npm package ships.

If you maintain the skill: when the npm package ships, update this doc and the Phase 7 instructions in one PR. The clone path becomes the fallback.
