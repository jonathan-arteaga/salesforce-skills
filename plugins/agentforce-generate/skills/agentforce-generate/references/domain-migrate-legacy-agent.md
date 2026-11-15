# Migrate a Legacy Agent to Agent Script

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Migrate a Legacy Agent to Agent Script

User wants to upgrade a legacy `GenAiPlannerBundle` agent into an NGA `AiAuthoringBundle` (Agent Script) agent. May say "migrate my legacy agent", "upgrade to the new builder", "convert agent", "start migration", or mention `genAiPlannerBundle` / `aiAuthoringBundle` migration. (Distinct from Einstein **Bot** upgrades — this covers existing Agentforce **agents**. To convert an Einstein **Bot** into a new agent, use a dedicated Einstein Bot migration workflow if available, or report the missing dependency.)

#### Required Steps

Read [Upgrade a Legacy Agent to Agent Script](upgrade-legacy-agent-to-agentscript.md) for the full workflow, exact commands, and the NGA-vs-legacy discriminator. In brief:

1. **Set up the project** — **Confirm the target org via a selectable menu — never assume the default org** (show `sf org list`, mark the default, require an explicit pick). Confirm a DX project (create one if needed); run all retrieves from inside it.
2. **Pick the legacy agent version** — Two-screen selection: choose the agent, then a **non-NGA** version. Exclude versions whose planner `PlannerType` is `Atlas__ConcurrentMultiAgentOrchestration` (already NGA).
3. **Migrate via the Connect API** — POST the chosen `botVersionId` to `migrateAgentToNga`. Mutating call; confirm org + id first. Run it in a **subagent** so the large response (inline `agentScript`) does not bloat context — return only `bundleVersionApiName` (+ `conversionWarnings`, `agentResponse`).
4. **Retrieve the new bundle** — Pull the `AiAuthoringBundle` into the project (by `bundleVersionApiName`, or map `bundleVersionId → fullName` as fallback).
5. **Analyze, optimize, iterate** — The migration is a mechanical transform that ignores Agent Script primitives. Hand off to **Comprehend an Existing Agent**, then **Optimize an Agent**, then validate/preview.

#### Reference Files

1. [Upgrade a Legacy Agent to Agent Script](upgrade-legacy-agent-to-agentscript.md) — full step-by-step workflow, commands, and discriminator logic
2. [Core Language](agent-script-core-language.md) — read the migrated `.agent` structure
