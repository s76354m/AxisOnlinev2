from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.project_service import ProjectService
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
import getpass

router = APIRouter()

@router.get("/projects/", response_model=List[Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve projects.
    """
    projects = ProjectService.get_projects(db, skip=skip, limit=limit)
    return projects

@router.post("/projects/", response_model=ProjectCreate)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Create new project.
    """
    try:
        # Set the LastEditMSID if not provided
        if not project.LastEditMSID:
            project.LastEditMSID = getpass.getuser()
            
        return ProjectService.create_project(db=db, project=project)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/projects/{record_id}", response_model=Project)
def read_project(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Get project by ID.
    """
    project = ProjectService.get_project(db=db, record_id=record_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{record_id}", response_model=Project)
def update_project(
    record_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update project.
    """
    updated_project = ProjectService.update_project(
        db=db, record_id=record_id, project=project
    )
    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@router.delete("/projects/{record_id}", response_model=Project)
def delete_project(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete project.
    """
    project = ProjectService.delete_project(db=db, record_id=record_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/projects/check/{project_id}")
def check_project_exists(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Check if a project ID already exists"""
    project = ProjectService.get_project_by_project_id(db=db, project_id=project_id)
    return {"exists": project is not None} 