# tests/test_login.py
import os
import uuid
import requests
import pytest

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:5000").rstrip("/")
REGISTER_URL = f"{BASE_URL}/auth/register_credentials/"
LOGIN_URL = f"{BASE_URL}/auth/validate_credentials/"

@pytest.fixture(scope="session")
def http():
    return requests.Session()

def unique_email(prefix="login"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

def register_user(http, email: str, password: str):
    payload = {
        "email": email,
        "repeat_email": email,
        "password": password,
        "repeat_password": password,
    }
    resp = http.post(REGISTER_URL, json=payload, timeout=5)
    assert resp.status_code == 201, f"register failed: {resp.status_code} {resp.text}"
    return resp.json()

def test_login_success_returns_token(http):
    email = unique_email("ok")
    password = "Secret123!"
    # crear usuario
    register_user(http, email, password)

    # login
    resp = http.post(
        LOGIN_URL,
        json={"email": email, "password": password},
        timeout=5,
    )
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    body = resp.json()
    assert isinstance(body.get("access_token"), str) and len(body["access_token"]) > 0
    assert body.get("token_type") == "Bearer"

def test_login_wrong_password(http):
    email = unique_email("wrongpw")
    password = "Secret123!"
    # crear usuario
    register_user(http, email, password)

    # login con password incorrecto
    resp = http.post(
        LOGIN_URL,
        json={"email": email, "password": "NotTheSame123!"},
        timeout=5,
    )
    assert resp.status_code == 401
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    assert resp.json().get("error") == "invalid_credentials"
