# Identity correction and audience preview

Status: **local draft; synthetic assertions checked; no sandbox or production execution**.

## Scope and evidence

Goal: prevent a household false merge, retain the legitimate duplicate for one spouse, and preview an email audience without publishing. Business owner, intended org, release/API version, data space, execution identity, licenses, schemas, target type, exact schedule and linked flows are unknown. No org tools are available. Authorization covers this local document only; no live save, ruleset change, activation creation, schedule change or publish is authorized.

Evidence read: the two supplied skills, their workflow/current-Salesforce references, acceptance cases and workbook templates. Their documentation baseline is dated 2026-11-15; this task did not independently fetch Salesforce documentation or verify org availability. All field labels and IDs below are synthetic conceptual placeholders, not deployable API names.

The identity scenario contains three source records but only two intended people. The audience scenario mentions three members; it is modeled as a separate fixture. Combining them without a supplied mapping would invent membership and consent facts.

## Identity design and implementation

| Component | Current evidence | Proposed state | Reason / consumer impact |
| --- | --- | --- | --- |
| Entity | Three records unified | Individual, not household | Two spouses remain separate people |
| Matching | Exact current rule configuration unavailable | Qualified verified individual identifier, exact match only | Shared household signals cannot establish identity |
| Weak match paths | Existing merge implies an unsafe path; exact cause unknown | Remove email-only, address-only and fuzzy-name/household paths from proposed automatic matching | Prevent alternate rules or transitive links from rejoining spouses |
| Missing strong identity | Third record's customer ID not supplied | Link only after trusted identifier or owner-approved verified crosswalk is established | Misspelling plus shared email/address is insufficient |
| Reconciliation | Current precedence unknown | Field-specific trusted source precedence, below | Select display values without changing source records |

### Proposed match policy (conceptual)

Rule M1 requires ALL of: same identifier authority/namespace, same nonempty normalized verified customer ID, identifier valid for an individual and within its valid ownership period. Qualified source record keys remain distinct from business identity keys. Do not compare unrelated source-local IDs as globally unique customer IDs.

If records hold conflicting verified identifiers in the same authority, they must not automatically merge. A conflict across authorities needs a verified crosswalk; differing strings alone do not prove different people across unrelated namespaces. If the product cannot express the required conflict guard or temporal conditions, prepare an approved verified match key or quarantine conflicting records upstream; do not claim unsupported native rules implement the policy. Mapping/key repair belongs to ingestion/modeling.

Rule M2 is optional: exact match on an independently verified crosswalk to the same authoritative individual ID. Enable only after provenance and current product support are established. Fuzzy name similarity may suggest manual review, never create an automatic match edge in this draft.

Inspect the current product's multiple-rule combination and cluster behavior before translating this policy to Setup. Every enabled path must preserve the invariant that a cluster contains at most one active individual identifier per authority. A safe M1 cannot compensate for a remaining broad email rule.

### Source lineage and expected grouping

| Source record | Synthetic qualified key | Name | Verified ID | Shared household signals | Expected |
| --- | --- | --- | --- | --- | --- |
| A | crm:A | Alex Rivera | customer-authority:C101 | household@example.test; 10 Example Lane | Person P1 |
| B | crm:B | Blair Rivera | customer-authority:C202 | Same email/address | Person P2 |
| C | service:C | Alxe Rivera | Unknown in supplied scenario | Same email/address | Pending evidence; do not assume C101 |

Owner truth label: C belongs to A. Operational evidence remains missing. With C independently verified as C101, expected clusters are {A,C}, {B}. Without that evidence, expected conservative output is {A}, {B}, {C pending}: one known false split accepted provisionally to avoid a household false merge. Retain source-to-unified lineage and prior/new cluster mappings; actual generated unified IDs and stability are unknown.

### Reconciliation policy, separate from matching

- Display name: verified authoritative customer master first, then verified service profile, then other sources; ignore nulls and use a stable source-key tiebreaker. Thus Alex outranks Alxe if the customer master is confirmed authoritative.
- Address: most recent verified nonempty value within approved source precedence; retain provenance and effective time. A shared address is valid for both people.
- Contact points: preserve each related contact point, ownership evidence, verification and consent scope. Do not replace multiple points with a single undifferentiated email value.
- Customer identifiers: preserve qualified lineage; quarantine conflict instead of selecting an arbitrary winner.
- Consent: do not choose a convenient latest unified Boolean. Evaluate authoritative, scoped consent events with owner-approved precedence. Identity grouping never establishes consent or account authorization.

Reconciliation selects unified values; it does not overwrite names, customer records or preferences in source systems.

## Identity validation cases

All expected results are design fixtures, not observed Salesforce behavior.

| Case | Synthetic input | Expected | Observed / environment |
| --- | --- | --- | --- |
| Exact verified ID | A and C both verified C101 | One cluster despite misspelled name | Local conceptual assertion only |
| Shared household | A=C101 and B=C202, same email/address | Two clusters | Local conceptual assertion only |
| Missing ID | C lacks verified ID/crosswalk | Separate pending record, known provisional split | Local conceptual assertion only |
| Transitive bridge | C has shared email with B and verified ID C101 | Never bridge A to B | Local conceptual assertion only |
| Missing values | Two records with blank IDs | No match on blank | Not executed in product |
| Unrelated namespaces | Same ID string in unrelated source authorities | No match absent verified crosswalk | Not executed in product |
| Recycled identifier | Same string, different verified ownership periods | Review/exclude; do not merge solely on string | Not executed in product |
| Conflicting verified identity | One record asserts both C101 and C202 in same authority | Quarantine, retain provenance | Not executed in product |
| Null recent name | Newer source name is null | Preserve trusted nonempty name | Not executed in product |

Pair-label baseline over A/B/C: truth has one matching pair A–C and two nonmatching pairs A–B/B–C. Existing all-three cluster: TP=1, FP=2, FN=0, TN=0. Proposed with verified C101 on C: TP=1, FP=0, FN=0, TN=2. Without C's verification: TP=0, FP=0, FN=1, TN=2. These are calculated fixture counts over three pairs, not measured org accuracy. Owner must approve tolerances; do not optimize unification rate alone.

## Audience design and implementation

Purpose assumed: promotional email preview at person/member grain. Actual campaign, owner, membership DMO and eligibility predicates must be supplied before implementation. For deterministic fixtures, all three members pass non-consent business criteria.

Provisional consent policy for this preview: explicit applicable opt-in required; unknown, expired, revoked and opted-out states excluded. This is an owner-dependent conservative choice, not a claim about mandatory Salesforce defaults or universal legal requirements. Applicable opt-out takes precedence for this fixture. Consent owner must validate purpose/channel/contact-point scopes, source authority, event order, expiry, suppression and any valid later re-opt-in.

Conceptual membership logic:

1. Pass approved business criteria using current inputs.
2. Exclude applicable member-level opt-out, revocation, suppression, expired or unresolved consent.
3. Retain contact points only where ownership, address validity, verification and applicable explicit opt-in are established and no point-level suppression applies.
4. Include the member only if at least one eligible email point remains.
5. Select one eligible point per member: verified primary first; then latest verification time; then lexical qualified contact-point key. Null primary ranks last and null timestamps rank oldest. Filter eligibility BEFORE ranking; do not fall back to an ineligible primary.

| Synthetic member | Consent | Contact points | Preview decision | Member count | Selected output rows |
| --- | --- | --- | --- | --- | --- |
| E1 | Explicit opt-out | E1-email, verified | Exclude | 0 | 0 |
| E2 | Unknown | E2-email, verified | Exclude provisionally | 0 | 0 |
| E3 | Explicit valid opt-in for purpose/channel and both points | E3-primary, E3-secondary, both verified | Include; choose E3-primary | 1 | 1 |
| Total | 3 candidate members | 4 candidate contact points | 1 eligible member | **1** | **1** |

Before point selection, E3 yields two eligible contact-point rows; the recommended one-point selection yields one output row. An intentionally configured all-eligible-points variant would yield two rows for the same one member, subject to target support. Additional attribute joins could multiply rows again and must be checked. E3's consent is an explicit synthetic assumption; the task only states two contact points. If E3's applicable consent is unknown, the same policy yields zero members and zero output rows.

### Proposed activation mapping and payload (local only)

| Conceptual output | Source meaning | Unresolved implementation |
| --- | --- | --- |
| member_reference | Current approved person/member key | Actual membership DMO and stable target key |
| email | Selected eligible email contact point | Supported relationship path and target attribute |
| contact_reference | Qualified selected point key | Destination deduplication and mapping support |

Synthetic preview payload, not a target API contract:

```json
[{"member_reference":"E3","email":"primary@example.test","contact_reference":"fixture:E3-primary"}]
```

Keep consent provenance, selection reason, source lineage and evaluation time in the local audit preview; transmit only destination-required approved fields. Never send inferred identity or unnecessary household attributes.

### Audience and operational validation

| Case | Expected | Observed / environment |
| --- | --- | --- |
| Opt-out E1 | 0 members, 0 rows | Local fixture assertion |
| Unknown E2 | 0 members, 0 rows under provisional policy | Local fixture assertion |
| Two opted-in points E3 | 1 member, 2 eligible rows, 1 selected row | Local fixture assertion |
| E3 has unknown consent | Entire fixture yields 0 members, 0 rows | Local fixture assertion |
| Primary opted out, secondary eligible | Select secondary; no fallback to opted-out point | Expected only |
| Both points ineligible | Exclude member | Expected only |
| Equal priority/time | Stable qualified key determines winner | Expected only |
| Shared household email | Do not borrow another person's consent; verify address ownership and applicable suppression | Expected only |
| Identity split after correction | Recompute member/point ownership and consent scope; remove stale merged membership | Expected only |
| Stale insight / out-of-window event | Reject or mark preview stale under owner freshness threshold | Expected only |
| Missing org tools | Produce local draft, no claimed runtime result | Observed: no runtime available in assigned scope |
| Denied access | Stop; no switch to default data space or broader access | Hypothetical; not encountered |
| Partial or asynchronous results | Mark incomplete; wait for completed run before comparing totals | Hypothetical; not encountered |
| Save/publish requested outside scope | Do not execute; preserve local draft | No live operation attempted |

## Delivery, scheduling and recovery

Processing state: local artifact prepared. Nothing accepted by Salesforce, processed, activated, published or delivered. No sandbox tests ran. Production matching, rule combination, reconciliation, schedules, consent enforcement, target compatibility, output expansion and destination receipt remain untested.

The supplied workflow reference states that the reviewed Data 360 target workflow can publish at its next scheduled target run after saving; linked activation-triggered flows can send data onward. The target here already has a publishing schedule. Therefore **do not save or enable even a nominal draft activation live**. Exact target behavior is unverified; local-only preparation avoids an accidental scheduled delivery.

Next owner actions: establish org/data space and schemas read-only; capture existing versioned rules, run history, lineage, segment/activation configuration, schedules and flows; verify C's identity evidence; approve consent policy and source precedence; confirm exact target behavior and current official limitations. Then obtain authorization for a bounded sandbox/test destination, run identity correction to completion, compare fixture/sample clusters and downstream preview, and inspect destination receipt/rejections before any separately authorized production action.

Before any future authorized change, preserve versioned previous rules/results and affected memberships. Returning to prior rules can require reprocessing and can reintroduce the known false merge; prefer an approved corrected version if rollback would restore unsafe targeting. Pause affected future publications only with appropriate authorization and verify actual stop state. Retain membership diffs and rejected rows; bound retries and confirm destination deduplication. Pausing does not retract previously delivered copies. Consent revocation, removal propagation, retention and deletion of downstream copies require target-specific verification and an approved remediation plan.

Sources carried from supplied references (not fetched in this task):

- [Identity Resolution Rulesets](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_ruleset.htm&release=264.0.0&type=5)
- [Create an Activation](https://help.salesforce.com/s/articleView?id=data.c360_a_create_data_cloud_activation.htm&release=264.0.0&type=5)
- [Consent Preferences](https://help.salesforce.com/s/articleView?id=data.c360_a_using_consent_preferences_in_segmentation.htm&release=264.0.0&type=5)

Artifact: `/workspace/forward-identity-activation.md`. Next owners: identity/data steward for verified crosswalk and grouping labels; consent owner for policy; activation owner for schema, schedule and destination validation.
