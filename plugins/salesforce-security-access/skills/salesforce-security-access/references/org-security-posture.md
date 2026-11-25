# Org Security Posture Reference

Assess and harden Salesforce org-wide security posture across My Trust Center / Security Health Check, file upload malware scanning, Experience Cloud & guest access boundaries, and external app controls.

## 1. Posture Triage: My Trust Center, Security Center & Health Check

Inspect posture read-only before recommending any org setting changes:

- **My Trust Center & Trust Status**: Verify org instance, Hyperforce region, active trust notifications, and tenant-level security advisories before attributing anomalies to local misconfiguration.
- **Security Health Check / Security Center**: Review baseline compliance score and high-risk settings:
  - Password policies, session timeout, lock sessions to IP/domain, clickjack protection, HSTS, and TLS requirements.
  - Multi-Factor Authentication (MFA) enforcement for UI logins and SSO identity provider assurance.
  - Connected Apps & External Client Apps (2026 preference: migrate legacy Connected Apps to External Client Apps where supported): audit OAuth scopes, refresh-token rotation/expiration, admin-approved pre-authorization, and IP relaxation policies.
  - Certificate and key expiration (`Certificate` / Named Credential / External Credential hygiene; delegate callout configuration to `salesforce-integrations`).

Read-only posture inspection examples (pin `--target-org <user-or-alias>`):

```bash
# Check Security Health Check risks (requires View Setup and Configuration / Health Check access)
sf data query --target-org <org> --use-tooling-api --json \
  --query "SELECT RiskType, Setting, SettingGroup, OrgValue, StandardValue FROM SecurityHealthCheckRisks WHERE RiskType = 'HIGH_RISK'"

# Audit active Experience Cloud sites and statuses
sf data query --target-org <org> --json \
  --query "SELECT Id, Name, Status, UrlPathPrefix, OptionsAllowMembersToFlag, OptionsGuestChatterEnabled FROM Network"
```

If Tooling API or Security Center objects are unavailable due to license or permissions, record the exact missing evidence rather than inferring a clean bill of health.

## 2. File Upload Security & Malware Scanning Boundaries

Untrusted files enter Salesforce via CRM attachments (`ContentVersion`/`ContentDocument`), Email-to-Case, Experience Cloud uploads, and Agentforce `config.file_upload`:

- **Platform vs add-on scanning boundary**: Salesforce platform file upload settings (file size limits, MIME/extension allowlists/blocklists, download behavior such as "Execute in Browser" disabled for HTML/SVG/active content) reduce browser-execution risk, but **do not substitute for dedicated malware/antivirus scanning**. Verify whether the org uses a verified AppExchange/ICAP/cloud malware scanner, Shield Event Monitoring file events, or an external quarantine pipeline before marking file uploads scanned.
- **Hardening controls**:
  1. Disable inline browser execution for active MIME types (`.html`, `.htm`, `.svg`, `.js`, `.swf`).
  2. Enforce strict file extension allowlists and size ceilings on Experience Cloud upload components and Agentforce file-upload subagents.
  3. Quarantine or scan external uploads asynchronously before exposing them to internal agents, RAG Data Libraries, or downstream integrations.
  4. Never treat uploaded file content as trusted system instructions (prompt-injection risk in RAG and Agentforce).

## 3. Experience Cloud & Guest User Access Boundaries

Guest (unauthenticated) access is the highest-impact external exposure surface in Salesforce:

| Control Area | Required Posture | Common Misconfiguration |
| --- | --- | --- |
| Guest User OWD | External OWD set to **Private** on sensitive objects; enable "Secure guest user record access" | Relying on public read-only external OWD |
| Guest Sharing Rules | Strictly criteria-based, **read-only**, minimal record subset | Over-broad criteria exposing all Accounts, Cases, or Contacts |
| Guest Profile Object/Field Access | Remove unnecessary Read/Edit/Delete; never grant View All / Modify All | Leaving legacy object CRUD or PII fields readable by Guest |
| Apex & LWC Exposure | Explicit `@AuraEnabled` allowlisting on Guest Profile; enforce `with sharing` + `USER_MODE` | `without sharing` Apex controllers callable by unauthenticated guests without strict server-side record/token checks |
| Flow Exposure | Never expose `System Context Without Sharing` Flows to Guest users without narrow, verified anti-enumeration controls | Public Flow accepting arbitrary record IDs from URL parameters |
| Site Security Headers | Strict CSP (`Content-Security-Policy`), Trusted URLs allowlist, Clickjack protection | Relaxed CSP allowing arbitrary third-party scripts |
| Site Membership & Self-Registration | Explicit Profile/Permission Set membership; rate-limit / CAPTCHA self-registration; verify email/identity before linking existing Contacts | Auto-linking unverified registrants to existing customer Accounts |

Delegate LWC implementation changes to `salesforce-lwc`, Apex controller hardening to `salesforce-apex`, and Flow fixes to `salesforce-flow`.

## 4. Governance, Authorization, and Audit Integrity

- **Never claim regulatory certification**: Do not state that an org or architecture is "HIPAA compliant", "PCI certified", "SOC 2 certified", or "GDPR compliant". Document concrete technical controls inspected, gaps found, and evidence required for the customer's compliance team.
- **No silent mutations**: Posture reviews are strictly read-only unless the user explicitly authorizes specific metadata or Setup changes for a named target org.
- **Evidence separation**: Report (1) verified org query results, (2) static/architectural recommendations, (3) sandbox test results (including unauthenticated guest negative tests), and (4) production items not yet verified.

## Sources Verified

- Secure Your Experience Cloud Site: `https://help.salesforce.com/s/articleView?id=experience.networks_security.htm&release=264.0.0&type=5`
- Salesforce Well-Architected Security: `https://architect.salesforce.com/docs/architect/well-architected/guide/framework.html`
