from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.db.base import Base

class Project(Base):
    __tablename__ = "CS_EXP_Project_Translation"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), unique=True, index=True)
    BenchmarkFileID = Column(String(50))
    ProjectType = Column(String(1))
    ProjectDesc = Column(String(100))
    Analyst = Column(String(50))
    PM = Column(String(50))
    GoLiveDate = Column(DateTime)
    MaxMileage = Column(Float)
    Status = Column(String(20))
    NewMarket = Column(Boolean)
    ProvRef = Column(String(50))
    DataLoadDate = Column(DateTime, server_default=func.now())
    LastEditDate = Column(DateTime, server_default=func.now(), onupdate=func.now())
    LastEditMSID = Column(String(50))
    NDB_LOB = Column(String(50))
    RefreshInd = Column(String(1))