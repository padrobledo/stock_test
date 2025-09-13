# tests/test_login_client.py
import uuid

def unique_email(prefix="login"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

# --- Helpers HTTP ------------------------------------------------------------

def register_user(http, urls, email: str, password: str):
    resp = http.post(
        urls["register"],
        json={
            "email": email,
            "repeat_email": email,
            "password": password,
            "repeat_password": password,
        },
        timeout=5,
    )
    assert resp.status_code == 201, f"register failed: {resp.status_code} {resp.text}"
    body = resp.json()
    assert body.get("message") == "Account successfully created"
    return body

def login_get_token(http, urls, email: str, password: str) -> str:
    resp = http.post(
        urls["login"],
        json={"email": email, "password": password},
        timeout=5,
    )
    assert resp.status_code == 200, f"login failed: {resp.status_code} {resp.text}"
    body = resp.json()
    token = body.get("access_token")
    assert token and isinstance(token, str)
    assert body.get("token_type") == "Bearer"
    return token

def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

def create_business(http, urls, token: str, name: str):
    return http.post(
        urls["business_create"],
        headers=auth_headers(token),
        json={"business_name": name},
        timeout=5,
    )

# Helpers de aserción para login
def _login_body(http, urls, email, password):
    resp = http.post(urls["login"], json={"email": email, "password": password}, timeout=5)
    assert resp.status_code == 200, f"login failed: {resp.status_code} {resp.text}"
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    return resp.json()

def _by_name(business_list):
    return {b["business_name"]: b for b in business_list}

# --- Tests -------------------------------------------------------------------

def test_login_success_returns_token(http, urls):
    email = unique_email("ok")
    password = "Secret123!"
    register_user(http, urls, email, password)

    body = _login_body(http, urls, email, password)
    assert isinstance(body.get("access_token"), str) and body["access_token"]
    assert body.get("token_type") == "Bearer"

def test_login_wrong_password(http, urls):
    email = unique_email("wrongpw")
    password = "Secret123!"
    register_user(http, urls, email, password)

    resp = http.post(urls["login"], json={"email": email, "password": "NotTheSame123!"}, timeout=5)
    assert resp.status_code == 401
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    assert resp.json().get("error") == "invalid_credentials"

def test_login_business_list_has_default_my_business_and_branch(http, urls):
    email = unique_email("defaultbiz")
    password = "Secret123!"
    register_user(http, urls, email, password)

    body = _login_body(http, urls, email, password)

    # Debe venir 1 negocio por defecto con su branch por defecto
    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 1

    biz = body["business_list"][0]
    assert biz["business_name"] == "My Business"
    assert isinstance(biz["business_id"], int)

    # Branches del negocio por defecto
    assert "branches" in biz and isinstance(biz["branches"], list)
    assert len(biz["branches"]) == 1
    default_branch = biz["branches"][0]
    assert default_branch["branch_name"] == "My Branch"
    assert isinstance(default_branch["branch_id"], int)

def test_login_returns_business_list_with_two_after_creating_one_and_branches(http, urls):
    email = unique_email("one_extra")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Crear 1 negocio adicional (sin branch por defecto)
    biz_name = "MyStore"
    resp_create = create_business(http, urls, token, biz_name)
    assert resp_create.status_code == 201, resp_create.text

    body = _login_body(http, urls, email, password)

    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 2

    # Mapeamos por nombre para revisar ramas esperadas
    by_name = _by_name(body["business_list"])

    # My Business → debe tener 1 branch por defecto
    assert "My Business" in by_name
    mb = by_name["My Business"]
    assert isinstance(mb["business_id"], int)
    assert "branches" in mb and isinstance(mb["branches"], list)
    assert len(mb["branches"]) == 1
    assert mb["branches"][0]["branch_name"] == "My Branch"
    assert isinstance(mb["branches"][0]["branch_id"], int)

    # MyStore → aún sin branches
    assert "MyStore" in by_name
    ms = by_name["MyStore"]
    assert isinstance(ms["business_id"], int)
    assert "branches" in ms and isinstance(ms["branches"], list)
    assert ms["branches"] == []

# ---- Refactor del test largo en 3 pruebas pequeñas ----

def test_login_three_businesses_after_creating_two(http, urls):
    email = unique_email("two_extra_count")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Crear 2 negocios adicionales
    assert create_business(http, urls, token, "BizOne").status_code == 201
    assert create_business(http, urls, token, "BizTwo").status_code == 201

    body = _login_body(http, urls, email, password)
    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 3

    names = sorted([b["business_name"] for b in body["business_list"]])
    assert names == ["BizOne", "BizTwo", "My Business"]

def test_login_default_business_has_one_default_branch_after_creating_two(http, urls):
    email = unique_email("two_extra_def_branch")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Crear 2 negocios adicionales
    assert create_business(http, urls, token, "BizOne").status_code == 201
    assert create_business(http, urls, token, "BizTwo").status_code == 201

    body = _login_body(http, urls, email, password)
    by_name = _by_name(body["business_list"])

    assert "My Business" in by_name
    mybiz = by_name["My Business"]
    assert isinstance(mybiz["business_id"], int)
    assert "branches" in mybiz and isinstance(mybiz["branches"], list)
    assert len(mybiz["branches"]) == 1
    assert mybiz["branches"][0]["branch_name"] == "My Branch"
    assert isinstance(mybiz["branches"][0]["branch_id"], int)

def test_login_new_businesses_start_with_no_branches_after_creating_two(http, urls):
    email = unique_email("two_extra_empty_branches")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Crear 2 negocios adicionales
    assert create_business(http, urls, token, "BizOne").status_code == 201
    assert create_business(http, urls, token, "BizTwo").status_code == 201

    body = _login_body(http, urls, email, password)
    by_name = _by_name(body["business_list"])

    assert "BizOne" in by_name and "BizTwo" in by_name
    assert isinstance(by_name["BizOne"]["business_id"], int)
    assert isinstance(by_name["BizTwo"]["business_id"], int)

    assert "branches" in by_name["BizOne"] and isinstance(by_name["BizOne"]["branches"], list)
    assert "branches" in by_name["BizTwo"] and isinstance(by_name["BizTwo"]["branches"], list)

    assert by_name["BizOne"]["branches"] == []
    assert by_name["BizTwo"]["branches"] == []
