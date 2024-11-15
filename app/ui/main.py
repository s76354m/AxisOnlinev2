"""Main UI module for Axis Program Management"""
import streamlit as st
import logging
from datetime import datetime
from app.ui.pages import (
    dashboard,
    project_management,
    csp_lob_management,
    competitor_management,
    service_area_management,
    y_line_management
)

logger = logging.getLogger(__name__)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Projects"
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "list"
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = None

def main():
    """Main entry point for the UI"""
    try:
        st.set_page_config(
            page_title="Axis Program Management",
            page_icon="🏢",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        initialize_session_state()

        # Sidebar navigation
        with st.sidebar:
            st.title("Navigation")
            
            selected_page = st.radio(
                "Select Page",
                ["Dashboard", "Projects", "CSP LOB", "Competitors", 
                 "Service Areas", "Y-Line"]
            )
            
            # Update current page in session state
            st.session_state.current_page = selected_page
            
            st.divider()
            st.markdown("### Settings")
            st.checkbox("Verbose Logging", key="verbose_logging")
            
            st.divider()
            st.markdown("### User Info")
            st.text(f"Last Update: {datetime.now():%Y-%m-%d %H:%M}")

        # Main content area
        if selected_page == "Dashboard":
            dashboard.render_page()
        elif selected_page == "Projects":
            project_management.render_page()
        elif selected_page == "CSP LOB":
            csp_lob_management.render_page()
        elif selected_page == "Competitors":
            competitor_management.render_page()
        elif selected_page == "Service Areas":
            service_area_management.render_page()
        elif selected_page == "Y-Line":
            y_line_management.render_page()

    except Exception as e:
        logger.error(f"Error in main UI: {str(e)}")
        st.error("An error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()