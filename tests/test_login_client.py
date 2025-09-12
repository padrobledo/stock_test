# tests/test_login.py
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
    return resp.json()

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

# --- Tests -------------------------------------------------------------------

def test_login_success_returns_token(http, urls):
    email = unique_email("ok")
    password = "Secret123!"
    register_user(http, urls, email, password)

    resp = http.post(urls["login"], json={"email": email, "password": password}, timeout=5)
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    body = resp.json()
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

def test_login_business_list_empty_when_none(http, urls):
    email = unique_email("nobiz")
    password = "Secret123!"
    register_user(http, urls, email, password)

    resp_login = http.post(urls["login"], json={"email": email, "password": password}, timeout=5)
    assert resp_login.status_code == 200
    body = resp_login.json()
    assert body.get("business_list") == []

def test_login_returns_business_list_when_one(http, urls):
    email = unique_email("onebiz")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    biz_name = "MyStore"
    resp_create = create_business(http, urls, token, biz_name)
    assert resp_create.status_code == 201, resp_create.text

    resp_login = http.post(urls["login"], json={"email": email, "password": password}, timeout=5)
    assert resp_login.status_code == 200
    body = resp_login.json()
    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 1
    assert body["business_list"][0]["business_name"] == biz_name
    assert isinstance(body["business_list"][0]["business_id"], int)

def test_login_returns_business_list_with_two_businesses(http, urls):
    email = unique_email("twobiz")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    resp_create_1 = create_business(http, urls, token, "BizOne")
    assert resp_create_1.status_code == 201, resp_create_1.text
    resp_create_2 = create_business(http, urls, token, "BizTwo")
    assert resp_create_2.status_code == 201, resp_create_2.text

    resp_login = http.post(urls["login"], json={"email": email, "password": password}, timeout=5)
    assert resp_login.status_code == 200
    body = resp_login.json()

    assert "business_list" in body and isinstance(body["business_list"], list)
    assert len(body["business_list"]) == 2
    names = sorted([b["business_name"] for b in body["business_list"]])
    assert names == ["BizOne", "BizTwo"]
    for b in body["business_list"]:
        assert isinstance(b["business_id"], int)
