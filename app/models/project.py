from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.db.base import Base

class ProjectStatus(str, Enum):
    """Project status enumeration"""
    NEW = "New"
    ACTIVE = "Active"
    REVIEW = "Review"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"

class ProjectType(str, Enum):
    """Project type enumeration"""
    TRANSLATION = "Translation"
    REVIEW = "Review"
    QA = "QA"
    OTHER = "Other"

class Project(Base):
    __tablename__ = "CS_EXP_Project_Translation"

    ProjectID = Column(Integer, primary_key=True, autoincrement=True)
    ProjectType = Column(String(50), nullable=False)
    ProjectDesc = Column(String(500), nullable=True)
    Status = Column(String(50), nullable=False, default=ProjectStatus.NEW.value)
    Analyst = Column(String(50), nullable=True)
    PM = Column(String(50), nullable=True)
    LastEditDate = Column(DateTime, default=func.now(), onupdate=func.now())
    LastEditMSID = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Project(ProjectID={self.ProjectID}, Type={self.ProjectType}, Status={self.Status})>"