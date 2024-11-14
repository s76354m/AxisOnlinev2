from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseResponse
from app.models.csp_lob import LOBType, CSPStatus

class CSPLOBBase(BaseModel):
    csp_code: str = Field(..., description="CSP identifier code")
    lob_type: LOBType
    description: Optional[str] = None
    status: CSPStatus = CSPStatus.ACTIVE
    effective_date: Optional[datetime] = None
    termination_date: Optional[datetime] = None

class CSPLOBCreate(CSPLOBBase):
    project_id: int

class CSPLOBUpdate(BaseModel):
    csp_code: Optional[str] = None
    lob_type: Optional[LOBType] = None
    description: Optional[str] = None
    status: Optional[CSPStatus] = None
    effective_date: Optional[datetime] = None
    termination_date: Optional[datetime] = None

class CSPLOBResponse(CSPLOBBase, BaseResponse):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 