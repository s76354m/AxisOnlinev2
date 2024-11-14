from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.competitor import competitor as competitor_crud
from app.models.competitor import Competitor
from app.schemas.competitor import CompetitorCreate, CompetitorUpdate

class CompetitorService:
    @staticmethod
    def get_competitor(db: Session, record_id: int) -> Optional[Competitor]:
        return competitor_crud.get(db=db, record_id=record_id)
    
    @staticmethod
    def get_competitors_by_project(db: Session, project_id: str) -> List[Competitor]:
        return competitor_crud.get_by_project_id(db=db, project_id=project_id)
    
    @staticmethod
    def get_competitors(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[Competitor]:
        return competitor_crud.get_multi(db=db, skip=skip, limit=limit)
    
    @staticmethod
    def create_competitor(db: Session, competitor: CompetitorCreate) -> Competitor:
        return competitor_crud.create(db=db, obj_in=competitor.dict())
    
    @staticmethod
    def update_competitor(
        db: Session, record_id: int, competitor: CompetitorUpdate
    ) -> Optional[Competitor]:
        db_competitor = competitor_crud.get(db=db, record_id=record_id)
        if db_competitor:
            return competitor_crud.update(
                db=db, db_obj=db_competitor, obj_in=competitor.dict(exclude_unset=True)
            )
        return None
    
    @staticmethod
    def delete_competitor(db: Session, record_id: int) -> Optional[Competitor]:
        return competitor_crud.remove(db=db, record_id=record_id) 