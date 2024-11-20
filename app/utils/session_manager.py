import streamlit as st

def initialize_session_state():
    """Initialize all required session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    if 'show_new_project' not in st.session_state:
        st.session_state.show_new_project = False
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'project_status': 'All',
            'date_range': 'Last 30 days',
            'analyst': 'All'
        }
    if 'last_error' not in st.session_state:
        st.session_state.last_error = None 