"""Unit tests for service layer"""
import pytest
from unittest.mock import Mock, patch
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.core.error_handler import AppError
from sqlalchemy.exc import SQLAlchemyError

class TestProjectService:
    @pytest.fixture
    def service(self):
        return ProjectService()
    
    def test_create_project(self, service, mock_db_session):
        """Test project creation"""
        project_data = ProjectCreate(
            project_type="T",
            description="Test Project",
            analyst="Test Analyst",
            pm="Test PM"
        )
        
        result = service.create_project(mock_db_session, project_data)
        assert result.project_type == "T"
        assert result.description == "Test Project"
    
    def test_create_project_error(self, service, mock_db_session):
        """Test project creation error handling"""
        mock_db_session.add.side_effect = SQLAlchemyError("Test error")
        
        with pytest.raises(AppError):
            service.create_project(mock_db_session, ProjectCreate())
    
    def test_update_project(self, service, mock_db_session):
        """Test project update"""
        update_data = ProjectUpdate(status="Active")
        result = service.update_project(mock_db_session, "TEST001", update_data)
        assert result.status == "Active"
    
    def test_bulk_update_projects(self, service, mock_db_session):
        """Test bulk project updates"""
        project_ids = ["TEST001", "TEST002"]
        update_data = {"status": "Active"}
        
        results = service.bulk_update_projects(mock_db_session, project_ids, update_data)
        assert all(r.status == "Active" for r in results)

class TestCSPLOBService:
    @pytest.fixture
    def service(self):
        return CSPLOBService()
    
    def test_create_csp_lob(self, service, mock_db_session):
        """Test CSP LOB creation"""
        lob_data = CSPLOBCreate(
            csp_code="TEST",
            lob_type="Medical",
            description="Test LOB"
        )
        
        result = service.create_csp_lob(mock_db_session, lob_data)
        assert result.csp_code == "TEST"
        assert result.lob_type == "Medical" 