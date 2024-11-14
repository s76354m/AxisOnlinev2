import streamlit as st
from app.ui.pages import (
    project_management,
    csp_lob_management,
    competitor_management,
    service_area_management,
    y_line_management
)
from app.db.session import SessionLocal
from app.core.config import settings

def initialize_session_state():
    """Initialize session state variables"""
    if 'db_session' not in st.session_state:
        st.session_state.db_session = SessionLocal()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Projects"

def main():
    st.set_page_config(
        page_title=settings.PROJECT_NAME,
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
            ["Projects", "CSP LOB", "Competitors", "Service Areas", "Y-Line"]
        )
        
        st.divider()
        st.markdown("### User Info")
        st.text(f"Connected to: {settings.DB_NAME}")

    # Main content area
    if selected_page == "Projects":
        project_management.render_page(st.session_state.db_session)
    elif selected_page == "CSP LOB":
        csp_lob_management.render_page(st.session_state.db_session)
    elif selected_page == "Competitors":
        competitor_management.render_page(st.session_state.db_session)
    elif selected_page == "Service Areas":
        service_area_management.render_page(st.session_state.db_session)
    elif selected_page == "Y-Line":
        y_line_management.render_page(st.session_state.db_session)

if __name__ == "__main__":
    main() 