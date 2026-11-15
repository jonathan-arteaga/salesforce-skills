# Integration guidance

- Prefer External Client Apps for new integrations, including simple single-org apps. Connected App creation is restricted as of Spring 26; existing apps continue to work, and unavoidable new creation requires Salesforce Support eligibility.
- Use minimum OAuth scopes, exact callbacks, PKCE for public clients, and a suitable server-to-server flow for confidential clients. Preserve existing integrations while testing a migration; do not revoke working credentials prematurely.
- Use enhanced Named Credentials with External Credentials for outbound authentication. Map principals to least-privilege permission sets and configure User External Credentials access where required. Keep tokens and secrets out of source and tool output.
- Confirm endpoint availability, action schema, authentication, API version, retry/idempotency behavior, and permission boundaries. A documentation MCP is read-only documentation access, not a Salesforce org connector.

## Sources checked 2026-11-15

- [ConnectedApp](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_connectedapp.htm)
- [Create Named Credentials and External Credentials](https://help.salesforce.com/s/articleView?id=xcloud.nc_named_creds_and_ext_creds.htm&release=264.0.0&type=5)
- [Enable User External Credentials](https://help.salesforce.com/s/articleView?id=xcloud.nc_user_external_credentials.htm&release=264.0.0&type=5)
