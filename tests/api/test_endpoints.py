"""API endpoint tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.project import ProjectStatus
from app.models.csp_lob import LOBType

client = TestClient(app)

def test_project_endpoints():
    """Test project API endpoints"""
    # Create project
    response = client.post(
        "/api/v1/projects/",
        json={
            "ProjectType": "Translation",
            "ProjectDesc": "API Test Project",
            "Status": ProjectStatus.NEW.value,
            "Analyst": "Test Analyst",
            "PM": "Test PM"
        }
    )
    assert response.status_code == 201
    project_id = response.json()["ProjectID"]

    # Get project
    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["ProjectID"] == project_id

    # Update project
    response = client.put(
        f"/api/v1/projects/{project_id}",
        json={"Status": ProjectStatus.ACTIVE.value}
    )
    assert response.status_code == 200
    assert response.json()["Status"] == ProjectStatus.ACTIVE.value

    # Delete project
    response = client.delete(f"/api/v1/projects/{project_id}")
    assert response.status_code == 204 