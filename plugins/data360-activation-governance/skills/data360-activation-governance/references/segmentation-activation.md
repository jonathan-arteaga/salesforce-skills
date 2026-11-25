# Data 360 Segmentation & Activation

Build and troubleshoot consent-aware segments, contact-point selection, activation mappings, and destination reconciliation with strict publish gates.

## Audience Grain & Count Reconciliation

Always track and compare counts separately across each stage — one segment member can expand into multiple output rows when multiple contact points or related attributes are mapped:

| Stage | What to Measure | Common Pitfall |
| --- | --- | --- |
| Segment membership | Distinct membership entities (e.g., Unified Individual) | Forcing identity resolution when source-level membership fits |
| Consent & suppression | Explicit opt-in/opt-out, unknown, expired, revoked exclusions | Subtracting overlapping missing-contact-point and opt-out counts twice |
| Eligible contact points | Members with at least one prioritized valid channel identifier | Zero destination audience despite non-zero segment population |
| Activation export | Exported rows, payload attributes, run timestamp, error count | Treating Save or Queued Publish as proof of delivery |
| Destination receipt | Platform ingestion, match rate, rejections, visible audience | Assuming external destination accepted rows without target confirmation |

## Consent Exclusion Rules

- Express all inclusion, exclusion, and suppression criteria explicitly in segment logic, aligned with owner-approved Privacy Data Model rules from `data-spaces-governance.md`.
- Handle **opt-out**, **unknown/null**, **expired**, and **revoked** consent explicitly — never assume a destination platform or downstream flow enforces Data 360 consent automatically.
- Preview on synthetic records covering every consent state, null attributes, date-window boundaries, identity splits/merges, and Calculated Insight freshness:

| Synthetic Fixture | Consent / Contact State | Expected Segment & Activation Outcome |
| --- | --- | --- |
| Opted-in + valid email | Active opt-in, prioritized email | Included and exported with primary email |
| Opted-out / revoked | Revoked or opted-out preference | Excluded before activation export |
| Unknown / expired consent | Null or expired consent timestamp | Handled per owner-approved default (exclude unless explicitly permitted) |
| Opted-in + missing contact point | Active opt-in, no channel value | In segment membership; 0 eligible activation rows (do not double-subtract overlap) |

## Authorized Activation Gate (Save Is Consequential)

- **Inspect before saving**: Review existing activation target schedules, related-attribute relationship paths, target-specific attribute limits, and linked activation-triggered Flows before touching a live org.
- **Local draft first**: Saving or enabling an activation in Data 360 can trigger publishing on the next scheduled target run and fire downstream Flows. Never treat `Save` as a harmless draft action; produce a local specification and sample payload until the user explicitly authorizes target, audience scope, fields, and schedule.
- **No production shortcuts**: Never activate a real customer audience just to verify payload formatting. Test in an authorized sandbox or designated test destination using synthetic records.

## Pre-Publish Verification & Reconciliation Template

Complete this checklist before authorizing any live activation save:

1. **Membership & Data Space**: Confirm target Data Space, membership DMO, and whether Unified or source-level membership is required.
2. **Contact-point priority**: Specify exact channel DMO (`ContactPointEmail`, `ContactPointPhone`, `ContactPointAddress`), source priority order, and fallback rules per target.
3. **Related attributes**: Verify target-supported relationship path depth and attribute caps; never copy a Data 360 native target config unchanged to an external ad or messaging target.
4. **Reconciliation report**: Record `segment_members`, `excluded_consent`, `excluded_missing_contact_point`, `overlap_count`, `eligible_members`, `exported_rows`, and `destination_accepted_rows`.
5. **Bounded retries**: Verify destination deduplication semantics before retrying a failed or partial publish; bound retry attempts and capture run/job IDs.

## Honest Delivery & Rollback

- Report `exported; destination unverified` when Data 360 reports publish success but destination acceptance/visibility has not been directly checked.
- Document how to pause or disable future scheduled publishes, and state explicitly that pausing a schedule does not retract records already delivered to external destinations — handle removal/revocation per destination capabilities.
