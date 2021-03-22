# noqa: E402
import os
import sys
from fastapi.testclient import TestClient

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)

from src.api.main import app  # type: ignore # noqa: E402

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SPOC Endpoint"}


def test_read_paper():
    # Existing Paper
    response = client.get("/papers/hms_by815vx7135")
    assert response.status_code == 200
    assert response.json()["id"] == "hms_by815vx7135"
    assert len(response.json()["records"]) == 7


def test_fail_read_paper():
    # Paper not found
    response = client.get("/papers/madeup_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "madeup_id not found"}


def test_read_record():
    # Existing Record
    pass
