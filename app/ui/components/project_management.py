"""Project management component"""
import streamlit as st
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def display_project_management():
    """Display project management interface"""
    try:
        st.header("Project Management")
        
        # Add new project button with proper layout and unique key
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            if st.button("+ New Project", type="primary", key="project_mgmt_new_btn"):
                print("New Project button clicked in component")  # Debug print
                st.session_state.current_view = 'new_project'
                st.rerun()
                return  # Exit after state change
        
        # Project List/Grid Toggle
        view_type = st.radio("View", ["List", "Grid"], horizontal=True)
        
        # Project Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Status", ["All", "Active", "Completed", "On Hold"])
        with col2:
            st.selectbox("Type", ["All", "Translation", "Analysis"])
        with col3:
            st.text_input("Search", placeholder="Search projects...")
        
        # Project List
        st.dataframe(
            {
                "Project ID": ["PROJ001", "PROJ002"],
                "Name": ["Test Project 1", "Test Project 2"],
                "Status": ["Active", "On Hold"],
                "Type": ["Translation", "Analysis"],
                "Last Updated": ["2024-01-01", "2024-01-02"]
            }
        )
        
    except Exception as e:
        logger.error(f"Error displaying project management: {str(e)}")
        st.error("Error loading project management interface") 