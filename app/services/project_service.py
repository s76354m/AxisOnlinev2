from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.project import project as project_crud
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    @staticmethod
    def get_project(db: Session, record_id: int) -> Optional[Project]:
        return project_crud.get(db=db, record_id=record_id)
    
    @staticmethod
    def get_project_by_project_id(db: Session, project_id: str) -> Optional[Project]:
        return project_crud.get_by_project_id(db=db, project_id=project_id)
    
    @staticmethod
    def get_projects(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return project_crud.get_multi(db=db, skip=skip, limit=limit)
    
    @staticmethod
    def create_project(db: Session, project: ProjectCreate) -> Project:
        return project_crud.create(db=db, obj_in=project.dict())
    
    @staticmethod
    def update_project(
        db: Session, record_id: int, project: ProjectUpdate
    ) -> Optional[Project]:
        db_project = project_crud.get(db=db, record_id=record_id)
        if db_project:
            return project_crud.update(
                db=db, db_obj=db_project, obj_in=project.dict(exclude_unset=True)
            )
        return None
    
    @staticmethod
    def delete_project(db: Session, record_id: int) -> Optional[Project]:
        return project_crud.remove(db=db, record_id=record_id) 