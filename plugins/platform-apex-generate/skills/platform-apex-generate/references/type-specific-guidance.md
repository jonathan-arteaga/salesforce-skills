# Type-Specific Guidance

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Type-Specific Guidance
  - Service
  - Selector
  - Domain
  - Batch
  - Queueable
  - Schedulable
  - DTO / Wrapper
  - Utility
  - Interface
  - Abstract
  - Custom Exception
  - Trigger
  - Trigger Action (TAF)
  - Invocable Method (`@InvocableMethod`)
  - REST Resource (`@RestResource`)
  - `@AuraEnabled` Controller

## Type-Specific Guidance

### Service
- Template: `assets/service.cls` · Reference: `references/AccountService.cls`
- `with sharing`; stateless — no `public` fields or mutable instance state; keep public APIs focused and `static` where reasonable
- Delegate all SOQL to Selectors and SObject behavior to Domains
- Wrap business errors in a custom exception (e.g., `AccountServiceException`)

### Selector
- Template: `assets/selector.cls` · Reference: `references/AccountSelector.cls`
- `inherited sharing`; one per SObject or query domain
- Return `List<SObject>` or `Map<Id, SObject>`; use a shared base field list constant (no inline duplication)
- Accept filter parameters; always include `WITH USER_MODE`

### Domain
- Template: `assets/domain.cls`
- `with sharing`; encapsulate field defaults, derivations, and validations
- Operate on in-memory lists only; no SOQL/DML (belongs in Services/Selectors)

### Batch
- Template: `assets/batch.cls` · Reference: `references/AccountDeduplicationBatch.cls`
- `with sharing`; implement `Database.Batchable<SObject>` (add `Database.Stateful` when tracking across chunks)
- `start()` = query definition; `execute()` = business logic; `finish()` = logging/notification
- Use `QueryLocator` for large datasets; handle partial failures via `Database.SaveResult`
- Accept filter parameters via constructor for reusability

### Queueable
- Template: `assets/queueable.cls`
- `with sharing`; implement `Queueable` and optionally `Database.AllowsCallouts` when HTTP callouts are needed
- Accept data via constructor
- Add chain-depth guards to prevent infinite chains
- Optionally implement `Finalizer` for recovery/cleanup
- Use `AsyncOptions` for configurable delay (up to 10 min) and dedup signatures

### Schedulable
- Template: `assets/schedulable.cls`
- `with sharing`; `execute()` delegates to Queueable or Batch
- Provide CRON constants and a convenience `scheduleDaily()` helper

### DTO / Wrapper
- Template: `assets/dto.cls`
- No sharing keyword needed (pure data containers)
- Simple public properties; no-arg + parameterized constructors; `Comparable` when ordering matters
- Use `@JsonAccess` on private/protected inner DTOs that are serialized/deserialized

### Utility
- Template: `assets/utility.cls`
- No sharing keyword needed; all methods `public static`; `private` constructor
- Pure, side-effect-free; no SOQL/DML

### Interface
- Template: `assets/interface.cls`
- Define clear contracts with ApexDoc on each method signature

### Abstract
- Template: `assets/abstract.cls`
- `with sharing`; offer default behavior via `virtual` methods
- Mark extension points `protected virtual` or `protected abstract`
- Include a concrete example in the ApexDoc showing how to extend the class

### Custom Exception
- Template: `assets/exception.cls`
- No sharing keyword; extend `Exception` with descriptive names
- Supported constructors: `()`, `('msg')`, `(cause)`, `('msg', cause)`

### Trigger
- Template: `assets/trigger.cls`
- One trigger per object; delegate all logic to handler/TAF action classes
- Include all relevant DML contexts; if TAF: `new MetadataTriggerHandler().run();`

### Trigger Action (TAF)
- One class per concern per context; implement `TriggerAction.{Context}`
- Register via `Trigger_Action__mdt` (actions are inactive without registration)
- Name: `TA_{SObject}_{ActionName}`; prefer field-value comparison over static booleans for recursion

### Invocable Method (`@InvocableMethod`)
- Template: `assets/invocable.cls`
- `with sharing`; inner `Request`/`Response` with `@InvocableVariable`
- Method must be `public static`; non-static or single-object signatures will not compile
- Accept `List<Request>`, return `List<Response>`; bulkify (SOQL/DML outside loops)
- Decorator parameters: `label` (required — Flow Builder display name), `description`, `category` (groups actions in Builder), `callout=true` (required when method makes HTTP callouts)
- `@InvocableVariable` parameters: `label` (required), `description`, `required=true/false`
- `@InvocableVariable` supports: primitives, `Id`, `SObject`, `List<T>` only (no `Map`/`Set`/`Blob`); use `List<Id>` or `List<SObject>` fields for Flow collection I/O
- Always include `isSuccess`, `errorMessage`, and `errorType` (`e.getTypeName()`) in Response
- Return errors in Response (recommended); throwing an exception triggers the Flow Fault path — reserve for unrecoverable failures only

### REST Resource (`@RestResource`)
- Template: `assets/rest-resource.cls`
- `global with sharing`; both class and methods must be `global`
- Versioned URL: `@RestResource(urlMapping='/{resource}/v1/*')`
- Use proper HTTP status codes per branch (`200`/`201`/`400`/`404`/`422`/`500`); never default all errors to `500`
- Validate inputs (Id format: `Pattern.matches('[a-zA-Z0-9]{15,18}', value)`); bind all user input in SOQL
- Include `LIMIT`/`ORDER BY` in queries; implement pagination (`pageSize`/`offset`)
- Standardized `ApiResponse` wrapper (`success`, `message`, `data`/`records`); inner request/response DTOs
- Thin controller: delegate business logic to Service classes

### `@AuraEnabled` Controller
- `with sharing`; use `WITH USER_MODE` in all SOQL
- Use `@AuraEnabled(cacheable=true)` only for read-only queries; leave `cacheable` unset for DML operations
- Catch exceptions and rethrow as `AuraHandledException` with user-friendly messages

---
