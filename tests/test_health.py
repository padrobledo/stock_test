import os
import time
import requests

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:5000").rstrip("/")

def test_root_is_up():
    last_exc = None
    for _ in range(5):
        try:
            resp = requests.get(f"{BASE_URL}/", timeout=3)
            assert resp.status_code == 200
            status = ""
            if resp.headers.get("content-type", "").lower().startswith("application/json"):
                status = (resp.json().get("status") or "").lower()
            else:
                status = resp.text.lower()
            assert "up" in status
            return
        except Exception as e:
            last_exc = e
            time.sleep(1)
    raise AssertionError(f"No se pudo verificar la API en {BASE_URL}/: {last_exc}")