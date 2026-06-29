import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    yield s
    s.close()

@pytest.fixture
def valid_capa_payload():
    return {
        "title": "CAPA-2026-001: Deviation in sterilization process",
        "body": "Root cause: temperature excursion. Corrective action: recalibrate sensor.",
        "userId": 1
    }

@pytest.fixture
def valid_audit_item_payload():
    return {
        "title": "Verify CAPA closure evidence for audit finding AF-2026-003",
        "completed": False,
        "userId": 1
    }
