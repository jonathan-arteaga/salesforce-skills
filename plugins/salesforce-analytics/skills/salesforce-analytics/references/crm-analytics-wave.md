# CRM Analytics (Wave) Recipes, Datasets & Dashboards

End-to-end SFDX + REST authoring workflow for CRM Analytics apps (`.wapp`), R3 recipes (`.wdpr`), datasets (`InsightsExternalData`), SAQL, and grid dashboards (`.wdash`).

## Wave R3 Recipe Rules (`.wdpr` + `.wdpr-meta.xml`)

- **Paired metadata files**: Always pair every `.wdpr` with `.wdpr-meta.xml` (required tags: `<application>`, `<masterLabel>`, `<targetDatasetAlias>`, `<dataflow>` matching dataset alias; omit `<description>`, `<label>`, `<accessType>`, `<shareType>`, `<format>`). Same pairing applies to `.wapp` and `.wdash`.
- **Top-level `.wdpr` shape**: Contains ONLY `runMode` (`"full"` default, `"incremental"`, or `"streaming"` — NEVER `"R3"`), `nodes` (root-level map with UPPERCASE keys, never inside `ui`), and `ui` (Designer-native dict, not array). Do NOT wrap in an API envelope.
- **Node & formula gotchas**: Use `sources` (array), one field per `formula` node (chain sequentially; multiple fields break Recipe Designer), action `"formula"`, keys `"fields"` and `"formulaExpression"` with `expressionType: "SQL"` and `type: "NUMBER"` or `"TEXT"` (no backticks around field names). Derive date dimensions with `date_format(field, 'yyyy')` or `'MM/yyyy'` (`'MMM'` outputs numeric month). Insert an `extractGrains` node before `aggregate`.
- **Compile & execute via REST**: Always POST or PATCH recipes as JSON body at `/wave/recipes?format=R3` (never multipart — multipart leaves `targetDataflowId` null or triggers `tableModelInfo is null`; fix via DELETE + re-POST). Trigger execution on `/wave/dataflowjobs` using `targetDataflowId` (`02K...`), never the recipe ID (`05v...`). On `Failure`, run `check_connector_error.sh`: exit 0 (`System`) is safe to retry (`POST /wave/dataConnectors/{id}/ingest`); exit 1 (`User`/`Limit`) requires fixing config first.

## Dashboard Deploy + PATCH & SAQL Re-Encoding Trap

- **Two-step authoring**: Deploy minimal `.wdash` (root contains ONLY `state`; `dataSourceLinksInfo: {}`; `numColumns: 24`; gridLayout entries use `column` not `col` and omit `type`; SAQL steps omit `isGlobal`, `receiveFacet`, `datasets`, `label`) via `sf project deploy start` (`POST /wave/dashboards` only creates retired classic dashboards), then apply styling via `PATCH /wave/dashboards/{id}`.
- **Mandatory `decodeAll` before PATCH**: GET returns HTML-encoded SAQL (`"` -> `&quot;`). PATCHing without decoding double-encodes (`&amp;quot;`) and breaks every widget with Error 119. Always decode every `state.steps[*].query` immediately after GET:

```javascript
function decodeAll(s) {
  let prev = null;
  while (prev !== s) {
    prev = s;
    s = s.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
  }
  return s;
}
```

- **Widget styling limits**: `widgetStyle.borderRadius` must be an integer (`8`, not `"8px"`). `valuestable` rejects styling at PATCH — use `chart` with `visualizationType: "flatTable"`. On `listselector` with dark themes, set `filterStyle.valueColor` explicitly.
- **SAQL storage & KPI totals**: Store name-based loads (`q = load "MyDataset";`), never `id/versionId` (rejected by PATCH). When testing via `/wave/query`, swap dataset name for `datasetId/currentVersionId`. KPI totals MUST run `group q by all;` before `foreach` (otherwise `foreach` returns one row per source row):

```sql
q = load "MyDataset";
q = group q by all;
q = foreach q generate sum('TotalRevenue') as 'TotalRevenue';
```

- **Non-faceted selector bindings**: Put `{{column(step_sel.selection, ["Industry"]).asEquality("Account.Industry")}}` in the target SAQL step and set `broadcastFacet` and `useGlobal` to `false` on both steps.

## Bundled Deterministic Scripts (Black-Box CLI)

All scripts live in `scripts/`, accept `<org_alias>` as arg 1, and authenticate via `sf org display`:

| Script | CLI Usage | Purpose |
| --- | --- | --- |
| `create_app.js` | `node scripts/create_app.js <alias> <appName>` | Idempotently create CRMA app folder (no `assetIcon`) |
| `deploy_and_run_recipe.js` | `node scripts/deploy_and_run_recipe.js <alias> <file.wdpr> <app> <name>` | Upsert R3 recipe, assert `targetDataflowId`, run & poll job |
| `probe_recipe.js` | `node scripts/probe_recipe.js <alias> <recipeId>` | Check R3 compile status and `targetDataflowId` |
| `check_connector_error.sh` | `bash scripts/check_connector_error.sh <alias> <connectorId>` | Exit 0 = retryable `System` error; exit 1 = `User`/`Limit` |
| `fetch_dataset_xmd.js` / `gen_synthetic_dataset.js` | `node scripts/<script> <alias> <datasetName>` | Dump live XMD or generate schema-matched synthetic CSV + metadata |
| `upload_dataset.js` / `verify_synthetic_dataset.js` | `node scripts/upload_dataset.js <alias> <csv> <meta> <name> <folderId>` | Upload via `InsightsExternalData` (wait for `Status=Completed`) & SAQL-check |
| `verify_dashboard_steps.js` / `patch_t_oppo_view.js` | `node scripts/<script> <alias>` | Decode + `/wave/query` verify every step (edit `DASH_ID`/`DS`), or PATCH template |
| `find_unused_dataset_fields.js` | `node scripts/find_unused_dataset_fields.js <alias> <datasetName>` | Audit XMD fields unreferenced by dashboard SAQL |
