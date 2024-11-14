from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.notes import ProjectNote
from app.schemas.notes import NoteCreate, NoteUpdate
from datetime import datetime
import getpass

router = APIRouter()

@router.post("/notes/", response_model=NoteCreate)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = ProjectNote(**note.dict())
    db_note.DataLoadDate = datetime.now()
    db_note.LastEditDate = datetime.now()
    db_note.OrigNoteMSID = getpass.getuser()
    db_note.LastEditMSID = getpass.getuser()
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/notes/{project_id}", response_model=List[NoteCreate])
def get_notes(project_id: str, db: Session = Depends(get_db)):
    return db.query(ProjectNote).filter(ProjectNote.ProjectID == project_id).all()

@router.put("/notes/{record_id}", response_model=NoteUpdate)
def update_note(record_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(ProjectNote).filter(ProjectNote.RecordID == record_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for key, value in note.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    
    db_note.LastEditDate = datetime.now()
    db_note.LastEditMSID = getpass.getuser()
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/notes/{record_id}")
def delete_note(record_id: int, db: Session = Depends(get_db)):
    db_note = db.query(ProjectNote).filter(ProjectNote.RecordID == record_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"} 