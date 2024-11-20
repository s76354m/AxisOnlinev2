import streamlit as st
import pandas as pd
from app.services.project_service import ProjectService

def render_page(db_session):
    st.title("Project Management")
    
    try:
        with st.spinner("Loading projects..."):
            project_service = ProjectService(db_session)
            
            tab1, tab2 = st.tabs(["Project List", "Add Project"])
            
            with tab1:
                render_project_list(project_service)
            
            with tab2:
                render_add_project_form(project_service)
                
    except Exception as e:
        st.error(f"Error loading project management: {str(e)}")

def render_project_list(project_service):
    # Add New Project button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("➕ New Project", type="primary", key="new_project_btn"):
            st.session_state.current_view = 'new_project'
            st.rerun()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Inactive", "Pending"],
            key="status_filter"
        )
    with col2:
        search = st.text_input("Search Projects", key="project_search")
    
    # Project Table
    projects = project_service.get_projects(status=status_filter if status_filter != "All" else None)
    
    if projects:
        df = pd.DataFrame([{
            "Project ID": p.ProjectID,
            "Description": p.ProjectDesc,
            "Status": p.Status,
            "Analyst": p.Analyst,
            "PM": p.PM,
            "Last Updated": p.LastEditDate
        } for p in projects])
        
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No projects found matching the criteria.")

def render_add_project_form(project_service):
    st.header("Add New Project")
    
    with st.form("new_project_form"):
        name = st.text_input("Project Name")
        status = st.selectbox("Status", ["Active", "Inactive", "Pending"])
        service_area = st.text_input("Service Area")
        
        if st.form_submit_button("Create Project"):
            try:
                project_service.create_project({
                    "name": name,
                    "status": status,
                    "service_area": service_area
                })
                st.success("Project created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating project: {str(e)}")