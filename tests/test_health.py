# tests/test_health.py
def test_root_is_up_json(http, base_url):
    resp = http.get(f"{base_url}/", timeout=3)
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").lower().startswith("application/json")
    assert resp.json() == {"status": "Stock API up!!!!!"}
