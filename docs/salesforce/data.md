# Data guidance

- Data 360 is the current product name; Data Cloud remains in API identifiers, permissions, and older UI. Preserve actual names rather than mechanically renaming code.
- Distinguish DLO ingestion, DMO harmonization, unified DMOs from identity resolution, and calculated insights. Discover actual schema, mapping, keys, and types; do not infer successful identity resolution or usable grounding from object existence.
- Resolve the intended org and data space from evidence. An access error must not trigger a silent fallback to default. Data space permissions and governance policies are separate checks; avoid broad grants merely to make a query pass.
- Use the selected API family and its own pagination contract. Connect metadata collections use nextPageUrl/limit/offset; Query V2 uses done and nextBatchId. Do not mix those with core REST nextRecordsUrl. Query V2 has a newer successor: check current guidance before new implementations.
- For retained Query V2 implementations, fetch batches until done, within one hour overall and less than three minutes between batches. Record truncated or incomplete results honestly. Discover SQL fields from metadata; core SOQL and Data 360 SQL are not interchangeable.

## Sources checked 2026-11-15

- [Object Model in Data 360](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-object-model.html)
- [Secure Your Data with Data Spaces](https://help.salesforce.com/s/articleView?id=data.c360_a_data_spaces_secure_data.htm&release=264.0.0&type=5)
- [Data 360 Connect API](https://developer.salesforce.com/docs/data/connectapi/references/spec)
- [Request Data With Query V2](https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/data-cloud-query-api-reference/c360a-api-query-v2.html)
