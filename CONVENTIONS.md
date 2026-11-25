# Salesforce Skills — Authoring & Architecture Conventions

This repository is a domain-focused AI skill library for Salesforce, Data 360, and Agentforce, engineered for **Gemini 4 / Google Antigravity** and **OpenAI Codex** progressive disclosure.

## 1. Design Philosophy

Every skill in this library MUST follow six core principles:

1. **Encode invariants, not textbooks.** Frontier models already know standard Apex, LWC, SOQL, and Flow syntax. Spend context tokens only on real platform pitfalls, API 67+ / Release 264+ changes, governor and transaction invariants, Agentforce / Data 360 failure modes, strict org safety gates, and concrete verification loops.
2. **Progressive disclosure by default.**
   - **Layer 1 (Discovery — always in context):** Lean single-line YAML metadata across the entire library (~1,000–1,600 tokens total) to preserve prompt-prefix cache stability.
   - **Layer 2 (Activation — loaded on match):** `SKILL.md` kept to **~50–75 lines** with an upfront **Mode / Domain routing table**, core invariants, safety boundaries, and verification rules.
   - **Layer 3 (Execution — loaded on demand):** Deep checklists, schemas, and playbooks live in focused `references/*.md` files (~40–75 lines each), loaded only for the active mode. Never ship a duplicate `compiled.md` monolith or stamp duplicate reference copies across skills.
3. **One owner per concern.** Every skill's single-line `description` MUST state both clear positive triggers and explicit negative handoffs to sibling skills.
4. **Verification integrity.** Always separate static metadata/code inspection from executed Salesforce CLI commands (`sf apex run test`, `sf project deploy validate`, `sf agent test run`), live org readback, and `Not verified` gaps. Never claim a deployment, test, or org mutation succeeded without observed command output.
5. **Hard org & safety gates.**
   - Read-only reviews, audits, traces, and schema inspections MUST NEVER mutate org metadata or records.
   - Local generation or planning MUST NEVER deploy to production, run destructive data loads, modify production profiles/permission sets, activate Data 360 segments, or publish Agentforce agents live without explicit user approval and pinned `--target-org` identity.
6. **Black-box helper scripts.** When bundling deterministic helper CLIs under `scripts/`, instruct the agent to execute them directly via CLI flags rather than reading script source into context.

## 2. Canonical Skill Anatomy

Every skill lives as a standalone package under `plugins/<skill-name>/`:

```text
plugins/<skill-name>/
├── plugin.json                        # Package manifest (description matches SKILL.md verbatim)
└── skills/<skill-name>/
    ├── SKILL.md                       # Layer 2 entrypoint (~50–75 lines, single-line YAML frontmatter)
    ├── LICENSE                        # Apache-2.0 license text
    ├── agents/
    │   └── openai.yaml                # Codex UI metadata + explicit policy.allow_implicit_invocation
    ├── references/                    # Layer 3 on-demand guides (~40–75 lines each, zero orphans)
    │   └── <mode>.md
    └── scripts/                       # Optional deterministic black-box CLI helpers (+ tests/)
```

## 3. Metadata & Markdown Rules (CI-Enforced)

`scripts/validate_skills.py` and `scripts/package_marketplace.py --check` enforce these invariants on every commit and PR:

- **Single-line YAML frontmatter:** `name` and `description` in `SKILL.md` must each be a single line (no `|-`, `>-`, or multi-line folded scalars). `name` must be hyphen-case (≤ 64 chars) matching the folder name. `description` must be ≤ 1024 chars (≤ 300 chars recommended) with no `<` or `>` characters.
- **Exact description parity:** `plugins/<name>/plugin.json` `"description"` MUST match `SKILL.md` frontmatter `description` verbatim.
- **Required `LICENSE`:** Every `plugins/<name>/skills/<name>/LICENSE` file must exist and be non-empty.
- **Required `agents/openai.yaml`:** Must define `interface.display_name`, `interface.short_description` (25–64 chars), `interface.default_prompt` (referencing exact `$<skill-name>`), and `policy.allow_implicit_invocation` (`true` or `false` boolean).
- **Clean Markdown in `SKILL.md`:** Zero raw HTML tags (`<br>`, `<b>`, `<i>`, `<quote>`) and zero escaped-pipe tables (`\|`).
- **Zero orphaned references:** Every file under `references/` must be linked via relative Markdown link from `SKILL.md` or another reachable reference file inside the same skill. All internal relative links must resolve cleanly inside the skill package.
- **Manifest lockstep:** Both `.antigravity-plugin/plugin.json` and `.agents/plugins/marketplace.json` are generated and verified in lockstep by `scripts/package_marketplace.py`.

## 4. Growth & Maintenance Workflow

### Scaffold a new skill
```sh
python3 scripts/new_skill.py <skill-name> \
  --display-name "My Skill Title" \
  --category "Core Platform & Integrations" \
  --short-description "Concise 25-64 char summary for catalog cards." \
  --description "Single-line trigger description with explicit negative handoffs."
```

### Sync manifests after edits
```sh
python3 scripts/package_marketplace.py
```

### Install directly into Google Antigravity (`~/.gemini/config/skills/`)
```sh
python3 scripts/install_antigravity.py --sync-skills
```

### Run full local verification gate
```sh
python3 -m pip install -r requirements-validation.txt
python3 scripts/package_marketplace.py --check
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```
