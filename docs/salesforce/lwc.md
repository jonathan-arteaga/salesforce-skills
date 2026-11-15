# Lwc guidance

- Prefer Lightning Data Service/UI API for supported record operations; it handles sharing, CRUD, and FLS. Apex controllers also require class access and explicit data-access enforcement.
- Use USER_MODE in reusable Apex examples; WITH SECURITY_ENFORCED cannot compile at API 67+. Sanitize user-facing errors and do not log secrets or record payloads. Test unauthorized and guest access as relevant.
- Confirm target API version and release status before adopting template, TypeScript, GraphQL, or other newer features. Jest verifies client behavior; it does not certify server permissions or an Experience Cloud deployment.

## Sources checked 2026-11-15

- [Secure Apex Classes](https://developer.salesforce.com/docs/platform/lwc/guide/apex-security.html)
