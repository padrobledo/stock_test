// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Register New Client - Negative Cases', () => {

    const newClientData = {};

    test('Registration endpoint rejects duplicated email', async ({ request, endpoints, randomString, assertions }) => {

        await test.step('Register a new email', async () => {

            const email = `user_${randomString(6)}@example.com`;

            const password = randomString(10);

            newClientData.email = email;

            newClientData.repeat_email = email;

            newClientData.password = password;

            newClientData.repeat_password = password;

            const response = await request.post(endpoints.auth.register_new_client, { data: newClientData });

            assertions.expectStatus(response, 201);

        });

        await test.step(`POST to '${endpoints.auth.register_new_client}'`, async () => {

            const response = await request.post(endpoints.auth.register_new_client, { data: newClientData });

            const responseBody = await response.json();

            assertions.expectStatus(response, 409);

            assertions.expectHasProperty(responseBody, 'error');

            assertions.expectPropertyValue(responseBody, 'error', 'Email already registered');

        });

    });

    test('Registration endpoint rejects when passwords do not match', async ({ request, endpoints, randomString, assertions }) => {

        const wrongClientData = newClientData;

        await test.step('Prepare credentials', async () => {

            wrongClientData.repeat_password = "do-not-match";

        });

        await test.step(`POST to '${endpoints.auth.register_new_client}'`, async () => {

            const response = await request.post(endpoints.auth.register_new_client, { data: wrongClientData });

            const responseBody = await response.json();

            assertions.expectStatus(response, 400);

            assertions.expectHasProperty(responseBody, 'error');

            assertions.expectPropertyValue(responseBody, 'error', 'Passwords do not match');

        });

    });

    test('Registration endpoint rejects when emails do not match', async ({ request, endpoints, randomString, assertions }) => {

        const wrongClientData = newClientData;

        await test.step('Prepare credentials', async () => {

            wrongClientData.repeat_email = "do-not-match@email.com";

        });

        await test.step(`POST to '${endpoints.auth.register_new_client}'`, async () => {

            const response = await request.post(endpoints.auth.register_new_client, { data: wrongClientData });

            const responseBody = await response.json();

            assertions.expectStatus(response, 400);

            assertions.expectHasProperty(responseBody, 'error');

            assertions.expectPropertyValue(responseBody, 'error', 'Emails do not match');

        });

    });

});
