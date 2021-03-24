# noqa: E402
import os
import sys
from fastapi.testclient import TestClient

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)

from src.api.main import app  # type: ignore # noqa: E402

client = TestClient(app)


def test_read_main():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "SPOC Endpoint"}


def test_read_paper():
    # Existing Paper
    response = client.get("/api/papers/hms_by815vx7135")
    assert response.status_code == 200
    assert response.json()["id"] == "hms_by815vx7135"
    assert len(response.json()["records"]) == 7


def test_fail_read_paper():
    # Paper not found
    response = client.get("/api/papers/madeup_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "madeup_id not found"}


def test_missing_paper_div():
    response = client.get("/api/div/?paper_id=123&div_num=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cannot find 123 XML"}
    response = client.get("/api/div/?paper_id=hms_by815vx7135&div_num=90")
    assert response.status_code == 404


def test_read_record():
    # Existing Record
    pass
