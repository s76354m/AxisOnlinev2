"""Integration tests"""
import pytest
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.csp_lob import CSPLOB
from app.services.csp_lob_service import CSPLOBService
from app.services.project_service import ProjectService

@pytest.mark.integration
def test_create_project_with_lob_mapping(db_session: Session):
    """Test creating a project with CSP LOB mapping"""
    # Create project
    project_service = ProjectService(db_session)
    project = project_service.create_project({
        "ProjectType": "Translation",
        "ProjectDesc": "Test Project",
        "Status": "New",
        "Analyst": "Test Analyst",
        "PM": "Test PM",
        "LastEditMSID": "TEST"
    })
    
    # Create CSP LOB mapping
    csp_lob_service = CSPLOBService(db_session)
    csp_lob = csp_lob_service.create_csp_lob({
        "csp_code": "TEST123",
        "lob_type": "Medical",
        "description": "Test LOB",
        "status": "Active",
        "project_id": project.ProjectID
    })
    
    # Verify relationship
    assert csp_lob.project_id == project.ProjectID
    assert len(project.csp_lob_mappings) == 1

@pytest.mark.integration
def test_project_workflow(db_session: Session):
    """Test complete project workflow"""
    project_service = ProjectService(db_session)
    csp_lob_service = CSPLOBService(db_session)
    
    # Create project
    project = project_service.create_project({
        "ProjectType": "Translation",
        "ProjectDesc": "Workflow Test",
        "Status": "New",
        "Analyst": "Test Analyst",
        "PM": "Test PM",
        "LastEditMSID": "TEST"
    })
    
    # Update project status
    project = project_service.update_project(
        project.ProjectID,
        {"Status": "Active"}
    )
    assert project.Status == "Active"
    
    # Add CSP LOB mapping
    csp_lob = csp_lob_service.create_csp_lob({
        "csp_code": "WORKFLOW123",
        "lob_type": "Medical",
        "description": "Workflow Test LOB",
        "status": "Active",
        "project_id": project.ProjectID
    })
    assert csp_lob.status == "Active" 