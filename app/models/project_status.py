from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class ProjectStatus(Base):
    __tablename__ = "CS_EXP_Project_Status"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), ForeignKey("CS_EXP_Project_Translation.ProjectID"))
    Status = Column(String(50))
    StatusDate = Column(DateTime, default=datetime.utcnow)
    UpdatedBy = Column(String(100))
    Comments = Column(String(500))
    
    project = relationship("Project", back_populates="statuses") 