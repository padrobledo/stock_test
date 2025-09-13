// tests/fixtures/common.fixture.js

const playwright = require('@playwright/test');
const endpoints = require('../configuration/endpoints');
const randomString = require('../helpers/random_string');
const assertions = require('../helpers/assertions');
const base = playwright.test;
const expect = playwright.expect;

const test = base.extend({

  endpoints: async ({}, use) => {
    await use(endpoints);
  },

  randomString: async ({}, use) => {
    await use(randomString);
  },
  
  assertions: async ({}, use) => {
    await use(assertions);
  }

});

module.exports = { test, expect };
