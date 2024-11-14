import streamlit as st
import pandas as pd
from app.services.project_service import ProjectService
from app.models.project import ProjectStatus, ProjectType

def render_page(db_session):
    st.title("Project Management")
    
    # Initialize services
    project_service = ProjectService(db_session)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Project List", "Add Project", "Reports"])
    
    with tab1:
        render_project_list(project_service)
    
    with tab2:
        render_add_project_form(project_service)
    
    with tab3:
        render_project_reports(project_service)

def render_project_list(project_service):
    st.header("Project List")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Status",
            options=[s.value for s in ProjectStatus]
        )
    with col2:
        type_filter = st.multiselect(
            "Type",
            options=[t.value for t in ProjectType]
        )
    with col3:
        search = st.text_input("Search", "")
    
    # Get and display projects
    projects = project_service.get_projects(
        status_filter=status_filter,
        type_filter=type_filter,
        search=search
    )
    
    if projects:
        df = pd.DataFrame(projects)
        st.dataframe(
            df,
            column_config={
                "id": "Project ID",
                "name": "Project Name",
                "status": "Status",
                "type": "Type",
                "created_at": "Created Date"
            },
            hide_index=True
        )
    else:
        st.info("No projects found matching the criteria.")

def render_add_project_form(project_service):
    st.header("Add New Project")
    
    with st.form("add_project"):
        name = st.text_input("Project Name")
        status = st.selectbox("Status", options=[s.value for s in ProjectStatus])
        type = st.selectbox("Type", options=[t.value for t in ProjectType])
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Add Project")
        
        if submitted:
            try:
                project_service.create_project(
                    name=name,
                    status=status,
                    type=type,
                    description=description
                )
                st.success("Project added successfully!")
            except Exception as e:
                st.error(f"Error adding project: {str(e)}")

def render_project_reports(project_service):
    st.header("Project Reports")
    
    # Status summary
    status_summary = project_service.get_status_summary()
    if status_summary:
        st.subheader("Status Summary")
        st.bar_chart(status_summary)
    
    # Type summary
    type_summary = project_service.get_type_summary()
    if type_summary:
        st.subheader("Type Summary")
        st.bar_chart(type_summary) 