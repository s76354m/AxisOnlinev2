"""Dashboard page implementation"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService
from app.utils.db_monitor import display_db_monitor
from app.db.session import engine
from sqlalchemy import text

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return result.scalar() == 1, "Database connection successful"
    except Exception as e:
        return False, f"Database connection error: {str(e)}"

def render_page():
    """Render the dashboard page"""
    st.title("System Dashboard")
    
    # Database Status Section
    st.subheader("System Status")
    col1, col2 = st.columns(2)
    
    with col1:
        status, message = test_connection()
        if status:
            st.success("Database Connection: Active")
        else:
            st.error(f"Database Connection: {message}")
    
    with col2:
        display_db_monitor()
    
    # Add monitoring metrics
    with st.expander("Database Performance Metrics"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Connections", db_monitor.get_active_connections())
        with col2:
            st.metric("Query Response Time", f"{db_monitor.get_avg_response_time():.2f}ms")
        with col3:
            st.metric("Error Rate", f"{db_monitor.get_error_rate():.2f}%")
    
    # Page Configuration
    st.title("Dashboard")
    
    # Breadcrumb Navigation
    st.markdown("🏠 Home / Dashboard")
    
    # Initialize Services
    project_service = ProjectService()
    csp_service = CSPLOBService()
    y_line_service = YLineService()
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_projects = len(project_service.get_all_projects())
        st.metric("Total Projects", total_projects)
        
    with col2:
        active_projects = len([p for p in project_service.get_all_projects() if p.status == "Active"])
        st.metric("Active Projects", active_projects)
        
    with col3:
        total_csps = len(csp_service.get_all_csps())
        st.metric("Total CSPs", total_csps)
        
    with col4:
        total_y_lines = len(y_line_service.get_all_y_lines())
        st.metric("Total Y-Lines", total_y_lines)
    
    # Activity Feed
    st.subheader("Recent Activity")
    
    tabs = st.tabs(["Projects", "CSP LOB", "Y-Lines"])
    
    with tabs[0]:
        recent_projects = project_service.get_recent_projects(limit=5)
        if recent_projects:
            for project in recent_projects:
                with st.expander(f"Project: {project.name}", expanded=False):
                    st.write(f"Status: {project.status}")
                    st.write(f"Last Updated: {project.updated_at}")
                    st.write(f"Owner: {project.owner}")
        else:
            st.info("No recent project activity")
    
    with tabs[1]:
        recent_csps = csp_service.get_recent_csps(limit=5)
        if recent_csps:
            for csp in recent_csps:
                with st.expander(f"CSP: {csp.name}", expanded=False):
                    st.write(f"Status: {csp.status}")
                    st.write(f"Last Updated: {csp.updated_at}")
        else:
            st.info("No recent CSP activity")
    
    with tabs[2]:
        recent_y_lines = y_line_service.get_recent_y_lines(limit=5)
        if recent_y_lines:
            for y_line in recent_y_lines:
                with st.expander(f"Y-Line: {y_line.id}", expanded=False):
                    st.write(f"Status: {y_line.status}")
                    st.write(f"Last Updated: {y_line.updated_at}")
        else:
            st.info("No recent Y-Line activity")