import streamlit as st
from typing import Optional, Callable
import traceback
from app.core.logging_config import logger
from typing import Tuple, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from app.utils.db_monitor import DatabaseMonitor

logger = logging.getLogger(__name__)
db_monitor = DatabaseMonitor()

class UIErrorHandler:
    @staticmethod
    def handle_error(error: Exception, message: str = "An error occurred", show_trace: bool = False):
        logger.error(f"{message}: {str(error)}")
        logger.error(traceback.format_exc())
        
        if show_trace:
            st.error(f"{message}: {str(error)}")
        else:
            st.error(message)

    @staticmethod
    def api_error_handler(response, success_message: str = "Operation successful"):
        if response.status_code == 200:
            st.success(success_message)
            return True
        else:
            error_message = response.json().get('detail', 'Unknown error occurred')
            st.error(f"Error: {error_message}")
            logger.error(f"API Error: {error_message}")
            return False

def handle_exceptions(func: Callable):
    """Decorator for handling exceptions in Streamlit functions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            UIErrorHandler.handle_error(e)
            return None
    return wrapper 

class AppError:
    """Application error types"""
    DB_CONNECTION = "Database Connection Error"
    DB_QUERY = "Database Query Error"
    VALIDATION = "Validation Error"
    FORM = "Form Error"
    BULK_OPERATION = "Bulk Operation Error"
    UNKNOWN = "Unknown Error"

def handle_error(error_type: str, error: Exception, context: Optional[dict] = None) -> str:
    """Centralized error handling"""
    error_message = str(error)
    
    # Log error with context
    logger.error(f"{error_type}: {error_message}", extra={"context": context})
    
    # Monitor database errors
    if isinstance(error, SQLAlchemyError):
        db_monitor.log_error(error_type, error)
    
    # Return user-friendly message
    return f"{error_type}: {error_message}"

def db_operation_handler(operation_name: str):
    """Decorator for database operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[bool, Any]:
            try:
                result = func(*args, **kwargs)
                db_monitor.log_operation(operation_name, "success")
                return True, result
            except SQLAlchemyError as e:
                error_msg = handle_error(AppError.DB_QUERY, e, {
                    "operation": operation_name,
                    "args": args,
                    "kwargs": kwargs
                })
                return False, error_msg
            except Exception as e:
                error_msg = handle_error(AppError.UNKNOWN, e, {
                    "operation": operation_name
                })
                return False, error_msg
        return wrapper
    return decorator

def form_validation_handler(form_name: str):
    """Decorator for form validation"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[bool, Any]:
            try:
                return True, func(*args, **kwargs)
            except ValueError as e:
                error_msg = handle_error(AppError.VALIDATION, e, {
                    "form": form_name
                })
                return False, error_msg
        return wrapper
    return decorator

def display_operation_result(success: bool, message: str):
    """Standardized way to display operation results"""
    if success:
        st.success(message)
    else:
        st.error(message) 