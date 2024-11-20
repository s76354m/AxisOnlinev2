"""End-to-end workflow tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestE2EWorkflows:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = TestClient(app)
        self.project_id = self._create_test_project()

    def _create_test_project(self):
        response = self.client.post(
            "/api/projects/",
            json={
                "name": "UAT Project",
                "status": "Active",
                "service_area": "North"
            }
        )
        return response.json()["id"]
