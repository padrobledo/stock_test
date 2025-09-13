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

def test_login_default_business_has_default_branch_and_section(http, urls):
    email = unique_email("defaultbiz")
    password = "Secret123!"
    register_user(http, urls, email, password)

    body = _login_body(http, urls, email, password)

    # Debe venir 1 negocio por defecto con su branch y section por defecto
    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 1

    biz = body["business_list"][0]
    assert biz["business_name"] == "My Business"
    assert isinstance(biz["business_id"], int)

    assert "branches" in biz and isinstance(biz["branches"], list)
    assert len(biz["branches"]) == 1

    default_branch = biz["branches"][0]
    assert default_branch["branch_name"] == "My Branch"
    assert isinstance(default_branch["branch_id"], int)

    # Sections dentro del branch
    assert "sections" in default_branch and isinstance(default_branch["sections"], list)
    assert len(default_branch["sections"]) == 1
    sec = default_branch["sections"][0]
    assert sec["section_name"] == "My Section"
    assert isinstance(sec["section_id"], int)

def test_login_two_businesses_after_creating_one_and_sections(http, urls):
    """
    Al crear 1 negocio adicional vía endpoint:
    - My Business mantiene su My Branch + My Section.
    - El nuevo negocio NO trae branches ni sections por defecto.
    """
    email = unique_email("one_extra")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Crear 1 negocio adicional (no debe crear branches/sections)
    biz_name = "MyStore"
    resp_create = create_business(http, urls, token, biz_name)
    assert resp_create.status_code == 201, resp_create.text

    body = _login_body(http, urls, email, password)
    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 2

    by_name = _by_name(body["business_list"])

    # My Business → 1 branch con 1 section
    assert "My Business" in by_name
    mb = by_name["My Business"]
    assert isinstance(mb["business_id"], int)
    assert "branches" in mb and isinstance(mb["branches"], list)
    assert len(mb["branches"]) == 1
    br_mb = mb["branches"][0]
    assert br_mb["branch_name"] == "My Branch"
    assert isinstance(br_mb["branch_id"], int)
    assert "sections" in br_mb and isinstance(br_mb["sections"], list)
    assert len(br_mb["sections"]) == 1
    assert br_mb["sections"][0]["section_name"] == "My Section"
    assert isinstance(br_mb["sections"][0]["section_id"], int)

    # MyStore → sin branches
    assert "MyStore" in by_name
    ms = by_name["MyStore"]
    assert isinstance(ms["business_id"], int)
    assert "branches" in ms and isinstance(ms["branches"], list)
    assert ms["branches"] == []

def test_login_three_businesses_after_creating_two_count(http, urls):
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

def test_login_new_businesses_start_with_no_branches_and_sections(http, urls):
    """
    Al crear 2 negocios nuevos vía endpoint:
    - Ambos deben arrancar sin branches (y por ende sin sections).
    - El negocio por defecto ya fue comprobado en otro test.
    """
    email = unique_email("two_extra_empty")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Crear 2 negocios adicionales
    assert create_business(http, urls, token, "BizOne").status_code == 201
    assert create_business(http, urls, token, "BizTwo").status_code == 201

    body = _login_body(http, urls, email, password)
    by_name = _by_name(body["business_list"])

    assert "BizOne" in by_name and "BizTwo" in by_name
    b1 = by_name["BizOne"]
    b2 = by_name["BizTwo"]

    assert isinstance(b1["business_id"], int)
    assert isinstance(b2["business_id"], int)

    assert "branches" in b1 and isinstance(b1["branches"], list)
    assert "branches" in b2 and isinstance(b2["branches"], list)
    assert b1["branches"] == []
    assert b2["branches"] == []
