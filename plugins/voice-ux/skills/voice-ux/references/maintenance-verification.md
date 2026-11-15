# Verification (for skill maintenance)

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

## Verification (for skill maintenance)

Self-checks the skill should run before declaring the work complete:

1. **Mode detection:** Mode was inferred AND surfaced to the developer with the signals behind it. The developer confirmed (or overrode).
2. **Layer integrity:** Each layer (A–E) is independently usable. Developer can drop Layer A into instructions without untangling other layers.
3. **Citation coverage:** Every `[changed]`, `[review needed]`, and `[consider]` entry has a `why:` citation pointing to a specific principle ID or mis-application ID.
4. **Conflict policy:** No silent overrides of original business logic. If voice principle and original logic disagree AND strong intentionality signal present, output is `[review needed]` regardless of mode. If only weak intentionality signal, behavior matches the mode (preserve in migrate, flag in optimize).
5. **Optimize-mode mis-application coverage:** In optimize mode, every principle present in the source was checked against its mis-application list, not just its presence.
6. **Trait sensitivity:** Rewrites against the same Script with different modality traits produce meaningfully different Layer D and Layer E outputs.
7. **Sample required:** A sample conversation was provided. The skill does not synthesize one; if missing, it refuses to proceed.
8. **Vocal identity:** a brief exists (or is labeled inferred), gender presentation was elicited rather than inferred, the casting record names a runner-up, the audition channel and listener tier are recorded, and Z05 has no unresolved hits.
9. **Tested with audio, not text (advised to the developer):** Typing utterances into a preview verifies the reasoning, but not the actual experience — barge-in, background noise, accents, and timing are where voice deployments struggle. Advise: call the agent from a car, from a noisy kitchen; hand the phone to someone who's never seen the script and ask them to complete the task; listen for the places you'd have interrupted and the agent kept talking, and for silences you didn't design. Then add scenario suites to Testing Center so regressions surface on later edits.
10. **Latency measured, not guessed (advised to the developer):** change one thing per version, place one live call on a fixed path, and compare per-turn response delay from the Data Cloud session trace against the last version. Keep the change or roll back with `sf agent activate --version N`. See `templates/v1-review-checklist.md` §9 for the query and the traps.
