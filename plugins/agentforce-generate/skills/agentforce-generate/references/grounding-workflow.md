# Grounding diagnosis

| Observation | Check next | Avoid |
| --- | --- | --- |
| No relevant chunks | Source inclusion, permissions, index readiness, language, filters and query | Prompt-only repairs for missing indexed content |
| Relevant chunks, unsupported answer | Action binding, prompt/context handling and answer evidence | Assuming retrieval success proves answer quality |
| Old answer | Source version, processing state, duplicate/conflicting content and freshness window | Treating an upload response as completed indexing |
| Cross-customer content | Effective retrieval identity and authorization boundaries | Relying only on prompt instructions or topic filters |
| Intermittent failures | Status, limits, retry details and request IDs | Deleting the library as a first retry |

Separate retrieval and answer evaluation. For each question retain source IDs/version, expected supporting evidence, actual retrieved evidence when exposed, answer, identity and pass/fail reason. Define acceptable behavior for no evidence before testing. Include hostile instructions embedded in a source document and verify they do not override the task or authorization.

Custom retriever readiness includes an active retriever and its supported search index configuration. For the reviewed Answer Questions with Knowledge path, only static prefilters are supported; dynamic user filtering needs a separately verified architecture, potentially a custom action. Do not infer per-user authorization from a filter alone.

Primary sources reviewed 2026-11-15: [Agentforce Data](https://help.salesforce.com/s/articleView?id=ai.agent_parent_data.htm&release=264.0.0&type=5); [Custom Retriever Data Library](https://help.salesforce.com/s/articleView?id=ai.data_library_custom_retriever.htm&release=264.0.0&type=5).

## Cross-audience regression

Use a synthetic public article and restricted article, then run the same question as authorized, unauthorized and elevated identities. Check retrieved chunks when available, citations and answer text. Missing retrieval traces remain unknown, not a pass. Capture source and agent versions. If chunks exist but an answer fails, test retriever readiness and actual agent-side access separately before changing source content.
