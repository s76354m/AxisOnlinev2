import streamlit as st
from app.ui.pages import (
    project_management,
    csp_lob_management,
    y_line_management,
    competitor_management,
    service_area_management,
    dashboard
)

def main():
    st.set_page_config(page_title="SwarmV2", layout="wide")
    
    pages = {
        "Dashboard": dashboard.render_page,
        "Project Management": project_management.render_page,
        "CSP LOB Management": csp_lob_management.render_page,
        "Y-Line Management": y_line_management.render_page,
        "Service Area Management": service_area_management.render_page,
        "Competitor Management": competitor_management.render_page
    }
    
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main() 