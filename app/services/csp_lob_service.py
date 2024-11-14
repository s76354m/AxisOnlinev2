from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.csp_lob import CSPLOB, LOBType, CSPStatus
from app.schemas.csp_lob import CSPLOBCreate, CSPLOBUpdate
from app.utils.validators import CSPLOBValidator

class CSPLOBService:
    def __init__(self, db: Session):
        self.db = db

    def create_csp_lob(self, data: CSPLOBCreate) -> CSPLOB:
        """Create a new CSP LOB mapping with validation"""
        # Validate input data
        CSPLOBValidator.validate_csp_code(data.csp_code)
        CSPLOBValidator.validate_dates(data.effective_date, data.termination_date)
        CSPLOBValidator.validate_lob_compatibility(
            data.project_id,
            data.lob_type,
            self.db
        )
        
        try:
            csp_lob = CSPLOB(**data.dict())
            self.db.add(csp_lob)
            self.db.commit()
            self.db.refresh(csp_lob)
            return csp_lob
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="CSP LOB mapping already exists"
            )

    def get_csp_lob(self, csp_lob_id: int) -> CSPLOB:
        """Retrieve a CSP LOB mapping by ID"""
        csp_lob = self.db.query(CSPLOB).filter(CSPLOB.id == csp_lob_id).first()
        if not csp_lob:
            raise HTTPException(status_code=404, detail="CSP LOB mapping not found")
        return csp_lob

    def get_project_csp_lobs(
        self,
        project_id: int,
        lob_type: Optional[LOBType] = None,
        status: Optional[CSPStatus] = None
    ) -> List[CSPLOB]:
        """Get all CSP LOB mappings for a project with optional filters"""
        query = self.db.query(CSPLOB).filter(CSPLOB.project_id == project_id)
        
        if lob_type:
            query = query.filter(CSPLOB.lob_type == lob_type)
        if status:
            query = query.filter(CSPLOB.status == status)
            
        return query.all()

    def update_csp_lob(self, csp_lob_id: int, data: CSPLOBUpdate) -> CSPLOB:
        """Update CSP LOB mapping with validation"""
        csp_lob = self.get_csp_lob(csp_lob_id)
        
        update_data = data.dict(exclude_unset=True)
        
        if 'csp_code' in update_data:
            CSPLOBValidator.validate_csp_code(update_data['csp_code'])
        
        if 'status' in update_data:
            CSPLOBValidator.validate_status_transition(
                csp_lob.status,
                update_data['status']
            )
        
        if 'effective_date' in update_data or 'termination_date' in update_data:
            effective_date = update_data.get('effective_date', csp_lob.effective_date)
            termination_date = update_data.get('termination_date', csp_lob.termination_date)
            CSPLOBValidator.validate_dates(effective_date, termination_date)
        
        for field, value in update_data.items():
            setattr(csp_lob, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(csp_lob)
            return csp_lob
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Update would create duplicate CSP LOB mapping"
            )

    def delete_csp_lob(self, csp_lob_id: int) -> bool:
        """Delete a CSP LOB mapping"""
        csp_lob = self.get_csp_lob(csp_lob_id)
        self.db.delete(csp_lob)
        self.db.commit()
        return True 