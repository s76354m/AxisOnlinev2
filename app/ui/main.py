"""Main UI module for Axis Program Management"""
import streamlit as st
from typing import Optional
from app.ui.pages import PAGE_ROUTES
from app.utils.session_manager import initialize_session_state

class AxisProgramUI:
    def __init__(self):
        initialize_session_state()
        self.setup_page_config()
    
    def setup_page_config(self):
        st.set_page_config(
            page_title="Axis Program",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_navigation(self):
        st.sidebar.title("Navigation")
        return st.sidebar.selectbox(
            "Select Page",
            list(PAGE_ROUTES.keys())
        )

    def run(self):
        try:
            selection = self.render_navigation()
            if selection in PAGE_ROUTES:
                PAGE_ROUTES[selection]()
            else:
                st.error("Page not found")
        except Exception as e:
            st.error(f"UI Error: {str(e)}")
            if st.button("Retry"):
                st.experimental_rerun()

def main():
    app = AxisProgramUI()
    app.run()

if __name__ == "__main__":
    main()