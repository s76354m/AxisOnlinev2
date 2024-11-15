"""Integration tests for services"""
import pytest
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService
from app.schemas.project import ProjectCreate
from app.schemas.csp_lob import CSPLOBCreate
from app.schemas.y_line import YLineCreate

class TestServiceIntegration:
    def test_project_workflow(self, db_session):
        """Test complete project workflow"""
        # Create services
        project_service = ProjectService(db_session)
        csp_lob_service = CSPLOBService(db_session)
        y_line_service = YLineService(db_session)

        # Create project
        project_data = ProjectCreate(
            ProjectType="Translation",
            ProjectDesc="Integration Test",
            Status="New",
            Analyst="Test Analyst",
            PM="Test PM"
        )
        project = project_service.create_project(project_data)
        
        # Add CSP LOB mapping
        csp_lob_data = CSPLOBCreate(
            csp_code="INT001",
            lob_type="Medical",
            description="Integration Test LOB",
            status="Active",
            project_id=project.ProjectID
        )
        csp_lob = csp_lob_service.create_csp_lob(csp_lob_data)
        
        # Add Y-Line
        y_line_data = YLineCreate(
            ipa_number="INT-IPA",
            product_code="INT-PROD",
            estimated_value=15000.00,
            status="Pending",
            project_id=project.ProjectID
        )
        y_line = y_line_service.create_y_line(y_line_data)

        # Verify relationships
        assert csp_lob.project_id == project.ProjectID
        assert y_line.project_id == project.ProjectID 