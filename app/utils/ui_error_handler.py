import streamlit as st
from app.utils.db_monitor import DatabaseMonitor
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
import traceback

db_monitor = DatabaseMonitor()

def handle_db_operation(operation_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                db_monitor.log_operation(operation_name, 'success')
                return result
            except SQLAlchemyError as e:
                error_msg = f"Database error in {operation_name}: {str(e)}"
                db_monitor.log_error(operation_name, e)
                st.error(error_msg)
                if st.checkbox("Show technical details"):
                    st.code(traceback.format_exc())
                return None
            except Exception as e:
                error_msg = f"Error in {operation_name}: {str(e)}"
                st.error(error_msg)
                return None
        return wrapper
    return decorator 