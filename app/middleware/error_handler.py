from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    SQLAlchemyError
)
from typing import Union
import logging

logger = logging.getLogger(__name__)

class ErrorHandler:
    async def __call__(
        self,
        request: Request,
        call_next
    ) -> Union[JSONResponse, Request]:
        try:
            return await call_next(request)
        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Database integrity error", "message": str(e)}
            )
        except OperationalError as e:
            logger.error(f"Database operational error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"detail": "Database connection error", "message": str(e)}
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Database error", "message": str(e)}
            )
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Validation error", "message": str(e)}
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error", "message": str(e)}
            ) 