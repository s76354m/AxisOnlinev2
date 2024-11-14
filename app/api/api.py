from fastapi import APIRouter
from app.api.endpoints import y_line

api_router = APIRouter()
api_router.include_router(y_line.router, tags=["y-lines"]) 