import streamlit as st
from typing import Optional, Callable
import traceback
from app.core.logging_config import logger

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