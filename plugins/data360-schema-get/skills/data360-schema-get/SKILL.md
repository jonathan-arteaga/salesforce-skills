---
name: |-
  data360-schema-get
description: |-
  Inspect Data 360 (Data Cloud) DLO or DMO field definitions and types. Return schema details for the selected org. Use agentforce-d360-analyze for runtime sessions.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# data360-schema-get Skill

## Overview

This skill retrieves Data Lake Object (DLO) and Data Model Object (DMO) schema information from Salesforce Data Cloud using the SSOT REST API. It can enumerate DLOs or DMOs visible to the selected user, or retrieve detailed schema for a specific DLO or DMO. Permission-limited visibility is not proof of a complete org inventory.

## When to Use

- User wants to see all DLOs or DMOs in a Data Cloud org
- User needs field schema for a specific DLO or DMO
- User is exploring Data Cloud data structures
- User needs to understand DLO or DMO field types and metadata

## Prerequisites

- SF CLI installed and authenticated to target org
- Org has Data Cloud enabled
- User has appropriate Data Cloud permissions

## Skill Execution

### Parameters

1. **org\_alias** (required): The SF CLI org alias (e.g., 'afvibe', 'myorg')
2. **dlo\_name** (optional): Specific DLO developer name (e.g., 'Employee\_\_dll')
3. **dmo\_name** (optional): Specific DMO developer name (e.g., 'Individual\_\_dlm')

### Step 1: Discover Connected Org

Use the explicitly selected org alias. If no target was given, inspect authenticated orgs and resolve the intended target; never silently choose the first connected org:

```bash
sf org list
```

Example output:

```txt
┌────┬───────┬──────────────────────────┬────────────────────┬───────────┐
│    │ Alias │ Username                 │ Org Id             │ Status    │
├────┼───────┼──────────────────────────┼────────────────────┼───────────┤
│    │ myorg │ admin@example.com │ 00D000000000000EAA │ Connected │
└────┴───────┴──────────────────────────┴────────────────────┴───────────┘
```

Resolve the intended alias and stable org identity before querying. Record the requested data space and inspect returned data-space metadata. The bundled collection endpoints enumerate visible metadata; they do not establish authorization for a particular space or all org data.

### Step 2: Validate SF CLI Authentication

Before making API calls, verify authentication through the bundled helper, which captures CLI output privately. Never print the raw JSON below: it can contain an access token. If running the command manually, capture it and emit only allowlisted identity/status fields:

```bash
sf org display --target-org <org_alias> --json
```

If not connected, inform user to run:

```bash
sf org login web --alias <org_alias>
```

### Step 3a: Execute DLO Schema Script

The Python scripts are bundled with this skill in the `scripts/` subdirectory. Resolve paths relative to this skill directory, not the project working directory. They use the Python standard library, follow metadata pagination, and fail explicitly on incomplete or unexpected responses. Their API default is pinned to `v64.0`; validate compatibility or pass `--api-version vNN.0` with a verified target version. List calls do not apply a server-side data-space filter: report returned space metadata and scope limits.

**To list all DLOs:**

```bash
python3 ./scripts/get_dlo_schema.py <org_alias>
```

**To get specific DLO schema:**

```bash
python3 ./scripts/get_dlo_schema.py <org_alias> <dlo_name>
```

### Step 3b: Execute DMO Schema Script

**To list all DMOs:**

```bash
python3 ./scripts/get_dmo_schema.py <org_alias>
```

**To get specific DMO schema:**

```bash
python3 ./scripts/get_dmo_schema.py <org_alias> <dmo_name>
```

### Step 4: Present Results

Parse and present the results in a user-friendly format:

**For DLO List:**

- Show DLO name, label, category, and ID
- Indicate total count
- Highlight DLOs with data (totalRecords > 0)

**For DLO Schema:**

- Show basic info (name, label, category, status)
- List all fields with:
  - Field name
  - Data type
  - Primary key indicator
  - Nullable status
- Highlight custom fields (exclude system fields like DataSource\_\_c, cdp\_sys\_\*)
- Show record count if available

**For DMO List:**

- Show DMO name, label, category, and ID
- Indicate total count

**For DMO Schema:**

- Show basic info (name, label, category, description)
- List all fields with:
  - Field name
  - Data type
  - Primary key indicator
  - Nullable status
- Show dataspace information if available

### Step 5: Offer Next Steps

After displaying results, suggest relevant follow-up actions:

- Query data from the DLO
- Create calculated insights
- Build segments
- Set up data streams
- Create DMO mappings

See [API endpoints, response shapes, and examples](references/api-and-output-examples.md) when you need request details or an example output.

## Notes

- DLO and DMO names commonly use `__dll` and `__dlm`. Use the names and field types returned by metadata, including standard namespaces and system fields; do not construct identifiers from suffix assumptions.
- System fields (DataSource\_\_c, KQ\_*, cdp\_sys\_*) are automatically added
- Identify primary keys from metadata when joining or correlating records; do not claim every read query must select a primary key.
- API supports pagination (limit/offset) for large result sets

## Related Skills

- **data360-ingestion-modeling**: For DLO-to-DMO mapping workflows, when installed
- For Data Kit validation, inspect current supported component documentation and available tooling; no dedicated Data Kit validator is bundled
- Use this skill before creating DMO mappings to understand source DLO structure
