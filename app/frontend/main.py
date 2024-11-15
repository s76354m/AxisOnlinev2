import streamlit as st
from typing import Optional
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService

class AxisProgramUI:
    def __init__(self):
        self.setup_session_state()
        self.setup_page_config()
        self.init_services()
    
    def setup_session_state(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Projects'
    
    def setup_page_config(self):
        st.set_page_config(
            page_title="Axis Program",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def init_services(self):
        """Initialize services using existing DB connection"""
        self.project_service = ProjectService()
        self.csp_lob_service = CSPLOBService()
        self.y_line_service = YLineService()
    
    def render_navigation(self):
        st.sidebar.title("Navigation")
        return st.sidebar.selectbox(
            "Select Page",
            ['Projects', 'CSP LOB', 'Y-Line', 'Service Areas']
        )

    def display_project_details(self, project_id: Optional[str] = None):
        try:
            if project_id:
                project = self.project_service.get_project(project_id)
                with st.expander(f"Project Details - {project_id}"):
                    st.write(project)
            else:
                st.write("No project selected")
        except Exception as e:
            st.error(f"Error displaying project details: {str(e)}") 