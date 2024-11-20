from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.project import project as project_crud
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_projects(
        self,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Get projects with optional status filter and pagination"""
        query = self.db.query(Project)
        if status and status != "All":
            query = query.filter(Project.Status == status)
        query = query.order_by(Project.ProjectID)
        if skip or limit:
            query = query.offset(skip).limit(limit)
        return query.all()
    
    def create_project(self, project_data: dict) -> Project:
        """Create a new project"""
        db_project_data = {
            "ProjectID": project_data["name"],  # Using name as ProjectID
            "Status": project_data["status"],
            "ProjectDesc": project_data.get("service_area", ""),  # Using service_area as description
            "Analyst": "",  # Default empty values
            "PM": "",
            "ProjectType": "T"  # Default project type
        }
        project = Project(**db_project_data)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_project(self, record_id: int) -> Optional[Project]:
        """Get project by record ID"""
        return self.db.query(Project).filter(Project.id == record_id).first()
    
    def get_project_by_project_id(self, project_id: str) -> Optional[Project]:
        """Get project by project ID"""
        return self.db.query(Project).filter(Project.project_id == project_id).first()
    
    def update_project(self, record_id: int, project_data: dict) -> Optional[Project]:
        """Update existing project"""
        db_project = self.get_project(record_id)
        if db_project:
            for key, value in project_data.items():
                setattr(db_project, key, value)
            self.db.commit()
            self.db.refresh(db_project)
        return db_project
    
    def delete_project(self, record_id: int) -> Optional[Project]:
        """Delete existing project"""
        return project_crud.remove(db=self.db, record_id=record_id) 