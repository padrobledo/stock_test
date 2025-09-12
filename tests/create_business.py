# tests/test_business.py
import uuid

def unique_email(prefix="biz"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

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

def test_business_create_happy_path(http, urls):
    email = unique_email("happy")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    name = "My Store"
    resp = create_business(http, urls, token, name)
    assert resp.status_code == 201
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    data = resp.json()
    assert isinstance(data.get("id"), int)
    assert data.get("message") == f"business {name} successfully created"

def test_business_already_registered(http, urls):
    email = unique_email("dup")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    # Primer alta
    first_name = "Primary Biz"
    resp1 = create_business(http, urls, token, first_name)
    assert resp1.status_code == 201
    first_id = resp1.json()["id"]

    # Segundo intento: debe fallar con 409 y devolver el mismo business_id
    resp2 = create_business(http, urls, token, "Another Name")
    assert resp2.status_code == 409
    body = resp2.json()
    assert body.get("error") == "client_already_have_business"
    assert body.get("business_id") == first_id

def test_business_name_too_long(http, urls):
    email = unique_email("toolong")
    password = "Secret123!"
    register_user(http, urls, email, password)
    token = login_get_token(http, urls, email, password)

    long_name = "x" * 31  # > 30 chars
    resp = create_business(http, urls, token, long_name)
    assert resp.status_code == 400
    assert resp.json().get("error") == "invalid_business_name"
