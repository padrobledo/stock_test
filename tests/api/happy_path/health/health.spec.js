// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Health Check', () => {

  test('Ensures API is up and running [@smoke]', async ({ request, endpoints, assertions }) => {

    const response = await request.get(endpoints.health);

    assertions.expectStatus(response, 200);

  });
  
});
