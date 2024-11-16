"""Unit tests for Y-Line Service"""
import pytest
from app.services.y_line_service import YLineService
from app.models.y_line import YLineStatus
from app.schemas.y_line import YLineCreate

class TestYLineService:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.service = YLineService(db_session)
        self.test_project_id = self._create_test_project(db_session)

    def _create_test_project(self, db_session):
        # Create test project
        from app.models import Project
        project = Project(
            name="Test Integration Project",
            status="Active",
            service_area="North"
        )
        db_session.add(project)
        db_session.commit()
        return project.id
