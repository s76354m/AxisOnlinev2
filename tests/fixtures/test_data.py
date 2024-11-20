"""Test fixtures and data"""
import pytest
from app.models.project import Project
from app.models.csp_lob import CSPLOB
from app.models.y_line import YLine

# Reference existing fixtures from: 

@pytest.fixture
def test_project(db_session):
    """Create a test project"""
    project = Project(
        ProjectType="Translation",
        ProjectDesc="Test Project",
        Status="New",
        Analyst="Test Analyst",
        PM="Test PM",
        LastEditMSID="TEST"
    )
    db_session.add(project)
    db_session.commit()
    return project

@pytest.fixture
def test_csp_lob(db_session):
    """Create a test CSP LOB mapping"""
    csp_lob = CSPLOB(
        csp_code="TEST123",
        lob_type="Medical",
        description="Test LOB",
        status="Active",
        created_by="TEST"
    )
    db_session.add(csp_lob)
    db_session.commit()