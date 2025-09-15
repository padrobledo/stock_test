// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Register New Client - Negative Cases', () => {

    test('Registration endpoint rejects duplicated email', async ({ request, endpoints, assertions, preconditions }) => {
        const newClientData = {};

        await test.step('Register a new client', async () => {
            const { email, password } = await preconditions.new_client();

            newClientData.email = email;
            newClientData.repeat_email = email;
            newClientData.password = password;
            newClientData.repeat_password = password;

        });

        await test.step(`POST to '${endpoints.auth.register_credentials}'`, async () => {
            const response = await request.post(endpoints.auth.register_credentials, { data: newClientData });
            const responseBody = await response.json();

            assertions.expectStatus(response, 409);
            assertions.expectHasProperty(responseBody, 'error');
            assertions.expectPropertyValue(responseBody, 'error', 'Email already registered');
        });
    });

    test('Registration endpoint rejects when passwords do not match', async ({ request, endpoints, randomString, assertions }) => {
        const wrongClientData = {
            email: 'pw-do-not-match@email.com',
            repeat_email: 'pw-do-not-match@email.com',
            password: randomString(10),
            repeat_password: randomString(10),
        };

        await test.step(`POST to '${endpoints.auth.register_credentials}'`, async () => {
            const response = await request.post(endpoints.auth.register_credentials, { data: wrongClientData });
            const responseBody = await response.json();

            assertions.expectStatus(response, 400);
            assertions.expectHasProperty(responseBody, 'error');
            assertions.expectPropertyValue(responseBody, 'error', 'Passwords do not match');
        });
    });

    test('Registration endpoint rejects when emails do not match', async ({ request, endpoints, randomString, assertions }) => {
        const wrongClientData = {
            email: `do-not-match-${randomString(6)}@email.com`,
            repeat_email: `do-not-match-${randomString(6)}@email.com`,
            password: 'TestPassword1234',
            repeat_password: 'TestPassword1234',
        };

        await test.step(`POST to '${endpoints.auth.register_credentials}'`, async () => {
            const response = await request.post(endpoints.auth.register_credentials, { data: wrongClientData });
            const responseBody = await response.json();

            assertions.expectStatus(response, 400);
            assertions.expectHasProperty(responseBody, 'error');
            assertions.expectPropertyValue(responseBody, 'error', 'Emails do not match');
        });
    });

    test('Registration endpoint rejects when password length is less than 6', async ({ request, endpoints, randomString, assertions }) => {
        
        const email = `shortpw_${randomString(6)}@email.com`;

        const wrongClientData = {
            email: email,
            repeat_email: email,
            password: '12345',
            repeat_password: '12345',
        };

        await test.step(`POST to '${endpoints.auth.register_credentials}'`, async () => {
            const response = await request.post(endpoints.auth.register_credentials, { data: wrongClientData });
            const responseBody = await response.json();

            assertions.expectStatus(response, 400);
            assertions.expectHasProperty(responseBody, 'error');
            assertions.expectPropertyValue(responseBody, 'error', 'Password must be at least 6 characters');
        });
    });

    test('Registration endpoint rejects when email is empty', async ({ request, endpoints, assertions }) => {
        const wrongClientData = {
            email: '',
            repeat_email: '',
            password: 'ValidPass123',
            repeat_password: 'ValidPass123',
        };

        await test.step(`POST to '${endpoints.auth.register_credentials}'`, async () => {
            const response = await request.post(endpoints.auth.register_credentials, { data: wrongClientData });
            const responseBody = await response.json();

            assertions.expectStatus(response, 400);
            assertions.expectHasProperty(responseBody, 'error');
            assertions.expectPropertyValue(responseBody, 'error', 'Email can not be empty');
        });
    });

    test('Registration endpoint rejects when password is empty', async ({ request, endpoints, randomString, assertions }) => {
        
        const email = `emptypw_${randomString(6)}@email.com`;

        const wrongClientData = {
            email: email,
            repeat_email: email,
            password: '',
            repeat_password: '',
        };

        await test.step(`POST to '${endpoints.auth.register_credentials}'`, async () => {
            const response = await request.post(endpoints.auth.register_credentials, { data: wrongClientData });
            const responseBody = await response.json();

            assertions.expectStatus(response, 400);
            assertions.expectHasProperty(responseBody, 'error');
            assertions.expectPropertyValue(responseBody, 'error', 'Password can not be empty');
        });
    });

});
