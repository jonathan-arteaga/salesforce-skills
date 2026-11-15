# Platform guidance

- Describe/retrieve actual object, field, relationship, and metadata definitions; validate required fields/enums against the target API. Do not invent fields or infer data-access permissions from metadata visibility.
- Select an explicit target org and inspect its identity before mutations. Preserve source control, dry-run/validation evidence, and requested deployment scope; use synthetic data for testing and report partial failures.
- For RunSpecifiedTests deployments, selected tests must pass and cover each deployed Apex class/trigger by at least 75%; an org-wide percentage alone is insufficient. Record actual deployment results and test level rather than equating a rubric score with production readiness.

## Sources checked 2026-11-15

- [CustomObject](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customobject.htm)
- [CustomField](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/customfield.htm)
- [Running a Subset of Tests in a Deployment](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_run_specific_tests.htm)
