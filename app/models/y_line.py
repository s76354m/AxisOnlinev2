from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base
from enum import Enum as PyEnum

class YLineStatus(str, PyEnum):
    PENDING = "Pending"
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class YLine(Base):
    __tablename__ = "CS_EXP_YLine"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)
    ipa_number = Column(String(50), unique=True, index=True)
    product_code = Column(String(50))
    description = Column(String(500))
    pre_award_status = Column(String(50))
    post_award_status = Column(String(50))
    estimated_value = Column(Float)
    actual_value = Column(Float)
    status = Column(Enum(YLineStatus), default=YLineStatus.PENDING)
    notes = Column(String(1000))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())