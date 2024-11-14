from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.y_line import YLineStatus

class YLineBase(BaseModel):
    ipa_number: str = Field(..., description="IPA number for the Y-Line")
    product_code: str = Field(..., description="Product code")
    description: Optional[str] = Field(None, description="Y-Line description")
    pre_award_status: Optional[str] = None
    post_award_status: Optional[str] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    actual_value: Optional[float] = Field(None, ge=0)
    status: Optional[YLineStatus] = YLineStatus.PENDING

class YLineCreate(YLineBase):
    pass

class YLineUpdate(BaseModel):
    ipa_number: Optional[str] = None
    product_code: Optional[str] = None
    description: Optional[str] = None
    pre_award_status: Optional[str] = None
    post_award_status: Optional[str] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    actual_value: Optional[float] = Field(None, ge=0)
    status: Optional[YLineStatus] = None

class YLineResponse(YLineBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 