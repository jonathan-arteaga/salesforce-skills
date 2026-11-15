# Create an Agent

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Create an Agent

Use for a new agent or authoring bundle.

1. Read [Design & Agent Spec](agent-design-and-spec-creation.md),
   then use an already-approved, sufficiently detailed supplied design as the
   build contract without regenerating or reapproving it. Otherwise capture the
   requirements in a saved Agent Spec and obtain explicit approval. Keep new
   action implementations as `NEEDS STUB` until the user chooses whether to
   reuse implementations, generate them, or leave placeholders.
2. Read the applicable sections of [CLI for Agents](salesforce-cli-for-agents.md)
   and validate the target-org prerequisites before org work. For document
   grounding, read [Data Library](data-library-reference.md). For a
   voice agent, read [Voice Modality](voice-modality-reference.md)
   and [Voice Latency](voice-latency-heuristics.md).
3. Generate the authoring bundle with Salesforce CLI. Edit the scaffolded
   `<ApiName>.agent` and preserve the matching `<ApiName>.bundle-meta.xml`.
   Read [Core Language](agent-script-core-language.md),
   [Instruction Resolution](instruction-resolution.md), and the
   applicable templates before writing.
4. Run the local compiler required by Rule 14. When an authenticated target org
   is available, also validate the authoring bundle in the org. Fix blocking
   diagnostics before implementing or deploying action dependencies.
5. Generate action implementations only when the user selected that path.
   Validate and deploy one dependency at a time.
6. Preview the draft and inspect traces using
   [Validation & Debugging](agent-validation-and-debugging.md).
   Cover realistic happy, adjacent, recovery, and cancellation paths.
7. Stay in the draft loop. Publish and activate only after the release gates in
   **Deploy, Publish, and Activate** pass and the user explicitly approves.
