"""
Bootstrap health tests for import-service.
Run: pytest services/import-service/tests/test_health.py
"""
import pytest
from fastapi.testclient import TestClient


def get_client():
    # Set minimal env before importing app
    import os
    os.environ.setdefault("SERVICE_NAME", "import-service")
    os.environ.setdefault("LOG_LEVEL", "INFO")
    os.environ.setdefault("LOG_FORMAT", "console")
    from src.api.main import app
    return TestClient(app)


def test_liveness():
    client = get_client()
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "import" in data["service"]


def test_readiness():
    client = get_client()
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ok", "degraded")


def test_passages_batch_not_implemented():
    """Bootstrap: batch endpoint returns 501."""
    from io import BytesIO
    client = get_client()
    response = client.post(
        "/api/import/batches/passages",
        files={"file": ("test.csv", BytesIO(b"header\nrow"), "text/csv")},
    )
    assert response.status_code == 501


def test_withdrawal_not_implemented():
    """Bootstrap: withdrawal endpoint returns 501."""
    client = get_client()
    response = client.post(
        "/api/import/withdrawals/",
        json={"entity_type": "passage", "entity_id": "PAS-01", "actor_role": "PolicyOwner", "reason": "test"},
    )
    assert response.status_code == 501


def test_openapi_schema_accessible():
    client = get_client()
    response = client.get("/openapi.json")
    assert response.status_code == 200
