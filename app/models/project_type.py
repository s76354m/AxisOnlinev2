from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class ProjectType(Base):
    __tablename__ = "CS_EXP_Project_Types"

    RecordID = Column(Integer, primary_key=True, index=True)
    TypeCode = Column(String(1), unique=True, index=True)
    Description = Column(String(100))
    IsActive = Column(Boolean, default=True) 