#!/bin/bash

# Fetch Routing Metadata
# Pulls live routing configuration from the target org

set -e

# Load environment variables
if [ ! -f .env ]; then
  echo "❌ .env file not found. Copy .env.example to .env and configure."
  exit 1
fi

source .env

# Verify non-production org
echo "🔍 Verifying org is non-production..."
IS_SANDBOX=$(sf org display --target-org "$SF_ORG_ALIAS" --json 2>/dev/null | jq -e '.result.isSandbox' 2>/dev/null)
if [ "$IS_SANDBOX" != "true" ]; then
  echo "❌ Target org '$SF_ORG_ALIAS' does not appear to be a sandbox. Refusing to run on production."
  exit 1
fi
echo "✅ Confirmed: org is a sandbox"

echo ""
echo "📋 Fetching Routing Metadata..."
echo "================================"

# 1. Omni-Channel routing configurations
echo ""
echo "1. Omni-Channel Routing Configurations:"
sf data query \
  --query "SELECT Id, DeveloperName, RoutingModel, Capacity FROM RoutingConfig" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.DeveloperName): Model=\(.RoutingModel), Capacity=\(.Capacity)"'

# 2. Queues
echo ""
echo "2. Queues:"
sf data query \
  --query "SELECT Id, Name, Type FROM Group WHERE Type = 'Queue'" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.Name) (Id: \(.Id))"'

# 3. Service Channels
echo ""
echo "3. Omni-Channel Service Channels:"
sf data query \
  --query "SELECT Id, DeveloperName, RelatedEntityType FROM ServiceChannel" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.DeveloperName): \(.RelatedEntityType)"'

# 4. Active Flows (routing/availability related)
echo ""
echo "4. Active Flows (routing-related):"
sf data query \
  --query "SELECT Id, ApiName, Label, ProcessType, Status FROM FlowDefinitionView WHERE Status = 'Active' AND (ApiName LIKE '%Route%' OR ApiName LIKE '%Avail%' OR ApiName LIKE '%Escalat%')" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.Label) (\(.ApiName)): \(.ProcessType)"'

# 5. Apex Classes (routing/availability related)
echo ""
echo "5. Apex Classes (routing-related):"
sf data query \
  --query "SELECT Id, Name FROM ApexClass WHERE Name LIKE '%Avail%' OR Name LIKE '%Route%' OR Name LIKE '%Escalat%'" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.Name)"'

# 6. Business Hours
echo ""
echo "6. Business Hours:"
sf data query \
  --query "SELECT Id, Name, IsActive, IsDefault FROM BusinessHours WHERE IsActive = true" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.Name) (Default: \(.IsDefault))"'

# 7. Presence Configurations
echo ""
echo "7. Presence Configurations:"
sf data query \
  --query "SELECT Id, DeveloperName, Capacity FROM ServicePresenceStatus" \
  --target-org "$SF_ORG_ALIAS" \
  --json | jq -r '.result.records[] | "  - \(.DeveloperName): Capacity=\(.Capacity)"'

echo ""
echo "================================"
echo "✅ Metadata fetch complete"
echo ""
echo "Next steps:"
echo "1. Review the routing configuration above"
echo "2. Configure acceptance criteria in config/test-config.js"
echo "3. Share this output with your team and begin manual test execution"
