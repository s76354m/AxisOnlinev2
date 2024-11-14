from fastapi.testclient import TestClient
from app.main import app

class TestYLineUserAcceptance:
    def setup_method(self):
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

    def test_complete_y_line_workflow(self):
        """Test full Y-Line workflow from creation to completion"""
        # Create Y-Line
        create_response = self.client.post(
            f"/api/{self.project_id}/y-lines/",
            json={
                "ipa_number": "UAT-001",
                "product_code": "TEST-001",
                "estimated_value": 100000.00,
                "status": "PENDING"
            }
        )
        assert create_response.status_code == 200
        y_line_id = create_response.json()["id"]

        # Update pre-award status
        self.client.put(
            f"/api/y-lines/{y_line_id}",
            json={"pre_award_status": "In Review"}
        )

        # Update post-award status
        self.client.put(
            f"/api/y-lines/{y_line_id}",
            json={"post_award_status": "Awarded"}
        )

        # Complete Y-Line
        complete_response = self.client.put(
            f"/api/y-lines/{y_line_id}",
            json={
                "status": "COMPLETED",
                "actual_value": 98000.00
            }
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["status"] == "COMPLETED"

    def test_bulk_operations_workflow(self):
        """Test bulk operations workflow"""
        # Create multiple Y-Lines
        bulk_create_response = self.client.post(
            f"/api/{self.project_id}/y-lines/bulk",
            json=[
                {
                    "ipa_number": f"BULK-{i}",
                    "product_code": f"TEST-{i}",
                    "estimated_value": 1000.00 * i
                } for i in range(1, 4)
            ]
        )
        assert bulk_create_response.status_code == 200
        assert len(bulk_create_response.json()) == 3

        # Update all to active
        y_line_ids = [y["id"] for y in bulk_create_response.json()]
        bulk_update_response = self.client.put(
            "/api/y-lines/bulk-status",
            json={
                "y_line_ids": y_line_ids,
                "status": "ACTIVE"
            }
        )
        assert bulk_update_response.status_code == 200 