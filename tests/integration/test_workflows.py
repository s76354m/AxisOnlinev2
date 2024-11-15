"""Integration tests for complete workflows"""
import pytest
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService
from app.schemas.project import ProjectCreate
from app.schemas.csp_lob import CSPLOBCreate
from app.schemas.y_line import YLineCreate
from app.models.project import ProjectStatus

class TestWorkflows:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.db = db_session
        self.project_service = ProjectService(db_session)
        self.csp_lob_service = CSPLOBService(db_session)
        self.y_line_service = YLineService(db_session)

    def test_complete_project_workflow(self):
        """Test complete project workflow including all services"""
        # Create project
        project_data = ProjectCreate(
            ProjectType="Translation",
            ProjectDesc="Integration Test",
            Status=ProjectStatus.NEW.value,
            Analyst="Test Analyst",
            PM="Test PM",
            LastEditMSID="TEST"
        )
        project = self.project_service.create_project(project_data)
        
        # Update project status
        updated_project = self.project_service.update_project(
            project.ProjectID,
            {"Status": ProjectStatus.ACTIVE.value}
        )
        assert updated_project.Status == ProjectStatus.ACTIVE.value
        
        # Add CSP LOB mapping
        csp_lob_data = CSPLOBCreate(
            csp_code="INT001",
            lob_type="Medical",
            description="Integration Test LOB",
            status="Active",
            project_id=project.ProjectID
        )
        csp_lob = self.csp_lob_service.create_csp_lob(csp_lob_data)
        
        # Add Y-Line
        y_line_data = YLineCreate(
            ipa_number="INT-IPA",
            product_code="INT-PROD",
            estimated_value=15000.00,
            status="Pending",
            project_id=project.ProjectID
        )
        y_line = self.y_line_service.create_y_line(y_line_data)

        # Verify relationships and state
        assert csp_lob.project_id == project.ProjectID
        assert y_line.project_id == project.ProjectID
        assert len(project.csp_lob_mappings) == 1