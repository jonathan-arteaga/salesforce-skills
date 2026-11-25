# Tableau Next Semantic Models & Querying

Distilled operational gates for profiling data, authoring and enriching Tableau Next Semantic Data Models (SDMs), and running semantic queries via `tableau-next-*` MCP tools.

## Universal Gates (G1–G7)

1. **G1 — MCP server required**: Match the advertised `tableau-next-*` tool prefix (never hand-construct names). If no `tableau-next-*` tool is connected, STOP immediately and never fabricate tool responses or IDs.
2. **G2 — Data presence**:
   - For every discovered candidate object, confirm `SELECT COUNT(*) > 0` before binding or charting — field-richness is not data presence.
   - For newly ingested flat-file DLOs (`category: "Other"` on both file DLO and DMO; literal `__c` on both mapping sides), run `run_data_stream` and wait for Active.
   - For self-created DLO-to-DMO mappings, `get_dlo_to_dmo_mapping_status: ACTIVE` is metadata-only; poll `run_query` (`SELECT 1 FROM <dmo>__dlm LIMIT 1`) until `42P01` ("table does not exist") clears (any success, even `COUNT = 0`, means query-ready). Transient `isEnabled: false` right after DMO creation is normal.
3. **G3 — Never invent `apiName`**: Always read stored names back via `list_semantic_model_*` tools. Do NOT use deprecated `shouldIncludeAllFields: true` (it appends unpredictable numeric suffixes like `Region4` and omits descriptions). Bind explicit nested `semanticDimensions[]` / `semanticMeasurements[]` at creation (`shouldIncludeAllFields: false`), including join keys. In relationships, use the semantic `apiName` with `leftFieldType: "TableField"`.
4. **G4 — No island objects**: Whenever an SDM has 2+ objects, every object must join into the graph. Do not set `queryUnrelatedDataObjects: "Exception"` and query unjoined objects.
5. **G5 — AI-readiness & coverage**:
   - Populate `description` on the model, every data object, calculated field, and metric; set `sentiment` on directional measures/metrics; set `businessPreferences` (`update_semantic_model_business_preferences`, full replacement of `# `-prefixed lines); and set `agentEnabled: true` via immediate `update_semantic_model` after creation.
   - `apiName` is permanent after creation — choose descriptive names and eliminate synonyms/homonyms. Note the known server bug: setting `primaryNameField` at create fails; record it as a known gap.
   - On sparse `update_semantic_model_dimension/_measure`, always `list_*` first and echo current `isVisible` and `dataObjectFieldName` (omitting `isVisible` unhides fields; omitting `dataObjectFieldName` fails with `SEMANTIC_FIELD_NOT_VALID`).
6. **G6 — Profile five essentials first**: Before adding metrics or calcs, profile **grain**, **field roles** (numeric IDs are dimensions, not measures), **cardinality**, **additivity** (never sum snapshots across dates), and **date roles** (business event date vs. load timestamp). For wide/cryptic flat files, call `infer_object_schema` first without reading the raw file into context, then verify one known total with `run_query` after ingest.
7. **G7 — Prove with live rows**: Validate new joins and models with `run_semantic_query` before charting. A join returning ~0 rows is broken.

## Enrichment, Metrics & Query Mechanics

| Component | Required Pre-Check | Critical Payload Rule |
| --- | --- | --- |
| Calculated Dimension | `list_semantic_model_calculated_dimensions` | Avoid duplicate coverage of the same source field |
| Calculated Measure | `list_semantic_model_calculated_measures` + `_metrics` | Use `aggregationType: "UserAgg"` when formula already aggregates (`AVG`, `COUNTD`) |
| Metric | `list_semantic_model_metrics` | Concrete `aggregationType` (NEVER `Auto`); numeric field + `Count` (not PK); full-PUT `insightsSettings` on update |

- **`run_semantic_query` proto shape**: Request bodies MUST use **snake_case proto keys** (camelCase REST examples fail). Prefer querying existing metrics or calculated measures over inline aggregations:

```json
{
  "semantic_model_name": "<sdm_api_name>",
  "fields": [{ "table_field": { "data_object_name": "<obj>", "field_name": "<dim>" } }],
  "measures": [{ "table_field": { "data_object_name": "<obj>", "field_name": "<meas>" }, "semantic_aggregation_method": "SUM" }]
}
```

- **No-dispatch boundary**: Decline pure prose copy-editing of existing descriptions (when no field, join, metric, or grain changes) and non-build advice/ideation. Keep read-only figures (`run_semantic_query`) and interpretive breakdowns (`analyze_data`) in scope without pinning an unnamed SDM.
- **Query vs. Analyze vs. Verified Questions**:

| User Intent | Correct Tool / Path | Guardrail |
| --- | --- | --- |
| Scalar, total, or structured table on an SDM | `run_semantic_query` (snake_case proto) | Discover unnamed SDM via `list_semantic_models` first |
| Raw DLO/DMO SQL when no SDM exists | `run_query` | Prefer `run_semantic_query` whenever a populated SDM covers the data |
| Interpretive ranking, trend, or "why" question | `analyze_data` | Do not pin `targetEntityNameOrId` unless user named an SDM |
| Score agent SQL against golden Q&A | `run_regression_evaluator` | Read-only evaluation; persists nothing |

- **AI readiness verification**: Do not declare a model AI-ready on metadata completeness alone; recommend running the Semantic Model AI Optimization similarity scan in UI (`modelHealth`).
