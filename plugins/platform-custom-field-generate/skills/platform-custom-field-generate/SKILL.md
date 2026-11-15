---
name: |-
  platform-custom-field-generate
description: |-
  Create or validate Salesforce custom field metadata. Return fields and type-specific validation. Use platform-custom-object-generate for object-level metadata.
---

For release-sensitive Salesforce work, consult [current Salesforce guidance](references/current-salesforce/guide.md) and verify the target org/version before applying examples.


# Salesforce Custom Field Generator and Validator

Use an available value-set workflow for changes to a shared value set. This skill owns the field that references it.

## Overview

Generates and validates Salesforce CustomField metadata XML, with special handling for the **highest-failure-rate types** — Roll-Up Summary and Master-Detail. The agent must verify the constraints below before outputting XML to prevent Metadata API deployment errors.

---

## 1. Universal Mandatory Attributes

Every generated field must include these tags:

| Attribute | Requirement | Notes |
| --- | --- | --- |
| `<fullName>` | Required | **Field** name only: derive from `<label>` — capitalize each word, replace spaces with `_`, append `__c`. Must start with a letter. E.g., label `Total Contract Value` → `Total_Contract_Value__c`. This rule is for the FIELD name. <b>Picklist VALUE </b>**`<fullName>`**<b> is different — keep it exactly as the user spelled it, spaces and all, no </b>**`__c`** (e.g. `Closed Won`, NOT `Closed_Won`). See [`references/advanced-picklists.md`](references/advanced-picklists.md) (ref §3). |
| `<label>` | Required | The UI name (Title Case) |
| `<description>` | Always include | Explain the business reason *why* this field exists. |
| `<inlineHelpText>` | Always include | Actionable end-user guidance that adds value beyond the label (e.g., "Enter the value in USD including tax", not "The amount"). |

`<description>` and `<inlineHelpText>` are mandatory even though the Metadata API does not enforce them — omitting them yields low-quality metadata.

**File path (SFDX source format):** save each field as `force-app/main/default/objects/<Object>/fields/<FieldName>__c.field-meta.xml`, where `<Object>` is the object's API name (`Account`, `Opportunity`, or a custom `Inventory_Item__c`). A correct XML at the wrong path is never seen by the Metadata API.

### External ID Configuration

**Trigger:** If the user mentions "integration," "importing data," "external system ID," or "unique key from \[System Name\]," set `<externalId>true</externalId>`.

**Applicable Types:** Text, Number, Email

---

## 2. Precision, Scale, and Length Rules

To ensure deployment success, follow these mathematical constraints:

### Precision vs. Scale Rules

- `precision` is the total digits; `scale` is the decimal digits
- **Rule:** `precision ≤ 18` AND `scale ≤ precision`
- **Calculation:** Digits to the left of decimal = `precision - scale`

### The "Fixed 255" Rule

<b>TextArea: do NOT include </b>**`<length>`** — the API fixes it at 255 implicitly and rejects an explicit value ("Can not specify 'length' for a CustomField of type TextArea"). The field needs only `<fullName>`, `<label>`, and `<type>TextArea</type>`.

### Visible Lines

Mandatory for Long/Rich text and Multi-select picklists to control UI height.

---

## 3. Field Data Types

### 3.1 Simple Attribute Types

| Type | `<type>` Value | Required Attributes |
| --- | --- | --- |
| Auto Number | `AutoNumber` | `displayFormat` (must include `{0}`), `startingNumber` |
| Checkbox | `Checkbox` | Default `defaultValue` to `false` |
| Date | `Date` | No precision/length required |
| Date/Time | `DateTime` | No precision/length required |
| Email | `Email` | Built-in format validation |
| Lookup Relationship | `Lookup` | `referenceTo`, `relationshipName`, `deleteConstraint` |
| Master-Detail Relationship | `MasterDetail` | `referenceTo`, `relationshipName`, `relationshipOrder` |
| Number | `Number` | `precision`, `scale` |
| Currency | `Currency` | Default precision: 18, scale: 2 |
| Percent | `Percent` | Default precision: 5, scale: 2 |
| Phone | `Phone` | Standardizes phone number formatting |
| Picklist | `Picklist` | `valueSet` containing EITHER `valueSetDefinition` (inline) OR `valueSetName` (reference); `restricted` (see "Picklist `restricted` default" below; advanced cases in §3.4) |
| Text | `Text` | `length` (Max 255) |
| Text Area | `TextArea` | None — do NOT include `<length>`; the API fixes length at 255 implicitly |
| Text (Long) | `LongTextArea` | `length`, `visibleLines` (default 3) |
| Text (Rich) | `Html` | `length`, `visibleLines` (default 25) |
| Time | `Time` | Stores time only (no date) |
| URL | `Url` | Validates for protocol and format |

### 3.2 Computed & Multi-Value Types

| Type | `<type>` Value | Required Attributes |
| --- | --- | --- |
| Formula | Result type (e.g., `Number`) | `formula`, `formulaTreatBlanksAs` |
| Roll-Up Summary | `Summary` | See Section 5 for complete requirements |
| Multi-Select Picklist | `MultiselectPicklist` | `valueSet`, `visibleLines` (default 4) |

### 3.3 Specialized Types

| Type | `<type>` Value | Required Attributes |
| --- | --- | --- |
| Geolocation | `Location` | `scale`, `displayLocationInDecimal` |

### Picklist `restricted` default

<b>Always set </b>**`<restricted>true</restricted>`** inside `<valueSet>` unless the user explicitly says the picklist should accept custom values not in the admin-defined list (e.g. "unrestricted"/"open"). Restricted sets are capped at 1,000 total values (active + inactive). Minimal inline shape:

```xml
<valueSet>
  <restricted>true</restricted>
  <valueSetDefinition>
    <sorted>false</sorted>
    <value><fullName>Option_A</fullName><default>false</default><label>Option A</label></value>
  </valueSetDefinition>
</valueSet>
```

### 3.4 Advanced Picklists

The inline `<valueSetDefinition>` above is the simple case. Full rules and worked correct/incorrect<br />examples for everything below are in<br />[`references/advanced-picklists.md`](references/advanced-picklists.md) — load it for any<br />non-trivial picklist. Section numbers in parentheses below (e.g. "ref §1") point to that<br />reference file, not to this skill. The hard rules:

- **Value-set reference (ref §1).** A `<valueSet>` holds EITHER `<valueSetName>` (reference) OR<br />`<valueSetDefinition>` (inline) — **never both**. Reference by the **bare** developer name —<br />Standard set `Industry`, GlobalValueSet `Priority_Levels` with <b>NO </b>**`__gvs`** and no `__c`<br />(the `__gvs` suffix is org-storage display only; the Metadata API uses the bare name). A<br />value-set-backed field is `<restricted>true</restricted>`. Creating the value set is the<br />job of an available value-set authoring workflow. This skill references existing sets.
- **Value-name fidelity (ref §3).** A picklist value's `<fullName>`/`<label>` keep the user's exact<br />text **including spaces** (`Closed Won`, never `Closed_Won`). The space→`_` + `__c` rule is for<br />the FIELD name only.
- **Dependent picklists (ref §2).** Use the **modern API 38.0+** form: `<controllingField>` +<br />one `<valueSettings>` (`<controllingFieldValue>`+`<valueName>`) per pair; never the legacy<br />`<picklist>`/`<picklistValues>`/`<controllingFieldValues>` tags. **Both** controlling and<br />dependent fields MUST be `<restricted>true</restricted>`, even if the request doesn't say so.
- **Enhanced value attributes (ref §3).** `<value>` entries also accept `<color>` (hex, leading<br />`#`), `<isActive>` (`false` retires a value), and a value-level `<description>`.
- **Scoping a picklist to a record type (ref §5).** Per-record-type value visibility lives on the<br />**RecordType** (`<picklistValues>`), not the field. The RecordType file carries its own<br />`<fullName>` (bare developer name). **First decide if the object needs a BusinessProcess:**<br />only **Opportunity / Lead / Case / Solution** require one — they won't deploy without a<br />`<businessProcess>` (`Required field is missing: businessProcess`), even when only a custom<br />picklist is filtered. There you emit **two coupled files**: the `businessProcesses/<Name>.businessProcess-meta.xml`<br />file AND a matching `<businessProcess><Name></businessProcess>` inside the `<RecordType>` (after<br />`<active>`, before `<picklistValues>`; the `<fullName>` in the BP file is **bare**, never<br />object-qualified). **Custom objects (****`*__c`****) and all other standard objects (Account, Contact, …)<br />need NO BusinessProcess — emit the RecordType alone; do not invent one.** **Scope limit:**<br />picklist-value visibility per record type only — NOT general record-type authoring (compact<br />layouts, page layouts, branding).

---

For these field types, read [master-detail, roll-up summary, and formula rules](references/relationship-rollup-and-formula-fields.md) before authoring metadata.

## 7. Common Deployment Errors

| Error Message | Cause | Fix |
| --- | --- | --- |
| `ConversionError: Invalid XML tags or unable to find matching parent xml file for CustomField` | XML comments placed before the root `<CustomField>` element | Remove XML comments (`<!-- ... -->`) that appear before `<CustomField>` in the `.field-meta.xml` file |
| `Field [FieldName] does not exist. Check spelling.` | Referenced field does not exist or has not been deployed yet | Verify the referenced field exists and is deployed before this field |
| `DUPLICATE_DEVELOPER_NAME` | Field fullName already exists on the object | Use a unique business-driven name |
| `MAX_RELATIONSHIPS_EXCEEDED` | More than 2 Master-Detail or 15 Lookup fields on the object | Use Lookup for 3rd+ Master-Detail; review Lookup count |
| Reserved keyword error | Using `Order__c`, `Group__c`, etc. | Rename to `Status_Order__c`, etc. |
| `Value set must reference a value set name or define a value set, but not both` | `<valueSet>` has both `<valueSetName>` and `<valueSetDefinition>` | Keep exactly one (see Section 3.4) |
| `duplicate value found: [X] is defined multiple times` | Two `<value>` entries share a `<fullName>` | Make every picklist value `<fullName>` unique |
| `Invalid fullName` on a picklist value | Value `<fullName>` starts with a digit or contains hyphens | Start with a letter; no hyphens, no leading digit. Spaces ARE allowed — do NOT underscore them (see §3.4 value-name fidelity) |
| `Element ...picklist is not allowed` | Deprecated ≤37.0 dependent-picklist syntax (`<picklist>`/`<picklistValues>`/`<controllingFieldValues>`) | Use the modern `valueSettings`/`controllingFieldValue`/`valueName` form (Section 3.4) |

---

## 8. Verification Checklist

Before generating CustomField XML, verify:

### Universal Checks

- [ ] Does `<fullName>` use valid format and end in `__c`?
- [ ] Are `<description>` and `<inlineHelpText>` both populated and meaningful?
- [ ] Is `<label>` in Title Case?
- [ ] Are there no XML comments (`<!-- ... -->`) before the root `<CustomField>` element? (Comments before the root element break SDR's parser)

### Master-Detail Field Checks CRITICAL

- [ ] Is `<required>` attribute ABSENT? (Master-Detail is always required)
- [ ] Is `<deleteConstraint>` attribute ABSENT? (Master-Detail always cascades)
- [ ] Is `<lookupFilter>` block ABSENT? (Only for Lookup fields)
- [ ] Is `<relationshipOrder>` set to `0` or `1`?
- [ ] Is parent object's `<sharingModel>` set to `ControlledByParent`?

### Lookup Field Checks

- [ ] Is `<deleteConstraint>` set to `SetNull`, `Restrict`, or `Cascade`?
- [ ] Is `<relationshipName>` in plural PascalCase?

### Picklist Field Checks

- [ ] Does each `<valueSet>` contain EITHER `<valueSetName>` OR `<valueSetDefinition>` — never both?
- [ ] For a value-set reference: is `<restricted>true</restricted>` set?
- [ ] For a StandardValueSet reference: is the name the bare enum with NO `__c` (e.g. `Industry`)?
- [ ] For a GlobalValueSet reference: is the name the **bare** developer name with NO `__gvs` suffix?
- [ ] For dependent picklists: is `<controllingField>` set, with one `<valueSettings>` (`<controllingFieldValue>` + `<valueName>`) per pair?
- [ ] For dependent picklists: is the deprecated `<picklist>`/`<picklistValues>`/`<controllingFieldValues>` form ABSENT?
- [ ] Are all picklist value `<fullName>` values unique, start with a letter, and free of hyphens? (spaces are allowed — do NOT replace them with underscores, per the §3.4 value-name fidelity rule)

### Roll-Up Summary Field Checks CRITICAL

- [ ] Is `<precision>` attribute ABSENT?
- [ ] Is `<scale>` attribute ABSENT?
- [ ] Is `<summaryForeignKey>` in format `ChildObject__c.MasterDetailField__c`?
- [ ] For SUM/MIN/MAX: Is `<summarizedField>` in format `ChildObject__c.FieldName__c`?
- [ ] For COUNT: Is `<summarizedField>` ABSENT?
- [ ] Does the child object have a Master-Detail field to this parent?

### Formula Field Checks

- [ ] Is `<type>` set to result type (NOT "Formula")?
- [ ] Is `<formula>` content wrapped in `<![CDATA[ ... ]]>`?
- [ ] Is `<returnType>` attribute ABSENT? (does not exist in Metadata API)
- [ ] Is `<length>` ABSENT? (formula fields never carry a length, even Text-result formulas)
- [ ] Is `<formulaTreatBlanksAs>` set to `BlankAsZero` for numeric results or `BlankAsBlank` for text/date results?
- [ ] Do all referenced fields exist and deploy before this field?

### Numeric Field Checks

- [ ] Is `scale ≤ precision`?
- [ ] Is `precision ≤ 18`?

### Text Area Checks

- [ ] For TextArea: Is `<length>` **omitted**? (The API rejects an explicit `<length>` value on TextArea fields.)
- [ ] For LongTextArea/Html: Is `<visibleLines>` set?

### Relationship Limit Checks

- [ ] Are there 2 or fewer Master-Detail relationships on the object?
- [ ] Are there 15 or fewer Lookup relationships on the object?

### Naming Checks

- [ ] Is the API name free of reserved words (`Order`, `Group`, `Select`, etc.)?
- [ ] Is the API name unique on this object?
