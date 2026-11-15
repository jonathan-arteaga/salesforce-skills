# Governance decisions

| Path | Question to prove |
| --- | --- |
| Interactive query | Does the intended identity receive only authorized rows/fields? |
| Saved insight | Are creation rights and consumption rights evaluated separately? |
| Dashboard/cache | When does policy change affect existing cached results? |
| Agent/retriever | Which principal retrieves data and where is customer authorization enforced? |
| Activation/export | Which consent conditions apply, and what remains in the destination after revocation? |
| Core application/system context | Which CRM safeguards are required in addition to Data 360 policy? |

A successful schema lookup is not a data-access test. Do not treat masking as deletion, a data-space label as a universal security boundary, or a consent field as an enforcement mechanism without a consuming filter/control.

Record requirements and owner decisions, then implement only supported controls. If the platform cannot enforce the desired rule in a consumer, document the gap and propose a supported alternate design; do not downgrade the rule silently.

Primary sources reviewed 2026-11-15: [Policy Enforcement](https://help.salesforce.com/s/articleView?id=data.c360_a_policy_enforcement_in_datacloud.htm&release=264.0.0&type=5); [Consent Preferences in Segmentation](https://help.salesforce.com/s/articleView?id=data.c360_a_using_consent_preferences_in_segmentation.htm&release=264.0.0&type=5).

## Audience and evidence matrix

Use synthetic public and restricted articles with at least an authorized user, unauthorized user and elevated service identity. Run the same question through the actual consumer for each. Inspect citations and retrieved evidence as well as answer text for leakage. Keep metadata visibility, feature operations and data access as separate assertions.
