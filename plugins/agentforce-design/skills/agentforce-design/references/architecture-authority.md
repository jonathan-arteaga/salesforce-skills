# Agentforce Architecture & Authority

Design-time architecture translates prioritized capabilities (`capabilities.yaml`) and optional baseline `.agent` exports into subagent boundaries, action specs, global instructions, and an integration map without introspecting live org metadata (route deployed introspection to `agentforce-review`).

## Architecture Modes

Greenfield is exclusive; Redesign, Channel customisation, and Script comparison compose freely.

| Mode | When to Use | Required Inputs | Primary Outputs |
| --- | --- | --- | --- |
| **Greenfield** | Net-new agent with no baseline | `capabilities.yaml` (or normalized pasted list) | `subagents.yaml`, `actions.yaml`, `global-instructions.md`, `architecture.json` |
| **Redesign** | Reshaping existing subagents or actions | Baseline `.agent` or prior YAML + `capabilities.yaml` | Above + continuity pills (`risk`, `carries_forward`, `changes_from_today`) |
| **Channel customisation** | Adapting settled shape (e.g., chat to voice) | Baseline `.agent` + target channel(s) | `<channel>_variant` overlays in `subagents.yaml`/`actions.yaml`, `voice_open_questions[]` |
| **Script comparison** | Surgical alignment to approved deliverables | Baseline `.agent` + approved persona/CD/requirements | `decision-points.yaml` (section-grouped before/after cards) |

If `capabilities.yaml` has `signoff.status: pending`, proceed with draft outputs and surface the pending status explicitly.

## Hybrid Reasoning & Subagent Decomposition

- **Start minimal:** Place focused reasoning and actions directly in `start_agent`. Split into distinct **subagents** (historically called topics) only for separate objectives, tool sets, authority boundaries, instruction overrides, or handoff paths.
- **Atlas Reasoning Engine vs. Agent Script:** Assign probabilistic decisions (intent classification, ambiguity recovery, summarization) to natural-language instructions. Assign mandatory prerequisites, eligibility checks, confirmation gates, and transitions to deterministic Agent Script constructs and Agent Graph transitions.
- **Pairwise routing clarity:** Test every pair of subagent classification descriptions for overlap before writing scope or action specs; ambiguous boundaries cause nondeterministic routing at runtime.
- **System override warning:** A subagent `system` block **replaces** global `system.instructions` instead of appending. Document every planned override and audit it for dropped persona, grounding, or compliance rules.
- **Multi-turn continuity:** Never assume every turn restarts at `start_agent`; explicitly design `runtime.reset_to_initial_node` expectations and verify with a two-turn preview trace in `agentforce-build`.

## Action Specs & Authority Boundaries

Every capability action must declare:

1. **Action & implementation type:** Standard Action, Autolaunched Flow, `@InvocableMethod` Apex, Prompt Template, MCP tool, Data Library/Retriever, or Headless.
2. **Execution identity & authorization:** Employee Agents run as the logged-in user; Service Agents run as an Agent User or verified site user. Prompts and action visibility filters never replace CRUD/FLS/sharing checks in backing Apex/Flow.
3. **Trusted verification gates:** Eligibility, customer identity, and write preconditions must come from trusted action outputs—never from customer assertions or model-set flags.
4. **Build ownership:** Assign an explicit owner (`FDE`, `Customer`, `Joint`, `External`) to every action and external integration; flag unowned actions as shipping blockers.
5. **Memory & file uploads:** Treat uploaded files as untrusted input (restrict to specific subagents); specify consent, retention, and cross-user isolation before enabling memory. Memory is never authorization.

## Review & Handoff Discipline

- **Output before questions:** Present a concrete 80% first draft (hybrid grouping by default) before soliciting edits.
- **Section-by-section confirmation:** In Script comparison mode, group `decision-points.yaml` by baseline section (`config` -> `global` -> `subagents` -> `actions`) for bulk or item-level approval.
- **Gated build handoff:** Never auto-generate `.agent` code from unapproved YAML. Once `architecture.json` or `decision-points.yaml` is approved, hand off to `agentforce-build` for `.agent` authoring and local compilation.
- **Dialect discipline:** Match `engagement.language` consistently across every user-facing design artifact with no silent fallback to US English.
