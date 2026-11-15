## API Endpoints Used

### List All DLOs

```txt
GET /services/data/v64.0/ssot/data-lake-objects
```

Response structure:

```json
{
  "dataLakeObjects": [
    {
      "name": "Employee__dll",
      "label": "Employee",
      "category": "Profile",
      "id": "1dlXXXXXXXXXXXXXXX",
      "status": "ACTIVE",
      "totalRecords": 12,
      "fields": [...]
    }
  ],
  "totalSize": 5
}
```

### Get DLO Schema

```txt
GET /services/data/v64.0/ssot/data-lake-objects/{dlo_name}
```

Response structure (same as individual object in list response, but wrapped in paginated format).

### List All DMOs

```txt
GET /services/data/v64.0/ssot/data-model-objects
```

Response structure:

```json
{
  "dataModelObjects": [
    {
      "name": "Individual__dlm",
      "label": "Individual",
      "category": "Profile",
      "id": "0dmXXXXXXXXXXXXXXX",
      "fields": [...]
    }
  ],
  "totalSize": 10
}
```

### Get DMO Schema

```txt
GET /services/data/v64.0/ssot/data-model-objects/{dmo_name}
```

Response structure (same as individual object in list response, but wrapped in paginated format).

## Error Handling

**Common Issues:**

1. **Org not connected**
   - Message: "Org not connected"
   - Solution: Ask user to authenticate via SF CLI
2. **DLO not found**
   - Message: "DLO 'XYZ\_\_dll' not found"
   - Solution: List all DLOs first to verify name
3. **DMO not found**
   - Message: "DMO 'XYZ\_\_dlm' not found"
   - Solution: List all DMOs first to verify name
4. **Permission issues**
   - Message: HTTP 403 errors
   - Solution: Verify user has Data Cloud permissions
5. **API version mismatch**
   - Current: v64.0
   - Solution: Script can be updated for newer API versions

## Example Usage

**Example 1: List all DLOs**

```txt
User: "Show me all DLOs in afvibe org"

Response:
1. Run sf org list to discover connected org alias
2. Authenticate to afvibe
3. Run: python3 ./scripts/get_dlo_schema.py afvibe
4. Display formatted list of DLOs
```

**Example 2: Get specific DLO schema**

```txt
User: "Get the schema for Employee__dll in afvibe"

Response:
1. Run sf org list to discover connected org alias
2. Authenticate to afvibe
3. Run: python3 ./scripts/get_dlo_schema.py afvibe Employee__dll
4. Display field schema with types and metadata
```

**Example 3: Explore DLOs then get schema**

```txt
User: "What DLOs exist in myorg and show me the schema for the Employee one"

Response:
1. Run sf org list to discover connected org alias
2. List all DLOs in myorg
3. Identify Employee__dll
4. Get detailed schema for Employee__dll
5. Present both results
```

**Example 4: List all DMOs**

```txt
User: "Show me all DMOs in afvibe org"

Response:
1. Run sf org list to discover connected org alias
2. Authenticate to afvibe
3. Run: python3 ./scripts/get_dmo_schema.py afvibe
4. Display formatted list of DMOs
```

**Example 5: Get specific DMO schema**

```txt
User: "Get the schema for Individual__dlm in afvibe"

Response:
1. Run sf org list to discover connected org alias
2. Authenticate to afvibe
3. Run: python3 ./scripts/get_dmo_schema.py afvibe Individual__dlm
4. Display field schema with types and metadata
```

**Example 6: Explore DMOs then get schema**

```txt
User: "What DMOs exist in myorg and show me the schema for the Individual one"

Response:
1. Run sf org list to discover connected org alias
2. List all DMOs in myorg
3. Identify Individual__dlm
4. Get detailed schema for Individual__dlm
5. Present both results
```

## Output Format

### DLO List Output

```txt
Found 5 DLOs in org 'afvibe':

1. DataCustomCodeLogs__dll
   Label: DataCustomCodeLogs
   Category: Engagement
   Records: 233

2. Employee__dll
   Label: Employee
   Category: Profile
   Records: 12

[...]
```

### DLO Schema Output

```yaml
DLO: Employee__dll
Label: Employee
Category: Profile
Status: ACTIVE
Records: 12

Custom Fields:
  • id__c (Text) - Primary Key
  • name__c (Text)
  • position__c (Text)
  • manager_id__c (Number)

System Fields:
  • DataSource__c (Text)
  • InternalOrganization__c (Text)
  • cdp_sys_SourceVersion__c (Text)

Next steps:
- Query data: SELECT * FROM Employee__dll LIMIT 10
- Create segment based on position field
- Set up data stream for real-time updates
```

### DMO List Output

```txt
Found 10 DMOs in org 'afvibe':

1. Individual__dlm
   Label: Individual
   Category: Profile

2. ContactPointEmail__dlm
   Label: Contact Point Email
   Category: Profile

[...]
```

### DMO Schema Output

```yaml
DMO: Individual__dlm
Label: Individual
Category: Profile
Description: Represents an individual person

Fields:
  • Id__c (Text) - Primary Key
  • FirstName__c (Text)
  • LastName__c (Text)
  • BirthDate__c (DateTime)

Next steps:
- Query data: SELECT * FROM Individual__dlm LIMIT 10
- View DLO mappings to this DMO
- Create calculated insights
```
