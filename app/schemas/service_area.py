"""Service Area schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServiceAreaBase(BaseModel):
    """Base Service Area schema"""
    area_code: str
    description: str
    status: str = "Active"

class ServiceAreaCreate(ServiceAreaBase):
    """Create Service Area schema"""
    pass

class ServiceAreaUpdate(ServiceAreaBase):
    """Update Service Area schema"""
    area_code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ServiceArea(ServiceAreaBase):
    """Service Area schema"""
    id: int
    created_date: datetime
    last_modified: datetime

    class Config:
        from_attributes = True 