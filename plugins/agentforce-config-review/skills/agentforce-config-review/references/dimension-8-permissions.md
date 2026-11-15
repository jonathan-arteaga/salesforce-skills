# Dimension 8 — Permissions, Identity & Access Control

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Contents

- Dimension 8 — Permissions, Identity & Access Control
  - Gate — Metadata required before filing any finding
  - A — Identify the Running User (Service / SDR agents)
  - B — Apex Class Access
  - C — Object CRUD
  - D — Field-Level Security (FLS)
  - E — Named Credential / External Credential Access
  - F — Permission Set Hygiene
  - Severity Summary

## Dimension 8 — Permissions, Identity & Access Control

> **REQUIRED for Service Agents and SDR/Sales Agents. NOT optional for these agent types.** Excluded from composite score (so findings do not skew the 7-dimension average), but findings feed Section 9 (Priority Remediation) at full severity and can block go-live. The scorecard in Section 8 shows a "Permission Readiness" row with one of: `CRITICAL GAPS` / `HIGH GAPS` / `NO GAPS CONFIRMED` / `NOT RUN — metadata required` — and the note *"Excluded from composite — requires org verification."*

> **When D8 is required:** Service Agents and SDR/Sales Agents (dedicated running user). **When D8 is not run:** Employee Agents (running user context — see `references/agent-type-variants.md`), Field Service Agents, AgentScript Agents. If you are reviewing a Service Agent or SDR agent and D8 was not run, that is an incomplete review — return to the D8 Execution Gate in Rule 3 and run it now.

---

### Gate — Metadata required before filing any finding

**Do not file any D8 finding without first reading the action schemas.** The correct check is:

1. **Check if action schemas are already local:**
```bash
find <project-root>/force-app/main/default/genAiPlannerBundles -name "schema.json" | sort
find <project-root>/force-app/main/default -name "*.genAiFunction-meta.xml" -o -name "*.genAiPlugin-meta.xml" | sort
```

2. **If not local and org is connected — prompt the FDE to retrieve them:**
```bash
sf project retrieve start --metadata "GenAiFunction" --target-org <alias>
sf project retrieve start --metadata "GenAiPlugin" --target-org <alias>
```

3. **If neither is available** — do not run D8. Set permission readiness to `NOT RUN — metadata required` in the scorecard and include this note:
> *"Dimension 8 was not run. Action schema metadata (GenAiFunction / GenAiPlugin) is required to determine which Apex classes, objects, and fields the running user must access. Retrieve with `sf project retrieve start --metadata "GenAiFunction" --target-org <alias>` and re-run the review to complete this dimension."*

**Only proceed once action schemas are confirmed read.**

---

### A — Identify the Running User (Service / SDR agents)

Confirm which user the agent runs as in production. Either:
- FDE provides the username directly, or
- Query the org:
```bash
sf data query --query "SELECT Id, Name, Username, Profile.Name FROM User \
  WHERE IsActive = true \
  AND (Profile.Name LIKE '%Einstein%' OR Profile.Name LIKE '%Agent%' \
    OR Username LIKE '%agentforce%' OR Username LIKE '%restaurant%' OR Username LIKE '%agent%')" \
  --target-org <alias>
```

Once identified, retrieve their permission sets:
```bash
sf data query --query "SELECT PermissionSetId FROM PermissionSetAssignment \
  WHERE AssigneeId = '<userId>'" --target-org <alias>

sf data query --query "SELECT Id, Name, Label FROM PermissionSet \
  WHERE Id IN ('<id1>','<id2>',...)" --target-org <alias>
```

Also check for permission set license assignments — some access (e.g. VoiceCall for voice agents) is license-controlled and will NOT appear in ObjectPermissions or FieldPermissions queries:
```bash
sf data query --query "SELECT PermissionSetLicense.DeveloperName \
  FROM PermissionSetLicenseAssign WHERE AssigneeId = '<userId>'" \
  --target-org <alias>
```

> **Voice agent note:** VoiceCall object access is granted via the `ServicePlannerAgentUserPsl` permission set license — it never appears in ObjectPermissions or FieldPermissions SOQL. If this PSL is assigned, mark VoiceCall access as PASS. Never file a VoiceCall gap finding based on absent ObjectPermissions rows alone.

---

### B — Apex Class Access

From the action schemas, identify every Apex class invoked (invocable methods called from GenAiFunction or Flow actions). Then check:

```bash
sf data query --query "SELECT SetupEntityId, SetupEntityType, ParentId \
  FROM SetupEntityAccess WHERE SetupEntityType = 'ApexClass' \
  AND ParentId IN ('<permSetId1>','<permSetId2>',...)" \
  --target-org <alias>

# Resolve class names
sf data query --query "SELECT Id, Name FROM ApexClass \
  WHERE Id IN ('<classId1>','<classId2>',...)" --target-org <alias>
```

Cross-reference: every Apex class invoked by an action must appear in the granted set.
- Class invoked by action + not granted → **CRITICAL** — throws `INSUFFICIENT_ACCESS` at runtime; action fails silently in Testing Center and production
- Class granted but not invoked by any action → note as over-permissioned (MEDIUM if significant)

**Perm set structure check:** If there is a dedicated agent permission set (e.g. `Restaurant_Agentforce_Voice_Permissions`) that contributes zero Apex entries, flag as **MEDIUM** — indicates the perm set was not curated for this agent and Apex grants may be missing or misattributed to a generic base perm set.

---

### C — Object CRUD

From the action schemas, determine for each object whether actions perform read-only SOQL or DML (insert/update). Then check:

```bash
sf data query --query "SELECT SobjectType, PermissionsRead, PermissionsCreate, \
  PermissionsEdit, PermissionsDelete FROM ObjectPermissions \
  WHERE ParentId IN ('<permSetId1>','<permSetId2>',...) \
  AND SobjectType IN ('Case','Contact','Account','Task','EmailMessage','CaseComment',...)" \
  --target-org <alias>
```

Severity rules — only applicable when action schemas confirm the operation:

| Situation | Severity |
|---|---|
| Action schema confirms DML on this object + Create/Edit missing | **CRITICAL** |
| Action schema confirms Read only + Create/Edit missing | Not a finding |
| Action schemas not reviewed / object not referenced in schemas | Do not file — prompt FDE to retrieve schemas first |

---

### D — Field-Level Security (FLS)

From the action schemas, identify every field read (input) or written (output). Then check:

```bash
sf data query --query "SELECT SobjectType, Field, PermissionsRead, PermissionsEdit \
  FROM FieldPermissions \
  WHERE ParentId IN ('<permSetId1>','<permSetId2>',...) \
  AND SobjectType IN ('Case','Contact','Account','Task','EmailMessage',...)" \
  --target-org <alias>
```

> **Important:** FLS is only queryable via permission sets, not profile-level directly. The profile-backed permission set (same ID as the Profile) is automatically included in PermissionSetAssignment — always include it in the ParentId list.

Severity rules:

| Situation | Severity |
|---|---|
| Action schema confirms field is written + Edit FLS missing | **CRITICAL** — DML silently omits the field or throws |
| Action schema confirms field is read + Read FLS missing | **HIGH** — field returns null; planner sees missing data |
| Field not referenced in any action schema | Skip |

---

### E — Named Credential / External Credential Access

If any action makes an external callout, verify the running user has access to the Named Credential or External Credential:

```bash
sf data query --query "SELECT SetupEntityId, SetupEntityType FROM SetupEntityAccess \
  WHERE SetupEntityType IN ('NamedCredential','ExternalCredential') \
  AND ParentId IN ('<permSetId1>','<permSetId2>',...)" \
  --target-org <alias>
```

- Callout action present + Named Credential not granted → **CRITICAL** — callout throws `CALLOUT_EXCEPTION`

---

### F — Permission Set Hygiene

- **No dedicated agent permission set:** running user relies entirely on the generic Einstein Agent User profile-backed perm set → **HIGH** — over-permissioned; hard to audit
- **Dedicated perm set present but cloned from another agent type** (e.g. chat classes on a voice agent) → **MEDIUM** — violates least-privilege; identify and remove irrelevant grants
- **Over-permissioned beyond action schema requirements** → **MEDIUM** — flag specific excess grants

---

### Severity Summary

| Check | Severity if failing |
|---|---|
| Apex class invoked by action + not granted | CRITICAL |
| DML object + Create/Edit missing | CRITICAL |
| External callout + Named Credential not granted | CRITICAL |
| FLS Edit missing on a field written by an action | CRITICAL |
| FLS Read missing on a field read by an action | HIGH |
| No dedicated agent permission set | HIGH |
| Dedicated perm set contributes zero Apex entries | MEDIUM |
| Perm set cloned from wrong agent type (irrelevant grants) | MEDIUM |
| Over-permissioned beyond action schema requirements | MEDIUM |

---
