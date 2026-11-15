# Salesforce skill-library gap assessment

Reviewed: **2026-11-15**. Baseline: PR #2 at `fc3f7026fdb58d83cf32a2a00d8c809a3e5896ca`, still unmerged when assessed. This is a build roadmap, not an implementation or a claim that every Salesforce product has been audited.

## Implementation status — 2026-11-15

Waves 1 and 2 are implemented in PR #2: nine new skill entrypoints, with grounding extracted from existing guidance. The event/routing maintenance items and broader offline CI suites below are also addressed. See [implementation and validation results](../../tests/results/2026-11-15-salesforce-expansion.md) and [practitioner evidence](practitioner-insights.md). Wave 3 and the later product-discovery backlog remain unimplemented. Live Salesforce acceptance remains pending. The assessment below records the original decision rationale.

## Recommendation

Build reusable Data 360 foundations and access controls next. Extract Agentforce grounding from the large generation skill instead of duplicating it. Repair stale guidance and missing routes before expanding the catalog.

Inventory: **67 canonical skills**, including **34 Salesforce entrypoints** (15 Agentforce and 19 platform/analytics). Packaged bundle copies are not additional capabilities. Existing strengths include Apex, LWC, Flow, metadata, integrations, agent design/generation/review/testing and observability.

A gap means there is no discoverable owner for a workflow's inputs, output artifact, validation and handoff—not merely that a keyword is absent. Priorities below are recommendations based on reuse, dependencies and Jon's Salesforce building work. Salesforce does not prescribe these skill names or this taxonomy.

Research: searched 17 workflow areas using the Salesforce Docs MCP and fetched 20 documents, including alternate detail pages. The linked source register records the selected evidence. Release 264 documentation is not proof a feature is available in a target org; check release, licenses, permissions, tooling and supported APIs during implementation. This review uses the remote MCP directly; activation of the ChatGPT plugin is a separate pending setup step.

## Phase 0: repair the foundation

1. Land the reviewed baseline in PR #2, then resolve the additional findings below. The earlier targeted audit did not verify every historical reference.
2. Correct `integration-connectivity-generate` references: `platform-events-guide.md` says 24-hour retention and calls ReplayId unique; `event-driven-architecture-guide.md` contains a 24h/72h retention table. Current Pub/Sub documentation specifies 72 hours for platform/CDC events, opaque replay IDs that cannot be calculated and may not be unique across maintenance. Platform event IDs and CDC identities require different handling. Label ManagedSubscribe's documented Beta status. Regenerate shared copies rather than patching generated files independently. See [events evidence](#source-register).
3. Resolve routes to absent catalog entries: `securing-agentforce` from regulated review, `platform-metadata-api-context-get` from custom-object generation, and `datakit_workflow` / `datakit_validation` from Data 360 schema guidance. Redirect to a verified owner or declare the missing capability explicitly; don't create placeholder skills just to satisfy links.
4. Extend CI beyond packaging, metadata and root tests to include appropriate existing skill-local suites and route-target validation. Existing tests are valuable; passing them does not validate all product guidance or live org behavior.

These findings were backlog items at assessment time; their implementation status is recorded above.

## Proposed build queue

Wave 1 is the next five skills. Access and governance are prerequisites to enabling production data consumption; ingestion/modeling and query work can use synthetic fixtures before those controls are deployed. Wave 2 follows validated foundations. Wave 3 is demand-driven.

| Wave | Proposed skill | Treatment | Deliverable | Existing coverage / gap | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | `salesforce-access-design` | New | Permission sets/groups, field and record access; produce an access matrix and metadata drafts. | Security guidance is scattered; no dedicated access-design owner. | Positive and denied-access cases for each persona; explain additive grants. [Docs](https://help.salesforce.com/s/articleView?id=platform.perm_set_groups.htm&release=264.0.0&type=5) |
| 1 | `data360-ingestion-modeling` | New | Choose ingestion versus federation; define source keys, refresh, DLO-to-DMO mappings and reconciliation. | data360-schema-get inventories schema; it does not build pipelines. | Schema/key validation, rejected-record handling, source-to-target reconciliation. [Docs](https://help.salesforce.com/s/articleView?id=data.c360_a_data_ingestion.htm&release=264.0.0&type=5) |
| 1 | `data360-query-insights` | New | Data 360 SQL and calculated insights with explicit grain, joins, measures and dimensions. | Core SOQL and CRM Analytics are different query/model systems. | Known-result fixtures; duplicate joins, nulls and aggregation; target API and pagination checks. [Docs](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_calculated_insights_sql_function.htm&release=264.0.0&type=5) |
| 1 | `data360-governance` | New | Data-space and policy design, masking and consent inputs, retention requirements and access evidence. | Existing guidance flags governance but does not own an end-to-end workflow. | Test allowed and denied consumption paths; distinguish metadata visibility from query access. [Docs](https://help.salesforce.com/s/articleView?id=data.c360_a_policy_enforcement_in_datacloud.htm&release=264.0.0&type=5) |
| 1 | `agentforce-grounding` | Extract + extend | Own library/source/index/retriever configuration and retrieval-quality evaluation. | Reuse the substantial agentforce-generate data-library reference; avoid a second competing owner. | Relevant, irrelevant, stale, no-answer and unauthorized-content cases. [Docs](https://help.salesforce.com/s/articleView?id=ai.data_library_custom_retriever.htm&release=264.0.0&type=5) |
| 2 | `data360-identity-resolution` | New | Match and reconciliation rules, unified-profile lineage and review metrics. | Schema inspection and trace analysis do not configure identity resolution. | False-merge and false-split fixtures; prove reconciliation leaves source records unchanged. [Docs](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_ruleset.htm&release=264.0.0&type=5) |
| 2 | `data360-segmentation-activation` | New | Audience definition, contact points, consent filters, target mappings and activation preview. | No complete audience-to-destination workflow. | Opt-out exclusions, membership/count checks, target mapping and authorized activation evidence. [Docs](https://help.salesforce.com/s/articleView?id=data.c360_a_create_data_cloud_activation.htm&release=264.0.0&type=5) |
| 2 | `prompt-template-build` | New | Create, ground, compare, version and test Prompt Builder templates. | Existing action-prompt-templates reference mainly consumes already-active templates. | Regression examples and version comparisons; activation recorded separately from drafts. [Docs](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_use_multiple_versions.htm&release=264.0.0&type=5) |
| 2 | `agentforce-api-integrate` | New | Authentication plus session creation, messages/streaming, feedback and session end. | General integrations do not provide the Agent API lifecycle workflow. | Mock protocol tests, expired auth/session, stream interruption and authorized sandbox smoke test. [Docs](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-lifecycle.html) |
| 3 | `salesforce-solution-design` | New, when needed | Cross-platform architecture decisions, reliability, security, operations and cost trade-offs. | agent-architecture focuses on agents; this would coordinate platform-wide decisions. | Trace requirements to decisions and delegate implementation to existing skills. [Docs](https://architect.salesforce.com/docs/architect/well-architected/guide/framework.html) |

### Dependencies and boundaries

- Ingestion/modeling reuses `data360-schema-get`; it must discover connector and federation support rather than assume one universal provisioning API.
- Identity resolution follows source mapping and governance. Match rules group profiles; reconciliation chooses field values. These are separate decisions.
- Segmentation/activation depends on modeled data, governance/consent, and identity or calculated insights only where the use case requires them. Consent filters must be explicit; do not assume activation automatically enforces every preference.
- Grounding reuses existing library material and delegates agent generation and agent tests. The documented Answer Questions with Knowledge custom-retriever path supports static prefilters; do not assume dynamic filters work on that path.
- Prompt templates own their creation/version lifecycle; agent generation retains action binding. An activated template version cannot simply be edited in place.
- Agent API integration reuses OAuth and general integration guidance, but owns the session lifecycle. Verify current endpoint and channel support before coding.
- Access design owns core CRM access; Data 360 governance owns its data-space/policy consumption model. Neither may claim regulatory certification or silently grant access.
- Solution design produces decisions and delegates execution. Avoid an all-Salesforce mega-skill that repeats every specialized workflow.

## Extend existing skills instead of adding duplicates

| Existing owner | Extension | Why reuse it |
| --- | --- | --- |
| `integration-connectivity-generate` | Repair event guidance; validate subscriber checkpoints, recovery, idempotency and failure handling. | Already covers REST/SOAP, credentials, events and CDC. |
| `agentforce-test` and `agentforce-escalation-test-generator` | Add grounding, authorization, handoff and failure regression cases to existing test workflows. | Test authoring and execution already have owners. |
| `platform-metadata-deploy` | Add verified component dependencies and Data 360 deployment checks where officially supported. | Existing release owner; don't imply every resource is deployable through Metadata API. |
| `agentforce-observe` / `agentforce-d360-analyze` | Connect test outcomes to quality, latency and cost evidence where available. | Observability exists; improve its evidence rather than create another generic monitor. |

## Later coverage, driven by actual projects

| Area | Candidate gap | Research boundary |
| --- | --- | --- |
| Service routing and channels | Configure Omni-Channel routing to agents and human handoff; existing escalation tests don't own configuration. | Routing documentation sampled; full channel lifecycle needs further discovery. |
| Knowledge lifecycle | Article taxonomy, visibility, publishing and maintenance upstream of grounding. | Category assignment/visibility verified; lifecycle implementation research still needed. |
| Experience Cloud | Site membership, guest access, authentication and sharing. | Site-security overview verified; LWC generation is not site administration. |
| Sales lifecycle | Lead conversion mapping and related business process configuration. | Conversion mapping sampled; broader opportunity/forecasting scope not yet assessed. |
| Marketing, Commerce, Industries, MuleSoft, Slack | Discover concrete frequent workflows before selecting skills. | Not deeply assessed; do not label these fully specified gaps or claim complete coverage. |

## Definition of done for every new or extracted skill

- Clear trigger and exclusions, with positive and negative routing examples against adjacent skills.
- One owner per workflow, small entrypoint and focused references; shared content maintained from a canonical source.
- Required inputs, tool discovery, environment/release checks, durable output and explicit next handoff.
- Official source URLs and verification date; mutable limits and commands verified at task time.
- Tests for useful output and failure behavior, including missing tools, denied access and malformed or partial data; not just frontmatter tests.
- Sandbox acceptance with synthetic data and authorized operations. Report offline checks separately from live Salesforce evidence.
- Data mutations, publication and destination activation stay within the user's authorization. A review or draft alone does not authorize them.

Build one workflow end to end, run routing and acceptance cases, then advance the queue. The assessment itself made no org changes; subsequent skill implementation is recorded above.

## Source register

Selected official pages fetched through the MCP. Product-specific scope and test requirements above include our design recommendations, not claims that the documentation supplies an automated implementation.

- **access**: [Permission Set Groups](https://help.salesforce.com/s/articleView?id=platform.perm_set_groups.htm&release=264.0.0&type=5) — `platform/264-0-0/perm_set_groups.html`.
- **ingestion-detail**: [Connect Data](https://help.salesforce.com/s/articleView?id=data.c360_a_data_ingestion.htm&release=264.0.0&type=5) — `data/264-0-0/c360_a_data_ingestion.html`.
- **calculated**: [Use SQL to Create Insights](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_calculated_insights_sql_function.htm&release=264.0.0&type=5) — `data/264-0-0/c360_a_create_a_calculated_insights_sql_function.html`.
- **data-governance**: [Policy Enforcement in Data 360](https://help.salesforce.com/s/articleView?id=data.c360_a_policy_enforcement_in_datacloud.htm&release=264.0.0&type=5) — `data/264-0-0/c360_a_policy_enforcement_in_datacloud.html`.
- **grounding-detail**: [Use a Custom Retriever](https://help.salesforce.com/s/articleView?id=ai.data_library_custom_retriever.htm&release=264.0.0&type=5) — `ai/264-0-0/data_library_custom_retriever.html`.
- **identity**: [Identity Resolution Rulesets](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_ruleset.htm&release=264.0.0&type=5) — `data/264-0-0/c360_a_identity_resolution_ruleset.html`.
- **activation**: [Create an Activation for a Data 360 Target](https://help.salesforce.com/s/articleView?id=data.c360_a_create_data_cloud_activation.htm&release=264.0.0&type=5) — `data/264-0-0/c360_a_create_data_cloud_activation.html`.
- **consent**: [Using Consent Preferences in Segmentation](https://help.salesforce.com/s/articleView?id=data.c360_a_using_consent_preferences_in_segmentation.htm&release=264.0.0&type=5) — `data/264-0-0/c360_a_using_consent_preferences_in_segmentation.html`.
- **prompts**: [Use Multiple Versions of a Prompt Template](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_use_multiple_versions.htm&release=264.0.0&type=5) — `ai/264-0-0/prompt_builder_use_multiple_versions.html`.
- **agent-api-detail**: [Agent API Session Lifecycle](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-api-lifecycle.html) — `genai/agentforce/guides/agentforce/agent-api/agent-api-lifecycle.html`.
- **events**: [Event Message Durability](https://developer.salesforce.com/docs/platform/pub-sub-api/guide/event-message-durability.html) — `event-bus/pub-sub-api/guides/event-message-durability.html`.
- **service**: [Route to an Agentforce Service Agent](https://help.salesforce.com/s/articleView?id=service.omnichannel_route_to_ai_agent_target.htm&release=264.0.0&type=5) — `service/264-0-0/omnichannel_route_to_ai_agent_target.html`.
- **solution**: [Well-Architected Framework](https://architect.salesforce.com/docs/architect/well-architected/guide/framework.html) — `well-architected/guides/framework.html`.
- **knowledge**: [Modify Default Category Group Assignments for Articles](https://help.salesforce.com/s/articleView?id=service.knowledge_category_assignment.htm&release=264.0.0&type=5) — `service/264-0-0/knowledge_category_assignment.html`.
- **sales**: [Lead Conversion Field Mapping](https://help.salesforce.com/s/articleView?id=sales.lead_conversion_mapping.htm&release=264.0.0&type=5) — `sales/264-0-0/lead_conversion_mapping.html`.
- **experience**: [Secure Your Experience Cloud Site](https://help.salesforce.com/s/articleView?id=experience.networks_security.htm&release=264.0.0&type=5) — `experience/264-0-0/networks_security.html`.
