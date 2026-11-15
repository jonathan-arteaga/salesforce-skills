---
name: |-
  agentforce-generate
description: |-
  Create, build, modify, review, or repair Salesforce agents with topics and actions using Agent Script and aiAuthoringBundle metadata. Return implementation artifacts and validation evidence. Use agent-architecture for design-only proposals, agentforce-grounding for retrieval diagnosis, and agentforce-test for test suites.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.

For industry-specific agents, cross-industry ideation, or role/personality choices, read the selected patterns in [industry and role design](references/shared/industry-patterns.md). Use them within this skill’s ownership; distinguish documented capabilities from proposed designs.


# Agent Script Skill

Use this workflow for Agent Script or supported migration to Agent Script. For Einstein Bot migration, use an available dedicated workflow or report the missing dependency. Without an authorized Salesforce org or CLI, limit validation to the available local checks.

## Read for the selected task

Follow current explicit user instructions over workflow defaults. Select the requested mode or phase first. For each reference below, read the sections needed for that mode, its prerequisites, and its output contract; skip unrelated modes and optional stages. Preserve all applicable identity, authorization, security, and validation checks. Reuse reference content already read unless it changed; a phase transition alone does not require rereading it.

For persona, instruction authoring, or a new agent, complete the [instruction design worksheet](references/instruction-design.md) before encoding the behavior. Reuse an existing persona handoff; keep its semantic design ownership with persona.

## What This Skill Is For

This skill is for developing Agentforce agents, primarily with Agent Script, Salesforce's scripting language for AI agents.

Org-backed workflows require the licenses, supported API/CLI versions, and execution identity appropriate to the agent type and channel. Employee agents run as the logged-in user; Service agent context depends on the channel and credential-based verification. Verify the target instead of assuming every agent requires an Einstein Agent User. Static authoring and review can proceed without org access.

**CRITICAL:** Agent Script is NOT AppleScript, JavaScript, Python, or any other<br />language. Do NOT confuse Agent Script syntax or semantics with any other<br />language you have been trained on.

Agent Script agents are defined by `AiAuthoringBundle` metadata: an<br />`<ApiName>.agent` file (agent behavior) plus a sibling<br />`<ApiName>.bundle-meta.xml` file (bundle metadata). The directory and both<br />filenames must use the same case-sensitive API name; a literal<br />`bundle-meta.xml` filename is not deployable. Actions can be implemented with<br />invocable Apex, autolaunched Flows, Prompt Templates, and other supported types.

This skill covers the full Agent Script lifecycle: designing agents,<br />writing Agent Script code, validating and debugging, deploying and<br />publishing, and testing.

## How to Use This Skill

This file maps user intent to task domains and relevant reference files in `references/`. Treat this file as the execution router for end-to-end agent development, and use references for deep detail.

Identify user intent from task descriptions. Read only the reference explicitly<br />required by the active step or needed for the current decision. Every<br />**Reference Files** section is a lookup index, not a preload list; do not load<br />files for later or inapplicable steps.

For a comprehensive health check, common-pitfall audit, or audit-fix-evaluate<br />loop over an existing agent, use the **Audit and Repair an Existing Agent**<br />task domain below as part of the same authoring lifecycle.

## Rules That Always Apply

1. <b>Always </b>**`--json`****.** ALWAYS include `--json` on EVERY `sf` CLI command. Do NOT pipe CLI output through `jq` or `2>/dev/null`. Read the full JSON response directly — LLMs parse JSON natively.
2. **Verify target org.** Before any org interaction, run `sf config get target-org --json` to confirm a target org is set. If none configured, ask the user to set one with `sf config set target-org <alias>`.
3. **Diagnose in proportion to the change.** For syntax or local static defects,<br />run the supported local parser/compiler first, then add target-org validation<br />when available.<br />For behavioral defects, preserve a baseline and use preview plus traces.<br />For a Surface repair, freeze the exact accepted edit list, then inspect the<br />final diff and revert every other hunk, including block-scalar or metadata<br />normalization. In a smallest-change repair, keep optional cosmetic findings<br />advisory unless the user explicitly includes cleanup in scope; valid syntax<br />with no diagnostic or use-case consequence is not an extra repair.<br />Simulation can establish routing and action selection; use<br />`--use-live-actions` only with explicit approval, a verified non-production<br />environment, and safe test data. Do not claim an external effect from<br />simulation or response text. See<br />[Validation & Debugging](references/agent-validation-and-debugging.md).
4. **Use a proportionate spec gate.** Obtain explicit Agent Spec approval for<br />greenfield agents and Structural or Rewrite changes. A user-authorized,<br />well-specified local repair does not require recreating or reapproving the<br />entire spec; record the affected use case and preserve the existing design.<br />When the user supplies a sufficiently detailed design and explicitly says it<br />is already approved, treat that as the approved spec: do not recreate it or<br />stop for another approval unless requirements are missing or materially change.
5. **Don't stall.** After a step completes successfully, announce the<br />next step and start it. Do not wait for the user to say "what's next"<br />or "ok, continue." Checkpoints that require explicit user approval include:<br />(a) Agent Spec approval when required by Rule 4, (b) the pre-Publish<br />CHECKPOINT, (c) destructive or consequential external operations, and (d)<br />any A/B branch the skill explicitly surfaces (e.g., Data Cloud not<br />provisioned during ADL setup). Long-running async work like ADL<br />indexing should run in the background while the skill continues with<br />work that doesn't depend on the result.
6. **Draft-first lifecycle.** During normal authoring, stay in draft iteration:<br />edit `.agent` + action implementations, validate, deploy, and preview as many<br />times as needed. Do NOT publish/activate by default. Publish + activate are<br />explicit release actions that require the user to confirm they are ready to<br />commit the current draft to metadata and expose it to end users.
7. **Start with one execution block and no mutable state.** A focused agent puts<br />reasoning and actions directly in `start_agent`. Add a subagent only for a<br />real objective, instruction, action, authority, or escalation boundary. Add<br />persistent state only for a named deterministic consumer and give it a<br />complete lifecycle. Ordinary continuity stays in surviving history. Apply<br />the concrete checks in [The Zen of AgentScript](references/zen-of-agentscript.md)<br />and [Posture & Determinism](references/posture-and-determinism.md).
8. **Use supported control flow.** Use the canonical conditional forms and<br />never generate a nested `if`, which Agentforce lint rejects. See<br />[Conditional Control Flow Syntax](references/agent-script-core-language.md#conditional-control-flow-syntax),<br />then run full bundle validation.
9. **Action implementation is a user decision.** During planning/spec work,<br />default new actions to `NEEDS STUB` placeholders. Always ask the user whether<br />they want to scan org/project for existing implementations and/or generate<br />new Apex/Flow/Prompt implementations before taking either path.
10. **Give each reachable branch one next outcome.** Choose exactly one primary<br />outcome: answer, ask, invoke an action, transition, refuse, or escalate.<br />The compiler selects a subagent `system.instructions` override instead of<br />the global value, and the current runtime assembles effective system and<br />resolved reasoning text for the model. Keep authoring constructs out of<br />model-facing text. See<br />[Instruction Resolution](references/instruction-resolution.md).
11. **Use portable structural indentation.** Generate new `.agent` files with<br />4 spaces per level. Preserve a consistently indented legacy file during a<br />surgical edit, or normalize the whole file as a separate validated change.
12. **Do not let prompt formatting impersonate control flow.** Indentation,<br />numbered steps, and words such as `Show`, `Ask`, `Call`, `Set`, or `STOP`<br />inside `|` text are model instructions, not executable scope. Gate actions<br />independently. Use one `|` per contiguous prompt block; repeated adjacent<br />markers do not create stages or priority. Do not use<br />`@utils.setVariables` to force a turn boundary or another reasoning<br />iteration. Apply the checklist in<br />[Common Control-Flow Pitfalls](references/common-control-flow-pitfalls.md).
13. **Choose who owns each decision.** Use runtime predicates when an exact<br />machine-known fact has a consequence that must remain stable. Use model<br />instructions when semantic intent, ambiguity, recovery, or<br />situation-aware judgment makes flexibility more valuable. A model cannot<br />read stored variable values unless prompt text injects them with<br />`{!@variables.X}`; interpolation reveals a value but does not make the<br />model's comparison deterministic. Apply the tradeoff test in<br />[Posture & Determinism](references/posture-and-determinism.md).
14. **Compile AgentScript locally first, cheaply, and visibly.** For every<br />authoring, repair, or audit task with an existing `.agent` file, attempt the<br />bundled local index/compiler before org-side validation or a completion<br />report. Run<br />`node <skill-directory>/scripts/index-agent.mjs <agent-file>`. If the SDK<br />cannot load, follow<br />[AgentScript Compiler Setup](references/agentscript-toolchain.md), retry,<br />and use its bounded npm/source fallback. Fix every severity-1 diagnostic<br />and rerun until clean. Report the provider and exact version or commit.<br />Org access does not replace this cheap local pass. If both local setup paths<br />fail, continue with target-org validation or a bounded static review and<br />state **compiler not used** with the cause; do not stall the task or imply<br />that a suggested future command was validation. **Offline** or<br />**non-interactive** mode does not waive this step: it prohibits network and<br />org operations, not the bundled local compiler.
15. **Keep the authoring-bundle shape deployable.** Under<br />`aiAuthoringBundles/<ApiName>/`, require exactly the matching pair<br />`<ApiName>.agent` and `<ApiName>.bundle-meta.xml`. Do not shorten the<br />metadata filename to `bundle-meta.xml`. Preserve scaffolded or retrieved<br />metadata rather than rewriting its schema. A new CLI-scaffolded bundle<br />normally uses `<bundleType>AGENT</bundleType>`; an existing descriptor can<br />instead use the established `fullName`/`type`/`status` shape, with optional<br />`label` and `description`. Do not create a partial hybrid or invent fields.<br />Local compilation of the `.agent` file does not verify the metadata<br />filename or XML, so check both before reporting validation success.

## Task Domains

Choose the domain that matches the user's current objective. Read its named<br />references before acting; the links are load instructions, not an optional<br />bibliography. Follow only the applicable workflow and preserve any satisfied<br />prerequisites. The normal lifecycle is design -> draft -> validate/preview -><br />explicitly approved release.

### Create an Agent

Consult [`references/domain-create-agent.md`](references/domain-create-agent.md) before creating an agent or authoring bundle.

### Comprehend an Existing Agent

Use when the user wants to understand an existing bundle.

1. Locate the package and matching authoring-bundle files.
2. Read [Core Language](references/agent-script-core-language.md), then map the<br />subagent graph, deterministic blocks, model instructions, actions, variables,<br />and action implementations.
3. Read [Design & Agent Spec](references/agent-design-and-spec-creation.md) and<br />reverse-engineer a saved Agent Spec. Use<br />[Subagent Map Diagrams](references/agent-subagent-map-diagrams.md) for the<br />graph. Annotate source only when the user requests it.
4. Flag supported anti-patterns, distinguishing observed behavior from static<br />inference. Load [Known Issues](references/known-issues.md) only for an<br />otherwise unexplained workaround.

### Audit and Repair an Existing Agent

Consult [`references/domain-audit-and-repair.md`](references/domain-audit-and-repair.md) before auditing or repairing an existing agent.

### Modify an Existing Agent

Consult [`references/domain-modify-agent.md`](references/domain-modify-agent.md) before modifying an existing agent.

### Diagnose Compilation Errors

1. Capture the exact reported errors and run the Rule 14 local compiler.
2. When an authenticated target org is available, run org validation; use live<br />preview only when compilation succeeds but runtime preparation still fails.
3. Classify and repair each concrete error using<br />[Validation & Debugging](references/agent-validation-and-debugging.md) and<br />[Core Language](references/agent-script-core-language.md).
4. Rerun the surfaces that exposed the error. Report exact executed checks,<br />remaining limitations, and no unexecuted command as validation evidence.

### Diagnose Behavioral or Production Issues

For a local behavioral problem, preserve a baseline, preview with realistic<br />utterances, and inspect traces using<br />[Validation & Debugging](references/agent-validation-and-debugging.md). Confirm<br />which subagent, action calls, action results, state changes, and final response<br />actually occurred before editing.

For a production session or trace ID, use **agentforce-observe** for retrieval<br />and reconstruction. Return here only when evidence identifies an AgentScript<br />change. Never invent unavailable action inputs, outputs, or model reasoning.

### Deploy, Publish, and Activate

Consult [`references/domain-deploy-publish-activate.md`](references/domain-deploy-publish-activate.md) before deploying, publishing, or activating.

### Delete or Rename an Agent

Read the delete/rename sections of [CLI for Agents](references/salesforce-cli-for-agents.md)<br />and [Metadata & Lifecycle](references/agent-metadata-and-lifecycle.md). Enumerate<br />references and dependencies, show the exact affected bundle, and obtain explicit<br />confirmation before deletion. For rename, create and validate the replacement<br />before deleting the original; verify orphaned metadata afterward.

### Test an Agent

Use **agentforce-test** for test-spec design, security coverage, metadata<br />creation, execution, and result analysis. First map the Agent Spec and all<br />reachable routes/actions into coverage targets. Confirm before adding security<br />tests or running tests that can invoke live actions.

### Migrate a Legacy Agent to Agent Script

Consult [`references/domain-migrate-legacy-agent.md`](references/domain-migrate-legacy-agent.md) before migrating a legacy agent.

### Optimize an Agent

1. Read [Core Language](references/agent-script-core-language.md) and scan every<br />reachable path using [Common Control-Flow Pitfalls](references/common-control-flow-pitfalls.md).
2. Load only applicable optimization references: data flow, deterministic<br />logic, reference syntax, human handoff, and voice readiness.
3. Report evidence-backed improvements and obtain approval before editing.
4. Apply only approved changes, compile locally, validate against the org when<br />available, and report the resulting evidence.

### Manage MCP Servers

Read [MCP Server Management](references/mcp-management-reference.md) before any<br />MCP operation. Verify the target org, use `--json`, keep secrets off command<br />lines, review tools before allowlisting, and require confirmation for destructive<br />or consequential changes.

## The Agent Spec

Consult [`references/agent-spec.md`](references/agent-spec.md) before writing, reading, or approving an Agent Spec.

## Assets

Read [`references/assets-catalog.md`](references/assets-catalog.md) when you need a template, example agent, or other bundled asset.

## Important Constraints

- **Use supported tooling for the evidence needed.** Use Salesforce CLI and the<br />target org for org-backed validation and release operations. Use the published<br />AgentScript SDK for local parse/compile checks, and invoke related skills only<br />within their documented boundaries.
- **Only certain implementation types are valid for actions.** For example, only invocable Apex (not arbitrary Apex classes) can back an action. Similar constraints may apply to Flows and Prompt Templates. When wiring actions to implementations, consult Design & Agent Spec reference file for valid types and stubbing methodology.
- **`sf agent generate test-spec`**<b> is not for agentic use.</b> It is interactive, REPL-style command designed for humans. When creating test specs, start from boilerplate template in assets instead.

## Common Issues Quick Reference

Read [`references/common-issues.md`](references/common-issues.md) when a compile, deploy, preview, or runtime error appears.

## Quick Links (Deep Detail Lives in References)

- Syntax and execution model: [Core Language](references/agent-script-core-language.md)
- Agent design/spec process: [Design & Agent Spec](references/agent-design-and-spec-creation.md)
- Posture dial (agentic vs deterministic): [Posture & Determinism](references/posture-and-determinism.md)
- Concrete authoring invariants: [The Zen of AgentScript](references/zen-of-agentscript.md)
- Pattern selection by scenario: [Patterns by Requirement](references/patterns-by-requirement.md)
- Architecture mechanics, HyperClassifier routing, and migration: [Architecture Patterns](references/architecture-patterns.md)
- Validation, preview, and traces: [Validation & Debugging](references/agent-validation-and-debugging.md)
- Deploy/publish/activate lifecycle: [Deploy Reference](references/deploy-reference.md)
- Metadata lifecycle and publish troubleshooting: [Metadata & Lifecycle](references/agent-metadata-and-lifecycle.md)
- For grounding design, retrieval failures and evaluation, use `agentforce-grounding` when available. For standalone provisioning and agent wiring, use the generated [Data Library Reference](references/data-library-reference.md); verify installed capabilities first.
- Agent access and permissions: [Agent Access Guide](references/agent-access-guide.md), [Agent User Setup](references/agent-user-setup.md)
- Voice modality and telephony agents: [Voice Modality Reference](references/voice-modality-reference.md)
- Safety review framework: [Safety Review](references/safety-review-reference.md)
- Rubric and review scoring: [Scoring Rubric](references/scoring-rubric.md)
- Optimization patterns: [Pattern 1 — Data Flow](references/optimization-pattern-1-data-flow.md), [Pattern 2 — Deterministic Logic](references/optimization-pattern-2-deterministic-logic.md), [Pattern 3 — Reference Syntax](references/optimization-pattern-3-reference-syntax.md), [Pattern 4 — Escalation](references/optimization-pattern-4-escalation.md)
- MCP server registration and tool whitelisting: [MCP Server Management](references/mcp-management-reference.md)
