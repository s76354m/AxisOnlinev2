"""Unit tests for services"""
import pytest
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.models.project import ProjectStatus

def test_create_project(db_session):
    """Test project creation through service"""
    service = ProjectService(db_session)
    project_data = {
        "ProjectType": "Translation",
        "ProjectDesc": "Service Test",
        "Status": ProjectStatus.NEW.value,
        "Analyst": "Test Analyst",
        "PM": "Test PM",
        "LastEditMSID": "TEST"
    }
    project = service.create_project(project_data)
    assert project.ProjectID is not None

def test_create_csp_lob(db_session):
    """Test CSP LOB creation through service"""
    service = CSPLOBService(db_session)
    lob_data = {
        "csp_code": "TEST123",
        "lob_type": "Medical",
        "description": "Test Description",
        "status": "Active"
    }
    csp_lob = service.create_csp_lob(lob_data)
    assert csp_lob.id is not None 