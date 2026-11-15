# Ruleset decisions

| Layer | Decision | Failure test |
| --- | --- | --- |
| Source provenance | Qualified IDs and lineage | Same local ID from unrelated sources |
| Matching | Which signals establish one entity | Shared email/phone and household false merges |
| Reconciliation | Which source/value wins by field | Conflicting names and missing latest value |
| Processing | Scheduled versus supported real-time mode | Pending/failed run and stale results |
| Consumers | Effect on memberships and authorization | Split profile or revoked consent downstream |

Track labeled true/false matches and true/false non-matches. Report counts and denominator, not a fabricated universal quality threshold. Have the owner choose tolerances and manual-review cases. Evaluate clusters as well as isolated pairs; pairwise-looking rules can create surprising groups through links.

Reconciliation does not delete/change source profiles or update connected systems. Preserve source lineage for traceability. Do not use identity resolution as authentication or proof of consent.

Source: [Identity Resolution Rulesets](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_ruleset.htm&release=264.0.0&type=5), fetched 2026-11-15.

## Entity grain before fuzzy matching

Separate legal entity, storefront/location, household and individual identities before selecting rules. Normalizing an address can improve comparison but does not turn it into a high-confidence Party ID. Require provenance for identity signals and test unrelated entities sharing an address as well as one entity using aliases.
