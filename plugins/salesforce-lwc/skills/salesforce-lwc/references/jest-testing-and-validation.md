# LWC Jest Testing, Local Validators, and Verification Boundaries

## Jest Unit Testing (`@salesforce/sfdx-lwc-jest`)

Create `__tests__/<componentName>.test.js` alongside every non-trivial component:

- **DOM lifecycle isolation**: Mount with `createElement('c-component-name', { is: ComponentName })` and clear `document.body.firstChild` in `afterEach()` plus `jest.clearAllMocks()`.
- **Async microtask flushing**: Always flush resolved promises (`await Promise.resolve()` or a microtask helper) after emitting wire data or clicking buttons before asserting DOM updates.
- **Mocking data sources**:
  - **LDS / GraphQL wire adapters**: Emit payloads with `adapter.emit(mockData)` and error cases with `adapter.error(mockError)`.
  - **Imperative Apex**: Mock via `jest.mock('@salesforce/apex/ClassName.methodName', () => ({ default: jest.fn() }), { virtual: true })` and test both `mockResolvedValue` and `mockRejectedValue`.
  - **Platform events / toast / navigation**: Mock `lightning/platformShowToastEvent`, `lightning/navigation`, and `lightning/messageService` handlers to assert dispatched event details.
- **Required test coverage**: Happy path rendering, empty state, loading spinner state, wire/imperative error state, user interaction + custom event payloads, Flow `FlowAttributeChangeEvent` / navigation events (if Flow screen), and accessibility attributes (`aria-*`, roles, labels).

## Hard Boundary: Jest vs Live Server Verification

| Verification Layer | What It Proves | What It Does NOT Prove |
| --- | --- | --- |
| Jest (`npm run test:unit`) | Client JS logic, DOM rendering, event contracts, mocked wire/error handling | Real Apex CRUD/FLS, sharing rules, Experience Cloud guest permissions, real SOQL/GraphQL schema |
| ESLint & Local Scripts | LWC lint rules, SLDS 2 hook usage, template anti-patterns | Runtime browser layout, org CSP/CORS, live Apex execution |
| Live Sandbox / Local Dev | Real LDS/GraphQL/Apex responses, user/guest security, Experience Cloud routing | Multi-org packaging edge cases without packaging tests |

- **Never claim Jest certifies server security**: When components call Apex or expose data on Experience Cloud, explicitly require live org testing with both authorized least-privileged users and unauthorized/guest users.

## Local Validation & Preview Commands

Run project tests, linters, and bundled validators directly:

```bash
# 1. Unit tests and lint
npm run test:unit
npx eslint force-app/main/default/lwc/<comp>

# 2. Bundled deterministic SLDS 2 & template validators
python3 scripts/validate_slds.py force-app/main/default/lwc/<comp>/<comp>.html
python3 scripts/validate_slds.py force-app/main/default/lwc/<comp>/<comp>.css
python3 scripts/template_validator.py force-app/main/default/lwc/<comp>/<comp>.html
python3 scripts/slds_linter_wrapper.py force-app/main/default/lwc/<comp>/<comp>.html

# 3. Live hot-reload preview against an authorized org
bash scripts/local-dev-preview.sh <org-alias> component
```

## Required Delivery Report Shape

Report: `LWC work` -> `Data pattern` (LDS / GraphQL / Apex / State Manager / LMS) -> `Files` -> `Local validation` (Jest, ESLint, SLDS/template scripts) -> `Remaining org checks` (Apex permissions, Experience Cloud guest test, deployment).
