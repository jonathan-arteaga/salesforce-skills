# Data 360 Schema Inspection

Use the bundled CLI scripts under `scripts/` to enumerate and inspect Data Lake Objects (DLOs) and Data Model Objects (DMOs) via the SSOT REST API.

## Prerequisites & Auth Safety

1. Discover connected orgs with `sf org list` and confirm the exact `<org_alias>` and stable Org ID. Never silently default to the first connected org.
2. Let `scripts/schema_client.py` invoke `sf org display` internally. Never print raw `sf org display --json` output because it contains `accessToken`.
3. If unauthenticated, instruct the user to run `sf org login web --alias <org_alias>`.

## CLI Invocation

Run commands relative to this skill directory:

```bash
python3 ./scripts/get_dlo_schema.py <org_alias>
python3 ./scripts/get_dlo_schema.py <org_alias> Employee__dll
python3 ./scripts/get_dmo_schema.py <org_alias>
python3 ./scripts/get_dmo_schema.py <org_alias> Individual__dlm --api-version v66.0
```

## SSOT Endpoints & Pagination Contract

| Operation | Endpoint | Collection Key |
| --- | --- | --- |
| List all DLOs | `GET /services/data/{ver}/ssot/data-lake-objects` | `dataLakeObjects` |
| Get one DLO | `GET /services/data/{ver}/ssot/data-lake-objects/{dlo_name}` | `dataLakeObjects` |
| List all DMOs | `GET /services/data/{ver}/ssot/data-model-objects` | `dataModelObjects` |
| Get one DMO | `GET /services/data/{ver}/ssot/data-model-objects/{dmo_name}` | `dataModelObjects` |

- **Pagination**: Connect/SSOT metadata endpoints paginate with `nextPageUrl` / `limit` / `offset` — never mix this contract with Query V2 (`nextBatchId`) or Core REST (`nextRecordsUrl`).
- **API version**: Scripts default to `v64.0`. Verify the org API version and pass `--api-version vNN.0` when needed.
- **Data Space limits**: List endpoints enumerate objects visible to the executing user and do not apply a server-side Data Space filter. Permission-limited visibility is not proof of a complete org inventory, and metadata visibility does not prove query-time row access.

## Presentation & Field Hygiene

When formatting output for the user:

1. **Inventory lists**: Display API name, label, category (`Profile`, `Engagement`, `Other`), ID, total count, and non-zero `totalRecords` (for DLOs).
2. **Object schemas**: Show status, category, Data Space metadata (if present), and separate custom/business fields from platform system fields (`DataSource__c`, `InternalOrganization__c`, `KQ_*`, `cdp_sys_*`).
3. **Keys & types**: Call out primary key flags, key qualifier (`KQ_*`) columns, data types, and nullable flags verbatim from metadata. Never infer field names or suffixes without metadata proof.

## Common Error Handling

| Error | Likely Cause | Action |
| --- | --- | --- |
| Org not connected | Missing or expired SF CLI auth | Run `sf org login web --alias <org_alias>` |
| Object not found (404) | Wrong developer name or missing `__dll`/`__dlm` | Run list mode first to copy exact API name |
| HTTP 403 Forbidden | Missing Data Cloud permission or Data Space grant | Stop and route to `data360-activation-governance`; do not switch Data Spaces |
| API version mismatch | Org requires newer SSOT version | Re-run with `--api-version vNN.0` |
