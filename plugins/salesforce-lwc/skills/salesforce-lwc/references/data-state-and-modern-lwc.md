# LWC Data Access, State Management, and 2026 Features

## Data Access Hierarchy

Choose the lightest platform-native pattern that fits the use case:

| Need | Default Pattern | Why |
| --- | --- | --- |
| Single-record CRUD / forms | LDS (`getRecord`, `lightning-record-form`, `lightning-record-edit-form`) | Automatic sharing, CRUD/FLS, shared client cache, minimal boilerplate |
| Related object graphs & pagination | GraphQL wire adapter (`lightning/graphql`) & GraphQL mutations | Multi-object queries, cursor pagination, schema-aware UI API security |
| Complex server logic / aggregations | Apex `@AuraEnabled(cacheable=true)` via `@wire` (reads) or imperative call (DML) | Custom domain logic; refresh with `refreshApex` or `notifyRecordUpdateAvailable` |
| Cross-DOM / sibling communication | Lightning Message Service (LMS) or LWC State Manager | Decoupled messaging across sibling or non-parent components |

## Supporting Apex Controller Security Rules

- **NEVER use `WITH SECURITY_ENFORCED`**: It cannot compile at API 67.0+. Use explicit `with sharing` plus `WITH USER_MODE` on SOQL and `AccessLevel.USER_MODE` on `Database` DML.
- **Explicit class access**: Users (including Experience Cloud authenticated and guest users) require explicit Apex class access via Permission Set or Profile in addition to object/field permissions.
- **Error & log hygiene**: Catch exceptions in `@AuraEnabled` methods and throw sanitized `AuraHandledException` with no internal stack details or PII. Do not log record payloads or tokens in browser `console`.
- **Cache synchronization**: After imperative Apex DML mutates records cached by LDS or GraphQL, call `notifyRecordUpdateAvailable([{ recordId }])` or `refreshApex(wiredResult)` so UI stays consistent.

## LWC State Management Spectrum

| Pattern | Scope | Best Fit |
| --- | --- | --- |
| Reactive fields (`@api`, `@track`, JS getters) | Single component | Local UI state, toggles, derived view values; reassign objects/arrays immutably |
| Singleton JS store (`store.js`) | Cross-component | Lightweight shared filters, cart, or client preferences |
| LWC State Managers (`@lwc/state` / Platform State Managers) | Complex app / record page | Atoms, computed values, async actions, and layout-aware shared state |
| Lightning Message Service (LMS) | Cross-DOM / Flexipage / VF-LWC | Loosely coupled pub/sub; always unsubscribe in `disconnectedCallback()` |

- **Immutable updates**: Reassign arrays/objects (`this.items = [...this.items, next]`) rather than mutating nested keys in place unless explicitly `@track`ed.

## 2026 LWC Capabilities (Verify Org API Version First)

Confirm the target org's API version and GA/Beta availability before adopting newer features:
- **GraphQL wire & mutations**: Use `lightning/graphql` for reactive reads with cursor pagination (`first`, `after`) and supported GraphQL record mutations (`executeMutation` / UI API mutation syntax); verify mutation GA status for the target release.
- **TypeScript support (API 66+)**: Use TypeScript 5.4.5+ with `@salesforce/lightning-types` for typed `@api` props, wire results (`WireResult<T>`), and DTOs; configure `tsconfig.json` per SFDX guidance.
- **Complex template expressions**: Newer LWC releases expand expression capabilities in HTML templates, but confirm target org API version and toolchain support; use clean JS getters whenever backward compatibility or strict `template_validator.py` compliance is required.
- **Dynamic listeners (`lwc:on`)**: Bind event maps programmatically when building generic wrappers.
- **Flow Screen integration**: Expose `@api` input/output properties (`role="inputOnly"` / `outputOnly`), fire `FlowAttributeChangeEvent` on mutations, check `availableActions`, and dispatch `FlowNavigationFinishEvent` / `FlowNavigationNextEvent`.
- **Agentforce & Dashboard surfaces**: Add `<capability>lightning__agentforce</capability>` with clear `masterLabel` and property descriptions for Agentforce discoverability; use `<target>lightning__Dashboard</target>` where enabled.

## Component Communication Contract

- **Parent -> Child**: Pass immutable `@api` properties or call narrowly scoped `@api` methods.
- **Child -> Parent**: Dispatch lowercase `CustomEvent` with minimal serializable `detail`; keep `bubbles: false, composed: false` unless intentionally crossing Shadow DOM boundaries.
- **Unrelated components**: Use LWC State Managers for shared reactive state or LMS channels for fire-and-forget notifications.
