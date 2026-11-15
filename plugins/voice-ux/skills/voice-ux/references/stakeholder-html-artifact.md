# Stakeholder HTML artifact

Guidance for generating an interactive, self-contained HTML page that communicates a voice
migration/optimization to a team — PMs, developers, QA, and executive stakeholders at once.

**This is inspiration, not a strict template.** Every voice project differs: the number of
changes, whether there's a persona section, how many conversation paths matter, whether the
audience is technical. Pull the patterns that fit; drop the ones that don't. Do not force a
project into a fixed structure. The bundle (Layers A–E) and the `.agent` file remain the
canonical artifacts — the HTML is a *communication* layer on top of them, not a replacement.

## When to offer it

After the bundle exists (Phase 6) or after the `.agent` file exists (Phase 7). It's optional
and offered, never automatic — see SKILL.md Phase 9. The page is built **from** the bundle
and the sample conversation; it does not introduce new design decisions.

## What makes it effective

The goal is a single file a PM can email to anyone, that lets a VP grasp the work in two
minutes and lets a developer dive deep in twenty. Effectiveness comes from: scanability
(filter + color-coding), specificity (real before/after quotes, not paraphrase), rationale
baked into every change (so stakeholders don't ask "why not just say X?"), and a journey
narrative that gives non-technical readers a mental model of what a caller actually hears.

## Reusable patterns

Pick from these. None is mandatory.

### Before/after compare-cards
The workhorse. A two-cell side-by-side: **Before** (muted/neutral color) and **After**
(accent color), each labeled, with a one-line **"Why it matters for voice"** footer citing the
principle (e.g. T-translate-2, P7). Sourced directly from **Layer B** copy changes and the
inline audit. Color-code consistently so "old vs new" is legible at a glance.

### Filter chips
A sticky bar of chips by change bucket (Grounding, Repair, Latency, Speakability, Brevity,
Confirmation, Persona, Opening/Closing, Scope) plus "All", filtering the compare-cards live and
showing a count ("Showing 12 of 50"). Lets stakeholders both see total scope and narrow to one
category for discussion. Buckets map to the bundle's summary-table categories.

### Journey tabs
Numbered stages of what the caller hears end to end (e.g. Opening → First intent → Data
capture → Lookup → Confirmation → Commit → Close). Each stage panel pairs *what the caller
hears* with *the voice-UX principle at work*. Built from **Layer A** behaviors and **Layer D**
opening. This is the section that earns buy-in from non-technical stakeholders.

### Conversation trees
Speaker-differentiated dialog cards (System/IVR, Agent, Caller visually distinct), with
branch/fork labels ("Happy path", "Repair tier 2", "After hours") and outcome links between
trees. Built from the **sample conversation** and the repair/grounding logic. Doubles as a test
spec (branch labels are test-case names) and onboarding material.

### Dark config-delta table
A visually-weighted (dark background) table separating **"what changed in the `.agent` file"**
from **"what needs platform/engineering work"** — Before / After / Why columns. The in-script
voice-channel config lands on the `.agent` side: `additional_configs` (`beepboop_config` 500ms,
speak-up timers) and `inbound_keywords`. The genuinely out-of-script
**Layer E** items live on the platform side: TTS voice casting, SSML/prosody, ASR confidence
thresholds, carrier/IVR split, etc. Makes the handoff to platform owners explicit.

## Mapping the bundle to the page

| Bundle source | HTML pattern |
|---|---|
| Layer B (copy changes) + inline audit | compare-cards |
| Summary-table categories | filter chips / buckets |
| Layer A (behaviors) + Layer D (opening) | journey tabs |
| Sample conversation + repair/grounding logic | conversation trees |
| Layer E + config deltas | dark config-delta table |

## Technical constraints

- **Fully self-contained.** One `.html` file, inline `<style>` and `<script>`. No build step,
  no bundler. A PM emails the file and it just opens.
- **No external runtime dependencies.** Google Fonts via `<link>` is acceptable; no CDN
  frameworks, no React/Vue. **Vanilla JS only.**
- **Data-attribute-driven interactivity** (`data-bucket`, `data-stage`) keeps the JS small —
  a few dozen lines for nav-on-scroll, tab selection, and chip filtering.
- **Responsive** with a couple of breakpoints; **CSS custom properties** for the color system
  so before/after coding stays consistent.
- Polish signals seriousness: smooth scroll, hover states, careful contrast. But content
  correctness (real quotes, correct citations) matters more than visual flourish.

## Output

Write to the same generated-artifacts location as the rest of the bundle, named
`<api_name>-voice-summary.html`. Offer to open it for review and iterate on stakeholder feedback.
