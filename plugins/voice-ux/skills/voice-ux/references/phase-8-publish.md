# Phase 8 — Publish with self-healing (optional)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Phase 8 — Publish with self-healing (optional)

If the developer wants the agent published to a target org:

1. **Confirm target org and agent name** via `AskUserQuestion`. Display org details (`sf org display --target-org <alias>`) before any deploy action — orgId, instanceUrl, alias, agent label, agent API name. Require explicit YES/NO confirmation.
2. **Verify bundle structure.** The bundle directory must contain `<name>.agent` and `<name>.bundle-meta.xml`. The bundle-meta.xml MUST contain `<bundleType>AGENT</bundleType>` (uppercase, case-sensitive — see `references/publish-errors/E006`). Filename suffix is `.bundle-meta.xml`, not `.aiAuthoringBundle-meta.xml` — the Agent Script CLI is specific.
3. **Publish (default command — note `--skip-retrieve`):**

   ```bash
   sf agent publish authoring-bundle --api-name <name> --target-org <org> --skip-retrieve
   ```

   The `--skip-retrieve` flag avoids the post-publish retrieve+deploy-back step which has recurring CLI bugs (E005 `target` undefined, E006 bundleType case). The agent itself publishes correctly without it. Only omit `--skip-retrieve` if you specifically need platform-generated supporting metadata pulled into your DX project — most voice migrations don't.
4. **Self-healing on failure:** initialise `PUBLISH_ITERATION = 0`, `MAX_PUBLISH_ITERATIONS = 15`. On error, capture stderr and match against `references/publish-errors/`. For each match:
   - If `auto_fix: true`, apply the canonical fix and re-publish.
   - If `auto_fix: false`, surface the canonical fix(es) to the developer and ask before applying. For multi-option errors (e.g. E007 schema drift, with three fix paths), surface all options with their tradeoffs and wait for the developer's choice.
   - If no match, surface the raw error and ask the developer to inspect.

   **What this loop catches:** static publish-XML issues (E003, E006), known runtime/dependency errors (E001 locale picklist, E002 missing target Apex/Flow, E007 action schema drift). Schema and dependency mismatches between the `.agent` and the target org are NOT knowable until publish time — the offline validator can't see the org. The self-heal loop is the right place to handle them. Phase 7 cannot pre-emptively detect them, and shouldn't try.
5. **Verify success.** Run two SOQL probes:

   ```bash
   sf data query --query "SELECT Id, DeveloperName, MasterLabel FROM BotDefinition WHERE DeveloperName = '<name>'" --target-org <org>

   sf data query --query "SELECT DeveloperName, PlannerType FROM GenAiPlannerDefinition WHERE DeveloperName LIKE '<name>_v%' ORDER BY LastModifiedDate DESC LIMIT 1" --target-org <org>
   ```

   Expect:
   - `BotDefinition` row exists with the right `DeveloperName`.
   - `GenAiPlannerDefinition` row exists with `PlannerType = Atlas__ConcurrentMultiAgentOrchestration`.

   Both confirm an NGA / Agent Script agent. If `PlannerType` is anything else, the agent is NOT NGA — review `additional_parameter__disable_graph_runtime` in the source `.agent` (see `references/publish-errors/E004`) and re-publish.
6. **Check that the voice config compiled.** A clean publish doesn't prove the `modality voice:` settings arrived. Validator 2.9.8 compiles the nested `outbound:`/`inbound:` format (H03) to an empty `modality_parameters.voice` with only warnings, and a field build reported flat `inbound_keywords` missing from the published agent. Open the published version in Agent Builder (or retrieve it) and confirm that `voice_id` or `persona_id`, the model, `outbound_stability`, `inbound_keywords`, `inbound_filler_words_detection`, `pronunciation_dict` and `additional_configs` are all there. If any is missing, re-emit it in the flat format and re-publish. Then confirm the model from a live session trace: compiled planner bundles don't show model names.
7. **Hand-back:** print agent ID, label, target org, and direct link to Agent Builder. Summarize any auto-fixes that were applied during the loop. State explicitly that the agent is in **draft / inactive** state. Add the activation pre-flight, because the "rings then hangs up" failure comes from these, not from the script:
   - `config: → default_agent_user` is set to a real user.
   - That user has access to every Apex class and flow the agent's actions call.
   - **Re-activate after granting any permission.** The runtime plan is cached at activation, so a fix granted afterwards doesn't take effect until the agent is activated again.
   - Apex that runs `with sharing` can see the records it needs as that user.

The agent publishes in **draft / inactive** state. It does not handle live traffic until separately activated. This is safe by default — no customer-facing impact from a publish alone.
