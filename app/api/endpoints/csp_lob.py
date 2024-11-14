from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.schemas.csp_lob import CSPLOBCreate, CSPLOBUpdate, CSPLOBResponse
from app.services.csp_lob_service import CSPLOBService
from app.models.csp_lob import LOBType, CSPStatus

router = APIRouter()

@router.post("/{project_id}/csp-lob/", response_model=CSPLOBResponse)
def create_csp_lob(
    project_id: int,
    csp_lob_data: CSPLOBCreate,
    db: Session = Depends(get_db)
):
    """Create a new CSP LOB mapping"""
    csp_lob_service = CSPLOBService(db)
    return csp_lob_service.create_csp_lob(csp_lob_data)

@router.get("/csp-lob/{csp_lob_id}", response_model=CSPLOBResponse)
def get_csp_lob(
    csp_lob_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific CSP LOB mapping"""
    csp_lob_service = CSPLOBService(db)
    return csp_lob_service.get_csp_lob(csp_lob_id)

@router.get("/{project_id}/csp-lob/", response_model=List[CSPLOBResponse])
def get_project_csp_lobs(
    project_id: int,
    lob_type: Optional[LOBType] = None,
    status: Optional[CSPStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all CSP LOB mappings for a project"""
    csp_lob_service = CSPLOBService(db)
    return csp_lob_service.get_project_csp_lobs(project_id, lob_type, status)

@router.put("/csp-lob/{csp_lob_id}", response_model=CSPLOBResponse)
def update_csp_lob(
    csp_lob_id: int,
    csp_lob_data: CSPLOBUpdate,
    db: Session = Depends(get_db)
):
    """Update a CSP LOB mapping"""
    csp_lob_service = CSPLOBService(db)
    return csp_lob_service.update_csp_lob(csp_lob_id, csp_lob_data)

@router.delete("/csp-lob/{csp_lob_id}")
def delete_csp_lob(
    csp_lob_id: int,
    db: Session = Depends(get_db)
):
    """Delete a CSP LOB mapping"""
    csp_lob_service = CSPLOBService(db)
    csp_lob_service.delete_csp_lob(csp_lob_id)
    return {"message": "CSP LOB mapping deleted successfully"} 