# Query correctness decisions

Define grain in one sentence, such as one row per customer per calendar month in the agreed timezone. Write expected rows before SQL. Avoid copying field names from documentation into the user's schema without verification.

A join example: two orders for customer A worth 10 and 20 joined to three contact points yields six joined rows and a naive SUM of 90. The intended customer total is 30. Aggregate orders at customer grain before joining contact points, or choose one contact point with a business rule; DISTINCT on amounts would fail when two legitimate orders have the same amount.

For each expression, document null and empty-set semantics. For each time filter, specify inclusive/exclusive boundaries and timestamp timezone. Check supported SQL functions against the current target API. A saved insight's dimensions determine its grain; adding a dimension changes the result, not just its display.

For segmentation use, verify the relevant primary-key dimension and supported relationships. Do not assume every ad hoc SQL feature is available in a calculated insight. Keep query completion, full result retrieval and result correctness as three separate checks.

Primary source: [Create a Calculated Insight with SQL](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_calculated_insights_sql_function.htm&release=264.0.0&type=5), reviewed 2026-11-15.

## Execution state and engine

Identify Data 360 SQL versus Legacy SQL for the actual insight; current creation options can differ from older examples. Test whitespace, types and nulls in that engine. Query Editor success is not proof of insight deployment or scheduling. Track request acceptance, component creation, active status, successful run, full output and schedule verification separately. Poll with a bounded deadline and preserve async error/correlation IDs. Do not delete/recreate an insight as an automatic workaround.

## Fully qualified keys

Inspect key qualifiers as well as record IDs. Where Data 360 uses fully qualified keys, join on both the ID and its key-qualifier columns; an ID alone can collide across sources. Do not guess the qualifier field name on another object or replace a platform key qualifier with arbitrary string concatenation. Validate the actual schema and relationship mapping. Include a fixture with identical IDs in different sources and prove they remain distinct.

Source: [Write a Simple Query](https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/write-simple-query.html), fetched 2026-11-15.
