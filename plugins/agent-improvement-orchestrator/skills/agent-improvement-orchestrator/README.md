# Agent Improvement Orchestrator Skill

**Make your Agentforce agent measurably better — without babysitting every step.**

A Codex skill that ties review, fixing, testing, and evaluation into a single loop that runs until the agent's score and pass rate actually go up — and rolls back any change that makes things worse.

---

## The problem

Improving an Agentforce agent is a slog. You review the config, write a fix, deploy it, re-run your tests, check nothing regressed — then repeat. The steps live in different tools and different context windows, so it's easy to fix one thing and silently break another, and easy to lose your place halfway through.

This skill ties those steps into one loop — **review → plan → implement → test → evaluate** — running until your agent's score and pass rate actually improve.

## It orchestrates, it doesn't reinvent

The real work — reviewing, testing, fixing, deploying — is done by skills you already have. This skill is the **conductor**: it sequences them, tracks state across context windows, and knows when to stop. It pulls in whatever each phase needs:

- **Review** — `/agentforce-config-review` for the scored audit
- **Test** — your project's testing skill (and if you don't have one, it walks you through creating it — see [Testing Skill Bootstrap](#testing-skill-bootstrap))
- **Fix** — the platform dev skills for correct conventions: `agentforce-generate` (agent DSL), `platform-apex-generate` + `platform-apex-test-generate` (Apex), `automation-flow-generate` (Flows), and the in-repo `persona` skill (brownfield mode) when the persona/tone score is low
- **Deploy** — `platform-metadata-deploy` conventions

It only invokes what a given run actually requires — a persona fix won't touch the Apex skills, and Plan Only mode never deploys. The full list is in [Integration Points](#integration-points).

## What it does

- Runs a structured improvement loop on any Agentforce agent
- Two modes: **Full Ownership** (implements and tests autonomously) vs **Plan Only** (advisory plan, no changes)
- Delegates config review and testing to existing skills
- On a regression, reverts the change (automatically if you granted auto-revert, otherwise stops and asks)
- Saves progress at every phase, so you can resume after a context window runs out

---

## How to invoke

```bash
# Full improvement loop from scratch
/agent-improvement-orchestrator Acme_Support_Agent --mode full --org myOrg

# Plan only — produces a fix plan without implementing
/agent-improvement-orchestrator Acme_Support_Agent --mode plan

# Resume after a context window ran out
/agent-improvement-orchestrator Acme_Support_Agent --resume

# Skip review, use existing findings
/agent-improvement-orchestrator Acme_Support_Agent --mode full --findings ./review-findings-2026-05-30.json
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--mode full\|plan` | Asked in Session Setup | `full` = implement + test, `plan` = advisory only |
| `--max-iterations N` | 3 | Max fix/test cycles before stopping |
| `--org <alias>` | Default org | Target Salesforce org |
| `--resume` | — | Resume from existing state file |
| `--skip-review` | — | Skip initial review (use existing findings) |
| `--findings <path>` | — | Path to existing findings JSON |

---

## How it works

```
PRE-FLIGHT → REVIEW → PLAN → [IMPLEMENT → TEST → EVALUATE] → RE-REVIEW → COMPLETE
                                  ↑__________________|
                                   (max N iterations)
```

### Phases

1. **PRE-FLIGHT** — 8 checks: org connectivity, agent file, testing skill, config review skill, baseline results, deployability, Python deps, git
2. **REVIEW** — Invokes `/agentforce-config-review` to produce the scored Config Review report
3. **PLAN** — Ranks findings by severity, groups into batches, produces a fix plan
4. **IMPLEMENT** — Applies fixes to the agent file + supporting metadata, deploys
5. **TEST** — Delegates to the testing skill, compares the Test report against baseline
6. **EVALUATE** — Pass rate held or improved? Continue. Regression? Revert and try an alternative.
7. **RE-REVIEW** — Runs the config review again and reports the score delta
8. **COMPLETE** — Writes the durable run summary, then offers history cleanup as a multi-select that also lets you generate an optional shareable HTML report

### The two reports

The loop produces two **different kinds** of report. Knowing which is which is the key to reading the output:

| | Config Review report | Test report |
|---|---|---|
| **File** | `.docx` | `.html` |
| **From phase** | REVIEW / RE-REVIEW | TEST |
| **What it measures** | The agent's *configuration* — scored 0–10 across dimensions (routing, guardrails, grounding…) | The agent's *behavior* — pass/fail on real questions run against the live agent |
| **Answers** | "Is this agent **well-built**?" | "Does this agent **actually behave correctly**?" |
| **Changes when** | You edit the agent's metadata/instructions | You change anything that affects responses |

In short: the **review** reads the blueprint; the **test** drives the car. The loop uses the review to decide *what* to fix, and the test to confirm the fix *worked* without breaking anything else.

### State persistence

Loop state is saved to `<project>/.agent-improvement/loop-state-<AgentName>__<OrgId>.json` after every phase transition — keyed by agent and org ID so runs against different orgs don't collide, and written under the project so a global install stays isolated. If the context window runs out mid-loop, use `--resume` to pick up where you left off.

### Testing Skill Bootstrap

If no testing skill exists for the agent, the orchestrator walks you through creating one:
- Confirms org and agent
- Reads the agent configuration (topics, actions, instructions)
- Develops test personas conversationally
- Generates a complete testing skill with personas, evaluation criteria, and parallel execution

---

## Integration Points

| Skill | Phase | Relationship |
|-------|-------|-------------|
| `/agentforce-config-review` | REVIEW / RE-REVIEW | Invoked — produces the Config Review report |
| Project testing skill | TEST | Invoked — produces the Test report; created via Bootstrap if missing |
| `agentforce-generate` | IMPLEMENT | Referenced for agent DSL patterns |
| `persona` | IMPLEMENT / RE-REVIEW | Invoked (brownfield mode) when the review scores persona/tone low — re-encodes only persona-bearing fields of the `.agent`; its 100-point rubric is scored before/after and governs whether persona findings count as resolved |
| `platform-apex-generate` | IMPLEMENT | Referenced for Apex class conventions |
| `platform-apex-test-generate` | IMPLEMENT | Referenced for Apex test patterns |
| `automation-flow-generate` | IMPLEMENT | Referenced for Flow XML metadata |
| `platform-metadata-deploy` | IMPLEMENT | Referenced for deploy conventions (or project AGENTS.md) |

---

## Guardrails

- Never deploys without scoped user authorization. Show each diff; reuse approval only while the target and permitted changes match. Ask for missing or materially changed scope.
- Max 3 fix attempts on the same batch (separate from `--max-iterations`, the whole-loop cycle cap)
- No silent regressions — on a failed iteration it reverts automatically if you granted auto-revert, otherwise it stops and asks before discarding any changes
- Versioned outputs (never overwrites existing files)
- Testing fully delegated to the testing skill (orchestrator doesn't manage sessions)
- Works without git (graceful degradation)

---

## Examples

Small, illustrative samples for a fictional `Acme_Support_Agent` (no real org or data) live in [`examples/`](examples):

| File | What it is |
|------|-----------|
| [`sample-improvement-plan.md`](examples/sample-improvement-plan.md) | The **Plan Only** deliverable produced by `--mode plan` — batched fixes citing Finding IDs, with deferrals and verification steps. The agent is not touched. |
| [`sample-run-summary.md`](examples/sample-run-summary.md) | The durable end-of-run **summary**: score/pass-rate deltas, fixes by Finding ID, deferrals, and an index of every output the run produced. |
| [`sample-improvement-report.html`](examples/sample-improvement-report.html) | The **optional shareable HTML report** rendered at COMPLETE — opt-in via the history-cleanup multi-select or by asking for it during the run — the same run summary as a self-contained, print/PDF-ready page (composite + per-dimension bars, severity before/after, fixes by Finding ID, persona rubric, carry-forward). |
| [`loop-state-example.json`](examples/loop-state-example.json) | The saved **loop state** written after each phase so a `--resume` can pick up where it left off. Includes the `outputs[]` manifest. |

---

## Prerequisites

- Salesforce CLI (`sf`) v2+
- Python 3.9+ with `python-docx` (`pip3 install python-docx`)
- An authenticated Salesforce org with the agent deployed
- Git (optional — enables progress commits and revert-on-regression)
- `agentforce-config-review` (ships in the personal Salesforce plugin) for REVIEW — or supply `--findings <path>` to skip it

The orchestrator locates the skills it delegates to in `.agents/skills/` and your distributed/marketplace plugins; missing optional skills degrade gracefully rather than blocking the loop.

---

## File locations

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition — operational instructions for Codex (control flow; loads `references/` on demand) |
| `README.md` | This file |
| `references/planning.md` | PLAN detail — Pattern Library, priority-scoring formula, implementation-skill map (loaded in PLAN) |
| `references/consumed-contracts.md` | Required/optional fields + validation rules for the findings JSON, `test-results.json`, and persona rubric (loaded at each validation step) |
| `references/testing-skill-bootstrap.md` | Interactive flow for creating a testing skill when pre-flight Check 3 finds none |
| `examples/sample-improvement-plan.md` | Plan Only deliverable sample |
| `examples/sample-run-summary.md` | Run summary sample |
| `examples/sample-improvement-report.html` | Optional shareable HTML report sample |
| `examples/loop-state-example.json` | Saved loop-state sample |
| `<project>/.agent-improvement/` | Per-run state and outputs (anchored to the current project root) |

---

## Acknowledgements

This orchestrator stands on skills and frameworks built by others. With thanks to:

- **Sarah Khalid** — the in-repo [`agentforce-config-review`](https://github.com/forward-deployed-engineering-emu/fde-skills/tree/main/plugins/auditing-agentforce/skills/agentforce-config-review) skill (personal Salesforce plugin)
- **Keith Mancuso** — [reusable Agent Testing Skill](https://salesforce.enterprise.slack.com/docs/T092Z56AE/F0AKSUKV4NP) 🔒
- **Nathan Lucy** — the in-repo [`persona`](https://github.com/forward-deployed-engineering-emu/fde-skills/tree/main/plugins/designing-agentforce/skills/persona) skill
- The [agentforce-adlc](https://github.com/SalesforceAIResearch/agentforce-adlc) and [sf-skills](https://github.com/forcedotcom/sf-skills) implementation teams

> 🔒 = Salesforce-internal link (Slack); resolves only inside the Salesforce workspace.
