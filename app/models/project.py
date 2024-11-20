from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from app.db.base_class import Base
from datetime import datetime

class ProjectStatus(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"

class ProjectType(str, Enum):
    TRANSLATION = "Translation"
    INTERPRETATION = "Interpretation"
    LOCALIZATION = "Localization"
    OTHER = "Other"

class Project(Base):
    __tablename__ = "CS_EXP_Project_Translation"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), unique=True, index=True)
    ProjectType = Column(String(50))
    ProjectDesc = Column(String(500))
    Status = Column(String(50))
    Analyst = Column(String(100))
    PM = Column(String(100))
    LastEditDate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)