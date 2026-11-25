---
name: salesforce-lwc
description: "Build, style, test, and review Salesforce Lightning Web Components with LDS/UI API, GraphQL wire and mutations, LWC State Managers, TypeScript, SLDS 2 hooks, and Jest tests. Use salesforce-apex for Apex controllers, salesforce-flow for Flows, and salesforce-devops-deploy for rollouts."
---

# Salesforce LWC

Lifecycle skill for building, styling, optimizing, and Jest-testing Lightning Web Components (`lwc/**/*.{js,ts,html,css,js-meta.xml}`).

## Mode Routing

Select the active mode first and load only the matching reference before authoring or reviewing:

| Mode | When to Use | Reference |
| --- | --- | --- |
| Data, State & 2026 LWC | LDS/UI API, GraphQL wire & mutations, LWC State Managers, TypeScript, complex expressions, Flow/Agentforce targets | [data-state-and-modern-lwc.md](references/data-state-and-modern-lwc.md) |
| SLDS 2, A11y & Perf | SLDS 2 styling hooks, dark mode, WCAG accessibility, Shadow DOM, rerender safety | [slds2-accessibility-and-performance.md](references/slds2-accessibility-and-performance.md) |
| Jest & Validation | `@salesforce/sfdx-lwc-jest` tests, mocks, local validators, Jest vs live-server boundaries | [jest-testing-and-validation.md](references/jest-testing-and-validation.md) |

## Core 2026 Invariants

- **LDS / UI API First**: Prefer Lightning Data Service (`getRecord`, `lightning-record-form`, `lightning-record-edit-form`) for supported record operations — it enforces sharing, CRUD, and FLS automatically. Escalate to GraphQL wire/mutations for related-object graphs, and Apex `@AuraEnabled` only when custom server logic is required.
- **Apex Controller Security**: NEVER use `WITH SECURITY_ENFORCED` in supporting Apex controllers (rejected at API 67+). Always declare `with sharing`, enforce `WITH USER_MODE` / `AccessLevel.USER_MODE`, require explicit Apex class access, and sanitize errors via `AuraHandledException`.
- **Modern 2026 LWC Features**: Confirm target org API version and release status before adopting LWC State Managers (`@lwc/state` / Platform State Managers), TypeScript (`@salesforce/lightning-types`, TS 5.4.5+), GraphQL mutations, or complex template expressions (fall back to JS getters on older orgs).
- **SLDS 2 & Accessibility**: Use base Lightning components and SLDS 2 styling hooks (`--slds-g-*`); zero hardcoded hex colors; enforce WCAG 2.1 AA semantics, keyboard navigation, and modal focus traps.
- **Jest vs Live Server Boundary**: Jest verifies client rendering and JS behavior ONLY — it does not certify Apex CRUD/FLS, sharing rules, Experience Cloud guest-user access, or live org deployment.

## Hard Org & Safety Gates

- Confirm target surface (`lightning__RecordPage`, `lightning__AppPage`, `lightning__FlowScreen`, Experience Cloud, `lightning__Dashboard`) and org API version before generating metadata.
- Never log secrets, session tokens, or sensitive record payloads to `console.log`. Sanitize user-facing errors.
- Always test unauthorized and Experience Cloud guest-user access in a live org when external surfaces are in scope.
- Never trigger unconditional state mutations in `renderedCallback()` or bypass Shadow DOM encapsulation.

## Deterministic Scripts (Black-Box Usage)

Run the bundled validators directly on generated LWC files without modifying script internals:

```bash
python3 scripts/validate_slds.py force-app/main/default/lwc/<comp>/<comp>.html
python3 scripts/template_validator.py force-app/main/default/lwc/<comp>/<comp>.html
python3 scripts/slds_linter_wrapper.py force-app/main/default/lwc/<comp>/<comp>.css
bash scripts/local-dev-preview.sh <org-alias> component
```

Note: `post-tool-validate.py` and `lwc-lsp-validate.py` are legacy hook helpers; run `validate_slds.py`, `template_validator.py`, `npm run test:unit`, and ESLint directly as verification.

## Required Deliverables & Verification Integrity

- **Bundle deliverables**: `<comp>.js` (or `.ts`), `<comp>.html`, `<comp>.css`, `<comp>.js-meta.xml`, and `__tests__/<comp>.test.js`.
- Report **local checks** (Jest pass/fail, ESLint, `validate_slds.py`, `template_validator.py`) separately from **org verification** (deployed Apex/LDS permissions, Experience Cloud guest checks, Local Dev preview).

## Cross-Skill Handoffs

- `salesforce-apex`: Apex controllers (`with sharing`, `WITH USER_MODE`), services, and Apex unit tests
- `salesforce-flow`: parent Flow XML embedding LWC Flow Screen components
- `salesforce-security-access`: Permission Sets, Apex class access, and Experience Cloud guest policies
- `salesforce-devops-deploy`: component bundle deployment and CI/CD rollouts
