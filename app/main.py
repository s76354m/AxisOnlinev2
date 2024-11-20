import streamlit as st
import logging
from app.ui.pages import (
    project_management,
    competitor_management,
    service_area_management,
    y_line_management,
    csp_lob_management
)
from app.db.session import SessionLocal
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        st.set_page_config(
            page_title="Project Management",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize session state
        if 'db_session' not in st.session_state:
            st.session_state.db_session = SessionLocal()
        if 'verbose_logging' not in st.session_state:
            st.session_state.verbose_logging = False
            
        # Sidebar
        with st.sidebar:
            st.title("Navigation")
            selected_page = st.selectbox("Select Page", [
                "Dashboard",
                "Project Management",
                "Service Area Management",
                "CSP LOB Management"
            ])
            
            st.divider()
            st.checkbox("Enable Verbose Logging", 
                       key="verbose_logging",
                       help="Show detailed logging information")
            
            st.divider()
            st.markdown("### User Info")
            st.text(f"Connected to: {settings.DB_NAME}")
        
        # Main content
        if selected_page == "Dashboard":
            from app.frontend.dashboard import display_dashboard
            display_dashboard()
        else:
            pages = {
                "Project Management": project_management,
                "Service Area Management": service_area_management,
                "CSP LOB Management": csp_lob_management
            }
            pages[selected_page].render_page(st.session_state.db_session)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please try refreshing the page.")
    
    finally:
        if 'db_session' in st.session_state:
            st.session_state.db_session.close()

if __name__ == "__main__":
    main() 