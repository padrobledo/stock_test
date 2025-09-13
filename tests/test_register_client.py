# tests/test_register_client.py
import uuid

def unique_email(prefix="user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

def test_register_happy_path(http, urls):
    email = unique_email("happy")
    payload = {
        "email": email,
        "repeat_email": email,
        "password": "Secret123!",
        "repeat_password": "Secret123!",
    }
    resp = http.post(urls["register"], json=payload, timeout=5)
    assert resp.status_code == 201
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    data = resp.json()
    # la respuesta ahora es sólo un mensaje de éxito
    assert data.get("message") == "Account successfully created"

def test_register_emails_do_not_match(http, urls):
    payload = {
        "email": unique_email("mismatch"),
        "repeat_email": unique_email("mismatch_other"),
        "password": "Secret123!",
        "repeat_password": "Secret123!",
    }
    resp = http.post(urls["register"], json=payload, timeout=5)
    assert resp.status_code == 400
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    assert resp.json().get("error") == "emails_do_not_match"

def test_register_passwords_do_not_match(http, urls):
    email = unique_email("pw_mismatch")
    payload = {
        "email": email,
        "repeat_email": email,
        "password": "Secret123!",
        "repeat_password": "Different123!",
    }
    resp = http.post(urls["register"], json=payload, timeout=5)
    assert resp.status_code == 400
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    assert resp.json().get("error") == "passwords_do_not_match"

def test_register_email_already_exists(http, urls):
    email = unique_email("dup")
    payload_ok = {
        "email": email,
        "repeat_email": email,
        "password": "Secret123!",
        "repeat_password": "Secret123!",
    }
    # Primera vez: crea OK
    resp1 = http.post(urls["register"], json=payload_ok, timeout=5)
    assert resp1.status_code == 201

    # Segunda vez: debe dar conflicto por email ya registrado
    resp2 = http.post(urls["register"], json=payload_ok, timeout=5)
    assert resp2.status_code == 409
    assert resp2.headers.get("content-type", "").lower().startswith("application/json")
    assert resp2.json().get("error") == "email_already_exists"
