from typing import Optional
from pydantic import BaseModel, validator
from decimal import Decimal
from app.models.yline import YLineItem

class ServiceAreaValidator(BaseModel):
    Mileage: Optional[Decimal]
    
    @validator('Mileage')
    def validate_mileage(cls, v):
        if v is not None and v < 0:
            raise ValueError('Mileage cannot be negative')
        return v

class ProjectValidator(BaseModel):
    ProjectID: str
    
    @validator('ProjectID')
    def validate_project_id(cls, v):
        if not v or len(v) > 12:
            raise ValueError('ProjectID must be between 1 and 12 characters')
        return v 

def validate_yline_item(item: YLineItem) -> bool:
    """Validate Y-Line item"""
    if not item.ipa_number:
        raise ValueError("IPA number is required")
    
    if not item.product_code:
        raise ValueError("Product code is required")
    
    if item.pre_award and item.post_award:
        raise ValueError("Item cannot be both pre-award and post-award")
    
    return True