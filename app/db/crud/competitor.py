from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.crud.base import CRUDBase
from app.models.competitor import Competitor

class CRUDCompetitor(CRUDBase[Competitor]):
    def get_by_project_id(self, db: Session, project_id: str) -> List[Competitor]:
        return db.query(Competitor).filter(Competitor.ProjectID == project_id).all()
    
    def get_by_product(self, db: Session, product: str) -> List[Competitor]:
        return db.query(Competitor).filter(Competitor.Product == product).all()
    
    def get_by_payor(self, db: Session, payor: str) -> List[Competitor]:
        return db.query(Competitor).filter(Competitor.Payor == payor).all()

competitor = CRUDCompetitor(Competitor) 