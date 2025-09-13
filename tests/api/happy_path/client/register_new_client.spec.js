// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Register New Client', () => {

    test('Registration endpoint works properly [@smoke]', async ({ request, endpoints, randomString, assertions }) => {

        const newClientData = {};

        await test.step('Prepare new client credentials', async () => {

            const email = `user_${randomString(6)}@example.com`;

            const password = randomString(10);

            newClientData.email = email;

            newClientData.repeat_email = email;

            newClientData.password = password;

            newClientData.repeat_password = password;

        });

        await test.step(`POST to '${endpoints.auth.register_new_client}'`, async () => {

            const response = await request.post(endpoints.auth.register_new_client, { data: newClientData });

            const responseBody = await response.json();

            assertions.expectStatus(response, 201);

            assertions.expectHasProperty(responseBody, 'message');

            assertions.expectPropertyValue(responseBody, 'message', 'Account successfully created');

        });

    });

});
