from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.service_area import service_area as service_area_crud
from app.models.service_area import ServiceArea
from app.schemas.service_area import ServiceAreaCreate, ServiceAreaUpdate

class ServiceAreaService:
    @staticmethod
    def get_service_area(db: Session, record_id: int) -> Optional[ServiceArea]:
        return service_area_crud.get(db=db, record_id=record_id)
    
    @staticmethod
    def get_service_areas_by_project(db: Session, project_id: str) -> List[ServiceArea]:
        return service_area_crud.get_by_project_id(db=db, project_id=project_id)
    
    @staticmethod
    def get_service_areas(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[ServiceArea]:
        return service_area_crud.get_multi(db=db, skip=skip, limit=limit)
    
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