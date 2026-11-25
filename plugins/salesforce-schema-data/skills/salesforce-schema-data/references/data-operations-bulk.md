# Salesforce Data Operations & Bulk API 2.0

Perform authorized org data CRUD, Bulk API 2.0 imports/upserts/deletes, relational tree seeding, synthetic test-data generation, and disciplined cleanup.

## Mode & Pre-Flight Gates

1. **Confirm mode first**: Ask or confirm whether the user wants **local script generation** (`.apex`, CSV, JSON) or **remote org execution** against an explicitly named sandbox/scratch org.
2. **Verify schema exists**: Objects and fields must already be deployed before inserting data. If metadata is missing, author it first (Objects & Fields mode) and hand off deployment to `salesforce-devops-deploy`.
3. **Describe-first pre-flight**: Inspect required fields, createable/updateable flags, active picklist values, and parent lookups before creating records:

```bash
sf sobject describe --sobject Account --target-org <alias> --json \
  | jq '.result.fields[] | select(.createable == true) | {name, type, nillable, picklistValues: [.picklistValues[]?.value]}'
```

## Choosing the Right `sf data` Mechanism

| Scenario | Recommended Mechanism | Example Command |
| --- | --- | --- |
| Single-record CRUD | `sf data create/update/delete record` | `sf data create record -s Account -v "Name='Synth Corp'" -o <alias>` |
| Small parent-child seed (<= 200 recs) | SObject Tree JSON | `sf data import tree --plan plan.json -o <alias>` |
| Large volume / migration (251–100k+) | Bulk API 2.0 (`sf data ... bulk`) | `sf data upsert bulk -s Account -f accounts.csv -i External_Id__c -w 10 -o <alias>` |
| Complex relational test seeding | Anonymous Apex factory + savepoint | `sf apex run --file seed.apex -o <alias>` |
| Bulk export | Bulk query CSV | `sf data query -f query.soql --bulk -r csv -w 10 -o <alias>` |

## Bulk Testing, Data Hygiene & Common Errors

- **251+ bulk threshold**: When testing triggers, Flows, or roll-ups for bulkification, seed **251+ records** so execution spans multiple 200-record batches. Avoid one-record-at-a-time loops.
- **Synthetic data only**: Use clearly tagged synthetic names (`Synth_Test_001`) and never include real customer PII, SSNs, or payment card numbers in CSVs or Apex factories.
- **Bounded retry discipline**: Inspect the exact error, correct parameters once, re-run describe if needed, and pivot rather than repeating identical failing commands. Report Bulk API 2.0 partial failures with exact succeeded/failed counts (`sf data import resume -i <jobId> -o <alias>`).

| Error Code | Likely Cause | Fix Direction |
| --- | --- | --- |
| `INVALID_FIELD` | Wrong API name or missing FLS | Verify with `sf sobject describe` and user permissions |
| `REQUIRED_FIELD_MISSING` | Mandatory field omitted | Add required fields from describe output |
| `INVALID_CROSS_REFERENCE_KEY` | Missing or wrong parent ID | Create/query parent records first or use External ID upsert |
| `FIELD_CUSTOM_VALIDATION_EXCEPTION` | Validation rule rejected test payload | Align synthetic values with active business rules |
| Non-writeable field error | System/formula/read-only field in CSV | Strip non-createable columns before import |

## Cleanup, Rollback & Validation Script

Always pair data creation with explicit cleanup before leaving the org:

- **Delete-by-ID / pattern / window**: Save created record IDs (or tag records with a unique batch token) and supply exact `sf data delete bulk` or anonymous Apex cleanup commands.
- **Reversible dry runs**: Wrap exploratory anonymous Apex scripts in a savepoint when verifying automation side effects without persisting rows:

```apex
Savepoint sp = Database.setSavepoint();
Database.insert(testAccounts, true, AccessLevel.USER_MODE);
Database.rollback(sp);
```

- **Pre-flight script validator**: Run `scripts/validate_data_operation.py` on generated `.apex`, `.soql`, `.csv`, or `.json` files via CLI to check query efficiency, bulk safety, PII patterns, and cleanup discipline before execution.
