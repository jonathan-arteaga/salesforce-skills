# Salesforce skills documentation baseline

Reviewed on **2026-11-15**, against main `70275758de3f37c3c9762ecb9daa76edd8ff0781`.

The review inspected all 34 Salesforce/Agentforce skill entrypoints and selected high-risk references, scripts, and templates. It used 33 successful search result sets and 52 fetched documents from the [Salesforce Docs MCP published by Agentforce Labs](https://labs.agentforce.com/docs/salesforce-docs-mcp). The maintained baseline cites 27 distinct official pages in [manifest.json](manifest.json). This is a targeted review, not exhaustive certification of every reference or Salesforce product.

## Corrections

| Area | Change |
| --- | --- |
| Apex and LWC | Replace retired `WITH SECURITY_ENFORCED` in reusable examples; document API 67+ behavior, explicit security modes, and target-version checks. |
| Agentforce actions | Correct the claim that missing CRUD/FLS silently returns zero rows; distinguish permission errors from record visibility and filters. Use bound dynamic queries without an unsupported blanket parser-error claim. |
| Agent identity | Distinguish Employee, Service, channel, and credential-verification execution contexts. Verify customer authorization in backing actions. |
| OAuth | Prefer External Client Apps for new integrations, including simple single-org apps; retain existing Connected App compatibility and explain creation restrictions. |
| Voice | Replace “recording is always N/A” with configuration-specific recording and participant notice/consent checks. |
| Trust Layer | Remove a contradictory case-input masking recommendation; distinguish disabled Agentforce LLM masking from separately configured trace/transcript controls. |
| Observability | Do not switch to the default data space after an access failure; distinguish missing data from failed access. Read-only reviews do not authorize helper deployments, live tests, or agent publication. |
| Agent tests | State sandbox, synthetic-data, credit, mutation, agent-version, and simulated/live evidence boundaries. |
| Flow | Scope the three-step MCP pipeline to its actual connector; allow a documented Metadata API/local draft path with honest validation limits. |
| Data 360 schema | Resolve the intended org, avoid raw authentication output, follow pagination, reject malformed/partial inventories, constrain pagination URLs, disable redirects, bound timeouts, and expose an API-version option. Named-object requests no longer fetch an unrelated full inventory. |
| Analytics and metadata | Add current source-backed checks for row security, data-space governance, asset sharing, schema, and per-component deployment coverage. |

## How the baseline is maintained

Edit the concise domain files here and update their source entries in `manifest.json`. `common.md` describes tool discovery, search/fetch, release/edition checks, and official-documentation fallback. The manifest maps each skill to only the domains it needs.

Run `python scripts/package_marketplace.py` to generate self-contained `references/current-salesforce/guide.md` copies inside the individual plugins. Do not edit those copies directly. CI checks generated copies, source coverage, packaged links, and metadata. The copies are necessary because a standalone installed plugin cannot depend on another package's filesystem.

At task time, agents must still verify the target API version, release, licenses, permissions, schema, and available tools. The Docs MCP collection index reported indexing on November 10, 2026 for the primary collections examined. Documentation versions can be ahead of a particular org. A search excerpt alone is insufficient to establish availability.

## Coverage and remaining gaps

- All 15 Agentforce and 19 Salesforce Platform/Analytics entrypoints receive scoped current-documentation guidance.
- Domain checks cover Agentforce design/generation/review/testing, voice, session analysis/observability, Data 360 schema/query/governance, Apex/SOQL/LWC, Flow, OAuth/callouts, CRM Analytics/Tableau Next, metadata and deployment.
- Data 360 ingestion, mapping, identity resolution, segmentation, activation, and zero-copy implementations are not full dedicated workflows in this repository. Neither are every Sales, Service, Marketing, Commerce, Industries, MuleSoft, or Slack workflow. Use the live docs and target evidence; do not imply the catalog covers all Salesforce products end to end.
- Large legacy references contain target- or field-observation-specific material. Current guidance takes precedence when verified for the task; those references were not all revalidated line by line.
- No live Salesforce org was connected. Apex compilation, Flow deployment, OAuth authentication, Data 360 responses, voice calls, and production behavior remain unverified. Offline mocks are not a substitute for sandbox execution.

See [validation results](../../tests/results/2026-11-15-salesforce.md).

## Expansion roadmap

See [the Salesforce library gap assessment](gap-assessment.md) for prioritized new workflows, extractions, existing-skill extensions, maintenance findings and acceptance criteria. The roadmap is planning work; it does not mean those skills are implemented.

## Implemented expansion

Nine additional skills now cover CRM access, Data 360 ingestion/modeling, queries/insights, governance, identity resolution, segmentation/activation, Agentforce grounding, Prompt Builder versions and Agent API integration. This brings the Salesforce catalog to 43 entrypoints. Read [the practitioner evidence](practitioner-insights.md) for 12 qualitative insights and [the validation report](../../tests/results/2026-11-15-salesforce-expansion.md) for offline evidence and remaining live-org limits.
