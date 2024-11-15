"""Main entry point for Streamlit application"""
import streamlit as st
from app.ui.main import AxisProgramUI
from app.ui.pages import (
    dashboard,
    project_management,
    csp_lob_management,
    y_line_management,
    service_area_management
)

def main():
    try:
        ui = AxisProgramUI()
        page = ui.render_navigation()
        
        if page == 'Dashboard':
            dashboard.render_dashboard()
        elif page == 'Projects':
            project_management.render_page()
        elif page == 'CSP LOB':
            csp_lob_management.render_page()
        elif page == 'Y-Line':
            y_line_management.render_page()
        elif page == 'Service Areas':
            service_area_management.render_page()
            
    except Exception as e:
        st.error(f"Application Error: {str(e)}")

if __name__ == "__main__":
    main() 