/**
 * Test Configuration
 *
 * This file contains test configuration and flags.
 * NO CREDENTIALS should be stored here - all auth is in .env
 */

module.exports = {
  // Org configuration (alias only - credentials in .env)
  orgAlias: process.env.SF_ORG_ALIAS,

  // Agent configuration
  agentName: process.env.AGENT_NAME,
  humanAgentCount: parseInt(process.env.HUMAN_AGENT_COUNT || '2'),

  // Test configuration
  testCaseCount: parseInt(process.env.TEST_CASE_COUNT || '10'),
  availabilityCheckMethod: process.env.AVAILABILITY_CHECK_METHOD || 'flow',

  // Scenario flags - which scenarios to run
  scenarios: {
    A: true,  // No agents available — fallback
    B: true,  // Agents available — successful routing
    C: process.env.AVAILABILITY_CHECK_METHOD === 'flow',
    D: process.env.AVAILABILITY_CHECK_METHOD === 'apex',
    E: true,  // Capacity exceeded
    F: true,  // Business hours boundary
    G: true,  // Routing model stress test
    H: !!process.env.EXTERNAL_SYSTEM_ENDPOINT,  // External integration
    I: true,  // Messaging Session status lifecycle
    J: true,  // Agent ends session
  },

  // Timeout configuration (milliseconds)
  timeouts: {
    apiCall: 30000,
    sessionRouting: 60000,
    flowExecution: 45000,
    apexExecution: 30000,
  },

  // Acceptance criteria (can be overridden at runtime)
  acceptanceCriteria: {
    caseCreatedOnFallback: true,
    sessionStatusUpdated: true,
    fallbackMessageSent: false,
    transcriptAttached: false,
    externalSystemNotified: false,
    botReEngagement: false,
  },
};
