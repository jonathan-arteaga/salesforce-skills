# Salesforce skill expansion validation — 2026-11-15

## Delivered

Nine new canonical entrypoints: `salesforce-access-design`, `data360-ingestion-modeling`, `data360-query-insights`, `data360-governance`, `agentforce-grounding`, `data360-identity-resolution`, `data360-segmentation-activation`, `prompt-template-build`, and `agentforce-api-integrate`.

Each includes a scoped trigger, workflow, current-documentation guidance, focused reference, workbook and acceptance cases. Grounding owns the extracted provisioning reference; agent generation receives generated standalone copies. CLI examples are conditional on actual installed help, not assumed availability. The catalog now contains 78 packages, 82 packaged skill folders and 76 unique skills, including 43 Salesforce entrypoints. These are repository packages, not a claim that every package has been installed in ChatGPT or an org.

Corrected known event replay/retention guidance, added Beta qualification for ManagedSubscribe, and removed routes to absent companions. Explicit handoff contracts now have automated target checks. Agent creation versus design-only routing was clarified after an independent test failure. CI now includes existing persona, architecture-analysis and Data 360 analysis suites.

## Evidence

| Check | Result | Meaning |
| --- | --- | --- |
| Packaging, generated copies and local Markdown links | Passed | Standalone package consistency, not org compatibility |
| Repository metadata validation | 82 folders / 76 unique names passed | Catalog metadata valid |
| OpenAI basic validator | All nine new skills passed | Frontmatter/shape validation |
| Root unit suite | 29 passed | Includes schema-client, metadata, routing scorer, handoff and generated-copy tests |
| Existing persona suite | 164 passed | Local contracts |
| Existing architecture-analysis suite | 604 passed | Existing mocked/fixture behavior |
| Existing Data 360 analysis suite | 407 passed | Existing mocked/fixture behavior |
| Total automated unit checks | **1,204 passed** | Most are existing regression coverage, not 1,204 tests of the new workflows |
| Independent metadata routing | **21/21 passed** in final run | One fresh selection per request; not host discovery/install testing |
| Independent offline scenarios | Six useful artifacts covering all nine new workflows | Draft behavior and failure handling; no live product execution |
| Whitespace/diff validation | Passed | Patch hygiene |

## Routing iteration

The initial 15-case run selected `agent-architecture` for “Create an agent with topics and custom actions” (14/15). The generation description had been limited to Agent Script terminology. Clarified implementation versus design-only descriptions, then a fresh 15-case run passed. After adding the remaining four skills and adjacent boundaries, a separate fresh 21-case run passed.

Raw decisions: [initial](salesforce-expansion/routing-initial.json), [revised](salesforce-expansion/routing-revised.json), [final](salesforce-expansion/routing-final.json). Inputs/expected routes: [routing cases](../salesforce_foundation_cases.json). Evaluators received only names/descriptions and request text, not expected routes.

## Scenario review

Fresh agents received the skills and task-local facts, not audit conclusions or expected outputs. They could read normal bundled acceptance references. This is a one-pass practical evaluation, not a statistically independent benchmark of unseen tasks. Source-based key-qualifier guidance was strengthened during implementation and exercised in a separate qualified-key scenario.

| Artifact | Reviewed outcome |
| --- | --- |
| [Access and governance](salesforce-expansion/forward-access-governance.md) | Explained surviving profile/direct grants; drafted separate CRUD/FLS/row controls and 20 access/cache/export/consent cases; no live success claims. |
| [Ingestion and query](salesforce-expansion/forward-ingestion-query.md) | Preserved source identity, rejects/retries and downstream dependencies; corrected 90 to 30; treated async failure as failure. |
| [Grounding](salesforce-expansion/forward-grounding.md) | Separated source/index/retrieval/binding/answer; tested audience/citation isolation; used a Setup handoff when CLI absent. |
| [Qualified keys](salesforce-expansion/forward-qualified-keys.md) | Joined IDs plus qualifiers; expected CRM=10, ERP=20 instead of duplicated total 60; distinguished local arithmetic from target compilation. |
| [Identity and activation](salesforce-expansion/forward-identity-activation.md) | Kept spouses separate, made the third record conditional on verified identity, separated reconciliation and source writeback; previewed consent/contact counts without saving a scheduled activation. |
| [Prompt and API](salesforce-expansion/forward-prompt-api.md) | Drafted a new immutable-history-safe version and grounded response tests; blocked blind resend after uncertain action outcome; local mock assertions only. |

Task prompts are retained in [scenario-prompts.json](salesforce-expansion/scenario-prompts.json). Synthetic assertions inside outputs are illustrative local checks, not a deployed client, Salesforce SQL compiler, model-quality evaluation or extra tests included in the 1,204 count.

## Practitioner input and limits

[Practitioner evidence](../../docs/salesforce/practitioner-insights.md) records 12 selected discussions across Reddit, Salesforce Stack Exchange and Trailblazer, with official corroboration and unresolved claims. Used them for failure cases and usability, not prevalence estimates or product guarantees. No destructive workaround, obsolete price or unsupported host substitution was adopted.

No Salesforce org, production data, agent deployment, external activation, API session or live model test was used. Current release, licenses, schema, execution identity and feature availability must be verified at task time. Full live acceptance requires an authorized sandbox and appropriate connectors. Later product-specific discovery and the demand-driven solution-design skill remain outside this implemented set. PR #2 remains a review branch unless separately merged.
