"""Unit tests for service layer"""
import pytest
from datetime import datetime
from app.services.csp_lob_service import CSPLOBService
from app.services.project_service import ProjectService
from app.models.project import ProjectStatus

def test_create_project(db_session):
    """Test project creation through service"""
    service = ProjectService(db_session)
    project = service.create_project({
        "ProjectType": "Translation",
        "ProjectDesc": "Service Test",
        "Status": ProjectStatus.NEW.value,
        "Analyst": "Test Analyst",
        "PM": "Test PM",
        "LastEditMSID": "TEST"
    })
    
    assert project.ProjectID is not None
    assert project.Status == ProjectStatus.NEW.value

def test_create_csp_lob(db_session):
    """Test CSP LOB creation through service"""
    service = CSPLOBService(db_session)
    csp_lob = service.create_csp_lob({
        "csp_code": "SERVICE123",
        "lob_type": "Medical",
        "description": "Service Test LOB",
        "status": "Active"
    })
    
    assert csp_lob.id is not None
    assert csp_lob.status == "Active"

def test_update_project_status(db_session, test_project):
    """Test project status update through service"""
    service = ProjectService(db_session)
    updated_project = service.update_project(
        test_project.ProjectID,
        {"Status": ProjectStatus.ACTIVE.value}
    )
    
    assert updated_project.Status == ProjectStatus.ACTIVE.value
    assert isinstance(updated_project.LastEditDate, datetime)

def test_delete_csp_lob(db_session, test_csp_lob):
    """Test CSP LOB deletion through service"""
    service = CSPLOBService(db_session)
    service.delete_csp_lob(test_csp_lob.id)
    
    result = service.get_csp_lob(test_csp_lob.id)
    assert result is None 