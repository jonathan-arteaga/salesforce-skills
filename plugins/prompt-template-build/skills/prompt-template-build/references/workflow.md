# Template version decisions

Record template name/type, version, model, input bindings and intended consumer. Never equate a draft saved successfully with a version active for users. Previously activated versions remain immutable; deactivation does not reopen editing. Create a new version, compare results, then activate only within scope.

Use an output contract rather than vague quality adjectives. For a structured task, define required keys, allowed missing-value behavior and evidence references. Validate formatting independently from whether the answer is supported. Use the same test inputs for candidate/baseline comparison and retain disagreement cases for review.

Template evaluation is not retrieval readiness or a security certification. Test actual consumer identity separately. When resource binding syntax or template type is unknown, produce labeled placeholders and required discovery steps rather than an apparently deployable artifact.

Source: [Use Multiple Versions of a Prompt Template](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_use_multiple_versions.htm&release=264.0.0&type=5), fetched 2026-11-15.

## Packaging and target environment

If packaging is requested, record source org, package-build context and subscriber/target org separately. Verify model availability, resource/Flow dependencies, packaging support and target activation using current deployment documentation. A preview or source deployment does not prove package creation or subscriber execution. Keep change-set-specific activation settings distinct from other delivery mechanisms; do not apply a forum scratch-org feature list blindly.
