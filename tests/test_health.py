import os
import requests

#BASE_URL = os.getenv("API_URL", "http://127.0.0.1:5000").rstrip("/")
BASE_URL = os.getenv("API_URL", "https://pocholo.pythonanywhere.com").rstrip("/")

def test_root_is_up_json():
    resp = requests.get(f"{BASE_URL}/", timeout=3)
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    assert resp.json() == {"status": "Stock API up!!!!!"}
