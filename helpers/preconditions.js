// tests/helpers/preconditions.js

async function new_client({ request, endpoints, randomString, assertions }) {
    const email = `user_${randomString(6)}@email.com`;
    const password = randomString(10);

    const res = await request.post(endpoints.auth.register_credentials, {
        data: { email, repeat_email: email, password, repeat_password: password },
    });

    assertions.expectStatus(res, 201);
    return { email, password, response: res };
}

async function login_client({ request, endpoints, assertions, email, password }) {
    const res = await request.post(endpoints.auth.validate_credentials, {
        data: { email, password },
    });
    assertions.expectStatus(res, 201);

    const setCookie = res.headers()['set-cookie'];
    if (!setCookie) throw new Error("Missing 'set-cookie' in login response");
    const [nameValue] = setCookie.split(';');
    const [cookieName, cookieVal] = nameValue.split('=');

    return {
        cookieName,
        cookieVal,
        cookie: `${cookieName}=${cookieVal}`,
        response: res,
    };
}

module.exports = { new_client, login_client };
