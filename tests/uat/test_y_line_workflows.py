import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.y_line import YLineStatus

client = TestClient(app)

class TestYLineWorkflows:
    """User Acceptance Tests for Y-Line Management"""
    
    def test_complete_y_line_lifecycle(self):
        """Test the complete lifecycle of a Y-Line from creation to completion"""
        # Create a new project
        project_response = client.post(
            "/api/projects/",
            json={
                "name": "UAT Test Project",
                "status": "Active",
                "service_area": "North"
            }
        )
        assert project_response.status_code == 200
        project_id = project_response.json()["id"]
        
        # Create a Y-Line
        y_line_data = {
            "ipa_number": "UAT-IPA-001",
            "product_code": "TEST-001",
            "description": "UAT Test Y-Line",
            "estimated_value": 100000.00,
            "status": "PENDING"
        }
        create_response = client.post(
            f"/api/{project_id}/y-lines/",
            json=y_line_data
        )
        assert create_response.status_code == 200
        y_line_id = create_response.json()["id"]
        
        # Update pre-award status
        update_response = client.put(
            f"/api/y-lines/{y_line_id}",
            json={"pre_award_status": "Approved"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["pre_award_status"] == "Approved"
        
        # Complete the Y-Line
        complete_response = client.put(
            f"/api/y-lines/{y_line_id}",
            json={
                "status": "COMPLETED",
                "actual_value": 98000.00
            }
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["status"] == "COMPLETED"

    def test_bulk_y_line_operations(self):
        """Test handling multiple Y-Lines simultaneously"""
        # Implementation follows... 