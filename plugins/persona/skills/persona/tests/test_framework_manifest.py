"""Validate the machine-readable Persona framework inventory."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "check_framework_manifest.py"
MANIFEST = SKILL_ROOT / "references" / "framework-manifest.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_framework_manifest", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrameworkManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = _load_module()
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_matches_shipping_sources(self):
        self.assertEqual([], self.module.validate(SKILL_ROOT))

    def test_manifest_has_fourteen_unique_dimensions(self):
        dimensions = self.manifest["dimensions"]
        self.assertEqual(14, len(dimensions))
        self.assertEqual(14, len({item["id"] for item in dimensions}))
        self.assertEqual(14, len({item["name"] for item in dimensions}))
        self.assertTrue(all(item.get("status") for item in dimensions))

    def test_register_partial_evidence_status_is_explicit(self):
        register = next(
            item
            for item in self.manifest["dimensions"]
            if item["id"] == "DIM-REGISTER"
        )
        self.assertEqual(
            "partly effective; Peer overlaps Advisor without genuine shared work",
            register["status"],
        )

    def test_emotional_coloring_partial_evidence_status_is_explicit(self):
        coloring = next(
            item
            for item in self.manifest["dimensions"]
            if item["id"] == "DIM-EMOTIONAL-COLORING"
        )
        self.assertEqual(
            "partly effective; non-Neutral cues required, compound-position leakage documented, and Clinical with Playful has a cross-fixture non-blocking instruction-competition warning",
            coloring["status"],
        )
        humor = next(
            item
            for item in self.manifest["dimensions"]
            if item["id"] == "DIM-HUMOR"
        )
        self.assertEqual(
            "directional positive; Playful cue and high-stakes suppression observed; Clinical interaction remains a cross-fixture non-blocking warning",
            humor["status"],
        )

    def test_reconstructed_personification_is_canonical(self):
        personification = next(
            item
            for item in self.manifest["dimensions"]
            if item["id"] == "DIM-PERSONIFICATION"
        )
        self.assertEqual(
            ["Not personal", "Individuated", "Anthropomorphic"],
            personification["positions"],
        )

    def test_generic_heuristic_and_progression_statuses_are_explicit(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertEqual(
            "retain; behaviorally defined and directionally validated",
            components["CMP-RADIO-TEST"]["status"]
        )
        self.assertEqual(
            "owned by conversation-design; no universal Persona rule",
            components["CMP-TAPERING"]["status"],
        )

    def test_identity_component_evidence_statuses_are_explicit(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertEqual(
            "retain; behavioral definitions directionally validated",
            components["CMP-IDENTITY"]["status"],
        )
        self.assertEqual(
            "retain; directionally validated",
            components["CMP-NEGATIVE-IDENTITY"]["status"],
        )
        self.assertEqual(
            "conditional; incremental runtime effect unproven",
            components["CMP-VALUES"]["status"],
        )

    def test_verbal_fingerprint_evidence_statuses_are_explicit(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertEqual(
            "retain; varied palette directionally validated; figurative/signature cues need bounded semantic jobs",
            components["CMP-PHRASE-BOOK"]["status"],
        )
        self.assertEqual(
            "retain conditionally; function-bound directional evidence",
            components["CMP-DISCOURSE-MARKERS"]["status"],
        )
        self.assertEqual(
            "retain; exact anti-phrases and controlled boundary calibration validated; runtime proof handed to agentforce-test",
            components["CMP-NEVER-SAY"]["status"],
        )

    def test_tone_policy_evidence_statuses_are_explicit(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertEqual(
            "retain conditionally; pair plausible drift with preferred behavior",
            components["CMP-TONE-BOUNDARIES"]["status"],
        )
        self.assertEqual(
            "retain; observable lexical/discourse cues and reset conditions directionally validated",
            components["CMP-TONE-FLEX"]["status"],
        )
        self.assertIn("Persona owns semantic and lexical policy", components["CMP-TONE-FLEX"]["ownership"])
        self.assertIn("voice-ux", components["CMP-TONE-FLEX"]["ownership"])

    def test_content_contract_evidence_statuses_are_explicit(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertEqual(
            "retain; definitions and stable meaning validated",
            components["CMP-LEXICON"]["status"],
        )
        self.assertEqual(
            "retain; verbatim precedence validated",
            components["CMP-IMMUTABLE"]["status"],
        )
        self.assertEqual(
            "retain as agent-design-adjacent; content boundary validated",
            components["CMP-GUARDRAILS"]["status"],
        )
        self.assertEqual(
            "agent-design-adjacent",
            components["CMP-GUARDRAILS"]["ownership"],
        )

    def test_static_copy_candidates_defer_to_canonical_authoring(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertIn("wording candidates", components["CMP-STATIC-MESSAGES"]["status"])
        self.assertIn("canonical authoring owner", components["CMP-STATIC-MESSAGES"]["status"])
        self.assertEqual(
            "agentforce-generate validates state honesty and applies the candidate",
            components["CMP-ACTION-PROGRESS"]["ownership"],
        )

    def test_subagent_calibration_is_semantic_handoff(self):
        components = {item["id"]: item for item in self.manifest["components"]}
        self.assertIn("approved semantic delta", components["CMP-SUBAGENT-CALIBRATION"]["status"])
        self.assertIn("canonical authoring owner", components["CMP-SUBAGENT-CALIBRATION"]["status"])

    def test_encoding_manifest_names_canonical_owners(self):
        encoding = self.manifest["encoding"]
        self.assertIn("agentforce-generate", encoding["agent_script_owner"])
        self.assertIn("semantic character deltas", encoding["brownfield_invariant"])
        self.assertIn("conversation-design", encoding["content_contract_invariant"])
        self.assertIn("agentforce-test", encoding["content_contract_invariant"])

    def test_cli_reports_success(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("14 dimensions", result.stdout)


if __name__ == "__main__":
    unittest.main()
