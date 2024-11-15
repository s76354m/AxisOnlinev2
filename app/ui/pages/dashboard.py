"""Dashboard page implementation"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService

def render_page():
    st.title("Project Dashboard")
    
    try:
        # Initialize services
        project_service = ProjectService()
        csp_lob_service = CSPLOBService()
        y_line_service = YLineService()
        
        # Top-level metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            projects = project_service.get_all_projects()
            st.metric("Total Projects", len(projects))
        
        with col2:
            active_projects = len([p for p in projects if p.Status == "Active"])
            st.metric("Active Projects", active_projects)
        
        with col3:
            csp_lobs = csp_lob_service.get_all_csp_lobs()
            st.metric("LOB Mappings", len(csp_lobs))
        
        with col4:
            y_lines = y_line_service.get_all_y_lines()
            st.metric("Y-Lines", len(y_lines))
        
        # Charts section
        st.subheader("Analytics")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Project Status Distribution
            if projects:
                df_projects = pd.DataFrame([vars(p) for p in projects])
                fig1 = px.pie(df_projects, names='Status', 
                             title='Project Status Distribution')
                st.plotly_chart(fig1, use_container_width=True)
        
        with chart_col2:
            # Project Timeline
            if projects:
                df_timeline = pd.DataFrame([{
                    'Project': p.ProjectID,
                    'Start': p.CreatedDate,
                    'End': p.LastEditDate
                } for p in projects])
                fig2 = px.timeline(df_timeline, x_start='Start', x_end='End',
                                 y='Project', title='Project Timeline')
                st.plotly_chart(fig2, use_container_width=True)
        
        # Recent Activity Feed
        st.subheader("Recent Activity")
        tabs = st.tabs(["Projects", "CSP LOB", "Y-Lines"])
        
        with tabs[0]:
            if projects:
                recent_projects = sorted(
                    projects, 
                    key=lambda x: x.LastEditDate, 
                    reverse=True
                )[:5]
                for project in recent_projects:
                    with st.expander(
                        f"Project: {project.ProjectID} - {project.ProjectType}"
                    ):
                        cols = st.columns(3)
                        with cols[0]:
                            st.write(f"Status: {project.Status}")
                        with cols[1]:
                            st.write(f"PM: {project.PM}")
                        with cols[2]:
                            st.write(
                                f"Last Updated: {project.LastEditDate.strftime('%Y-%m-%d')}"
                            )
        
        with tabs[1]:
            if csp_lobs:
                for lob in csp_lobs[:5]:
                    with st.expander(f"CSP: {lob.csp_code}"):
                        st.write(f"Type: {lob.lob_type}")
                        st.write(f"Status: {lob.status}")
        
        with tabs[2]:
            if y_lines:
                for y_line in y_lines[:5]:
                    with st.expander(f"Y-Line: {y_line.ipa_number}"):
                        st.write(f"Product: {y_line.product_code}")
                        st.write(f"Status: {y_line.status}")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.exception(e)