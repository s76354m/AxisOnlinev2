from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.competitor_service import CompetitorService
from app.schemas.competitor import Competitor, CompetitorCreate, CompetitorUpdate
import getpass

router = APIRouter()

@router.get("/competitors/", response_model=List[Competitor])
def read_competitors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve competitors.
    """
    competitors = CompetitorService.get_competitors(db, skip=skip, limit=limit)
    return competitors

@router.get("/competitors/project/{project_id}", response_model=List[Competitor])
def read_competitors_by_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    """
    Get competitors by project ID.
    """
    competitors = CompetitorService.get_competitors_by_project(db=db, project_id=project_id)
    return competitors

@router.post("/competitors/", response_model=CompetitorCreate)
def create_competitor(competitor: CompetitorCreate, db: Session = Depends(get_db)):
    db_competitor = Competitor(**competitor.dict())
    db_competitor.LastEditMSID = getpass.getuser()
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    return db_competitor

@router.get("/competitors/{project_id}", response_model=List[CompetitorCreate])
def get_competitors(project_id: str, db: Session = Depends(get_db)):
    return db.query(Competitor).filter(Competitor.ProjectID == project_id).all()

@router.put("/competitors/{record_id}", response_model=CompetitorUpdate)
def update_competitor(record_id: int, competitor: CompetitorUpdate, db: Session = Depends(get_db)):
    db_competitor = db.query(Competitor).filter(Competitor.RecordID == record_id).first()
    if not db_competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    for key, value in competitor.dict(exclude_unset=True).items():
        setattr(db_competitor, key, value)
    
    db_competitor.LastEditMSID = getpass.getuser()
    db.commit()
    db.refresh(db_competitor)
    return db_competitor

@router.delete("/competitors/{record_id}")
def delete_competitor(record_id: int, db: Session = Depends(get_db)):
    db_competitor = db.query(Competitor).filter(Competitor.RecordID == record_id).first()
    if not db_competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    db.delete(db_competitor)
    db.commit()
    return {"message": "Competitor deleted successfully"} 