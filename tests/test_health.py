import os
import requests

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:5000").rstrip("/")

def test_root_is_up():
    resp = requests.get(f"{BASE_URL}/", timeout=3)
    assert resp.status_code == 200
    if resp.headers.get("content-type", "").lower().startswith("application/json"):
        status = (resp.json().get("status") or "").lower()
    else:
        status = resp.text.lower()
    assert "up" in status
