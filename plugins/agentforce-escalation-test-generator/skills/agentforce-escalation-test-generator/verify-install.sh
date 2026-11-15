#!/bin/bash

# Check the package beside this script, or an explicitly supplied directory.
set -euo pipefail
skill_dir="${1:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}"

echo "🔍 Verifying Agentforce Escalation Test Generator Installation"
echo "=============================================================="
echo ""

# Check SKILL.md exists
if [ -f "$skill_dir/SKILL.md" ]; then
  echo "✅ SKILL.md found"
else
  echo "❌ SKILL.md not found"
  exit 1
fi

# Check templates directory
if [ -d "$skill_dir/templates" ]; then
  echo "✅ templates/ directory found"
else
  echo "❌ templates/ directory not found"
  exit 1
fi

# Check modules directory
if [ -d "$skill_dir/modules" ]; then
  echo "✅ modules/ directory found"
else
  echo "❌ modules/ directory not found"
  exit 1
fi

# Check required module files
REQUIRED_MODULES=(
  "modules/SOQL_QUERIES.md"
  "modules/BUSINESS_LOGIC_EXAMPLES.md"
  "modules/SAFETY_PROBES.md"
  "modules/GRACEFUL_DEGRADATION.md"
  "modules/TEST_TEMPLATES.md"
  "modules/OUTPUT_FORMATS.md"
  "modules/EXECUTION_SUMMARY.md"
)

for module in "${REQUIRED_MODULES[@]}"; do
  if [ -f "$skill_dir/$module" ]; then
    echo "✅ $module"
  else
    echo "❌ $module missing"
    exit 1
  fi
done

# Check required template files
REQUIRED_TEMPLATES=(
  "templates/test-dashboard.html"
  "templates/README.md"
  "templates/scripts/fetch-metadata.sh"
)

for file in "${REQUIRED_TEMPLATES[@]}"; do
  if [ -f "$skill_dir/$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file missing"
    exit 1
  fi
done

echo ""
echo "=============================================================="
echo "✅ Skill installation verified successfully!"
echo ""
echo "Usage:"
echo '  In Codex: $agentforce-escalation-test-generator'
echo ""
echo "Or describe your testing needs and Codex can select the skill when it fits."
