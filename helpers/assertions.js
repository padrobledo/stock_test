// helpers/assertions.js

const { expect } = require('@playwright/test');

// Validates the status of a response

function expectStatus(response, expectedStatus) {

  const status = response.status();

  expect(
    status,
    `Expected status code ${expectedStatus}, but got ${status}`
  ).toBe(expectedStatus);

}

// Validates that a body has a given property

function expectHasProperty(body, propName) {

  expect(
    body,
    `Argument '${propName}' missing in response`
  ).toHaveProperty(propName);

}

// Validates that a property has the expected value

function expectPropertyValue(body, propName, expectedValue) {

  expectHasProperty(body, propName); // reuse the check above

  expect(
    body[propName],
    `Expected '${propName}' to be "${expectedValue}", but got "${body[propName]}"`
  ).toBe(expectedValue);

}

module.exports = {

  expectStatus,
  expectHasProperty,
  expectPropertyValue,
  
};
