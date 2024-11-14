"""Main UI module for Axis Program"""
import streamlit as st
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Import components
from app.frontend.components import (
    display_project_management,
    display_competitor_management,
    display_service_area_management,
    display_notes_management,
    display_status_tracker
)
from app.frontend.dashboard import display_dashboard

logger = logging.getLogger(__name__)

class AxisProgramUI:
    """Main UI class for Axis Program Management"""
    
    def __init__(self):
        try:
            st.set_page_config(
                page_title="Axis Program Management",
                page_icon="📊",
                layout="wide"
            )
            
            # Initialize session state
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 'Projects'
            if 'current_view' not in st.session_state:
                st.session_state.current_view = 'dashboard'
            if 'selected_project' not in st.session_state:
                st.session_state.selected_project = None
            if 'last_update' not in st.session_state:
                st.session_state.last_update = datetime.now()
                
            logger.info("AxisProgramUI initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AxisProgramUI: {str(e)}")
            raise

    def render_navigation(self) -> None:
        """Render navigation sidebar"""
        try:
            with st.sidebar:
                st.title("Navigation")
                
                # Main navigation
                selected_page = st.radio(
                    "Select Page",
                    options=['Dashboard', 'Projects', 'Competitors', 
                            'Service Areas', 'Notes', 'Status Tracker']
                )
                
                if selected_page != st.session_state.current_page:
                    st.session_state.current_page = selected_page
                    st.session_state.current_view = 'dashboard'
                    logger.info(f"Navigation changed to: {selected_page}")
                
                # Additional controls based on page
                if selected_page == 'Projects':
                    st.selectbox(
                        "View",
                        options=['List View', 'Grid View', 'Timeline'],
                        key='project_view'
                    )
                
                # User info and settings
                st.sidebar.markdown("---")
                st.sidebar.text(f"Last Update: {st.session_state.last_update:%Y-%m-%d %H:%M}")
                
        except Exception as e:
            logger.error(f"Error rendering navigation: {str(e)}")
            st.error("Error loading navigation. Please refresh the page.")

    def render_content(self) -> None:
        """Render main content based on current page"""
        try:
            # Page header
            st.title(f"Axis Program - {st.session_state.current_page}")
            
            # Render page content
            if st.session_state.current_page == 'Dashboard':
                display_dashboard()
            
            elif st.session_state.current_page == 'Projects':
                display_project_management()
            
            elif st.session_state.current_page == 'Competitors':
                display_competitor_management()
            
            elif st.session_state.current_page == 'Service Areas':
                display_service_area_management()
            
            elif st.session_state.current_page == 'Notes':
                display_notes_management()
            
            elif st.session_state.current_page == 'Status Tracker':
                display_status_tracker()
            
            # Update last update timestamp
            st.session_state.last_update = datetime.now()
            
        except Exception as e:
            logger.error(f"Error rendering content: {str(e)}")
            st.error("Error loading content. Please try again or contact support.")

    def handle_session_state(self) -> None:
        """Handle session state updates and cleanup"""
        try:
            # Clear temporary states if needed
            if 'temp_data' in st.session_state:
                del st.session_state.temp_data
            
            # Validate selected project
            if (st.session_state.selected_project and 
                st.session_state.current_page != 'Projects'):
                st.session_state.selected_project = None
            
            # Update session metadata
            st.session_state.last_update = datetime.now()
            
        except Exception as e:
            logger.error(f"Error handling session state: {str(e)}")
            # Don't raise here to prevent UI crashes

    def run(self) -> None:
        """Main entry point to run the UI"""
        try:
            self.render_navigation()
            self.handle_session_state()
            self.render_content()
            
            logger.info(f"UI rendered successfully: {st.session_state.current_page}")
            
        except Exception as e:
            logger.error(f"Error running UI: {str(e)}")
            st.error("An error occurred. Please refresh the page or contact support.")

def main():
    """Main function to initialize and run the UI"""
    try:
        ui = AxisProgramUI()
        ui.run()
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        st.error("Fatal error occurred. Please contact support.")

if __name__ == "__main__":
    main()