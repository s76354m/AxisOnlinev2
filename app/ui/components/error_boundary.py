import streamlit as st
from functools import wraps
from typing import Callable, Optional
from app.utils.session_state_manager import SessionStateManager

def error_boundary(component_name: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                st.error(f"Error in {component_name}")
                st.error(f"Details: {str(e)}")
                SessionStateManager.set('error_state', {
                    'component': component_name,
                    'error': str(e),
                    'timestamp': st.session_state.last_activity
                })
                if st.button("Retry"):
                    st.experimental_rerun()
                return None
        return wrapper
    return decorator 