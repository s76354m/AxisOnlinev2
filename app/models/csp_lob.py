from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class LOBType(enum.Enum):
    MEDICAL = "medical"
    PHARMACY = "pharmacy"
    DENTAL = "dental"
    VISION = "vision"
    OTHER = "other"

class CSPStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class CSPLOB(Base):
    __tablename__ = 'csp_lob'
    
    id = Column(Integer, primary_key=True)
    csp_code = Column(String(50), nullable=False)
    lob_type = Column(Enum(LOBType), nullable=False)
    description = Column(String(500))
    status = Column(Enum(CSPStatus), default=CSPStatus.ACTIVE)
    effective_date = Column(DateTime)
    termination_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    project = relationship("Project", back_populates="csp_lobs")
    
    # Add unique constraint for csp_code + lob_type combination
    __table_args__ = (
        UniqueConstraint('csp_code', 'lob_type', name='uix_csp_lob'),
    ) 