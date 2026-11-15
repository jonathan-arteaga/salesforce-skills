# Analytics guidance

- CRM Analytics dataset access grants all dataset rows by default unless row-level security is configured. Validate sharing inheritance and/or security predicates with representative restricted users; dashboard filters are not row security.
- Tableau Next uses multiple layers: licenses/permission sets, Data 360 policies, and asset sharing. Sharing a dashboard or semantic model does not independently prove correct underlying data access.
- Check the metric grain, aggregation, joins, filters, refresh state, and null handling. Test totals and restricted-user results against source evidence before publishing or changing sharing.

## Sources checked 2026-11-15

- [Set Up Dataset Security to Control Access to Rows](https://help.salesforce.com/s/articleView?id=analytics.bi_security_datasets_row_level.htm&release=264.0.0&type=5)
- [Data Governance and Sharing in Tableau Next](https://help.salesforce.com/s/articleView?id=analytics.tua_governance.htm&release=264.0.0&type=5)
