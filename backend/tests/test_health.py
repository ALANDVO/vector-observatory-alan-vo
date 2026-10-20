"""Backend health endpoint tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_health_endpoint(client: TestClient) -> None:
    """Test basic health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Vector Observatory"
    assert data["version"] == "1.0.0"


def test_health_db_endpoint(client: TestClient) -> None:
    """Test database health endpoint."""
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "unhealthy")
    assert "database" in data