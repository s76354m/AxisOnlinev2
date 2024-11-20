"""Base class for service integration tests"""
import pytest
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService

class BaseServiceTest:
    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session):
        self.db = db_session
        self.project_service = ProjectService(self.db)
        self.csp_lob_service = CSPLOBService(self.db)
        self.y_line_service = YLineService(self.db)
