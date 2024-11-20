from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class CSPLOB(Base):
    __tablename__ = 'csp_lob'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True)
    description = Column(String(500))
    status = Column(String(50)) 