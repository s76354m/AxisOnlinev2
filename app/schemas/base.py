from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseResponse(BaseSchema):
    success: bool
    message: str
    data: Optional[Any] = None 