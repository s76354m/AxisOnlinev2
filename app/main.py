import streamlit as st
from app.ui.pages import PAGE_ROUTES
from app.utils.db_monitor import DatabaseMonitor, display_db_status
from app.utils.startup_verification import verify_startup_requirements
from app.utils.session_state_manager import SessionStateManager

def main():
    try:
        # Initialize session state
        SessionStateManager.initialize()
        
        # Page config
        st.set_page_config(page_title="SwarmV2", layout="wide")
        
        # Verify startup requirements
        startup_checks = verify_startup_requirements()
        if not all(check[1] for check in startup_checks):
            for check in startup_checks:
                if not check[1]:
                    st.error(f"{check[0]}: {check[2]}")
            if st.button("Retry Startup"):
                st.experimental_rerun()
            return
        
        # Initialize and display database monitoring
        db_monitor = DatabaseMonitor()
        st.sidebar.title("System Status")
        display_db_status(db_monitor)
        
        # Navigation
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(PAGE_ROUTES.keys()))
        SessionStateManager.set('current_page', selection)
        
        # Breadcrumb
        st.markdown(f"🏠 **Navigation:** {selection}")
        
        # Render selected page
        if selection in PAGE_ROUTES:
            PAGE_ROUTES[selection]()
        else:
            st.error("Page not found")
            
    except Exception as e:
        st.error("Application Error")
        st.error(f"Details: {str(e)}")
        if st.button("Retry"):
            st.experimental_rerun()

if __name__ == "__main__":
    main() 