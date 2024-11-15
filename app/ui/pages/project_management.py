import streamlit as st
import pandas as pd
from datetime import datetime
from app.models.project import ProjectStatus, ProjectType
from app.db.session import get_db

def render_page():
    """Render project management page"""
    st.title("Project Management")

    # Add new project button
    if st.button("+ New Project"):
        st.session_state.current_view = "new_project"
        st.rerun()

    # Project List/Grid Toggle
    view_type = st.radio("View", ["List", "Grid"], horizontal=True)

    # Project Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All"] + [status.value for status in ProjectStatus]
        )
    with col2:
        type_filter = st.selectbox(
            "Type",
            ["All"] + [ptype.value for ptype in ProjectType]
        )
    with col3:
        search = st.text_input("Search", placeholder="Search projects...")

    try:
        db = next(get_db())
        # Query to get projects based on filters
        query = """
        SELECT 
            ProjectID,
            ProjectType,
            ProjectDesc,
            Status,
            Analyst,
            PM,
            LastEditDate
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        WHERE 1=1
        """
        
        params = []
        if status_filter != "All":
            query += " AND Status = ?"
            params.append(status_filter)
        if type_filter != "All":
            query += " AND ProjectType = ?"
            params.append(type_filter)
        if search:
            query += " AND (ProjectDesc LIKE ? OR Analyst LIKE ? OR PM LIKE ?)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])

        query += " ORDER BY LastEditDate DESC"
        
        df = pd.read_sql(query, db.bind, params=params)
        
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "ProjectID": "Project ID",
                    "ProjectType": "Type",
                    "ProjectDesc": "Description",
                    "Status": "Status",
                    "Analyst": "Analyst",
                    "PM": "Project Manager",
                    "LastEditDate": "Last Updated"
                },
                hide_index=True
            )
        else:
            st.info("No projects found matching the criteria.")

    except Exception as e:
        st.error(f"Error loading projects: {str(e)}")
    finally:
        db.close() 