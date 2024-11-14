from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import ProjectException, DatabaseException, NotFoundException

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error occurred", "error": str(e)}
        )
    except ProjectException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": str(e.detail)}
        )
    except NotFoundException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": str(e.detail)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(e)}
        ) 