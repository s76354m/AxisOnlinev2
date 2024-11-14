from pydantic import BaseModel

class BaseResponse(BaseModel):
    """Base response model with common fields"""
    class Config:
        orm_mode = True 