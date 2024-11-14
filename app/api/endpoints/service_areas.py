from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.service_area import ServiceArea
from app.schemas.service_area import ServiceAreaCreate, ServiceAreaUpdate
from datetime import datetime

router = APIRouter()

@router.post("/service-areas/", response_model=ServiceAreaCreate)
def create_service_area(service_area: ServiceAreaCreate, db: Session = Depends(get_db)):
    db_service_area = ServiceArea(**service_area.dict())
    db_service_area.DataLoadDate = datetime.now()
    db.add(db_service_area)
    db.commit()
    db.refresh(db_service_area)
    return db_service_area

@router.get("/service-areas/{project_id}", response_model=List[ServiceAreaCreate])
def get_service_areas(project_id: str, db: Session = Depends(get_db)):
    return db.query(ServiceArea).filter(ServiceArea.ProjectID == project_id).all()

@router.put("/service-areas/{record_id}", response_model=ServiceAreaUpdate)
def update_service_area(record_id: int, service_area: ServiceAreaUpdate, db: Session = Depends(get_db)):
    db_service_area = db.query(ServiceArea).filter(ServiceArea.RecordID == record_id).first()
    if not db_service_area:
        raise HTTPException(status_code=404, detail="Service Area not found")
    
    for key, value in service_area.dict(exclude_unset=True).items():
        setattr(db_service_area, key, value)
    
    db.commit()
    db.refresh(db_service_area)
    return db_service_area

@router.delete("/service-areas/{record_id}")
def delete_service_area(record_id: int, db: Session = Depends(get_db)):
    db_service_area = db.query(ServiceArea).filter(ServiceArea.RecordID == record_id).first()
    if not db_service_area:
        raise HTTPException(status_code=404, detail="Service Area not found")
    
    db.delete(db_service_area)
    db.commit()
    return {"message": "Service Area deleted successfully"} 