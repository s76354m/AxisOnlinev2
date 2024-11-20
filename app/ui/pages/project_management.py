from typing import Optional, List
import streamlit as st
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate

def render_page():
    st.title("Project Management")
    project_service = ProjectService()
    
    # Create New Project Section
    with st.expander("Create New Project", expanded=st.session_state.get('show_new_project', False)):
        with st.form("new_project_form"):
            project_type = st.selectbox(
                "Project Type*",
                ["Translation", "Implementation", "Maintenance"]
            )
            description = st.text_area("Description*")
            analyst = st.text_input("Analyst*")
            pm = st.text_input("Project Manager*")
            
            submitted = st.form_submit_button("Create Project")
            if submitted:
                if not all([project_type, description, analyst, pm]):
                    st.error("Please fill in all required fields")
                else:
                    try:
                        project_data = ProjectCreate(
                            ProjectType=project_type,
                            ProjectDesc=description,
                            Status="New",
                            Analyst=analyst,
                            PM=pm
                        )
                        project = project_service.create_project(project_data)
                        st.success(f"Project created successfully: {project.ProjectID}")
                        st.session_state.show_new_project = False
                    except Exception as e:
                        st.error(f"Error creating project: {str(e)}")
    
    # Project List Section
    st.subheader("Project List")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["New", "Active", "Completed", "On Hold"],
            default=["New", "Active"]
        )
    with col2:
        analyst_filter = st.text_input("Analyst Filter")
    with col3:
        pm_filter = st.text_input("PM Filter")
    
    try:
        projects = project_service.get_all_projects()
        if projects:
            # Apply filters
            filtered_projects = [
                p for p in projects
                if (not status_filter or p.Status in status_filter) and
                   (not analyst_filter or analyst_filter.lower() in p.Analyst.lower()) and
                   (not pm_filter or pm_filter.lower() in p.PM.lower())
            ]
            
            # Convert to DataFrame for display
            df_projects = pd.DataFrame([vars(p) for p in filtered_projects])
            
            # Bulk Actions
            if len(filtered_projects) > 0:
                selected_projects = st.multiselect(
                    "Select Projects for Bulk Actions",
                    df_projects['ProjectID'].tolist()
                )
                
                if selected_projects:
                    action = st.selectbox(
                        "Bulk Action",
                        ["Update Status", "Assign PM", "Assign Analyst"]
                    )
                    
                    if st.button("Apply Bulk Action"):
                        try:
                            if action == "Update Status":
                                new_status = st.selectbox("New Status", 
                                    ["New", "Active", "Completed", "On Hold"])
                                for pid in selected_projects:
                                    project_service.update_project_status(pid, new_status)
                            st.success("Bulk action completed successfully")
                        except Exception as e:
                            st.error(f"Error in bulk operation: {str(e)}")
            
            # Project List
            st.dataframe(
                df_projects,
                column_config={
                    "ProjectID": "Project ID",
                    "ProjectType": "Type",
                    "ProjectDesc": "Description",
                    "Status": "Status",
                    "Analyst": "Analyst",
                    "PM": "Project Manager",
                    "LastEditDate": "Last Updated"
                },
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Error loading projects: {str(e)}")

def display_project_details(project_id: Optional[str] = None):
    if project_id:
        with st.expander(f"Project Details - {project_id}"):
            st.write("Project details would be displayed here") 