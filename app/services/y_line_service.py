from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.y_line import YLine, YLineStatus
from app.schemas.y_line import YLineCreate, YLineUpdate

class YLineService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_y_lines(
        self,
        status: Optional[str] = None,
        product_code: Optional[str] = None,
        project_id: Optional[int] = None
    ) -> List[YLine]:
        query = self.db.query(YLine)
        
        if status and status != "All":
            query = query.filter(YLine.status == status)
        if product_code:
            query = query.filter(YLine.product_code.ilike(f"%{product_code}%"))
        if project_id:
            query = query.filter(YLine.project_id == project_id)
            
        return query.all()
    
    def create_y_line(self, project_id: int, data: YLineCreate) -> YLine:
        y_line = YLine(
            project_id=project_id,
            ipa_number=data.ipa_number,
            product_code=data.product_code,
            description=data.description,
            pre_award_status=data.pre_award_status,
            post_award_status=data.post_award_status,
            estimated_value=data.estimated_value,
            actual_value=data.actual_value,
            status=data.status or YLineStatus.PENDING,
            notes=data.notes
        )
        
        self.db.add(y_line)
        self.db.commit()
        self.db.refresh(y_line)
        return y_line

    def bulk_create_y_lines(self, project_id: int, y_lines_data: List[YLineCreate]) -> List[YLine]:
        y_lines = []
        for data in y_lines_data:
            y_line = YLine(
                project_id=project_id,
                **data.dict(exclude_unset=True)
            )
            y_lines.append(y_line)
        
        self.db.add_all(y_lines)
        self.db.commit()
        
        for y_line in y_lines:
            self.db.refresh(y_line)
        
        return y_lines

    def bulk_update_status(self, y_line_ids: List[int], status: YLineStatus) -> List[YLine]:
        self.db.query(YLine)\
            .filter(YLine.id.in_(y_line_ids))\
            .update({YLine.status: status}, synchronize_session=False)
        
        self.db.commit()
        return self.db.query(YLine).filter(YLine.id.in_(y_line_ids)).all()