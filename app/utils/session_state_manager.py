import streamlit as st
from typing import Dict, Any
from datetime import datetime

class SessionStateManager:
    @staticmethod
    def initialize():
        """Initialize all required session state variables"""
        defaults = {
            'current_page': 'Dashboard',
            'last_activity': datetime.now(),
            'filters': {
                'project_status': 'All',
                'date_range': 'Last 30 days',
                'analyst': 'All'
            },
            'error_state': None,
            'db_status': None
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any):
        st.session_state[key] = value
        st.session_state.last_activity = datetime.now() 