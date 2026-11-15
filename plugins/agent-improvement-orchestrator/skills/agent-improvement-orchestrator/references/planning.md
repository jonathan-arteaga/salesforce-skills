# Planning Reference

Detail for the **PLAN** phase: how to classify findings into fix patterns, how to score them for
priority, and which skills to read before generating fix code. The PLAN phase's control flow (Finding
ID assignment, the batch state machine, the Mode Branch) stays in SKILL.md; this file holds the
stable lookup material it draws on.

## Pattern Library

Classify each HIGH/MEDIUM finding into a fix pattern:

| Category | Signal | Fix Pattern |
|----------|--------|-------------|
| Determinism gap | "LLM interprets", "non-deterministic" | Extract to variable + `set` block + `if` gate |
| Missing error gate | "No handling for failure", "status not checked" | Add `if status != SUCCESS` after `run` block |
| Consent/safety gap | "No explicit gate", "not enforced" | Add deterministic `if` before action |
| Variable type mismatch | D4 findings, type errors | Fix type in declaration or add adapter |
| Knowledge grounding | "hallucination risk", "no fallback" | Add knowledge action call + no-result fallback |
| Instruction ambiguity | "contradictory", "unclear" | Rewrite for single interpretation |
| Persona / tone weakness | low persona-or-tone rating, "inconsistent voice", "role unclear", "off-brand" | Delegate to `persona` (brownfield mode) to rework the agent's persona/tone (see Reference Skills for Implementation, below) |

## Priority Scoring

Score each finding and sort by descending **priority**, so effort lands on what matters — not every
same-severity finding is equal:

```
priority = severity_weight × determinism_impact × fix_confidence
  severity_weight   : HIGH = 3, MEDIUM = 2   (LOW already filtered out)
  determinism_impact: high = 3, medium = 2, low = 1   (inferred from the finding's title/detail
                      per the Pattern Library; default to 2 if no signal is present)
  fix_confidence    : 3 = clean Pattern Library match; 2 = match needing judgement;
                      1 = delegated (e.g. designing-agentforce:persona) or no clear pattern
```

All three factors come from data already present in the findings JSON + the Pattern Library match — no
new inputs. Break ties by severity DESC. A high-severity, high-impact, clean-pattern fix outranks a
marginal one of the same severity.

## Reference Skills for Implementation

Before generating fix code (in IMPLEMENT), read the relevant skill content for conventions:
- For `.agent` file changes: read `agentforce-generate` SKILL.md (or project alias `/sf-ai-agentscript`)
- **For persona / tone findings (low persona rating): delegate to `persona` in brownfield mode.** When the review scores the persona/tone dimension low — unclear role, inconsistent voice, off-brand tone — don't hand-edit instructions; invoke the `persona` skill from the personal Salesforce plugin, pointed at `$AGENT_FILE_PATH`, in its **brownfield** lane. Brownfield audits the existing `.agent` and re-encodes **only persona-bearing fields** (`system.instructions`, `system.messages.welcome`/`error`, and per-subagent tone in `reasoning.instructions`) — it never touches routing, subagents, actions, or variables. Take its brownfield output (`persona/<agent>/<agent>.agent` and the annotated `persona/<agent>/persona-diff.md`) and fold those persona-bearing fields into the `.agent` file as the batch's change. Cite the Finding ID(s) it resolves. The persona rubric for these findings is captured separately (see **Persona Rubric** in SKILL.md) and governs whether they count as resolved at RE-REVIEW.
- For Apex changes: read `platform-apex-generate` and `platform-apex-test-generate` SKILL.md
- For Flow changes: read `automation-flow-generate` SKILL.md
- For deployment: follow `platform-metadata-deploy` conventions (or project AGENTS.md deploy section)

Locate these by checking:
1. `.agents/skills/` in the current project
2. The active personal Salesforce plugin; use the loaded skill paths
