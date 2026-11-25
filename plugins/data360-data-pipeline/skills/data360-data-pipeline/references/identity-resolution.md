# Data 360 Identity Resolution

Design, evaluate, and troubleshoot Identity Resolution rulesets, match rules, and field reconciliation without corrupting source lineage or over-merging profiles.

## Entity Grain Before Matching

Define entity grain explicitly before selecting rules — one ruleset does not fit every entity:

- **Individual vs. Household vs. Legal Entity vs. Location**: Separate person profiles from households, corporate accounts, and storefront/shipping locations.
- **Provenance over synthesis**: Normalizing an address or phone improves comparison, but never manufacture a supposedly high-confidence Party Identification value from a weak address just to force records to match.
- **Precondition check**: Inspect mapped DMOs, Fully Qualified Keys (`KQ_*`), and source provenance first. Identity resolution cannot fix malformed ingestion keys; fix key defects in ingestion/modeling first.

## Match Rules vs. Reconciliation Rules

| Layer | Responsibility | Key Failure Test |
| --- | --- | --- |
| Source provenance | Qualified IDs, data source lineage, Data Space scope | Identical local ID from two unrelated sources |
| Match rules | Decide which source profiles group into one Unified record | Shared household email/phone or shared corporate address false merge |
| Reconciliation | Select winning attribute values per field (`Last Updated`, `Most Frequent`, `Source Sequence`) | Conflicting names, blank latest value overwriting valid value |
| Processing mode | Scheduled batch vs. supported real-time unification | Pending/failed run, stale unified views, missed re-evaluation |
| Downstream impact | Unified DMO consumers (segments, insights, retrievers) | Split profile losing history or revoked consent propagating inconsistently |

- **Rule interaction**: Document every criterion that must all match within a single match rule (AND) and how multiple match rules union across the ruleset (OR) in the target release.
- **Non-destructive reconciliation**: Reconciliation populates unified DMOs; it does not delete or overwrite source DMO records or write back to source systems.
- **Consent & auth boundary**: Never treat an inferred unified identity as proof of authentication, account authorization, or channel consent.

## Labeled Synthetic Evaluation Protocol

Before promoting a ruleset change, build a synthetic test set with business-owner truth labels:

| Fixture Category | Synthetic Scenario | Expected Outcome | Defect Caught |
| --- | --- | --- | --- |
| Deterministic match | Same verified Party ID + provenance across two sources | Merge | Broken FQK or overly strict rule |
| Shared-attribute non-match | Two household members sharing one email or storefront address | Stay separate | Over-aggressive false merge |
| Alias / formatting match | Nickname, legal entity suffix (`Inc.` vs `Incorporated`), phone format | Merge | Excessive false split |
| Null / recycled key | Missing email or recycled corporate phone across two people | Stay separate | Null-equality or stale-key merge |
| Transitive cluster | Chain A-B (shared email) + B-C (shared phone) | Evaluate cluster | Pairwise rules causing mega-clusters |
| Conflicting attributes | Two valid names or blank latest value across merged sources | Winner per precedence | Misconfigured reconciliation rule |

Report true/false match and non-match counts with explicit denominators alongside unification rate. Never cite an arbitrary universal unification threshold; obtain business-owner sign-off on false-merge vs. false-split tolerance.

## Execution & Rollback

- Execute only in an authorized sandbox or explicitly scoped environment; wait for terminal run completion and inspect latest-run vs. run-history status.
- Preserve prior ruleset definitions and baseline counts before editing. Document that rolling back to previous rules requires re-running the ruleset and re-validating downstream segments/insights — never promise instantaneous state restoration.
