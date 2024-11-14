"""Test database operations"""
import pytest
from app.utils.db_monitor import (
    DatabaseMonitor,
    verify_database_connection,
    verify_table_integrity
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, Competitor, YLine

@pytest.fixture
def db_session():
    session = next(get_db())
    try:
        yield session
    finally:
        session.close()

def test_database_monitor(mock_db):
    """Test database monitoring"""
    # Arrange
    monitor = DatabaseMonitor()
    
    # Act
    monitor.log_operation('TEST', 'SUCCESS')
    monitor.log_error('TEST', Exception('Test error'))
    
    # Assert
    stats = monitor.get_stats()
    assert stats['operations'] == 1
    assert stats['errors'] == 1

def test_database_connection(mock_db):
    """Test database connection verification"""
    # Act
    result = verify_database_connection(mock_db)
    
    # Assert
    assert result is True

def test_table_integrity(mock_db):
    """Test table integrity check"""
    # Act
    result = verify_table_integrity()
    
    # Assert
    assert not result.empty
    assert 'CS_EXP_Project_Translation' in result['table'].values 

def test_project_crud(db_session: Session):
    # Test project creation
    new_project = Project(
        name="Test Project",
        status="Active",
        service_area="North"
    )
    db_session.add(new_project)
    db_session.commit()
    
    # Test project retrieval
    retrieved = db_session.query(Project).filter_by(name="Test Project").first()
    assert retrieved is not None
    assert retrieved.name == "Test Project"

def test_project_y_line_relationship(db_session):
    """Test Project and Y-Line relationship"""
    # Create project with Y-Lines
    project = Project(
        name="Test Project",
        status="Active",
        service_area="North"
    )
    
    y_lines = [
        YLine(
            ipa_number=f"IPA{i}",
            product_code=f"PC{i}",
            estimated_value=1000.00 * i
        ) for i in range(1, 4)
    ]
    
    project.y_lines = y_lines
    db_session.add(project)
    db_session.commit()
    
    # Verify relationship
    retrieved_project = db_session.query(Project).filter_by(name="Test Project").first()
    assert len(retrieved_project.y_lines) == 3
    assert all(isinstance(y_line, YLine) for y_line in retrieved_project.y_lines)

def test_y_line_cascade_delete(db_session):
    """Test Y-Lines are deleted when Project is deleted"""
    # Create project with Y-Lines
    project = Project(
        name="Test Project",
        status="Active",
        service_area="North"
    )
    
    y_line = YLine(
        ipa_number="IPA123",
        product_code="PC456",
        estimated_value=1000.00
    )
    
    project.y_lines = [y_line]
    db_session.add(project)
    db_session.commit()
    
    # Delete project
    db_session.delete(project)
    db_session.commit()
    
    # Verify Y-Line is also deleted
    assert db_session.query(YLine).filter_by(ipa_number="IPA123").first() is None