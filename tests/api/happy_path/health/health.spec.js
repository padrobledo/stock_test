// tests/api/health.spec.js

const { test, expect } = require('@playwright/test');

test.describe('Health Check', () => {

  test('Ensures API is up and running [@smoke]', async ({ request }) => {

    const res = await request.get('/');

    expect(res.ok()).toBeTruthy();

  });
  
});
