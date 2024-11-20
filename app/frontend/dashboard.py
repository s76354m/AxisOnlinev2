"""Dashboard component"""
import streamlit as st
import logging
import pandas as pd
import plotly.express as px
from app.services.project_service import ProjectService
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def display_dashboard():
    """Display main dashboard with real-time metrics"""
    st.header("Dashboard")
    
    try:
        project_service = ProjectService(st.session_state.db_session)
        all_projects = project_service.get_projects()
        
        # Project Metrics
        active_projects = [p for p in all_projects if p.Status == "Active"]
        pending_projects = [p for p in all_projects if p.Status == "Pending"]
        on_hold_projects = [p for p in all_projects if p.Status == "On Hold"]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Projects", len(active_projects))
        with col2:
            st.metric("Pending Projects", len(pending_projects))
        with col3:
            st.metric("On Hold", len(on_hold_projects))
        with col4:
            st.metric("Total Projects", len(all_projects))
        
        # Project Status Chart
        status_counts = pd.DataFrame([
            {"Status": p.Status, "Count": 1} for p in all_projects
        ]).groupby("Status").sum().reset_index()
        
        fig = px.pie(
            status_counts, 
            values="Count", 
            names="Status",
            title="Project Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent Activity
        st.subheader("Recent Activity")
        recent_projects = sorted(
            [p for p in all_projects if p.LastEditDate],
            key=lambda x: x.LastEditDate,
            reverse=True
        )[:5]
        
        if recent_projects:
            activity_df = pd.DataFrame([{
                "Project ID": p.ProjectID,
                "Status": p.Status,
                "Last Updated": p.LastEditDate.strftime("%Y-%m-%d %H:%M"),
                "Updated By": getattr(p, "LastEditMSID", "Unknown")
            } for p in recent_projects])
            st.dataframe(activity_df, hide_index=True)
            
    except Exception as e:
        logger.error(f"Error displaying dashboard: {str(e)}")
        st.error("Error loading dashboard")