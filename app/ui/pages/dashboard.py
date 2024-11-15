"""Dashboard page implementation"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from app.db.session import get_db

def render_page():
    """Render dashboard page"""
    st.title("Dashboard")

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        db = next(get_db())
        
        # Active Projects
        with col1:
            active_query = """
            SELECT COUNT(*) as count 
            FROM CS_EXP_Project_Translation WITH (NOLOCK)
            WHERE Status IN ('New', 'Active')
            """
            active_df = pd.read_sql(active_query, db.bind)
            st.metric("Active Projects", active_df['count'].iloc[0])

        # Projects in Review
        with col2:
            review_query = """
            SELECT COUNT(*) as count 
            FROM CS_EXP_Project_Translation WITH (NOLOCK)
            WHERE Status = 'Review'
            """
            review_df = pd.read_sql(review_query, db.bind)
            st.metric("In Review", review_df['count'].iloc[0])

        # Completed This Month
        with col3:
            completed_query = """
            SELECT COUNT(*) as count 
            FROM CS_EXP_Project_Translation WITH (NOLOCK)
            WHERE Status = 'Completed' 
            AND LastEditDate >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)
            """
            completed_df = pd.read_sql(completed_query, db.bind)
            st.metric("Completed (This Month)", completed_df['count'].iloc[0])

        # Total Projects
        with col4:
            total_query = """
            SELECT COUNT(*) as count 
            FROM CS_EXP_Project_Translation WITH (NOLOCK)
            """
            total_df = pd.read_sql(total_query, db.bind)
            st.metric("Total Projects", total_df['count'].iloc[0])

        # Recent Activity
        st.subheader("Recent Activity")
        recent_query = """
        SELECT TOP 10
            p.ProjectID,
            p.ProjectType,
            p.Status,
            p.LastEditMSID as Editor,
            CONVERT(VARCHAR(23), p.LastEditDate, 126) as EditDate
        FROM CS_EXP_Project_Translation p WITH (NOLOCK)
        ORDER BY p.LastEditDate DESC
        """
        recent_df = pd.read_sql(recent_query, db.bind)
        
        if not recent_df.empty:
            st.dataframe(
                recent_df,
                column_config={
                    "ProjectID": "Project ID",
                    "ProjectType": "Type",
                    "Status": "Status",
                    "Editor": "Last Editor",
                    "EditDate": "Edit Date"
                },
                hide_index=True
            )
        else:
            st.info("No recent activity found.")

        # Status Distribution Chart
        st.subheader("Project Status Distribution")
        status_query = """
        SELECT 
            Status,
            COUNT(*) as Count
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        GROUP BY Status
        """
        status_df = pd.read_sql(status_query, db.bind)
        
        if not status_df.empty:
            st.bar_chart(status_df.set_index('Status'))

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
    finally:
        db.close() 