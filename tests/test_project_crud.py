import pytest
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate

def test_create_project(db: Session):
    project_data = ProjectCreate(
        ProjectID="TEST001",
        ProjectType="T",
        ProjectDesc="Test Project",
        Analyst="Test Analyst",
        PM="Test PM"
    )
    project = ProjectService.create_project(db=db, project=project_data)
    assert project.ProjectID == "TEST001"
    assert project.ProjectType == "T"

def test_get_project(db: Session):
    project = ProjectService.get_project_by_project_id(db=db, project_id="TEST001")
    assert project is not None
    assert project.ProjectID == "TEST001"

def test_update_project(db: Session):
    project = ProjectService.get_project_by_project_id(db=db, project_id="TEST001")
    update_data = ProjectUpdate(ProjectDesc="Updated Test Project")
    updated_project = ProjectService.update_project(
        db=db, record_id=project.RecordID, project=update_data
    )
    assert updated_project.ProjectDesc == "Updated Test Project"

def test_delete_project(db: Session):
    project = ProjectService.get_project_by_project_id(db=db, project_id="TEST001")
    deleted_project = ProjectService.delete_project(db=db, record_id=project.RecordID)
    assert deleted_project is not None
    assert ProjectService.get_project(db=db, record_id=project.RecordID) is None 