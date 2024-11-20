"""Unit tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.csp_lob import CSPLOB

client = TestClient(app)

def test_create_csp_lob():
    """Test creating a new CSP LOB mapping"""
    response = client.post(
        "/api/v1/csp-lob/",
        json={
            "csp_code": "TEST123",
            "lob_type": "Medical",
            "description": "Test LOB",
            "status": "Active"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["csp_code"] == "TEST123"
    assert data["lob_type"] == "Medical"

def test_get_csp_lob():
    """Test retrieving a CSP LOB mapping"""
    response = client.get("/api/v1/csp-lob/TEST123")
    assert response.status_code == 200
    data = response.json()
    assert data["csp_code"] == "TEST123"

def test_update_csp_lob():
    """Test updating a CSP LOB mapping"""
    response = client.put(
        "/api/v1/csp-lob/TEST123",
        json={
            "description": "Updated Test LOB",
            "status": "Inactive"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated Test LOB"
    assert data["status"] == "Inactive"

def test_delete_csp_lob():
    """Test deleting a CSP LOB mapping"""
    response = client.delete("/api/v1/csp-lob/TEST123")
    assert response.status_code == 204 