from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.base import CRUDBase
from app.models.project import Project

class CRUDProject(CRUDBase[Project]):
    def get_by_project_id(self, db: Session, project_id: str) -> Optional[Project]:
        return db.query(Project).filter(Project.ProjectID == project_id).first()
    
    def get_by_analyst(self, db: Session, analyst: str) -> List[Project]:
        return db.query(Project).filter(Project.Analyst == analyst).all()
    
    def get_active_projects(self, db: Session) -> List[Project]:
        return db.query(Project).filter(Project.IsActive == True).all()

project = CRUDProject(Project) 