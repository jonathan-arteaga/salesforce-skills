# External Client Apps (ECAs) and OAuth App Configuration

## Spring '26 Rule: External Client Apps First

- **Default for all new integrations**: Build an **External Client App (ECA)**, including for simple single-org integrations. ECAs separate global/local settings, improve secret rotation, and support packaging cleanly.
- **Connected App creation restriction**: As of Spring '26, creating new Connected Apps is restricted by default. Existing Connected Apps continue operating normally. Do not assume an org toggle or Metadata API deployment bypasses this restriction — unavoidable new Connected App creation requires Salesforce Support eligibility.
- **Safe migration**: When migrating a Connected App to an ECA, build and test the new ECA side-by-side and verify token issuance before revoking or rotating existing production credentials.

## OAuth 2.0 Flow Selection

| Client / Use Case | Recommended Flow | Security Requirement |
| --- | --- | --- |
| SPA / mobile / public client | Authorization Code + **PKCE** | Mandatory PKCE (`S256`); no client secret in public client |
| Confidential backend web app | Authorization Code | Server-side secret + exact HTTPS callback URL |
| Server-to-server / CI-CD / Agent API | **JWT Bearer** | X.509 certificate uploaded; pre-authorized Permission Set |
| Service-account M2M (ECA) | **Client Credentials** | Named integration user (`Run As`) with least-privilege Perm Set |
| CLI / headless device | Device Flow | Short-lived codes + explicit user verification |

## ECA Metadata Directory & Exact Suffixes

Detect the active `packageDirectory` from `sfdx-project.json` before writing files. ECA suffixes are strictly abbreviated — using long forms breaks deployment:

| Directory | Metadata Type | Exact Suffix |
| --- | --- | --- |
| `<pkg>/externalClientApps/` | `ExternalClientApplication` | `.eca-meta.xml` |
| `<pkg>/extlClntAppGlobalOauthSets/` | `ExtlClntAppGlobalOauthSettings` | `.ecaGlblOauth-meta.xml` |
| `<pkg>/extlClntAppOauthSettings/` | `ExtlClntAppOauthSettings` | `.ecaOauth-meta.xml` |
| `<pkg>/extlClntAppOauthSecuritySettings/` | `ExtlClntAppOauthSecuritySettings` | `.ecaOauthSecurity-meta.xml` (retrieve-only) |
| `<pkg>/extlClntAppOauthPolicies/` | `ExtlClntAppOauthConfigurablePolicies` | `.ecaOauthPlcy-meta.xml` |
| `<pkg>/extlClntAppPolicies/` | `ExtlClntAppConfigurablePolicies` | `.ecaPlcy-meta.xml` |

- **Retrieve-only security settings**: Never hand-craft `.ecaOauthSecurity-meta.xml` from scratch; retrieve from the org first:
  `sf project retrieve start --metadata ExtlClntAppOauthSecuritySettings:<AppName> --target-org <alias>`
- **Consumer key generation**: Consumer keys are generated post-deploy; retrieve after first deployment and store secrets only in a secret manager or CI vault.

## OAuth Security Hardening Checklist

- Request **minimum OAuth scopes** (`api`, `refresh_token` only when offline refresh is required — never `Full` by default).
- Enforce **exact non-wildcard HTTPS callback URLs** (avoid broad redirect patterns).
- Enforce **PKCE** for all public clients (SPAs, native mobile apps) and **certificate-based JWT auth** for unattended server jobs.
- Configure **refresh-token rotation/expiration** and IP relaxation policies aligned to client network topology.
- Restrict app access to **Admin-approved users are pre-authorized** via dedicated Permission Sets rather than "All users may self-authorize".

## Common Deployment Errors

- **`DUPLICATE_VALUE`**: An app with that developer name already exists — retrieve and update instead of re-creating.
- **`INVALID_CROSS_REFERENCE_KEY`**: The `externalClientApplication` value inside settings/policy XML does not match the `.eca-meta.xml` filename exactly.
- **`INSUFFICIENT_ACCESS_OR_READONLY`**: Deploying user lacks Manage Connected Apps / External Client App administrative permissions.
