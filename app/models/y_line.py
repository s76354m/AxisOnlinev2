from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class YLineStatus(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class YLine(Base):
    __tablename__ = 'y_lines'
    
    id = Column(Integer, primary_key=True)
    ipa_number = Column(String(50), unique=True, nullable=False)
    product_code = Column(String(50), nullable=False)
    description = Column(String(500))
    pre_award_status = Column(String(20))
    post_award_status = Column(String(20))
    estimated_value = Column(Float)
    actual_value = Column(Float)
    status = Column(Enum(YLineStatus), default=YLineStatus.PENDING)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="y_lines")