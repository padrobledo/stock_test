// tests/api/happy_path/client/get_client_data.spec.js
const { test } = require('../../../../fixtures/common.fixture');

test.describe('Get Client Data', () => {
  test('GET Client Data endpoint returns businesses tree [@smoke]', async ({ request, endpoints, assertions, preconditions }) => {

    let email, password, cookie;

    await test.step('Register and login a new client', async () => {
      const res = await preconditions.new_client(); // crea y valida 201 internamente
      email = res.email;
      password = res.password;

      const login = await preconditions.login_client({ email, password }); // valida 201 internamente
      cookie = login.cookie; // "cid=<token>"
    });

    await test.step(`GET to '${endpoints.data.get_client}'`, async () => {
      const dataRes = await request.get(endpoints.data.get_client, {
        headers: { Cookie: cookie },
      });
      assertions.expectStatus(dataRes, 200);

      const body = await dataRes.json();

      // Estructura: { data: { businesses: [ { business_id, business_name, branches: [...] } ] } }
      assertions.expectHasProperty(body, 'data');
      assertions.expectHasProperty(body.data, 'businesses');

      const defaultBusiness = body.data.businesses[0];
      assertions.expectHasProperty(defaultBusiness, 'business_id');
      assertions.expectPropertyTruthy(defaultBusiness.business_id);
      assertions.expectHasProperty(defaultBusiness, 'business_name');
      assertions.expectPropertyTruthy(defaultBusiness.business_name);
      assertions.expectHasProperty(defaultBusiness, 'branches');

      const defaultBranch = defaultBusiness.branches[0];
      assertions.expectHasProperty(defaultBranch, 'branch_id');
      assertions.expectPropertyTruthy(defaultBranch.branch_id);
      assertions.expectHasProperty(defaultBranch, 'branch_name');
      assertions.expectPropertyTruthy(defaultBranch.branch_name);
      assertions.expectHasProperty(defaultBranch, 'sections');

      const defaultSection = defaultBranch.sections[0];
      assertions.expectHasProperty(defaultSection, 'section_id');
      assertions.expectPropertyTruthy(defaultSection.section_id);
      assertions.expectHasProperty(defaultSection, 'section_name');
      assertions.expectPropertyTruthy(defaultSection.section_name);
    });

  });
});
