import streamlit as st
import pandas as pd
from app.services.project_service import ProjectService

def render_page(db_session):
    st.title("Project Management")
    
    try:
        project_service = ProjectService(db_session)
        
        # Add New Project button
        col1, _ = st.columns([1, 3])
        with col1:
            if st.button("➕ New Project", type="primary"):
                st.session_state.show_add_project = True
                st.rerun()
        
        # Project List/Grid Toggle
        view_type = st.radio("View", ["List", "Grid"], horizontal=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "Active", "Inactive", "Pending"],
                key="status_filter"
            )
        with col2:
            project_type = st.selectbox(
                "Type",
                ["All", "Translation", "Analysis"],
                key="type_filter"
            )
        with col3:
            search = st.text_input("Search", placeholder="Search projects...")
        
        # Project Table
        projects = project_service.get_projects(
            status=status_filter if status_filter != "All" else None
        )
        
        if projects:
            df = pd.DataFrame([{
                "Project ID": p.ProjectID,
                "Description": p.ProjectDesc,
                "Status": p.Status,
                "Type": p.ProjectType,
                "Analyst": p.Analyst,
                "PM": p.PM,
                "Last Updated": p.LastEditDate
            } for p in projects])
            
            if search:
                df = df[df.astype(str).apply(
                    lambda x: x.str.contains(search, case=False)
                ).any(axis=1)]
            
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No projects found matching the criteria.")
            
    except Exception as e:
        st.error(f"Error loading project management: {str(e)}")