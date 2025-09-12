# conftest.py
import os
import pytest
import requests

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        choices=["local", "prod"],
        help="Entorno de la API (local o prod).",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="Override de la URL base (si se pasa, ignora --env).",
    )

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    # Prioridad: --base-url > env var API_URL > --env
    cli_url = pytestconfig.getoption("--base-url")
    if cli_url:
        return cli_url.rstrip("/")

    env = pytestconfig.getoption("--env")
    if env == "prod":
        url = os.getenv("API_URL", "https://pocholo.pythonanywhere.com")
    else:
        url = os.getenv("API_URL", "http://127.0.0.1:5000")

    return url.rstrip("/")

@pytest.fixture(scope="session")
def urls(base_url):
    return {
        "register": f"{base_url}/auth/register_credentials/",
        "login": f"{base_url}/auth/validate_credentials/",
        "business_create": f"{base_url}/business/create_new",
    }

@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    yield s
    s.close()
