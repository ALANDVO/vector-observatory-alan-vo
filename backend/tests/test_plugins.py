"""Plugin and Skill API endpoint tests."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.db.session import init_db
from app.db.init_db import seed_data


@pytest.fixture
def client() -> TestClient:
    """Create test client with initialized database."""
    app = create_app()
    # Initialize database for tests
    init_db()
    seed_data()
    return TestClient(app)


class TestPluginEndpoints:
    """Tests for plugin endpoints."""

    def test_list_plugins(self, client: TestClient) -> None:
        """Test listing plugins with pagination."""
        response = client.get("/api/v1/plugins")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
        assert data["total"] >= 4  # Seeded plugins
        assert len(data["items"]) <= data["page_size"]

    def test_list_plugins_with_search(self, client: TestClient) -> None:
        """Test searching plugins."""
        response = client.get("/api/v1/plugins?search=claude")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any("claude" in p["name"].lower() for p in data["items"])

    def test_list_plugins_with_tag_filter(self, client: TestClient) -> None:
        """Test filtering plugins by tag."""
        response = client.get("/api/v1/plugins?tag=ai")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any("ai" in (p["tags"] or "").lower() for p in data["items"])

    def test_list_plugins_pagination(self, client: TestClient) -> None:
        """Test plugin pagination."""
        response = client.get("/api/v1/plugins?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert len(data["items"]) <= 2

    def test_get_plugin_by_id(self, client: TestClient) -> None:
        """Test getting a plugin by ID."""
        # First list to get an ID
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        assert len(plugins) > 0
        plugin_id = plugins[0]["id"]

        response = client.get(f"/api/v1/plugins/{plugin_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == plugin_id
        assert "skills" in data

    def test_get_plugin_by_slug(self, client: TestClient) -> None:
        """Test getting a plugin by slug."""
        response = client.get("/api/v1/plugins/slug/claude-code")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == "claude-code"
        assert "skills" in data
        assert len(data["skills"]) >= 3

    def test_get_plugin_not_found(self, client: TestClient) -> None:
        """Test getting non-existent plugin returns 404."""
        response = client.get("/api/v1/plugins/99999")
        assert response.status_code == 404

    def test_get_plugin_by_slug_not_found(self, client: TestClient) -> None:
        """Test getting non-existent plugin by slug returns 404."""
        response = client.get("/api/v1/plugins/slug/nonexistent")
        assert response.status_code == 404


class TestSkillEndpoints:
    """Tests for skill endpoints."""

    def test_list_skills_for_plugin(self, client: TestClient) -> None:
        """Test listing skills for a plugin."""
        # Get a plugin first
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        plugin_id = plugins[0]["id"]

        response = client.get(f"/api/v1/plugins/{plugin_id}/skills")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1

    def test_list_skills_with_search(self, client: TestClient) -> None:
        """Test searching skills."""
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        plugin_id = plugins[0]["id"]

        response = client.get(f"/api/v1/plugins/{plugin_id}/skills?search=code")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    def test_list_skills_pagination(self, client: TestClient) -> None:
        """Test skill pagination."""
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        plugin_id = plugins[0]["id"]

        response = client.get(f"/api/v1/plugins/{plugin_id}/skills?page=1&page_size=1")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 1
        assert len(data["items"]) <= 1

    def test_get_skill(self, client: TestClient) -> None:
        """Test getting a specific skill."""
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        plugin_id = plugins[0]["id"]

        skills_resp = client.get(f"/api/v1/plugins/{plugin_id}/skills")
        skills = skills_resp.json()["items"]
        skill_id = skills[0]["id"]

        response = client.get(f"/api/v1/plugins/{plugin_id}/skills/{skill_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == skill_id
        assert data["plugin_id"] == plugin_id

    def test_get_skill_not_found(self, client: TestClient) -> None:
        """Test getting non-existent skill returns 404."""
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        plugin_id = plugins[0]["id"]

        response = client.get(f"/api/v1/plugins/{plugin_id}/skills/99999")
        assert response.status_code == 404

    def test_get_skill_wrong_plugin(self, client: TestClient) -> None:
        """Test getting skill from wrong plugin returns 404."""
        list_resp = client.get("/api/v1/plugins")
        plugins = list_resp.json()["items"]
        plugin_id = plugins[0]["id"]

        # Find another plugin's skill
        other_plugin = next((p for p in plugins if p["id"] != plugin_id), None)
        if other_plugin:
            skills_resp = client.get(f"/api/v1/plugins/{other_plugin['id']}/skills")
            other_skills = skills_resp.json()["items"]
            if other_skills:
                skill_id = other_skills[0]["id"]
                response = client.get(f"/api/v1/plugins/{plugin_id}/skills/{skill_id}")
                assert response.status_code == 404

