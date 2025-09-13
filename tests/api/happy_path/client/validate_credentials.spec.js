// tests/api/health.spec.js

const { test } = require('../../../../fixtures/common.fixture');

test.describe('Validate User Credentials', () => {

    test('Validate credentials endpoint works properly [@smoke]', async ({ request, endpoints, randomString, assertions }) => {

        const clientData = {};

        await test.step('Creates a new user', async () => {

            const email = `user_${randomString(6)}@example.com`;

            const password = randomString(10);

            const response = await request.post(endpoints.auth.register_new_client, { data: {

                    "email": email,
                    "repeat_email": email,
                    "password": password,
                    "repeat_password": password,

                }

            });

            assertions.expectStatus(response, 201);

            clientData.email = email;

            clientData.password = password;

        });

        await test.step(`POST to '${endpoints.auth.validate_user_credentials}'`, async () => {

            const response = await request.post(endpoints.auth.validate_user_credentials, { data: clientData });

            const responseBody = await response.json();

            assertions.expectStatus(response, 201);

            // Token assertions
            assertions.expectHasProperty(responseBody, 'access_token');
            assertions.expectPropertyTruthy(responseBody, 'access_token');
            assertions.expectHasProperty(responseBody, 'token_type');
            assertions.expectPropertyValue(responseBody, 'token_type', 'Bearer');

            // Business assertions
            assertions.expectHasProperty(responseBody, 'business_list');
            const firstBusiness = responseBody.business_list[0];
            assertions.expectHasProperty(firstBusiness, 'branches');

            // Branch assertions
            const firstBranch = firstBusiness.branches[0];
            assertions.expectHasProperty(firstBranch, 'branch_id');
            assertions.expectPropertyTruthy(firstBranch.branch_id);
            assertions.expectHasProperty(firstBranch, 'branch_name');
            assertions.expectPropertyTruthy(firstBranch.branch_name);
            assertions.expectHasProperty(firstBranch, 'sections');

            // Section assertions
            const firstSection = firstBranch.sections[0];
            assertions.expectHasProperty(firstSection, 'section_id');
            assertions.expectPropertyTruthy(firstSection.section_id);
            assertions.expectHasProperty(firstSection, 'section_name');
            assertions.expectPropertyTruthy(firstSection.section_name);

        });

    });

});
