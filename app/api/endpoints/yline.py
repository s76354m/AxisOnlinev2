from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.y_line import YLineCreate, YLineUpdate, YLineResponse
from app.services.y_line_service import YLineService

router = APIRouter()

@router.post("/{project_id}/y-lines/", response_model=YLineResponse)
def create_y_line(
    project_id: int,
    y_line_data: YLineCreate,
    db: Session = Depends(get_db)
):
    """Create a new Y-Line for a project"""
    y_line_service = YLineService(db)
    return y_line_service.create_y_line(project_id, y_line_data)

@router.get("/y-lines/{y_line_id}", response_model=YLineResponse)
def get_y_line(
    y_line_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific Y-Line by ID"""
    y_line_service = YLineService(db)
    return y_line_service.get_y_line(y_line_id)

@router.get("/{project_id}/y-lines/", response_model=List[YLineResponse])
def get_project_y_lines(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get all Y-Lines for a project"""
    y_line_service = YLineService(db)
    return y_line_service.get_project_y_lines(project_id)

@router.put("/y-lines/{y_line_id}", response_model=YLineResponse)
def update_y_line(
    y_line_id: int,
    y_line_data: YLineUpdate,
    db: Session = Depends(get_db)
):
    """Update a Y-Line"""
    y_line_service = YLineService(db)
    return y_line_service.update_y_line(y_line_id, y_line_data)

@router.delete("/y-lines/{y_line_id}")
def delete_y_line(
    y_line_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Y-Line"""
    y_line_service = YLineService(db)
    y_line_service.delete_y_line(y_line_id)
    return {"message": "Y-Line deleted successfully"}

@router.post("/{project_id}/y-lines/bulk", response_model=List[YLineResponse])
def bulk_create_y_lines(
    project_id: int,
    y_lines_data: List[YLineCreate],
    db: Session = Depends(get_db)
):
    """Create multiple Y-Lines for a project"""
    y_line_service = YLineService(db)
    return y_line_service.bulk_create_y_lines(project_id, y_lines_data)

@router.put("/y-lines/bulk-status", response_model=List[YLineResponse])
def bulk_update_status(
    y_line_ids: List[int],
    status: YLineStatus,
    db: Session = Depends(get_db)
):
    """Update status for multiple Y-Lines"""
    y_line_service = YLineService(db)
    return y_line_service.bulk_update_status(y_line_ids, status) 