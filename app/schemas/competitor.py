from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CompetitorBase(BaseModel):
    ProjectID: str
    Product: str
    Payor: str

class CompetitorCreate(CompetitorBase):
    pass

class CompetitorUpdate(BaseModel):
    ProjectID: Optional[str] = None
    Product: Optional[str] = None
    Payor: Optional[str] = None

class CompetitorInDBBase(CompetitorBase):
    RecordID: int
    CreatedDate: datetime
    ModifiedDate: datetime

    class Config:
        from_attributes = True

class Competitor(CompetitorInDBBase):
    pass 