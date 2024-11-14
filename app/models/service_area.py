from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ServiceArea(Base):
    __tablename__ = "CS_EXP_zTrxServiceArea"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), index=True)
    Region = Column(String(30))
    State = Column(String(2))
    County = Column(String(75))
    ReportInclude = Column(String(1))
    MaxMileage = Column(Integer)
    DataLoadDate = Column(DateTime, server_default=func.now())
    ProjectStatus = Column(String(10)) 