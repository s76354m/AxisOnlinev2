from pydantic import BaseModel
from typing import Optional
from .base import BaseSchema, BaseResponse

class CSPLOBBase(BaseSchema):
    csp_code: str
    lob_type: str
    description: Optional[str] = None
    status: str = "Active"

class CSPLOBCreate(CSPLOBBase):
    project_id: str

class CSPLOBUpdate(BaseSchema):
    description: Optional[str] = None
    status: Optional[str] = None 