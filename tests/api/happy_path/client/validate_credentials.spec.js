const { test } = require('../../../../fixtures/common.fixture');

test.describe('Validate User Credentials', () => {
  test('POST /auth/validate_credentials sets HttpOnly cid cookie [@smoke]', async ({ request, endpoints, randomString, assertions }) => {
    // 1) Crear usuario
    const email = `user_${randomString(6)}@email.com`;
    const password = randomString(10);

    const regRes = await request.post(endpoints.auth.register_credentials, {
      data: { email, repeat_email: email, password, repeat_password: password },
    });
    assertions.expectStatus(regRes, 201);

    // 2) Login (validate credentials)
    const response = await request.post(endpoints.auth.validate_credentials, {
      data: { email, password },
    });
    assertions.expectStatus(response, 201);

    // 3) Cookie HttpOnly 'cid'
    const setCookie = response.headers()['set-cookie']; // header en minúsculas
    assertions.expectPropertyTruthy(setCookie);

    const parts = setCookie.split(';').map(s => s.trim());
    const [nameValue, ...attrs] = parts;
    const [cookieName, cookieVal] = nameValue.split('=');

    // Nombre y valor
    assertions.expectPropertyValue({ cookieName }, 'cookieName', 'cid');
    assertions.expectPropertyTruthy(cookieVal);

    // Atributos esperados
    const has = (k) => attrs.some(a => a.toLowerCase() === k.toLowerCase());
    assertions.expectPropertyTruthy(has('HttpOnly'));
    assertions.expectPropertyTruthy(has('Path=/'));
    assertions.expectPropertyTruthy(has('SameSite=Lax'));

    // Secure depende de .env/.env.local (COOKIE_SECURE)
    const secureExpected = !!Number(process.env.COOKIE_SECURE || '0');
    if (secureExpected) {
      assertions.expectPropertyTruthy(has('Secure'));
    }
  });
});
