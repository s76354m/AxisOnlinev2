from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.service_area import service_area as service_area_crud
from app.models.service_area import ServiceArea
from app.schemas.service_area import ServiceAreaCreate, ServiceAreaUpdate

class ServiceAreaService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_service_areas(
        self,
        state_filter: Optional[str] = None,
        region_filter: Optional[str] = None
    ) -> List[ServiceArea]:
        query = self.db.query(ServiceArea)
        if state_filter:
            query = query.filter(ServiceArea.State.ilike(f"%{state_filter}%"))
        if region_filter:
            query = query.filter(ServiceArea.Region.ilike(f"%{region_filter}%"))
        return query.all()
    
    @staticmethod
    def get_service_area(db: Session, record_id: int) -> Optional[ServiceArea]:
        return service_area_crud.get(db=db, record_id=record_id)
    
    @staticmethod
    def get_service_areas_by_project(db: Session, project_id: str) -> List[ServiceArea]:
        return service_area_crud.get_by_project_id(db=db, project_id=project_id)
    
    @staticmethod
    def create_service_area(db: Session, service_area: ServiceAreaCreate) -> ServiceArea:
        return service_area_crud.create(db=db, obj_in=service_area.dict())
    
    @staticmethod
    def update_service_area(
        db: Session, record_id: int, service_area: ServiceAreaUpdate
    ) -> Optional[ServiceArea]:
        db_service_area = service_area_crud.get(db=db, record_id=record_id)
        if db_service_area:
            return service_area_crud.update(
                db=db, db_obj=db_service_area, obj_in=service_area.dict(exclude_unset=True)
            )
        return None
    
    @staticmethod
    def delete_service_area(db: Session, record_id: int) -> Optional[ServiceArea]:
        return service_area_crud.remove(db=db, record_id=record_id) 