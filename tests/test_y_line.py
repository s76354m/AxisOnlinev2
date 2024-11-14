import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models import YLine, Project
from app.models.y_line import YLineStatus

def test_y_line_creation(db_session):
    """Test Y-Line creation with all fields"""
    # Create a project first
    project = Project(
        name="Test Project",
        status="Active",
        service_area="North"
    )
    db_session.add(project)
    db_session.commit()
    
    # Create Y-Line
    y_line = YLine(
        ipa_number="IPA123",
        product_code="PC456",
        description="Test Y-Line",
        pre_award_status="Pending",
        post_award_status="N/A",
        estimated_value=100000.00,
        status=YLineStatus.PENDING,
        project_id=project.id
    )
    
    db_session.add(y_line)
    db_session.commit()
    
    # Verify creation
    assert y_line.id is not None
    assert y_line.ipa_number == "IPA123"
    assert y_line.status == YLineStatus.PENDING

def test_y_line_unique_ipa(db_session):
    """Test that IPA numbers must be unique"""
    # Create two Y-Lines with same IPA
    project = Project(name="Test Project", status="Active", service_area="North")
    db_session.add(project)
    db_session.commit()
    
    y_line1 = YLine(
        ipa_number="IPA123",
        product_code="PC456",
        project_id=project.id
    )
    db_session.add(y_line1)
    db_session.commit()
    
    y_line2 = YLine(
        ipa_number="IPA123",
        product_code="PC789",
        project_id=project.id
    )
    db_session.add(y_line2)
    
    with pytest.raises(IntegrityError):
        db_session.commit() 