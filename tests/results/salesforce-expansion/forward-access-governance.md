# Support access and Data 360 governance — local design draft

Status: **draft, locally checked**. No org connection, live inspection, sandbox execution, deployment, permission assignment, cache purge, export recall or deletion performed. Expected test outcomes below are not results.

## Scope and evidence

Goal: Support can read Cases and update Status only on its team's records, with no Diagnosis read or write. Separately, a Data 360 field denial changed yesterday; a dashboard cache and earlier export may retain the field, and consent was revoked yesterday. These are separate control planes; neither change proves the other is enforced.

Evidence consists solely of the supplied scenario and the two requested skills, including their current Salesforce guidance, workflows, workbook templates and acceptance cases. No Salesforce documentation connector was discovered. Following the task's restriction to these references, no external documentation or other agents' outputs were read. References contain dated official-source baselines (2026-11-15); no independent current verification or target-org applicability is claimed.

Unknown: target org/environment, release/API, licenses, feature availability, actual user and service identities, Case sharing configuration, team membership definition, Diagnosis API name, all grants, Data 360 field/object/data space/policy identifiers, cache architecture and destinations. “Yesterday” is retained as supplied: establish exact effective timestamps and time zone before implementation. Do not assume the Data 360 field is the CRM Diagnosis field.

Named owners must be assigned: CRM access administrator, Support business owner, Billing owner, Data 360 administrator, dashboard owner, downstream/export custodian and privacy/data owner. Local draft preparation is the only authorized scope.

## Salesforce Access Design workbook

### Desired versus effective matrix

| Persona | Identity | Object/field | Operation | Record scope | Current grants | Desired result | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Support | Actual user to resolve | Case | Read | Own team | Unknown object/sharing state | Allow | Scenario requirement; untested |
| Support | Same | Case.Status | Read/update | Own team | Unknown | Allow | Requires object Edit, Status edit and record edit access |
| Support | Same | Other editable Case fields | Update | Any | Unknown | Deny unless business owner explicitly expands scope | Field inventory and update-path review required |
| Support | Same | Diagnosis, API name unresolved | Read/write | All | Profile reads; Support group mutes; independent Billing set reads | Deny both | Scenario establishes independent read grants; write unknown |
| Support | Same | Case | Read/update | Other team | Unknown sharing, hierarchy and broad grants | Deny | Sharing review and target-user tests required |
| Support | Same | Case | Create/delete | Any | Unknown | No grant for this requirement | Inspect and remove unnecessary independent grants |
| Billing-only users | Separate identities | Billing task fields | Required Billing work | Approved Billing scope | Billing set grants Diagnosis | Preserve only if business-authorized | Billing owner decision; do not infer requirement |

**Critical finding:** muting Diagnosis inside the Support group does not revoke the profile grant or independent Billing permission set grant. The stated configuration therefore does not meet the no-Diagnosis requirement. UI hiding is insufficient. Enumerate profile, direct permission sets, every group and its muting set, and broad field/object grants before asserting effective denial.

### Proposed configuration diff (labels are proposals, not metadata/API names)

| Change | Metadata/configuration draft | Dependencies | Authorized scope | Rollback |
| --- | --- | --- | --- | --- |
| Establish Support baseline | Remove Diagnosis Read/Edit from Support's baseline profile; if shared, isolate affected Support users on an appropriate minimal profile instead of unintentionally changing all users | Profile population, license constraints, supported profile migration and all baseline privileges inspected | Draft only | Preserve previous profile and assignments; restore only after checking exposure implications |
| Remove independent grant | Unassign the Diagnosis-granting Billing set from Support; replace with a Billing variant containing only necessary non-sensitive permissions if Support has Billing duties | Billing owner confirms duties; inspect other sets/groups and broad grants | Draft only | Keep snapshots; do not automatically reintroduce Diagnosis |
| Grant task access | Proposed “Support Case Work” permission set: Case Read/Edit, Status Read/Edit, explicit read-only safe-field allowlist; no Diagnosis grant; no Create/Delete or broad View/Modify All grants | Actual field API names, required fields, license and edit behavior verified | Draft only | Remove proposed set/group assignment using captured before-state |
| Compose Support group | Include focused task sets; existing mute can remain defense against grants within this group but is not the global denial mechanism | Audit every assignment; wait for permission-group recalculation | Draft only | Restore prior composition only after access review |
| Constrain rows | Verify Case org-wide default and existing hierarchy, ownership, queues, Case teams, manual/rule shares and broad grants. Select narrow team-based sharing giving only intended team read/write | Define team; inspect cross-team access and inherited grants. A new narrow share cannot subtract existing broad access | Draft only; no automatic global OWD change | Snapshot sharing configuration/membership; assess wider impact before restoring |
| Restrict update surface | Deny Edit on non-Status fields where supported; inspect standard fields, actions, flows and custom/system-mode paths. If FLS cannot express strict Status-only writes, design a supported enforcement layer and separately review code | Field-level capabilities and automation effects unknown | Draft only; no invented code or metadata | Revert reviewed enforcement configuration only under approved change control |

Do not treat restriction rules as universally supported for Case, or use broad access to work around a failing test. Object Edit alone does not authorize every field; record edit sharing does not provide object or field permissions. A user holding both Support and sensitive Billing grants cannot satisfy “no Diagnosis” through group muting: remove the conflicting grant or explicitly redesign role separation with the owners.

### Synthetic sandbox test plan

Fixture: Support user S-A in team A, Support user S-B in team B, Billing-only control B, and any actual service/action identity; synthetic Case A1 in A and B1 in B, with distinctive fake Diagnosis markers. Use approved test identities, never admin success as a substitute.

| Test | Identity/operation | Expected | Actual/evidence to collect |
| --- | --- | --- | --- |
| C1 | S-A opens/queries A1 safe fields | Allowed | NOT RUN; user, assignments, operation, returned safe fields |
| C2 | S-A updates only A1 Status to a valid permitted transition | Allowed | NOT RUN; before/after and errors; distinguish validation failure from access denial |
| C3 | S-A reads Diagnosis through UI, report, API and each actual action | No sensitive value in response or rendered output; field omitted or explicit access error per channel | NOT RUN; synthetic response and error code; omission alone does not establish all channels |
| C4 | S-A attempts Diagnosis write | Denied; stored value unchanged | NOT RUN; write result and independently authorized verification |
| C5 | S-A reads/updates B1; repeat S-B against A1 | Denied/no unauthorized row returned; no mutation | NOT RUN; distinguish row filtering from CRUD/FLS or license errors |
| C6 | S-A changes another Case field; creates/deletes Case | Denied under stated scope | NOT RUN; exercise API and actual UI/action paths |
| C7 | Isolated synthetic assignment variants: mute only; profile grant only; direct Billing grant only; all unwanted grants removed | First three expose residual read grant where present; last denies Diagnosis | NOT RUN; preserve baseline; this proves additive grant behavior without live changes |
| C8 | Permission group recalculation, then fresh target-user session | Completed recalculation before final assertions; C1–C6 still pass | NOT RUN; status, timing, execution context |
| C9 | Real flow/custom action/integration/service identity on behalf of S-A | Same customer authorization, safe field handling and team scope; elevated identity must not leak data | NOT RUN; review system-mode safeguards separately |
| C10 | Team transfer, queue/Case-team membership changes and any hierarchy access | Old team loses access when required; new team gains intended access only | NOT RUN; effective row access and propagation timing |
| C11 | Billing-only control after Support changes | Approved Billing duties remain functional | NOT RUN; owner-approved regression scenarios |

## Data 360 Governance workbook

### Policy and consumption matrix

| Persona/purpose | Data space/object/field | Consumer/identity | Allow/deny/mask | Consent/retention requirement | Owner |
| --- | --- | --- | --- | --- | --- |
| Restricted user | Explicit intended space and denied field, all unresolved | Direct query under actual user | Deny field; safe fields only within approved rows | Check applicable purpose and consent separately | Data 360 admin |
| Restricted dashboard viewer | Same lineage | Dashboard plus refresh/service principal | No denied value in cached or fresh result; masking is not deletion | Revocation must affect relevant use; no assumption cache auto-invalidates | Dashboard owner |
| Insight consumer | Source and derived fields | Saved insight runtime principal | Validate consuming separately from creation | Exclude disallowed purpose/use; inspect derivations | Insight/data owner |
| Retrieval consumer | Source field and indexed/derived copies | Agent/retriever actual principal | No leakage in answers, citations or retrieved evidence | Verify applicable consent at retrieval and copied stores | Retrieval owner |
| Export/activation recipient | Source, prior file and destination copies | Export principal and downstream identity | Deny future unauthorized delivery; prior copies tracked separately | Explicit applicable consent filters; recipient handling per owner-approved retention policy | Export custodian/privacy owner |
| Authorized control | Synthetic permitted field/record scope | Intended authorized user | Allow only approved safe data | Consent still required where applicable | Data owner |
| Elevated service | Same sources | Real scheduled job/service principal | No unreviewed bypass; publish only authorized results | Purpose/consent constraints must survive service execution | Service owner |

### Actionable remediation draft

1. Capture policy versions, exact effective timestamps, consent revocation timestamp/source/purpose/subject linkage, runtime principals and affected field lineage. Resolve Privacy Data Model mapping or document custom mapping and provenance. Inspect actual enforcement capabilities by consumer and release.
2. Draft continued field denial for the intended audience, space and channels. Denial must not cause fallback to a default data space or elevated identity. If a consumer cannot enforce the requirement, keep that consumption path disabled/quarantined pending a supported alternative; do not silently weaken the rule.
3. Inventory dashboard caches, extracts, saved insights, retrieval indexes, prior exports and destination copies. Record creation/refresh times, owners, access controls, expiry and exposure after the policy change. A fresh query denial does not prove any older copy disappeared.
4. Prepare a dashboard-specific change ticket: suspend affected viewer access if exposure persists; invalidate/purge the affected cache using the supported mechanism; rebuild under the correct runtime policy; verify both existing-viewer and new-session views. Record inability to invalidate as an open gap, with restricted distribution until resolved.
5. Prepare export/downstream tickets: stop affected future delivery, restrict known copies, identify recipients and replicated/backed-up copies, then apply owner-approved deletion, quarantine, retention or suppression procedures. Obtain destination evidence/acknowledgments. Do not claim an export is recalled merely because source access changed. No recipient messages are sent by this draft.
6. For the revoked consent, apply explicit applicable-purpose exclusion in segments/exports/activation and every relevant consumer, including pending jobs and previously selected audiences. The data/privacy owner must define unknown, expired, opted-out and revoked behavior, lawful retained uses and retention exceptions. Proposed conservative interim rule for consent-dependent delivery: suppress until valid consent is established. No invented legal deadline or blanket assertion that every use requires consent.
7. Keep a remediation register per copy: synthetic identifier for testing, actual owner in implementation, location, purpose, creation time, policy/consent effective times, action, evidence, exception and due date assigned by the owner. Track backups and uncontrollable copies as explicit residual risks, not completed deletion.

### Separate consumption, cache and downstream tests

Synthetic data only: a permitted safe marker, a denied field marker, subjects with valid, revoked, unknown, expired and opted-out consent; pre-change cache/export fixtures created within an authorized sandbox.

| Test | Identity | Consumer/cache state | Expected | Actual | Evidence | Exception |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Restricted user | Fresh direct query | Field denied/omitted according to supported behavior, no marker; approved safe rows work | NOT RUN | Request, response, principal, policy version | API/feature behavior unresolved |
| D2 | Same | Existing pre-change dashboard cache | Inspect for stale exposure independently of D1; if marker present, record failure and contain | NOT RUN | Cache time, viewer response, marker check | Invalidation unknown |
| D3 | Same plus refresh principal | Purged/rebuilt cache, old and new sessions | No denied marker; only authorized content | NOT RUN | Purge/refresh result, runtime identity, screenshots/results | Do not call purge successful without evidence |
| D4 | Unauthorized user and authorized control | Saved insight creation versus consumption | Separate permissions verified; no unauthorized field/derived leakage | NOT RUN | Both operations and returned data | Derived lineage unresolved |
| D5 | Restricted user and elevated retriever | Actual agent/retrieval path | No denied marker in answer, citations or retrieved evidence | NOT RUN | Retrieval trace and output | Index copies assessed separately |
| D6 | Export principal | New export/segment after revocation, including previously queued job | No denied field; revoked subject excluded for applicable consent-dependent purpose | NOT RUN | Filter, job timing, output and destination receipt | Purpose mapping unresolved |
| D7 | Export recipient/custodian | Prior export and destination copies | Assess contents separately; verify approved quarantine/deletion/suppression action per copy | NOT RUN | Inventory, acknowledgments and action records | Historical copies may persist; not universally revocable |
| D8 | Actual consumers | Valid/unknown/expired/opted-out/revoked consent fixtures | Owner-approved truth table enforced, not merely visible consent metadata | NOT RUN | Provenance, mapping, filter and all fixture results | Owner decisions pending |
| D9 | Service identity and restricted user | Space/policy access denied | Denial preserved; no identity/space fallback | NOT RUN | Error and routing evidence | Keep configuration error distinct from empty rows |

### Rollback, failures and handoff

Preserve prior policies, grants, assignments, sharing, consumer settings, filters and job schedules as controlled snapshots before any later authorized change. Rollback must not restore revoked consent, re-enable unauthorized delivery, reintroduce Diagnosis grants, or republish stale caches. If a regression occurs, prefer keeping the affected path disabled while reviewing a safe restoration. Purge/deletion may be irreversible; follow owner-approved retention and recovery decisions, and reapply current restrictions to any restored backup.

CRM administrator owns grant inventory and minimal permission/sharing implementation; Support/Billing owners resolve dual-role conflicts and team definitions. Data 360 administrator and each consumer owner own policy/path verification; the privacy/data owner decides consent-purpose and retention treatment; destination custodians attest handling of prior copies. Implementation handoff requires exact org/version/schema, owner decisions, snapshots and separately authorized target scope. No deployment-ready metadata is provided because identifiers and feature support are unknown.

## Local validation and completion criteria

Local review checked that both workbook structures are populated, grant paths are explicit, field read/write and row scope are separate, current-versus-desired access is stated, cache and prior export tests are separate, consent revocation is independently addressed, rollback avoids re-exposure, and all tests are marked NOT RUN. Supplied acceptance cases are covered by C7 and D2/D3/D7. Sandbox checks executed: **none**. Production behavior: **untested**. No access or governance success is claimed.

Completion later requires evidence under actual identities across actual channels; completed permission recalculation; no Diagnosis access through any grant path; permitted team-only Status updates; cache verification; future consent-dependent exclusion; and documented disposition or explicit owner-accepted residual risk for each prior copy. A passed query alone cannot close the governance work.

## Provided official-source baseline (not independently fetched)

- [Permission Set Groups](https://help.salesforce.com/s/articleView?id=platform.perm_set_groups.htm&release=264.0.0&type=5) — supplied workflow, reviewed 2026-11-15.
- [Policy Enforcement](https://help.salesforce.com/s/articleView?id=data.c360_a_policy_enforcement_in_datacloud.htm&release=264.0.0&type=5) — supplied governance workflow, reviewed 2026-11-15.
- [Consent Preferences in Segmentation](https://help.salesforce.com/s/articleView?id=data.c360_a_using_consent_preferences_in_segmentation.htm&release=264.0.0&type=5) — supplied governance workflow, reviewed 2026-11-15.
- [Secure Your Data with Data Spaces](https://help.salesforce.com/s/articleView?id=data.c360_a_data_spaces_secure_data.htm&release=264.0.0&type=5) — supplied current guidance baseline, checked 2026-11-15.
- [Apex Security and Sharing Model](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_security_sharing_chapter.htm) — supplied current guidance baseline, checked 2026-11-15; execution-mode implementation remains outside this configuration draft.
