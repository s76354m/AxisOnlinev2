from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class Competitor(Base):
    __tablename__ = "CS_EXP_Competitor_Translation"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), index=True)
    ProjectStatus = Column(String(10))
    StrenuusProductCode = Column(String(50))
    Payor = Column(String(50))
    Product = Column(String(60))
    EI = Column(Boolean, default=False)
    CS = Column(Boolean, default=False)
    MR = Column(Boolean, default=False)
    DataLoadDate = Column(DateTime, server_default=func.now())
    LastEditMSID = Column(String(15)) 