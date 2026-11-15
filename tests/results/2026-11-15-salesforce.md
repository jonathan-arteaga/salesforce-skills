# Salesforce domain review validation — 2026-11-15

Base: merged main `70275758de3f37c3c9762ecb9daa76edd8ff0781`.

| Check | Observed result |
| --- | --- |
| Official Docs MCP | Initialization, tool discovery, collection discovery, search, and fetch worked through the documented endpoint. |
| Marketplace | 69 entries; generated copies, Markdown links, and private voice-profile checksum passed. |
| Metadata | 73 packaged skills / 67 unique names passed repository validation and OpenAI basic skill validation. |
| Unit tests | 26 passed: existing metadata/routing tests, 14 schema-client tests, and 2 guidance/package regressions. |
| Existing persona suite | 164 passed. |
| Independent skill task: configuration review | Identified missing verified-customer scoping, invalid masking assumption, recording notice gap, unresolved 403, and unauthorized helper deployment. Preserved static-only scope. |
| Independent skill task: integration and selector | Selected ECA for new single-org integration; produced a bound USER_MODE selector for API 68; distinguished draft metadata from an authenticated, deployed integration. |
| Diff whitespace | Passed. |

The schema tests exercise multi-page DMO and DLO inventories, offset fallback, short terminal pages, malformed responses, repeated pages/identities, incomplete totals, endpoint changes, cross-origin/non-HTTPS requests, redirect refusal, redacted HTTP/auth failures, and named-object CLI routing with an explicit API version. Tests use synthetic responses; no actual Salesforce credentials or customer data were used.

The two independent task contexts received only relevant skill directories and synthetic user requests, not the expected outcomes or audit findings. They made no external calls or mutations. Their output relied on the dated local documentation baseline and explicitly left live verification pending. These are two qualitative forward tests, not a complete statistical skill evaluation.

No live Salesforce org, Apex compiler, deployed Flow, Data 360 instance, OAuth application, or voice call was tested. The private Docs MCP plugin was saved, but host activation remains unverified because its tools did not appear in this chat and browser activation required sign-in. Direct MCP access verified the server independently.
