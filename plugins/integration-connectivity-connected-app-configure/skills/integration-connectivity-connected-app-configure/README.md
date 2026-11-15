# integration-connectivity-connected-app-configure

Salesforce Connected Apps & External Client Apps skill for Codex.

## Overview

This skill helps you create and manage:

- **Connected Apps**: Traditional OAuth-enabled applications for Salesforce integration
- **External Client Apps (ECAs)**: Modern, security-first applications with enhanced controls (API 61.0+)

## Features

| Feature | Description |
|---------|-------------|
| App Generation | Create Connected Apps or ECAs from requirements |
| Security Scoring | 120-point validation across 6 categories |
| Template Library | Pre-built templates for common OAuth flows |
| Migration Support | Guidance for Connected App → ECA migration |
| Best Practices | Built-in security recommendations |

## Quick Start

### Create a Connected App

```text
Use the integration-connectivity-connected-app-configure skill to create a Connected App named "MyIntegration"
with API and RefreshToken scopes for server-to-server integration.
```

### Create an External Client App

```text
Use the integration-connectivity-connected-app-configure skill to create an External Client App named
"MobileApp" for a mobile application with PKCE enabled.
```

### Review Existing Apps

```text
Use the integration-connectivity-connected-app-configure skill to review and score my existing Connected Apps
for security best practices.
```

## Scoring Categories

| Category | Points | Focus |
|----------|--------|-------|
| Security | 30 | PKCE, rotation, certificates |
| OAuth Configuration | 25 | Callbacks, flows, tokens |
| Metadata Compliance | 20 | Required fields, API version |
| Best Practices | 20 | Minimal scopes, admin approval |
| Scopes | 15 | Least privilege principle |
| Documentation | 10 | Description, contact info |

## When to Use Each App Type

### Choose Connected App When:
- Maintaining an existing integration with a documented compatibility requirement
- New creation is an exception requiring Salesforce Support eligibility as of Spring '26

### Choose External Client App When:
- Creating any new integration, including simple single-org integrations
- Multi-org or ISV distribution
- Automated secret rotation required
- Enhanced audit logging needed
- Full metadata compliance required
- Packaging in 2GP

## Directory Structure

```text
integration-connectivity-connected-app-configure/
├── skills/
│   └── integration-connectivity-connected-app-configure/
│       └── SKILL.md          # Main skill definition
├── assets/
│   ├── connected-app-basic.xml
│   ├── connected-app-oauth.xml
│   ├── connected-app-jwt.xml
│   ├── connected-app-canvas.xml
│   ├── external-client-app.xml
│   ├── eca-global-oauth.xml
│   ├── eca-oauth-settings.xml
│   └── eca-policies.xml
├── references/
│   └── example-usage.md
├── references/
│   ├── oauth-flows-reference.md
│   ├── security-checklist.md
│   └── migration-guide.md
└── README.md
```

## Dependencies

- **platform-metadata-deploy**: For deploying apps to orgs
