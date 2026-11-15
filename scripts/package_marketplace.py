"""Generate or check the committed packages derived from individual skills."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
BUNDLES = {
    "product-planning": (
        "Product Planning",
        "Explore a product decision, frame an experiment, or define a committed build.",
        ("think-with-me", "frame-concept-build", "frame-product-build"),
    ),
    "design-systems": (
        "Design Systems",
        "Build, document, or consolidate a design system.",
        ("build-design-system", "design-md", "design-system-consolidator"),
    ),
}
OPTIONAL_CATEGORIES = {"Agentforce", "Salesforce Platform and Analytics"}


SHARED_REFERENCES = (
    ("persona", "industry-patterns.md", "salesforce-industry-playbook"),
    ("persona", "industry-patterns.md", "agent-architecture"),
    ("persona", "industry-patterns.md", "conversation-design"),
    ("persona", "industry-patterns.md", "agentforce-generate"),
    ("persona", "industry-patterns.md", "agentforce-test"),
    ("persona", "industry-patterns.md", "agentforce-workshop-facilitator"),
    ("persona", "industry-patterns.md", "voice-ux"),

    ("agentforce-generate", "voice-latency-heuristics.md", "agentforce-observe"),
    ("agentforce-generate", "voice-latency-heuristics.md", "agentforce-test"),
    ("integration-connectivity-generate", "platform-events-guide.md", "experience-lwc-generate"),
)


def skill_path(name):
    return PLUGINS / name / "skills" / name


def package_files(root):
    if not root.exists():
        return {}
    return {
        path.relative_to(root): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not any(part in {".DS_Store", "__pycache__", ".pytest_cache"} for part in path.parts)
    }


def generated_packages():
    guidance = ROOT / "docs/salesforce"
    mapping = json.loads((guidance / "manifest.json").read_text())["skills"] if (guidance / "manifest.json").exists() else {}
    common = (guidance / "common.md").read_text() if mapping else ""
    for name, domains in mapping.items():
        body = common + "\n" + "\n".join((guidance / (domain + ".md")).read_text() for domain in domains)
        yield skill_path(name) / "references/current-salesforce", {Path("guide.md"): body.encode()}

    for name, (title, desc, members) in BUNDLES.items():
        if not (PLUGINS / name).exists():
            continue
        manifest = {
            "$schema": SCHEMA,
            "name": name,
            "version": "1.0.0",
            "description": desc,
            "extensions": {"com.openai": {"interface": {"displayName": title, "shortDescription": desc}}},
        }
        files = {Path("plugin.json"): (json.dumps(manifest, indent=2) + "\n").encode()}
        for member in members:
            source = package_files(skill_path(member))
            if Path("SKILL.md") not in source:
                raise ValueError(f"Missing {member} entrypoint")
            files.update({Path("skills") / member / path: data for path, data in source.items()})
        yield PLUGINS / name, files

    if skill_path("write-as-me").exists():
        source = skill_path("write-in-authentic-voice")
        workflow = (source / "SKILL.md").read_bytes().split(b"---", 2)[2].lstrip()
        writing = {Path("workflow.md"): workflow, Path("LICENSE"): (source / "LICENSE").read_bytes()}
        writing.update({Path("references") / path: data for path, data in package_files(source / "references").items()})
        yield skill_path("write-as-me") / "references/shared-writing", writing

    shared = {}
    for owner, name, consumer in SHARED_REFERENCES:
        if not skill_path(consumer).exists():
            continue
        source = skill_path(owner)
        files = shared.setdefault(consumer, {})
        files[Path(name)] = (source / "references" / name).read_bytes()
        for license_file in source.glob("LICENSE*"):
            files[Path(f"{owner}-{license_file.name}")] = license_file.read_bytes().rstrip(b"\r\n") + b"\n"
    for consumer, files in shared.items():
        yield skill_path(consumer) / "references/shared", files


def check_catalog():
    manifest = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    entries = manifest["plugins"]
    names = {entry["name"] for entry in entries}
    packages = {path.parent.name for path in PLUGINS.glob("*/plugin.json")}
    if manifest["name"] not in {"skills", "salesforce-skills"} or not entries or len(entries) != len(names) or names != packages:
        raise ValueError("Expected distinct marketplace entries matching the package folders")
    bundled_members = {member for _, _, members in BUNDLES.values() for member in members}
    for entry in entries:
        name = entry["name"]
        root = PLUGINS / name
        package = json.loads((root / "plugin.json").read_text())
        if package["name"] != name or entry["source"] != {"source": "local", "path": f"./plugins/{name}"}:
            raise ValueError(f"Invalid package name or path for {name}")
        category = entry["category"]
        if not category:
            raise ValueError(f"Missing catalog category for {name}")
        optional = category in OPTIONAL_CATEGORIES or name in bundled_members
        policy = "AVAILABLE" if optional else "INSTALLED_BY_DEFAULT"
        if entry["policy"]["installation"] != policy:
            raise ValueError(f"Expected {policy} for {name}")
        expected = set(BUNDLES[name][2]) if name in BUNDLES else {name}
        discovered = {path.parent.name for path in root.glob("skills/*/SKILL.md")}
        if discovered != expected:
            raise ValueError(f"Unexpected skill entrypoints in {name}")

    if skill_path("write-as-me").exists():
        writing = skill_path("write-as-me") / "references"
        release = json.loads((writing / "voice-release.json").read_text())
        if sha256((writing / "voice-profile.md").read_bytes()).hexdigest() != release["profile_sha256"]:
            raise ValueError("The private writing profile checksum differs from its release metadata")


def check_references():
    from urllib.parse import unquote, urlsplit

    link = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    example_targets = {"[docs-url]", "[homepage-url]", "CONTRIBUTING.md", "LICENSE", "url"}
    errors = []
    for f in sorted(PLUGINS.glob("*/skills/*/**/*.md")):
        package = PLUGINS / f.relative_to(PLUGINS).parts[0]
        for href in link.findall(f.read_text(encoding="utf-8")):
            target = unquote(href.strip("<>")).split("#", 1)[0]
            if not target:
                continue
            if re.fullmatch(r"http://[\w.-]+\.md", target, re.IGNORECASE):
                errors.append(f"{f.relative_to(ROOT)}: invalid filename URL {href}")
                continue
            if urlsplit(target).scheme:
                continue
            if f.name == "template.md" and "write-readme" in f.parts and target in example_targets:
                continue
            path = (f.parent / target).resolve()
            if not path.is_relative_to(package.resolve()) or not path.exists():
                errors.append(f"{f.relative_to(ROOT)}: missing packaged reference {href}")
    if errors:
        raise ValueError("\n".join(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify without rewriting generated files")
    args = parser.parse_args()
    stale = []
    if skill_path("agentforce-generate").exists():
        grounding_workflow = skill_path("agentforce-grounding") / "references/workflow.md"
        for name in ("agentforce-generate",):
            copy = skill_path(name) / "references/grounding-workflow.md"
            if not copy.exists() or copy.read_bytes() != grounding_workflow.read_bytes():
                if args.check:
                    stale.append(str(copy.relative_to(ROOT)))
                else:
                    copy.write_bytes(grounding_workflow.read_bytes())
        grounding_source = skill_path("agentforce-grounding") / "references/data-library-reference.md"
        grounding_copy = skill_path("agentforce-generate") / "references/data-library-reference.md"
        grounding_bytes = grounding_source.read_bytes().replace(b"(workflow.md)", b"(grounding-workflow.md)")
        if not grounding_copy.exists() or grounding_copy.read_bytes() != grounding_bytes:
            if args.check:
                stale.append(str(grounding_copy.relative_to(ROOT)))
            else:
                grounding_copy.write_bytes(grounding_bytes)
    for directory, files in generated_packages():
        if package_files(directory) == files:
            continue
        if args.check:
            stale.append(str(directory.relative_to(ROOT)))
            continue
        if directory.exists():
            shutil.rmtree(directory)
        for path, data in files.items():
            dest = directory / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    if stale:
        print("Regenerate these packages:\n" + "\n".join(stale), file=sys.stderr)
        return 1
    check_catalog()
    check_references()
    print("Checked catalog entries, applicable generated packages/checksums, and Markdown links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
