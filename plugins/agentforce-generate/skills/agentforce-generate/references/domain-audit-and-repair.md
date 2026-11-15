# Audit and Repair an Existing Agent

> Moved verbatim from this skill's `SKILL.md`. Relative paths in this file are relative to the skill folder (where `SKILL.md` lives), not to this file.

### Audit and Repair an Existing Agent

Use for “fix my AgentScript,” health checks, common-pitfall reviews, and
baseline-versus-candidate repair loops.

1. Read [Audit and Repair](agent-audit-and-repair.md), then follow its
   linked scope/path-review and repair/report workflow in order.
2. Use the [Diagnostic Catalog](agent-audit-diagnostic-catalog.md)
   and its focused diagnostic references only for categories present in the
   artifact. Use [Common Control-Flow Pitfalls](common-control-flow-pitfalls.md)
   and its focused references for suspected prompt/control-flow defects.
3. Freeze accepted Surface edits before changing the artifact. For Structural
   or Rewrite work, obtain the approval required by Rule 4.
4. Compile locally, compare the unchanged baseline and candidate against the
   same use cases, and follow
   [Audit Evaluation Loop](agent-audit-evaluation-loop.md).
5. Report Surface, Structural, and Rewrite assessments separately. Stay
   draft-only unless the user separately requests a release operation.

#### Audit Reference Files

- [Audit Scope and Path Review](agent-audit-scope-path-review.md)
- [Audit Repair and Report](agent-audit-repair-report.md)
- [Audit Candidate Verification](agent-audit-candidate-verification.md)
- [Instruction and Routing Diagnostics](agent-audit-diagnostics-instructions-routing.md)
- [Action and State Diagnostics](agent-audit-diagnostics-actions-state.md)
- [Architecture and Evaluation Diagnostics](agent-audit-diagnostics-architecture-evaluation.md)
- [Action and Sequencing Pitfalls](control-flow-actions-sequencing.md)
- [Lifecycle and Side-Effect Pitfalls](control-flow-lifecycle-side-effects.md)
- [AgentScript Compiler Setup](agentscript-toolchain.md)
