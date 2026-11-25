---
name: salesforce-schema-data
description: "Author Salesforce CustomObject and CustomField metadata XML, write or optimize SOQL/SOSL with USER_MODE, and execute safe sf data CRUD, Bulk 2.0, or test-data operations. Use salesforce-apex for Apex classes, salesforce-devops-deploy for deployments, or data360-data-pipeline for DLOs/DMOs."
---

# Salesforce Schema & Data

Author SFDX CustomObject and CustomField metadata XML, write and optimize API 67+ SOQL/SOSL queries with `WITH USER_MODE`, and execute or script safe `sf data` CRUD, Bulk API 2.0, and test-data operations.

## Mode Routing

Select the mode matching the request and load only its reference:

| Mode | Trigger | Reference |
| --- | --- | --- |
| Objects & Fields XML | Custom objects, custom fields, Master-Detail, roll-ups, formulas, picklists, validation rules | [Objects & Fields XML](references/objects-and-fields.md) |
| SOQL & SOSL | Query authoring, relationships, aggregates, selectivity, Query Plan, `WITH USER_MODE` | [SOQL & SOSL Optimization](references/soql-sosl-optimization.md) |
| Data Operations & Bulk | `sf data` CRUD, tree import/export, Bulk API 2.0, 251+ test data, cleanup & rollback | [Data Operations & Bulk](references/data-operations-bulk.md) |

## Core 2026 Invariants

- **Describe before assuming**: Inspect actual object, field, picklist, and relationship metadata (`sf sobject describe` or retrieved source) before generating XML, SOQL, or data payloads. Never invent field API names or infer runtime FLS/CRUD from metadata visibility.
- **API 67+ security mode**: Always enforce object and field permissions with `WITH USER_MODE` in SOQL (and `AccessLevel.USER_MODE` in Apex DML/Database calls) unless an explicit system-context justification is documented.
- **High-failure metadata traps**: Omit `<fullName>` at CustomObject root; set `<sharingModel>ControlledByParent</sharingModel>` whenever a Master-Detail exists; omit XML comments before `<CustomField>`; omit `<length>` on `TextArea` and Formula fields; omit `<required>`, `<deleteConstraint>`, and `<lookupFilter>` on Master-Detail fields; omit `<precision>` and `<scale>` on Roll-Up Summary fields.
- **Description enrichment gate**: Every CustomObject needs a human-written `<description>` under 50 words using field labels. Whenever a field or validation rule is added, updated, or deleted on an existing object, propose the refreshed description and wait for user approval before overwriting.
- **Selectivity & bulk discipline**: Query only required fields, filter on indexed fields, avoid leading wildcards and queries inside loops, and seed 251+ synthetic records when validating bulkified automation.

## Hard Org & Safety Gates

- **Local script vs. remote execution**: Confirm whether the user wants local assets (`.object-meta.xml`, `.field-meta.xml`, `.soql`, `.apex`, CSV/JSON) or authorized remote org mutations. Never silently mutate an org.
- **Explicit target org**: Inspect `sf org list` and confirm org alias and identity before remote operations; never print raw `sf org display --json` tokens.
- **Synthetic data & cleanup**: Use non-identifying synthetic test data (zero real PII/SSNs/payment cards) and always provide exact cleanup/rollback commands or savepoint scripts before creating org records.

## Bundled Scripts (Black-Box Execution)

Run the bundled Python validators directly via CLI relative to this skill directory rather than reading script source into context:

- Static SOQL check: `python3 ./scripts/soql_validator.py <path/to/query.soql>`
- Post-edit SOQL + optional Query Plan check (JSON on stdin): `echo '{"tool_input":{"file_path":"<file.soql>"},"tool_response":{"success":true}}' | python3 ./scripts/soql-post-validate.py`
- Data operation validator (`.apex`, `.soql`, `.csv`, `.json`): `python3 -c "import json, sys; sys.path.insert(0,'./scripts'); from validate_data_operation import DataOperationValidator; print(json.dumps(DataOperationValidator(sys.argv[1]).validate(), indent=2))" <path/to/file>`

## Verification Integrity & Output Contract

- Report static validator output, dry-run/Query Plan checks, and live sandbox executions separately; a static score is a review rubric, not production readiness.
- Report partial Bulk API 2.0 or DML failures explicitly with succeeded/failed counts and error codes.
- Deliver outputs in a consistent order:
  1. **Target & Mode**: Local artifact paths or explicitly confirmed org alias + API version.
  2. **Generated Artifact / Operation**: Metadata XML, `WITH USER_MODE` query, or `sf data` command/result.
  3. **Validation Evidence**: Validator output, Query Plan cost, or record counts.
  4. **Cleanup / Next Step**: Rollback/delete commands or deployment handoff.
- Check Metadata API and SOQL changes against Salesforce Docs MCP or official developer docs for the target org's API version.

## Handoffs

- Apex classes, triggers, selectors, or unit tests -> `salesforce-apex`
- SFDX deployments, validation runs, or CI/CD -> `salesforce-devops-deploy`
- Permission sets, profiles, or sharing architecture -> `salesforce-security-access`
- Data 360 DLO/DMO schema or Data 360 SQL -> `data360-data-pipeline` / `data360-activation-governance`
