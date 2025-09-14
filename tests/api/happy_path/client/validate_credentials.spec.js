// tests/api/health.spec.js
const { test } = require('../../../../fixtures/common.fixture');

test.describe('Validate User Credentials', () => {
  test('Validate credentials endpoint works properly [@smoke]', async ({ request, endpoints, randomString, assertions }) => {
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

      // ── Cookie HttpOnly 'cid' (acceso directo al header) ──
      // Reemplazá esta línea que rompe:
      // const setCookie = response.headerValue('set-cookie');

      // Por esto:
      const setCookie = response.headers()['set-cookie']; // header en minúsculas
      assertions.expectPropertyTruthy(setCookie);

      // Parse básico de la cookie
      const parts = setCookie.split(';').map(s => s.trim());
      const [nameValue, ...attrs] = parts;
      const [cookieName, cookieVal] = nameValue.split('=');

      // Validaciones
      assertions.expectPropertyValue({ cookieName }, 'cookieName', 'cid');
      assertions.expectPropertyTruthy(cookieVal);

      const has = (k) => attrs.some(a => a.toLowerCase() === k.toLowerCase());
      assertions.expectPropertyTruthy(has('HttpOnly'));
      assertions.expectPropertyTruthy(has('Path=/'));
      assertions.expectPropertyTruthy(has('SameSite=Lax'));

      const secureExpected = !!Number(process.env.COOKIE_SECURE || '0');
      if (secureExpected) {
        assertions.expectPropertyTruthy(has('Secure'));
      }


      // ✅ Business assertions
      assertions.expectHasProperty(body, 'data');
      assertions.expectHasProperty(body.data, 'businesses');

      const defaultBusiness = body.data.businesses[0];
      assertions.expectHasProperty(defaultBusiness, 'branches');

      // Branch assertions
      const defaultBranch = defaultBusiness.branches[0];
      assertions.expectHasProperty(defaultBranch, 'branch_id');
      assertions.expectPropertyTruthy(defaultBranch.branch_id);
      assertions.expectHasProperty(defaultBranch, 'branch_name');
      assertions.expectPropertyTruthy(defaultBranch.branch_name);
      assertions.expectHasProperty(defaultBranch, 'sections');

      // Section assertions
      const defaultSection = defaultBranch.sections[0];
      assertions.expectHasProperty(defaultSection, 'section_id');
      assertions.expectPropertyTruthy(defaultSection.section_id);
      assertions.expectHasProperty(defaultSection, 'section_name');
      assertions.expectPropertyTruthy(defaultSection.section_name);
    });
  });
});
