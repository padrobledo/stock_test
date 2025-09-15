// tests/fixtures/common.fixture.js

const playwright = require('@playwright/test');
const endpoints = require('../configuration/endpoints');
const randomString = require('../helpers/random_string');
const assertions = require('../helpers/assertions');
const preconditions = require('../helpers/preconditions');
const base = playwright.test;
const expect = playwright.expect;

const test = base.extend({

  endpoints: async ({ }, use) => {
    await use(endpoints);
  },

  randomString: async ({ }, use) => {
    await use(randomString);
  },

  assertions: async ({ }, use) => {
    await use(assertions);
  },

  preconditions: async ({ request, endpoints, randomString, assertions }, use) => {
    // Exponemos helpers ya atados a request/endpoints
    await use({
      new_client: () => preconditions.new_client({ request, endpoints, randomString, assertions }),
      login_client: ({ email, password }) =>
        preconditions.login_client({ request, endpoints, assertions, email, password }),
    });
  }

});

module.exports = { test, expect };
