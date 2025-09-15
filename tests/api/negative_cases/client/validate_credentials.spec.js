// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Validate Credentials - Negative Cases', () => {

    test('Validate Credentials endpoint rejects unknown email', async ({ request, endpoints, randomString, assertions }) => {

        await test.step(`POST to ${endpoints.auth.validate_credentials}`, async () => {

            const response = await request.post(endpoints.auth.validate_credentials, {
                data: {

                    "email": `unknown_email_${randomString(6)}@email.com`,
                    "password": randomString(10),

                }
            });

            assertions.expectStatus(response, 401);

            const responseBody = await response.json();

            assertions.expectHasProperty(responseBody, 'error');

            assertions.expectPropertyValue(responseBody, 'error', 'Invalid credentials');

        });
    });

    test('Validate Credentials endpoint rejects invalid password', async ({ request, endpoints, randomString, assertions }) => {

        const clientData = {};

        await test.step('Creates a new user', async () => {

            const email = `user_${randomString(6)}@email.com`;

            const password = randomString(10);

            const response = await request.post(endpoints.auth.register_credentials, {
                data: {

                    "email": email,
                    "repeat_email": email,
                    "password": password,
                    "repeat_password": password,

                }

            });

            assertions.expectStatus(response, 201);

            clientData.email = email;

        });

        await test.step(`POST to ${endpoints.auth.validate_credentials}`, async () => {

            const response = await request.post(endpoints.auth.validate_credentials, {
                data: {

                    "email": clientData.email,
                    "password": randomString(10),

                }
            });

            assertions.expectStatus(response, 401);

            const responseBody = await response.json();

            assertions.expectHasProperty(responseBody, 'error');

            assertions.expectPropertyValue(responseBody, 'error', 'Invalid credentials');

        });
    });

});
