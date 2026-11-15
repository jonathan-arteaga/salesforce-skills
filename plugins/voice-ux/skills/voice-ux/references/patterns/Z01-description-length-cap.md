---
id: Z01
name: description-length-cap
category: lint
severity: high
applies_to: [migrate, optimize]
detection:
  - structural: "any description: \"...\" field longer than 255 chars"
    in: [config, variables, actions, transitions]
principle_refs: []
---

# Description length cap (255 chars)

## Why it matters

The org-side metadata API rejects `description:` fields longer than 255 chars on any AiAuthoringBundle metadata location:
- `config.description`
- variable descriptions
- action descriptions
- transition descriptions

The offline `@agentscript/agentforce` validator does NOT enforce this length limit. The error only surfaces at publish time, with a single misleading message:

```
There were custom validation error(s) encountered while saving the affected
record(s). The first validation error encountered was "Description: data value
too large: <quoted text>... (max length=255)".
```

The error names ONE specific field, hiding however many others were also over. In the Nuffield run on 2026-05-19, 28 descriptions were over the limit; the publish error only mentioned one. Without proactive lint, you fix one, re-publish, hit the next, fix that, re-publish, etc. — many wasted minutes.

## Detection

Scan the `.agent` file for any `description: "..."` field where the quoted content exceeds 255 characters. Patterns to scan:

- `^\s*description:\s*"(.+?)"\s*$` (single-line — most common)
- Multi-line (rare with `description:`; usually variables/actions write descriptions inline)

## Auto-fix (recommended)

Truncate over-length descriptions to ≤240 chars. Prefer cutting at the last sentence boundary (`.`) within the first 240 chars; otherwise the last comma; otherwise hard-cut at 240 chars and append an ellipsis (`…`).

Example transformation:

```yaml
# Before (286 chars)
description: "This virtual assistant supports patients and visitors of Nuffield Hospital. It helps answer questions related to hospital services, departments, doctors, billing, insurance, and general enquiries. It can also guide patients through the appointment booking process."

# After (~150 chars, sentence-boundary cut)
description: "This virtual assistant supports patients and visitors of Nuffield Hospital. It helps answer questions related to hospital services, departments, doctors, billing, insurance, and general enquiries."
```

Reference Python implementation:

```python
import re

def truncate_description(text, limit=240):
    if len(text) <= limit:
        return text
    truncated = text[:limit]
    last_period = truncated.rfind(".")
    last_comma = truncated.rfind(",")
    cut = max(last_period, last_comma)
    if cut > 100:
        return text[:cut + 1]
    return truncated.rstrip() + "…"

# In Phase 7.2 lint pass:
import re
with open(path) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    m = re.match(r'^(\s*description:\s*")(.+?)("\s*)$', line)
    if m and len(m.group(2)) > 250:
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        lines[i] = f"{prefix}{truncate_description(body)}{suffix}"
```

Apply across the entire file in one batch before pattern application.

## Anti-patterns

- **Truncating at exactly 255 chars.** The org-side limit is 255 inclusive of the closing quote? Inclusive of the YAML quoting? Different platforms have surfaced subtly different limits. 240 with `…` suffix gives safety margin while preserving readability.
- **Hard-truncating mid-word.** "This virtual assistant supports patients and visitors of Nuffield Hospi…" reads as broken. Always prefer sentence or comma boundary first.
- **Skipping the lint because "the offline validator passes".** Offline doesn't enforce this. Skip → publish failure → wasted iteration.

## Where it lives

Phase 7.2 — pre-emptive lints, before pattern application. Re-run as a sanity check in Phase 7.5 in case patterns added new long descriptions.

## Worked example

The Nuffield migration had 28 over-length descriptions, ranging from 258 to 2854 chars. The 2854-char monster was on `save_sub_speciality` describing the supported sub-speciality list inline — pattern shows up when authors stuff catalog data into descriptions. Auto-truncation reduced all 28 to ≤240 chars in a single pass without losing the operational meaning of any description.
