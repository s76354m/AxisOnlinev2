from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.base import CRUDBase
from app.models.service_area import ServiceArea

class CRUDServiceArea(CRUDBase[ServiceArea]):
    def get_by_project_id(self, db: Session, project_id: str) -> List[ServiceArea]:
        return db.query(ServiceArea).filter(ServiceArea.ProjectID == project_id).all()
    
    def get_by_service_area(self, db: Session, service_area: str) -> List[ServiceArea]:
        return db.query(ServiceArea).filter(ServiceArea.ServiceArea == service_area).all()

service_area = CRUDServiceArea(ServiceArea) 