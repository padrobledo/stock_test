// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Health Check', () => {

  // TODO: Update endpoint to hit /health from endpoints
  test('Ensures API is up and running [@smoke]', async ({ request, endpoints, assertions }) => {

    const response = await request.get(endpoints.health);

    assertions.expectStatus(response, 200);

  });
  
});
