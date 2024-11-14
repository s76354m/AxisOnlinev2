from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.yline import YLine
from app.schemas.yline import YLineCreate, YLineUpdate
from datetime import datetime
import getpass

router = APIRouter()

@router.post("/ylines/", response_model=YLineCreate)
def create_yline(yline: YLineCreate, db: Session = Depends(get_db)):
    db_yline = YLine(**yline.dict())
    db_yline.DataLoadDate = datetime.now()
    db_yline.LastEditDate = datetime.now()
    db_yline.LastEditMSID = getpass.getuser()
    db.add(db_yline)
    db.commit()
    db.refresh(db_yline)
    return db_yline

@router.get("/ylines/{project_id}", response_model=List[YLineCreate])
def get_ylines(project_id: str, db: Session = Depends(get_db)):
    return db.query(YLine).filter(YLine.ProjectID == project_id).all()

@router.put("/ylines/{record_id}", response_model=YLineUpdate)
def update_yline(record_id: int, yline: YLineUpdate, db: Session = Depends(get_db)):
    db_yline = db.query(YLine).filter(YLine.RecordID == record_id).first()
    if not db_yline:
        raise HTTPException(status_code=404, detail="Y-Line not found")
    
    for key, value in yline.dict(exclude_unset=True).items():
        setattr(db_yline, key, value)
    
    db_yline.LastEditDate = datetime.now()
    db_yline.LastEditMSID = getpass.getuser()
    db.commit()
    db.refresh(db_yline)
    return db_yline

@router.delete("/ylines/{record_id}")
def delete_yline(record_id: int, db: Session = Depends(get_db)):
    db_yline = db.query(YLine).filter(YLine.RecordID == record_id).first()
    if not db_yline:
        raise HTTPException(status_code=404, detail="Y-Line not found")
    
    db.delete(db_yline)
    db.commit()
    return {"message": "Y-Line deleted successfully"} 