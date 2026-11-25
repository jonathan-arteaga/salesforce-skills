#!/usr/bin/env python3
"""Deterministically lint completed Persona Markdown artifacts.

The linter checks structural and cross-field contracts. It does not score taste,
brand fit, or probabilistic runtime quality.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


POSITIONS = {
    "Personification": {"Not personal", "Individuated", "Anthropomorphic"},
    "Register": {"Subordinate", "Peer", "Advisor", "Coach"},
    "Formality": {"Formal", "Professional", "Casual", "Informal"},
    "Warmth": {"Cool", "Neutral", "Warm", "Bright", "Radiant"},
    "Personality Intensity": {"Reserved", "Moderate", "Distinctive", "Bold"},
    "Reading Level": {"Plain Language", "Explained", "Technical"},
    "Emotional Coloring": {"Blunt", "Neutral", "Encouraging", "Enthusiastic", "Clinical"},
    "Empathy Level": {"Minimal", "Understated", "Moderate", "Attuned"},
    "Brevity": {"Terse", "Concise", "Moderate", "Expansive"},
    "Humor": {"None", "Dry", "Warm", "Playful"},
    "Emoji": {"None", "Functional", "Expressive"},
    "Formatting": {"Plain", "Selective", "Heavy"},
    "Punctuation": {"Conservative", "Standard", "Expressive"},
    "Capitalization": {"Standard", "Casual"},
}


def _line(text: str, needle: str) -> int | None:
    index = text.find(needle)
    return None if index < 0 else text.count("\n", 0, index) + 1


def _diag(severity: str, code: str, message: str, text: str, needle: str = "") -> dict:
    result = {"severity": severity, "code": code, "message": message}
    line = _line(text, needle) if needle else None
    if line is not None:
        result["line"] = line
    return result


def _section(text: str, heading: str) -> str:
    match = re.search(rf"(?m)^({re.escape(heading)})\s*$", text)
    if not match:
        return ""
    level = len(heading) - len(heading.lstrip("#"))
    end = re.search(rf"(?m)^#{{1,{level}}}\s+", text[match.end() :])
    return text[match.end() : match.end() + end.start()] if end else text[match.end() :]


def _profile(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(
        r"(?m)^\|\s*(?:Register|Voice|Tone|Delivery|Chatting Style)\s*"
        r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
    )
    for match in pattern.finditer(text):
        dimension, value = match.group(1).strip(), match.group(2).strip()
        if dimension in POSITIONS:
            values[dimension] = value
    personification_patterns = (
        r"(?m)^###\s+Degree of Personification:\s*([^\n]+?)\s*$",
        r"(?m)^\|\s*\*\*Personification\*\*\s*\|\s*([^|]+?)\s*\|",
    )
    for pattern_text in personification_patterns:
        match = re.search(pattern_text, text)
        if match:
            values["Personification"] = match.group(1).strip()
            break
    return values


def _table_rows(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if cells[0].lower() in {"situation", "term", "trigger", "category"}:
            continue
        rows.append(cells)
    return rows


def lint_text(text: str) -> list[dict]:
    diagnostics: list[dict] = []

    # Completed framework structure and allowed position values.
    profile = _profile(text)
    for dimension, allowed in POSITIONS.items():
        value = profile.get(dimension)
        if value is None:
            diagnostics.append(_diag("error", "missing-dimension", f"Missing {dimension} selection.", text))
        elif value not in allowed:
            diagnostics.append(
                _diag(
                    "error",
                    "invalid-position",
                    f"{dimension} has invalid value {value!r}; allowed: {', '.join(sorted(allowed))}.",
                    text,
                    value,
                )
            )

    identity = _section(text, "## Identity")
    traits_part = identity.split("### What You're Not", 1)[0]
    traits = re.findall(r"(?m)^-\s+\*\*[^*]+\*\*\s+[—:-]\s+.+$", traits_part)
    if not 3 <= len(traits) <= 5:
        diagnostics.append(
            _diag("error", "identity-definition", "Identity needs 3–5 behaviorally defined traits.", text, "## Identity")
        )
    negative = _section(text, "### What You're Not")
    negative_items = re.findall(r"(?m)^-\s+Not\s+.+$", negative, flags=re.IGNORECASE)
    if not 2 <= len(negative_items) <= 4:
        diagnostics.append(
            _diag("error", "negative-identity-count", "Negative Identity needs 2–4 character anti-patterns.", text, "### What You're Not")
        )

    # Tone Flex must be executable and return to baseline.
    tone = _section(text, "### Tone Flex")
    required_tone_headers = ("Observable cue", "Reset condition")
    if not tone or any(header.lower() not in tone.lower() for header in required_tone_headers):
        diagnostics.append(
            _diag(
                "error",
                "tone-flex-contract",
                "Tone Flex needs an observable cue and reset condition for every rule.",
                text,
                "### Tone Flex",
            )
        )

    # Phrase Book: alternative palette plus anti-repetition behavior.
    phrase = _section(text, "### Phrase Book")
    phrase_rows = _table_rows(phrase)
    if not phrase_rows:
        diagnostics.append(_diag("error", "phrase-book-missing", "Phrase Book table is missing or empty.", text))
    for row in phrase_rows:
        if len(row) < 2:
            continue
        alternatives = [item for item in re.split(r"\s*/\s*|<br\s*/?>", row[1]) if item.strip()]
        if len(alternatives) < 2:
            diagnostics.append(
                _diag(
                    "error",
                    "phrase-book-variety",
                    f"Phrase Book category {row[0]!r} needs at least two alternatives.",
                    text,
                    row[0],
                )
            )
    phrase_lower = phrase.lower()
    if "palette, not a script" not in phrase_lower or "do not reuse the same phrase stem" not in phrase_lower:
        diagnostics.append(
            _diag(
                "error",
                "phrase-book-repetition",
                "Phrase Book needs palette and phrase-stem anti-repetition instructions.",
                text,
                "### Phrase Book",
            )
        )

    never = _section(text, "### Never-Say List")
    never_items = re.findall(r"(?m)^-\s+.+$", never)
    if len(never_items) < 5:
        diagnostics.append(
            _diag("error", "never-say-count", "Never-Say List needs at least five explicit entries.", text, "### Never-Say List")
        )

    lexicon = _section(text, "### Lexicon")
    lexicon_rows = _table_rows(lexicon)
    for row in lexicon_rows:
        if len(row) >= 2 and not row[1].strip():
            diagnostics.append(
                _diag("error", "lexicon-definition", f"Lexicon term {row[0]!r} is missing a definition.", text, row[0])
            )
    if not lexicon_rows:
        diagnostics.append(_diag("warning", "lexicon-empty", "No complete Lexicon rows found; mark not applicable or add definitions.", text))

    normalized_never = {
        re.split(r"\s+[—-]\s+", item.removeprefix("-").strip(), maxsplit=1)[0]
        .strip(" \'\"“”`.*!")
        .casefold()
        for item in never_items
    }
    for row in lexicon_rows:
        term = row[0].strip(" \'\"“”`.*!").casefold()
        if term and term in normalized_never:
            diagnostics.append(
                _diag(
                    "error",
                    "lexicon-never-say-conflict",
                    f"Lexicon term {row[0]!r} is also an exact Never-Say entry.",
                    text,
                    row[0],
                )
            )

    immutable = _section(text, "### Immutable Content")
    if immutable:
        normalized = " ".join(immutable.split()).lower()
        if "overrides persona and user style requests" not in normalized:
            diagnostics.append(
                _diag(
                    "error",
                    "immutable-precedence",
                    "Immutable Content must explicitly override Persona and user style requests.",
                    text,
                    "### Immutable Content",
                )
            )
        if "surrounding response shape" not in normalized:
            diagnostics.append(
                _diag(
                    "error",
                    "immutable-shape",
                    "Immutable Content must declare whether surrounding response context is allowed.",
                    text,
                    "### Immutable Content",
                )
            )

    # Conditional Chatting Style contracts.
    emoji = profile.get("Emoji")
    if emoji in {"Functional", "Expressive"}:
        has_vocab = bool(re.search(r"approved emoji vocabulary|status indicators", text, re.IGNORECASE))
        has_cadence = bool(re.search(r"\bRare\b|\bOccasional\b|\bRegular\b|cadence", text, re.IGNORECASE))
        if not (has_vocab and has_cadence):
            diagnostics.append(
                _diag("error", "emoji-contract", f"Emoji {emoji} needs approved vocabulary and observable cadence.", text, "Emoji")
            )
    if profile.get("Punctuation") == "Expressive":
        has_pattern = bool(re.search(r"punctuation pattern|em dash|em dashes|ellips", text, re.IGNORECASE))
        if not has_pattern:
            diagnostics.append(
                _diag("error", "punctuation-contract", "Expressive punctuation needs named marks and cadence.", text, "Punctuation")
            )
    if profile.get("Capitalization") == "Casual":
        required = ("proper noun", "product name", "acronym", "unit", "reorder")
        missing = [item for item in required if item not in text.lower()]
        if missing:
            diagnostics.append(
                _diag("error", "capitalization-contract", "Casual capitalization needs protected-case exceptions and no forced sentence reordering.", text, "Capitalization")
            )

    # Unusual pairings are design tensions, not universal contradictions.
    if profile.get("Formality") == "Formal" and (
        profile.get("Punctuation") == "Expressive"
        or profile.get("Emoji") == "Expressive"
        or profile.get("Capitalization") == "Casual"
    ):
        diagnostics.append(
            _diag(
                "warning",
                "dimension-pairing-warning",
                "Formal formality with Expressive punctuation/emoji or Casual capitalization is unusual but valid. Confirm the pairing consciously and document where it appears.",
                text,
                "Formality",
            )
        )
    if profile.get("Emotional Coloring") == "Clinical" and profile.get("Humor") == "Playful":
        diagnostics.append(
            _diag(
                "warning",
                "dimension-interaction-risk",
                "Clinical Emotional Coloring with Playful Humor showed context-sensitive instruction competition across two fixtures: Clinical cue masking in one and a required content-contract omission in the other even when both cues appeared. This is not a universal contradiction or safe-coexpression result. Confirm the tension, constrain Humor to explicit low-stakes contexts, and test the final combined instructions against the use-case content contract; do not block solely on the pair.",
                text,
                "Emotional Coloring",
            )
        )

    org_we_no = bool(re.search(r"Organizational [“\"]we[”\"]\*\*\s*\|\s*No\b", text, re.IGNORECASE))
    if org_we_no and re.search(r"[“\"]?[Ww]e[”\"]?\s+language", text):
        diagnostics.append(
            _diag("error", "organizational-we-conflict", "Organizational 'we' is No but the Persona separately authorizes we-language.", text, "we")
        )

    # Persona must not absorb spoken-channel platform configuration.
    voice_patterns = r"(?m)^\s*modality\s+voice\s*:|\bvoice_id\b|\bturn_timeout\b|\bspeech[-_ ]recognition\b"
    if re.search(voice_patterns, text, re.IGNORECASE):
        diagnostics.append(
            _diag("error", "voice-scope", "Persona artifacts must not contain platform voice configuration.", text)
        )

    severity_rank = {"error": 0, "warning": 1, "info": 2}
    diagnostics.sort(key=lambda item: (severity_rank[item["severity"]], item.get("line", 10**9), item["code"]))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        if args.json:
            print(json.dumps({"ok": False, "path": str(args.path), "error": str(error)}))
        else:
            print(f"Error reading {args.path}: {error}")
        return 2
    diagnostics = lint_text(text)
    errors = [item for item in diagnostics if item["severity"] == "error"]
    payload = {"ok": not errors, "path": str(args.path), "summary": {"errors": len(errors), "warnings": sum(item["severity"] == "warning" for item in diagnostics)}, "diagnostics": diagnostics}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for item in diagnostics:
            location = f":{item['line']}" if "line" in item else ""
            print(f"[{item['severity'][0].upper()}] {item['code']}{location} — {item['message']}")
        if not diagnostics:
            print(f"Persona lint OK: {args.path}")
        else:
            print(f"Persona lint: {len(errors)} error(s), {payload['summary']['warnings']} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
