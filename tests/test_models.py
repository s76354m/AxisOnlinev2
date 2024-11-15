"""Unit tests for models"""
import pytest
from datetime import datetime
from app.models.project import Project, ProjectStatus
from app.models.csp_lob import CSPLOB

def test_project_creation(db_session):
    """Test project model creation"""
    project = Project(
        ProjectType="Translation",
        ProjectDesc="Test Project",
        Status=ProjectStatus.NEW.value,
        Analyst="Test Analyst",
        PM="Test PM",
        LastEditMSID="TEST"
    )
    db_session.add(project)
    db_session.commit()
    
    assert project.ProjectID is not None
    assert project.Status == ProjectStatus.NEW.value

def test_csp_lob_creation(db_session):
    """Test CSP LOB model creation"""
    csp_lob = CSPLOB(
        csp_code="TEST123",
        lob_type="Medical",
        description="Test LOB",
        status="Active",
        created_by="TEST"
    )
    db_session.add(csp_lob)
    db_session.commit()
    
    assert csp_lob.id is not None
    assert csp_lob.status == "Active" 