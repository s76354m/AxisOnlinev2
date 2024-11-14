from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    ProjectID: str
    BenchmarkFileID: Optional[str] = None
    ProjectType: str
    ProjectDesc: Optional[str] = None
    Analyst: Optional[str] = None
    PM: Optional[str] = None
    IsActive: bool = True

class ProjectCreate(ProjectBase):
    ProjectID: str = Field(..., max_length=12)
    BenchmarkFileID: Optional[str] = Field(None, max_length=50)
    ProjectType: str = Field(..., max_length=1)
    ProjectDesc: Optional[str] = Field(None, max_length=100)
    Analyst: Optional[str] = Field(None, max_length=50)
    PM: Optional[str] = Field(None, max_length=50)
    GoLiveDate: Optional[datetime] = None
    MaxMileage: Optional[float] = None
    Status: Optional[str] = Field("New", max_length=20)
    NewMarket: Optional[bool] = False
    ProvRef: Optional[str] = Field(None, max_length=50)
    LastEditMSID: Optional[str] = Field(None, max_length=50)
    NDB_LOB: Optional[str] = Field(None, max_length=50)
    RefreshInd: Optional[str] = Field(None, max_length=1)

class ProjectUpdate(BaseModel):
    ProjectID: Optional[str] = None
    BenchmarkFileID: Optional[str] = None
    ProjectType: Optional[str] = None
    ProjectDesc: Optional[str] = None
    Analyst: Optional[str] = None
    PM: Optional[str] = None
    IsActive: Optional[bool] = None

class ProjectInDBBase(ProjectBase):
    RecordID: int
    CreatedDate: datetime
    ModifiedDate: datetime

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass 