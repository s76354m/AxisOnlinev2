from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.project_status import ProjectStatus
from app.schemas.project_status import ProjectStatusCreate, ProjectStatusUpdate

class ProjectStatusService:
    @staticmethod
    def create_status(db: Session, status: ProjectStatusCreate) -> ProjectStatus:
        db_status = ProjectStatus(**status.dict())
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        return db_status

    @staticmethod
    def get_project_status_history(db: Session, project_id: str) -> List[ProjectStatus]:
        return db.query(ProjectStatus)\
            .filter(ProjectStatus.ProjectID == project_id)\
            .order_by(ProjectStatus.StatusDate.desc())\
            .all()

    @staticmethod
    def get_latest_status(db: Session, project_id: str) -> Optional[ProjectStatus]:
        return db.query(ProjectStatus)\
            .filter(ProjectStatus.ProjectID == project_id)\
            .order_by(ProjectStatus.StatusDate.desc())\
            .first() 