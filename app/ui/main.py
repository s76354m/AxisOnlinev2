"""Main UI module for Axis Program Management"""
import streamlit as st
from typing import Optional
from app.ui.pages import (
    dashboard,
    project_management,
    csp_lob_management,
    y_line_management,
    service_area_management,
    competitor_management,
    notes_management
)

class AxisProgramUI:
    def __init__(self):
        self.setup_session_state()
        self.setup_page_config()
        self.init_session_vars()
    
    def setup_session_state(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Dashboard'
        if 'show_new_project' not in st.session_state:
            st.session_state.show_new_project = False
    
    def setup_page_config(self):
        st.set_page_config(
            page_title="Axis Program",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def init_session_vars(self):
        """Initialize session variables for UI state"""
        if 'filters' not in st.session_state:
            st.session_state.filters = {
                'project_status': 'All',
                'date_range': 'Last 30 days',
                'analyst': 'All'
            }
    
    def render_navigation(self):
        with st.sidebar:
            st.title("Navigation")
            
            # Main Navigation
            selected_page = st.selectbox(
                "Select Page",
                [
                    'Dashboard',
                    'Projects',
                    'CSP LOB',
                    'Y-Line',
                    'Service Areas',
                    'Competitors',
                    'Notes'
                ]
            )
            
            # Quick Actions Section
            st.sidebar.markdown("---")
            st.sidebar.subheader("Quick Actions")
            
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("New Project"):
                    st.session_state.current_page = 'Projects'
                    st.session_state.show_new_project = True
                if st.button("New Note"):
                    st.session_state.current_page = 'Notes'
                    st.session_state.show_new_note = True
            
            with col2:
                if st.button("New CSP LOB"):
                    st.session_state.current_page = 'CSP LOB'
                    st.session_state.show_new_mapping = True
                if st.button("New Y-Line"):
                    st.session_state.current_page = 'Y-Line'
                    st.session_state.show_new_yline = True
            
            # Filters Section
            st.sidebar.markdown("---")
            st.sidebar.subheader("Filters")
            st.session_state.filters['project_status'] = st.sidebar.selectbox(
                "Project Status",
                ['All', 'New', 'Active', 'Completed', 'On Hold']
            )
            st.session_state.filters['date_range'] = st.sidebar.selectbox(
                "Date Range",
                ['Last 7 days', 'Last 30 days', 'Last 90 days', 'All time']
            )
            
            return selected_page

def main():
    try:
        app = AxisProgramUI()
        page = app.render_navigation()
        
        # Render breadcrumb navigation
        st.markdown(f"**Navigation:** {page}")
        
        # Render selected page
        if page == 'Dashboard':
            dashboard.render_page()
        elif page == 'Projects':
            project_management.render_page()
        elif page == 'CSP LOB':
            csp_lob_management.render_page()
        elif page == 'Y-Line':
            y_line_management.render_page()
        elif page == 'Service Areas':
            service_area_management.render_page()
        elif page == 'Competitors':
            competitor_management.render_page()
        elif page == 'Notes':
            notes_management.render_page()
            
    except Exception as e:
        st.error(f"Error in main UI: {str(e)}")
        st.exception(e)  # Display detailed error information

if __name__ == "__main__":
    main()