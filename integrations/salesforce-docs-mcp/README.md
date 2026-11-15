# Salesforce Docs MCP connection

Private ChatGPT plugin package for the existing remote server documented by [Agentforce Labs](https://labs.agentforce.com/docs/salesforce-docs-mcp). This does not host or impersonate Salesforce and does not connect to a customer's Salesforce org.

- Endpoint: `https://salesforce-docs-76258744c9d7.herokuapp.com/api/mcp`
- Transport: Streamable HTTP
- Authentication: none required by the endpoint during verification on 2026-11-15; no placeholder bearer token is included.
- Tools verified through MCP: `salesforce_docs_search`, `salesforce_docs_fetch`.
- Verified initialization, tools/list, collection discovery, search, and full-page retrieval.
- Private account plugin: [Salesforce Docs MCP](https://chatgpt.com/plugins/plugins_6af9d5f10c808191b3c06bd6097ed244).

Creation was verified through plugin metadata, but its tools did not appear in the active chat. The browser activation page required ChatGPT sign-in. Open the private plugin in the signed-in ChatGPT app to complete any enable/connect step, then select it in a conversation and verify a search. Do not equate package creation with verified host activation.

This connection package lives outside the skills marketplace catalog intentionally. It is a separately saved private plugin, not a 70th marketplace skill entry.
