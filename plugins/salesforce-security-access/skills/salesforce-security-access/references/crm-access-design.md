# CRM Access Design Reference

Design, audit, and troubleshoot Salesforce CRM authorization using least-privilege Permission Sets, Permission Set Groups, muting sets, Org-Wide Defaults (OWD), and sharing controls.

## 1. Establish Business Operations per Persona

Before inspecting metadata or proposing changes, map each persona separately:

- **Persona classes**: Employee users, integration users, Agentforce agent users, and external/Experience Cloud users.
- **Per-object operations**: Create, Read, Edit, Delete, View All, Modify All, plus sensitive fields (read vs edit separately).
- **Record population**: Own records, role-hierarchy subordinates, team/queue records, criteria-matched records, or restricted subsets.
- **Actual execution identity**: Resolve the true running user for each UI, API, Flow, Apex, or Agent action. Admin tests do not validate persona access.

## 2. Read-Only Discovery Checklist

Inspect current access before changing anything (pin `--target-org <user-or-alias>`):

```bash
sf data query --target-org <org> --json \
  --query "SELECT Assignee.Username, PermissionSet.Name, PermissionSet.IsOwnedByProfile, PermissionSetGroup.DeveloperName FROM PermissionSetAssignment WHERE Assignee.Username = '<username>'"

sf data query --target-org <org> --json \
  --query "SELECT SobjectType, PermissionsRead, PermissionsCreate, PermissionsEdit, PermissionsDelete, PermissionsViewAllRecords, PermissionsModifyAllRecords FROM ObjectPermissions WHERE Parent.Name = '<PermSetName>'"

sf data query --target-org <org> --json \
  --query "SELECT Field, PermissionsRead, PermissionsEdit FROM FieldPermissions WHERE Parent.Name = '<PermSetName>' AND SobjectType = '<ObjectApiName>'"
```

Distinguish five different root causes when access fails or leaks:
1. Missing object CRUD or field FLS grant.
2. Record visibility blocked by OWD, hierarchy, sharing rules, or restriction/scoping rules.
3. User license or permission-set license limitation.
4. Session-level or execution-context difference (e.g., high-assurance session, Flow system mode, Apex `without sharing`).
5. Pending Permission Set Group recalculation (`PermissionSetGroup.Status != 'Updated'`).

## 3. Desired vs Effective Access Matrix & Muting Rules

| Symptom | Inspect Before Changing Access | Evidence to Retain |
| --- | --- | --- |
| User sees object but cannot edit field | Object Edit, Field Edit, record Edit access, page layout / Dynamic Forms, validation/automation | Assignment snapshot and exact failing operation |
| Field remains visible after muting | Profile, direct Permission Sets, other PSGs, and View All Fields where supported | Every independent grant path, not only the edited PSG |
| Admin works, persona or agent fails | Actual running user, CRUD/FLS, row sharing, license assignment | Target-identity execution result |
| User sees too many records | OWD, Role Hierarchy, sharing rules, manual/Apex shares, View All / Modify All, restriction rules | Unexpected synthetic record IDs returned |

Key architecture rules:
- **Task-based Permission Sets + Persona PSGs**: Group atomic functional permissions into task-based Permission Sets and compose them into role/persona Permission Set Groups with a named owner. Avoid bloated monolithic profiles or mechanically generating every object/CRUD permutation.
- **Muting Permission Sets**: A muting permission set only mutes grants originating inside the same PSG (and propagates permission dependencies). It CANNOT subtract a grant given via Profile, a direct Permission Set, or another PSG.
- **View All / Modify All / View All Fields**: Treat as high-impact exceptions. Document business justification, blast radius, and reviewer sign-off; never apply as a quick fix.
- **Restriction / Scoping Rules**: Verify current release and object support before prescribing restriction rules; do not assume support across every standard object or execution mode.

## 4. Interaction with Apex and Flow Security

- **Apex API 67.0+ vs 66.0 and earlier**: API 67.0+ defaults database operations to user mode and rejects `WITH SECURITY_ENFORCED`. Use explicit sharing (`with sharing` / `inherited sharing`) and explicit `WITH USER_MODE` / `AccessLevel.USER_MODE` across versions.
- **System-mode code**: Configuration cannot override `without sharing` or `SYSTEM_MODE` queries/DML. When a leak or bypass originates in code or Flow context, hand off implementation fixes to `salesforce-apex` or `salesforce-flow`.

## 5. Sandbox Allow/Deny Verification Matrix

Run authorized sandbox tests with synthetic data as the **actual target persona** (after confirming PSG status is `Updated`):

| Test Case | Expected Outcome | What It Proves |
| --- | --- | --- |
| Allowed CRUD on owned/shared synthetic record | Succeeds | Baseline persona operation works |
| Allowed field read vs denied sensitive field read/edit | Allowed field succeeds; sensitive field denied | FLS enforced independently of object access |
| Unrelated record outside sharing scope | Not returned / edit denied | OWD + sharing boundary holds |
| Direct-grant vs PSG-muting test | Direct grant still applies; PSG-only grant muted | Additive grant model verified accurately |
| Alternate persona / cross-role negative test | Denied | No unintended privilege leakage |

## 6. Deliverable Workbook & Handoffs

Every CRM access engagement produces:
1. **Desired vs Effective Matrix** (persona, object, field, record scope, current grant paths).
2. **Proposed Diff** (new/edited Permission Sets, PSGs, muting sets, OWD/sharing changes, named owners).
3. **Metadata Readiness**: Generate deployment-ready XML only for verified API names and supported metadata types; mark unresolved org items explicitly. Hand off deployment to `salesforce-devops-deploy`.
4. **Verification Report**: Separate local drafts, executed sandbox allow/deny evidence, and untested production items.
5. **Rollback Plan**: Exact prior assignments, OWD values, and sharing rules needed to revert safely.

## Sources Verified

- Permission Set Groups: `https://help.salesforce.com/s/articleView?id=platform.perm_set_groups.htm&release=264.0.0&type=5`
- Object Permissions: `https://help.salesforce.com/s/articleView?id=platform.users_profiles_object_perms.htm&release=264.0.0&type=5`
- Field Permissions: `https://help.salesforce.com/s/articleView?id=platform.users_profiles_fls.htm&release=264.0.0&type=5`
- Apex Security and Sharing Model: `https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_security_sharing_chapter.htm`
