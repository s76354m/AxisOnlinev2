from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.db.base import Base
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import pandas as pd

class YLine(Base):
    __tablename__ = "CS_EXP_YLine_Translation"

    RecordID = Column(Integer, primary_key=True, index=True)
    ProjectID = Column(String(12), index=True)
    ProjectStatus = Column(String(10))
    NDB_Yline_ProdCd = Column(String(2))
    NDB_Yline_IPA = Column(Integer)
    NDB_Yline_MktNum = Column(Integer)
    DataLoadDate = Column(DateTime, server_default=func.now())
    LastEditDate = Column(DateTime, server_default=func.now(), onupdate=func.now())
    LastEditMSID = Column(String(15))
    PreAward = Column(Integer, default=0) 

@dataclass
class YLineItem:
    """Y-Line item model"""
    ipa_number: str
    product_code: str
    description: str
    pre_award: bool
    post_award: bool
    status: str
    last_updated: datetime
    notes: Optional[str] = None

class YLineManager:
    """Y-Line management functionality"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_yline_items(self, status_filter=None):
        """Get Y-Line items with optional filtering"""
        query = """
        SELECT 
            IPA_Number,
            ProductCode,
            Description,
            PreAward,
            PostAward,
            Status,
            LastEditDate,
            Notes
        FROM CS_EXP_YLine WITH (NOLOCK)
        WHERE 1=1
        """
        
        if status_filter:
            query += " AND Status = ?"
            return pd.read_sql(query, self.db.bind, params=(status_filter,))
        
        return pd.read_sql(query, self.db.bind)
    
    def create_yline_item(self, item: YLineItem):
        """Create new Y-Line item"""
        query = """
        INSERT INTO CS_EXP_YLine (
            IPA_Number,
            ProductCode,
            Description,
            PreAward,
            PostAward,
            Status,
            LastEditDate,
            Notes
        ) VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?)
        """
        
        self.db.execute(
            query,
            (
                item.ipa_number,
                item.product_code,
                item.description,
                item.pre_award,
                item.post_award,
                item.status,
                item.notes
            )
        )
        self.db.commit() 