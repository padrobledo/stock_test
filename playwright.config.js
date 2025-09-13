// playwright.config.js
const { defineConfig, devices } = require('@playwright/test');

const BASE_URL = process.env.BASE_URL;

module.exports = defineConfig({
  testDir: 'tests',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  use: {
    baseURL: BASE_URL,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    }
  ],
  reporter: [['html', { open: 'never' }], ['list']]
});
