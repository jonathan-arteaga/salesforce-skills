# Custom Objects & Custom Fields Metadata XML

Generate deployment-ready SFDX source-format metadata under `force-app/main/default/objects/<Object>/`.

## CustomObject Rules (`.object-meta.xml`)

- **Required elements**: `<label>`, `<pluralLabel>`, `<sharingModel>`, `<deploymentStatus>Deployed</deploymentStatus>`, `<visibility>Public</visibility>`, `<nameField>` (`<label>` + `<type>` of `Text` or `AutoNumber` with `<displayFormat>` and `<startingNumber>`), and `<description>`.
- **No root `<fullName>`**: API name comes from the filename (`Vehicle__c.object-meta.xml`). Never put `<fullName>` directly under `<CustomObject>`.
- **Sharing model**: Default `ReadWrite`; MUST be `ControlledByParent` if the object has any Master-Detail field (and update existing child objects to `ControlledByParent` when adding one).
- **Clean XML**: Only include `<enableSearch>`, `<enableReports>`, `<enableActivities>`, `<enableHistory>` as `true` on user-facing objects; omit default `false` tags on junctions/logs.
- **Validation rules**: Names must start with a letter, use alphanumeric + single underscores, never end in `_`, and NEVER end with `__c` (e.g., `Require_Start_Date`).
- **Reserved words**: Avoid `Select`, `From`, `Where`, `Limit`, `Order`, `Group`, `User`, `External`, `View`, `Type`, `Date`, `Number` as bare API names.
- **Description enrichment**: Write a concise (<= 50 words) human-readable `<description>` using field labels (purpose -> key fields with constraints -> computed behavior -> validation rules -> "Commonly used for..."). For brand-new objects, write directly; for ANY field or validation-rule change on an existing object, preserve existing domain context, show the proposed vs. current text, and WAIT for explicit user approval (`yes / keep current / edit`) per change.

## CustomField Rules (`.field-meta.xml`)

Save each field at `force-app/main/default/objects/<Object>/fields/<FieldName>__c.field-meta.xml`. Never place XML comments (`<!-- ... -->`) before `<CustomField>` (breaks SDR parser). Always populate `<fullName>`, `<label>`, `<description>`, and actionable `<inlineHelpText>`. Set `<externalId>true</externalId>` on `Text`, `Number`, or `Email` external keys.

| Field Type | Required Attributes | Forbidden / Critical Rules |
| --- | --- | --- |
| `Text` / `TextArea` | `Text`: `<length>` (<= 255); `TextArea`: none | NEVER include `<length>` on `TextArea` (fixed at 255 implicitly) |
| `LongTextArea` / `Html` | `<length>`, `<visibleLines>` | Default visible lines: 3 (LongTextArea), 25 (Html) |
| `Number` / `Currency` / `Percent` | `<precision>` (<= 18), `<scale>` (<= precision) | Left digits = `precision - scale`; defaults: Currency 18/2, Percent 5/2 |
| `Lookup` | `<referenceTo>`, `<relationshipName>` (plural PascalCase), `<deleteConstraint>` (`SetNull`/`Restrict`/`Cascade`) | Max 15 lookups per object; optional `<lookupFilter>` |
| `MasterDetail` | `<referenceTo>`, `<relationshipName>`, `<relationshipOrder>` (`0` or `1`) | FORBIDDEN: `<required>`, `<deleteConstraint>`, `<lookupFilter>`. Max 2 per object; child object needs `ControlledByParent` |
| `Summary` (Roll-Up) | `<type>Summary</type>`, `<summaryOperation>` (`count`/`sum`/`min`/`max`), `<summaryForeignKey>` (`Child__c.MD__c`), `<summarizedField>` (except `count`) | FORBIDDEN: `<precision>`, `<scale>`, `<required>`, `<length>`; omit `<summarizedField>` for `count` |
| Formula | `<type>` = result type (never `Formula`), `<formula>` in `<![CDATA[...]]>`, `<formulaTreatBlanksAs>` (`BlankAsZero` or `BlankAsBlank`) | FORBIDDEN: `<returnType>`, `<length>`; referenced fields must deploy first |

## Minimal Verified XML Shapes (High-Failure Types)

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Account__c</fullName>
  <label>Account</label>
  <description>Links child record to its parent Account.</description>
  <inlineHelpText>Select the owning parent Account.</inlineHelpText>
  <type>MasterDetail</type>
  <referenceTo>Account</referenceTo>
  <relationshipLabel>Child Records</relationshipLabel>
  <relationshipName>Child_Records</relationshipName>
  <relationshipOrder>0</relationshipOrder>
  <reparentableMasterDetail>false</reparentableMasterDetail>
  <writeRequiresMasterRead>false</writeRequiresMasterRead>
</CustomField>
```

## Picklists, Value Sets & Record Types

- **Restricted default**: Set `<restricted>true</restricted>` inside `<valueSet>` unless the user explicitly asks for an open picklist (capped at 1,000 total values).
- **Inline vs. reference**: `<valueSet>` holds EITHER `<valueSetDefinition>` OR `<valueSetName>` — never both. Reference StandardValueSets (`Industry`) and GlobalValueSets (`Priority_Levels`) by bare developer name with NO `__gvs` or `__c`.
- **Value-name fidelity**: Keep picklist value `<fullName>` and `<label>` matching the user's spelling including spaces (`Closed Won`, not `Closed_Won`); start with a letter and avoid hyphens.
- **Dependent picklists (API 38+)**: Use `<controllingField>` plus one `<valueSettings>` (`<controllingFieldValue>` + `<valueName>`) per valid pair. Both controlling and dependent fields MUST be `<restricted>true</restricted>`. Never emit deprecated `<picklist>`/`<picklistValues>`/`<controllingFieldValues>` field tags.
- **RecordType picklist scoping**: Per-record-type picklist visibility lives on `RecordType` (`<picklistValues>`). Only `Opportunity`, `Lead`, `Case`, and `Solution` require a coupled `businessProcesses/<Name>.businessProcess-meta.xml` and `<businessProcess>` reference; custom objects and other standard objects need no BusinessProcess.

## Common Metadata Deploy Fixes

- `ConversionError: Invalid XML tags` -> Remove XML comments placed before `<CustomField>`.
- `Cannot set sharingModel to ReadWrite` -> Update child `.object-meta.xml` to `<sharingModel>ControlledByParent</sharingModel>`.
- `Required field is missing: businessProcess` -> Pair `Opportunity`/`Lead`/`Case`/`Solution` RecordType with its `businessProcesses/*.businessProcess-meta.xml`.
