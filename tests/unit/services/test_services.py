"""Unit tests for services"""
import pytest
from datetime import datetime
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService
from app.models.project import ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session

class TestProjectService:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.db = db_session
        self.service = ProjectService(self.db)

    def test_create_project(self, db: Session):
        """Test project creation"""
        project_data = ProjectCreate(
            ProjectID="TEST001",
            ProjectType="T",
            ProjectDesc="Test Project",
            Analyst="Test Analyst",
            PM="Test PM"
        )
        project = self.service.create_project(db=db, project=project_data)
        assert project.ProjectID == "TEST001"
        assert project.ProjectType == "T"