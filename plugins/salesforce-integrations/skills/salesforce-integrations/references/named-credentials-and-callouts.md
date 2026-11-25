# Enhanced Named Credentials, External Services, and Callouts

## Enhanced Named Credentials + External Credentials

Use the enhanced **Named Credential + External Credential** architecture for all outbound authentication (never legacy hardcoded credentials or Remote Site Settings with raw API keys in Apex/Custom Metadata):

1. **External Credential (`.externalCredential-meta.xml`)**: Defines the auth protocol (OAuth 2.0, JWT Bearer, AWS SigV4, Custom Auth headers/formulas) and one or more **Principals** (`NamedPrincipal` for org-wide service identity or `PerUserPrincipal` for per-user OAuth).
2. **Named Credential (`.namedCredential-meta.xml`)**: Binds the base endpoint URL, references the External Credential, and controls `generateAuthorizationHeader` / custom formula headers (e.g., `{!$Credential.ExtCredName.ApiKey}`).
3. **Permission Set + User External Credentials mapping**:
   - Grant the External Credential Principal access on a least-privilege **Permission Set** (`<externalCredentialPrincipalAccesses>`).
   - Enable **Read** on the **`User External Credentials`** standard object on that Permission Set (required for runtime credential resolution by non-admin users).
4. **Secret injection**: Populate sensitive API keys/client secrets post-deploy via `bash scripts/configure-named-credential.sh <extCred> <principal> <alias>` (uses `ConnectApi.NamedCredentials`) or Setup UI — never commit secret values into XML or shell history.

## Outbound Callout & External Service Patterns

| Requirement | Recommended Pattern | Key Safeguards |
| --- | --- | --- |
| OpenAPI 2.0 / 3.0 REST API | **External Service** (`.externalServiceRegistration-meta.xml`) + Named Credential | Declarative Flow + typed Apex `ExternalService.*` classes; verify schema compatibility |
| Sync UI-triggered REST call | Apex `Http` + `callout:NamedCred/path` (or Continuation if slow) | Explicit timeout (`req.setTimeout(12000)`), check status codes, sanitize errors |
| Trigger-originated outbound sync | **Queueable** implementing `Database.AllowsCallouts` + `System.Finalizer` | Never execute sync callouts from triggers; guard against uncommitted DML before callout |
| High-volume / flaky downstream | Queueable + exponential backoff + **idempotency key** + dead-letter log | Cap retry count; persist correlation ID, redacted status, and payload hash on final failure |
| Legacy WSDL SOAP endpoint | `wsdl2apex` + Named Credential (`callout:NamedCred`) | Isolate generated stubs behind a thin service adapter; enforce explicit timeouts |
| Browser/LWC direct asset/API | **CSP Trusted Site** (`.cspTrustedSite-meta.xml`) | Scope exact origin and directives; prefer server-side Apex/Named Credential for authenticated APIs |

## Callout Resilience & Operational Checklist

- **Timeouts & governor limits**: Total callout time per transaction is 120 seconds (max 100 callouts; 6 MB sync / 12 MB async heap). Set explicit per-request timeouts (`10–30 s`) so slow endpoints fail fast instead of exhausting concurrent long-running request limits (max 10 calls over 5 seconds).
- **Uncommitted work rule**: Never perform DML before an HTTP callout in the same transaction. Commit first or enqueue a Queueable job (`Database.AllowsCallouts`) to execute the callout cleanly.
- **Retry & idempotency**: Retry only transient errors (`429`, `502`, `503`, `504`, network timeouts) with `Retry-After` awareness. Never auto-retry non-idempotent `POST` mutations unless the downstream supports an explicit idempotency key.
- **Redacted observability**: Log endpoint path, HTTP status, latency, and correlation ID to a structured log object — never log `Authorization` headers, tokens, or unmasked PII.

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint('callout:MyNamedCredential/v1/orders');
req.setMethod('POST');
req.setTimeout(15000);
req.setHeader('Idempotency-Key', correlationId);
```

## Deterministic Validation & Script Workflow

```bash
# 1. Validate callout Apex or Named Credential XML against the 120-pt integration rubric
python3 scripts/validate_integration.py force-app/main/default/namedCredentials/MyApi.namedCredential-meta.xml
python3 scripts/validate_integration.py force-app/main/default/classes/MyApiCallout.cls

# 2. Deploy metadata first, then inject runtime credential secrets via ConnectApi
bash scripts/configure-named-credential.sh MyExternalCred MyPrincipal <org-alias>
```

- Resolve security or bulkification deductions from `validate_integration.py` (target 108+/120) before org deployment.
