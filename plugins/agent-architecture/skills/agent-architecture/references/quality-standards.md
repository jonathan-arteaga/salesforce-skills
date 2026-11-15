# Quality Standards

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Quality Standards

A well-formed architecture deliverable:

- **Routing-clear classification descriptions** — pairwise comparison surfaces no overlap
- **Every action has a build owner** — no capability is unowned
- **Every subagent traces to capabilities** — capabilities and actions reference back to `capabilities.yaml` IDs
- **Subagent count passes the boundary test** — the shape should pass the five-part test from `agentforce-generate` `references/architecture-patterns.md`: a subagent is justified when it changes at least one of (objective, instructions, available actions, authority, escalation behavior) from its neighbours. If two candidate subagents don't change any of the five, they should merge. Each subagent's definition on the page must name which dimension(s) it changes — without that, routing-overlap reviews fall back to pattern-matching on names.
- **Continuity reasoning is honest (Redesign mode)** — `risk` reflects actual scope of change, not optimism
- **Open questions surfaced** — what's *not* decided is visible to reviewers
- **Global instructions are in persona voice** — or flagged for voice pass if persona is absent
- **Page renders gracefully without optional upstream data** — missing transcript-insights or persona shouldn't produce empty pills, just fewer fields
- Reference only patterns included in `references/patterns/`. Describe an unsupported design as a proposal; do not claim an existing pattern or upstream approval.
- **Dialect check passes before confirmation** — classification descriptions, global instructions, decision-point `after_text`, and variant deltas are all drafted in the dialect named by `engagement.language`. If US-ism patterns leak into an en-GB / en-AU draft (`color` instead of `colour`, `apartment` instead of `flat` where idiomatic, Oxford comma against UK style guides), flag and offer to retry drafting rather than silently writing.

**Channel-customisation-specific standards:**

- **Every subagent has a variant call** — either a drafted variant or an explicit "skip — no meaningful variant" acknowledgement. No subagents left silent.
- **Severity reflects real scope** — `minor` means channel tweaks only (progress message, ack tokens); `major` means capture / rendering / repair rewritten. Overstating severity dilutes the signal for reviewers.
- **Voice open questions surfaced separately from deltas** — open questions represent investigations that need to close before a variant can be locked; they're not the same as deltas that are locked and just haven't been built yet.

**Script-comparison-specific standards:**

- **Every recommendation cites verbatim `before_text`** — never paraphrase the baseline. Verbatim text is what makes the FDE trust the recommendation.
- **Every recommendation cites a specific `requirement_ref`** — persona §N, R-ID, CD scenario turn, or a workshop decision label. `requirement_ref: "user asked"` is a smell.
- **Recommendations flagged `pending` are honest** — `pending` means an authoritative source hasn't finalised yet, not that the recommendation is uncertain. Uncertain recommendations should be `decision: needs-discussion` instead.
- **Change scope reflects where the edit lands** — `script` for `.agent` edits, `flow` for Flow logic changes, `ivr` for Vonage/IVR configuration, etc. Miscategorising sends the recommendation to the wrong reviewer.
- **Proposed `.agent` never generated automatically** — the yaml is reviewed first; the proposed `.agent` follows on an explicit ask, is produced by `agentforce-generate`, and stays labelled "proposed, not validated" until it compiles. Prevents publishing unreviewed recommendations as if they were locked.

---
