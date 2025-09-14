// tests/api/health.spec.js
const { test } = require('../../../../fixtures/common.fixture');

test.describe('Validate User Credentials', () => {
  test.skip('Validate credentials endpoint works properly [@smoke]', async ({ request, endpoints, randomString, assertions }) => {
    const clientData = {};

    await test.step('Creates a new user', async () => {
      const email = `user_${randomString(6)}@email.com`;
      const password = randomString(10);

      const response = await request.post(endpoints.auth.register_new_client, {
        data: {
          email,
          repeat_email: email,
          password,
          repeat_password: password,
        },
      });

      assertions.expectStatus(response, 201);
      clientData.email = email;
      clientData.password = password;
    });

    await test.step(`POST to '${endpoints.auth.validate_user_credentials}'`, async () => {
      const response = await request.post(endpoints.auth.validate_user_credentials, { data: clientData });
      const body = await response.json();

      // 201 esperado
      assertions.expectStatus(response, 201);

      // // ✅ Acceso directo al header Set-Cookie (sin búsquedas en arrays)
      // const headers = response.headers();
      // const setCookie = headers['set-cookie'];

      // test.expect(setCookie, 'Expected Set-Cookie header').toBeTruthy();
      // test.expect(setCookie).toContain('access_token=');
      // test.expect(setCookie).toMatch(/HttpOnly/i);
      // // opcional si configuraste Lax:
      // // test.expect(setCookie).toMatch(/SameSite=Lax/i);

      // // ✅ Business assertions
      // assertions.expectHasProperty(body, 'business_list');
      // const defaultBusiness = body.business_list[0];
      // assertions.expectHasProperty(defaultBusiness, 'branches');

      // // Branch assertions
      // const defaultBranch = defaultBusiness.branches[0];
      // assertions.expectHasProperty(defaultBranch, 'branch_id');
      // assertions.expectPropertyTruthy(defaultBranch.branch_id);
      // assertions.expectHasProperty(defaultBranch, 'branch_name');
      // assertions.expectPropertyTruthy(defaultBranch.branch_name);
      // assertions.expectHasProperty(defaultBranch, 'sections');

      // // Section assertions
      // const defaultSection = defaultBranch.sections[0];
      // assertions.expectHasProperty(defaultSection, 'section_id');
      // assertions.expectPropertyTruthy(defaultSection.section_id);
      // assertions.expectHasProperty(defaultSection, 'section_name');
      // assertions.expectPropertyTruthy(defaultSection.section_name);
    });
  });
});
