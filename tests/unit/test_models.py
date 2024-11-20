"""Unit tests for all database models"""
import pytest
from datetime import datetime
from app.models.project import Project, ProjectStatus, ProjectType
from app.models.csp_lob import CSPLOB, LOBType
from app.models.y_line import YLine, YLineStatus
from app.models.competitor import Competitor
from sqlalchemy.exc import IntegrityError

def test_project_model(db_session):
    """Test project model creation and validation"""
    project = Project(
        ProjectType=ProjectType.TRANSLATION.value,
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
    assert isinstance(project.LastEditDate, datetime)

def test_csp_lob_model(db_session):
    """Test CSP LOB model creation and validation"""
    csp_lob = CSPLOB(
        csp_code="TEST123",
        lob_type=LOBType.MEDICAL.value,
        description="Test LOB",
        status="Active",
        created_by="TEST"
    )
    db_session.add(csp_lob)
    db_session.commit()

    assert csp_lob.id is not None
    assert csp_lob.lob_type == LOBType.MEDICAL.value

def test_y_line_model(db_session):
    """Test Y-Line model creation and validation"""
    y_line = YLine(
        ipa_number="TEST-IPA",
        product_code="TEST-PROD",
        estimated_value=10000.00,
        status=YLineStatus.PENDING.value
    )
    db_session.add(y_line)
    db_session.commit()

    assert y_line.id is not None
    assert y_line.status == YLineStatus.PENDING.value

def test_competitor_model(db_session):
    """Test Competitor model creation and validation"""
    competitor = Competitor(
        ProjectID="TEST001",
        StrenuusProductCode="TEST",
        Payor="Test Payor",
        Product="Test Product",
        EI=True,
        CS=False,
        MR=True
    )
    db_session.add(competitor)
    db_session.commit()

    assert competitor.ProjectID == "TEST001"
    assert competitor.EI is True 