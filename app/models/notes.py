from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class ProjectNote(Base):
    __tablename__ = "CS_EXP_ProjectNotes"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), index=True)
    Notes = Column(Text)
    ActionItem = Column(String(3))
    ProjectStatus = Column(String(8))
    DataLoadDate = Column(DateTime, server_default=func.now())
    LastEditDate = Column(DateTime, server_default=func.now(), onupdate=func.now())
    OrigNoteMSID = Column(String(15))
    LastEditMSID = Column(String(15))
    ProjectCategory = Column(String(50)) 