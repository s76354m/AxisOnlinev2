from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import or_

from app.models import YLine, Project
from app.models.y_line import YLineStatus
from app.schemas.y_line import YLineCreate, YLineUpdate
from app.utils.validators import validate_ipa_number, validate_y_line_values

class YLineService:
    def __init__(self, db: Session):
        self.db = db

    def create_y_line(self, project_id: int, y_line_data: YLineCreate) -> YLine:
        """Create a new Y-Line entry"""
        # Validate project exists
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Validate IPA number
        if not validate_ipa_number(y_line_data.ipa_number):
            raise HTTPException(status_code=400, detail="Invalid IPA number format")
        
        # Validate monetary values
        if not validate_y_line_values(y_line_data.estimated_value, y_line_data.actual_value):
            raise HTTPException(status_code=400, detail="Invalid monetary values")
        
        try:
            y_line = YLine(
                project_id=project_id,
                **y_line_data.dict()
            )
            self.db.add(y_line)
            self.db.commit()
            self.db.refresh(y_line)
            return y_line
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="IPA number already exists")

    def get_y_line(self, y_line_id: int) -> YLine:
        """Retrieve a Y-Line by ID"""
        y_line = self.db.query(YLine).filter(YLine.id == y_line_id).first()
        if not y_line:
            raise HTTPException(status_code=404, detail="Y-Line not found")
        return y_line

    def get_project_y_lines(self, project_id: int) -> List[YLine]:
        """Get all Y-Lines for a project"""
        return self.db.query(YLine).filter(YLine.project_id == project_id).all()

    def update_y_line(self, y_line_id: int, y_line_data: YLineUpdate) -> YLine:
        """Update a Y-Line entry"""
        y_line = self.get_y_line(y_line_id)
        
        update_data = y_line_data.dict(exclude_unset=True)
        
        if 'estimated_value' in update_data or 'actual_value' in update_data:
            est_val = update_data.get('estimated_value', y_line.estimated_value)
            act_val = update_data.get('actual_value', y_line.actual_value)
            if not validate_y_line_values(est_val, act_val):
                raise HTTPException(status_code=400, detail="Invalid monetary values")

        for field, value in update_data.items():
            setattr(y_line, field, value)
            
        self.db.commit()
        self.db.refresh(y_line)
        return y_line

    def delete_y_line(self, y_line_id: int) -> bool:
        """Delete a Y-Line entry"""
        y_line = self.get_y_line(y_line_id)
        self.db.delete(y_line)
        self.db.commit()
        return True 

    def bulk_create_y_lines(self, project_id: int, y_lines_data: List[YLineCreate]) -> List[YLine]:
        """Create multiple Y-Lines in a single transaction"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        y_lines = []
        try:
            for y_line_data in y_lines_data:
                if not validate_ipa_number(y_line_data.ipa_number):
                    raise ValueError(f"Invalid IPA number: {y_line_data.ipa_number}")
                    
                y_line = YLine(
                    project_id=project_id,
                    **y_line_data.dict()
                )
                self.db.add(y_line)
                y_lines.append(y_line)
                
            self.db.commit()
            return y_lines
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def bulk_update_status(self, y_line_ids: List[int], status: YLineStatus) -> List[YLine]:
        """Update status for multiple Y-Lines"""
        y_lines = self.db.query(YLine).filter(YLine.id.in_(y_line_ids)).all()
        if len(y_lines) != len(y_line_ids):
            raise HTTPException(status_code=404, detail="Some Y-Lines not found")
        
        try:
            for y_line in y_lines:
                y_line.status = status
            self.db.commit()
            return y_lines
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def get_filtered_y_lines(
        self,
        project_id: Optional[int] = None,
        status: Optional[YLineStatus] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        search_term: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[YLine]:
        """Get Y-Lines with advanced filtering"""
        query = self.db.query(YLine)
        
        if project_id:
            query = query.filter(YLine.project_id == project_id)
        if status:
            query = query.filter(YLine.status == status)
        if min_value:
            query = query.filter(YLine.estimated_value >= min_value)
        if max_value:
            query = query.filter(YLine.estimated_value <= max_value)
        if search_term:
            search = f"%{search_term}%"
            query = query.filter(
                or_(
                    YLine.ipa_number.ilike(search),
                    YLine.product_code.ilike(search),
                    YLine.description.ilike(search)
                )
            )
        
        return query.offset(skip).limit(limit).all() 