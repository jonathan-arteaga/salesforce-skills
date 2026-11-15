## 4. Master-Detail Relationship Rules CRITICAL

Master-Detail fields have **strict attribute restrictions** that differ from Lookup fields. Violating these rules causes deployment failures.

### Forbidden Attributes on Master-Detail Fields

**NEVER include these attributes on Master-Detail fields:**

| Forbidden Attribute | Why | What Happens |
| --- | --- | --- |
| `<required>` | Master-Detail is ALWAYS required by design | Deployment error |
| `<deleteConstraint>` | Master-Detail ALWAYS cascades deletes | Deployment error |
| `<lookupFilter>` | Only supported on Lookup fields | Deployment error |

### Master-Detail vs Lookup Comparison

| Attribute | Master-Detail | Lookup |
| --- | --- | --- |
| `<required>` | FORBIDDEN | Optional |
| `<deleteConstraint>` | FORBIDDEN (always CASCADE) | Required (`SetNull`, `Restrict`, `Cascade`) |
| `<lookupFilter>` | FORBIDDEN | Optional |
| `<relationshipOrder>` | Required (0 or 1) | Not applicable |
| `<reparentableMasterDetail>` | Optional | Not applicable |
| `<writeRequiresMasterRead>` | Optional | Not applicable |

### INCORRECT — Master-Detail with forbidden attributes:

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Account__c</fullName>
  <type>MasterDetail</type>
  <referenceTo>Account</referenceTo>
  <relationshipName>Contacts</relationshipName>
  <relationshipOrder>0</relationshipOrder>
  <required>true</required>                     <!-- WRONG: remove -->
  <deleteConstraint>Cascade</deleteConstraint>  <!-- WRONG: remove -->
  <lookupFilter>...</lookupFilter>              <!-- WRONG: remove entire block -->
</CustomField>
```

**Errors:** `Master-Detail Relationship Fields Cannot be Optional or Required` · `Can not specify 'deleteConstraint' for a CustomField of type MasterDetail` · `Lookup filters are only supported on Lookup Relationship Fields`

### CORRECT — Master-Detail field:

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Account__c</fullName>
  <label>Account</label>
  <description>Links this record to its parent Account</description>
  <type>MasterDetail</type>
  <referenceTo>Account</referenceTo>
  <relationshipLabel>Child Records</relationshipLabel>
  <relationshipName>ChildRecords</relationshipName>
  <relationshipOrder>0</relationshipOrder>
  <reparentableMasterDetail>false</reparentableMasterDetail>
  <writeRequiresMasterRead>false</writeRequiresMasterRead>
  <!-- NO required, deleteConstraint, or lookupFilter -->
</CustomField>
```

### CORRECT — Lookup field (with optional attributes):

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Related_Account__c</fullName>
  <label>Related Account</label>
  <description>Optional link to a related Account</description>
  <type>Lookup</type>
  <referenceTo>Account</referenceTo>
  <relationshipLabel>Related Records</relationshipLabel>
  <relationshipName>RelatedRecords</relationshipName>
  <required>false</required>
  <deleteConstraint>SetNull</deleteConstraint>
  <lookupFilter>
    <active>true</active>
    <filterItems>
      <field>Account.Type</field>
      <operation>equals</operation>
      <value>Customer</value>
    </filterItems>
    <isOptional>false</isOptional>
  </lookupFilter>
</CustomField>
```

### Additional Master-Detail Rules

- **Relationship Order:** First Master-Detail on object = `0`, second = `1`
- **Relationship Name:** Must be a plural PascalCase string (e.g., `Travel_Bookings`)
- **Junction Objects:** Use two Master-Detail fields for standard many-to-many (enables Roll-ups)
- **Limit:** Maximum 2 Master-Detail relationships per object. Use Lookup for additional relationships.

---

## 5. Roll-Up Summary Field Rules CRITICAL

Roll-up Summary fields have the **highest deployment failure rate**. Follow these rules exactly.

### Required Elements for Roll-Up Summary

| Element | Requirement | Format |
| --- | --- | --- |
| `<type>` | Required | Always `Summary` |
| `<summaryOperation>` | Required | `count`, `sum`, `min`, or `max` |
| `<summaryForeignKey>` | Required | `ChildObject__c.MasterDetailField__c` |
| `<summarizedField>` | Conditional | Required for `sum`, `min`, `max`. NOT for `count` |

### Forbidden Elements on Roll-Up Summary

**NEVER include these attributes on Roll-Up Summary fields:**

| Forbidden Attribute | Why |
| --- | --- |
| `<precision>` | Summary inherits from summarized field |
| `<scale>` | Summary inherits from summarized field |
| `<required>` | Not applicable to Summary fields |
| `<length>` | Not applicable to Summary fields |

### Format Rules for summaryForeignKey and summarizedField

**CRITICAL:** Both `summaryForeignKey` and `summarizedField` MUST use the fully qualified format:

```txt
ChildObjectAPIName__c.FieldAPIName__c
```

**Decision Logic:**

- `summaryForeignKey` = `ChildObject__c.MasterDetailFieldOnChild__c`
- `summarizedField` = `ChildObject__c.FieldToSummarize__c`

### INCORRECT — Roll-Up Summary with common errors:

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Total_Amount__c</fullName>
  <label>Total Amount</label>
  <type>Summary</type>
  <precision>18</precision>           <!-- WRONG: Remove - inherited from source -->
  <scale>2</scale>                    <!-- WRONG: Remove - inherited from source -->
  <summaryOperation>sum</summaryOperation>
  <summaryForeignKey>Order__c</summaryForeignKey>        <!-- WRONG: Missing field name -->
  <summarizedField>Amount__c</summarizedField>           <!-- WRONG: Missing object name -->
</CustomField>
```

**Errors:**

- `Can not specify 'precision' for a CustomField of type Summary`
- `Must specify the name in the CustomObject.CustomField format (e.g. Account.MyNewCustomField)`

### CORRECT — Roll-Up Summary (SUM operation):

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Total_Amount__c</fullName>
  <label>Total Amount</label>
  <description>Sum of all line item amounts</description>
  <inlineHelpText>Automatically calculated from child line items</inlineHelpText>
  <type>Summary</type>
  <summaryOperation>sum</summaryOperation>
  <summarizedField>Order_Line_Item__c.Amount__c</summarizedField>
  <summaryForeignKey>Order_Line_Item__c.Order__c</summaryForeignKey>
  <!-- NO precision, scale, required, or length -->
</CustomField>
```

**COUNT:** like SUM but <b>omit </b>**`<summarizedField>`** (keep `<summaryForeignKey>`). **MIN / MAX:** like SUM with `<summaryOperation>min</summaryOperation>` or `max`.

### Roll-Up Summary Quick Reference

| Operation | summarizedField Required? | Use Case |
| --- | --- | --- |
| `count` | NO | Count number of child records |
| `sum` | YES | Add up numeric values |
| `min` | YES | Find smallest value |
| `max` | YES | Find largest value |

### Roll-Up Summary Prerequisites

- Roll-Up Summary fields can ONLY be created on the **parent** object in a Master-Detail relationship
- The child object MUST have a Master-Detail field pointing to this parent
- The summarized field must exist on the child object

---

## 6. Formula Field Rules

### Formula Result Types

A Formula is not a type itself. The `<formula>` tag is added to a field whose `<type>` is the **result data type** (`Checkbox`, `Currency`, `Date`, `DateTime`, `Number`, `Percent`, `Text`).

- <b>A formula field never carries </b>**`<length>`** — not even a Text-result formula. The API rejects it: `Can not specify a length for CustomFields that have a formula`.

### Formula XML Generation Rules

- The contents of the `<formula>` tag MUST be wrapped in `<![CDATA[ ... ]]>`, so the parser does not read formula operators (`&`, `<`, `>`) as XML markup.
- If the formula text itself contains the literal sequence `]]>`, escape it by breaking the CDATA block: e.g., `<![CDATA[Text_Field__c & "]]]]><![CDATA[>"]]>`
- NEVER use an attribute or tag named `returnType`. This does not exist in the Metadata API. The `<type>` tag defines the return data type of the formula result.

### formulaTreatBlanksAs Rule

**Decision Logic:**

- IF formula result type = `Number`, `Currency`, or `Percent` → set `<formulaTreatBlanksAs>BlankAsZero</formulaTreatBlanksAs>`
- IF formula result type = `Text`, `Date`, or `DateTime` → set `<formulaTreatBlanksAs>BlankAsBlank</formulaTreatBlanksAs>`

### INCORRECT — Using Formula as type:

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Calculated_Value__c</fullName>
  <type>Formula</type>  <!-- WRONG: Formula is not a valid type -->
  <returnType>Number</returnType>  <!-- WRONG: returnType does not exist in Metadata API -->
  <formula>Field1__c + Field2__c</formula>  <!-- WRONG: Missing CDATA wrapper -->
</CustomField>
```

### CORRECT — Formula field:

```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
  <fullName>Calculated_Value__c</fullName>
  <label>Calculated Value</label>
  <description>Sum of Field1 and Field2</description>
  <type>Number</type>  <!-- Result type, not "Formula" -->
  <precision>18</precision>
  <scale>2</scale>
  <formula><![CDATA[Field1__c + Field2__c]]></formula>
  <formulaTreatBlanksAs>BlankAsZero</formulaTreatBlanksAs>
</CustomField>
```

### Formula Field Dependencies & Functions

- Formula fields that reference other fields fail deployment if the referenced field doesn't exist or hasn't deployed yet — deploy referenced fields first.
- Use `ISPICKVAL()` (not `==`) for picklist comparisons.
- For the full formula-function reference (TEXT/VALUE/CASE/DAY/MONTH/DATEVALUE/ISCHANGED type rules), defer to the `platform-validation-rule-generate` skill, which owns formula-function correctness.

---
