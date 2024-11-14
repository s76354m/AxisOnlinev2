import streamlit as st
import requests
import pandas as pd
from typing import Dict, List, Optional
from app.core.error_handler import UIErrorHandler, handle_exceptions
from app.core.logging_config import logger

# Configuration
API_URL = "http://localhost:8000/api/v1"

class AxisProgramUI:
    def __init__(self):
        try:
            st.set_page_config(
                page_title="Axis Program Management",
                page_icon="📊",
                layout="wide"
            )
            
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 'Projects'
                
            logger.info("AxisProgramUI initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AxisProgramUI: {str(e)}")
            raise

    def sidebar(self):
        with st.sidebar:
            st.title("Axis Program Management")
            selected = st.radio(
                "Navigate to",
                ['Projects', 'Competitors', 'Service Areas']
            )
            st.session_state.current_page = selected

    @handle_exceptions
    def fetch_projects(self) -> List[Dict]:
        logger.info("Fetching projects from API")
        try:
            response = requests.get(f"{API_URL}/projects/")
            if response.status_code == 200:
                projects = response.json()
                logger.info(f"Successfully fetched {len(projects)} projects")
                return projects
            else:
                error_message = response.json().get('detail', 'Unknown error')
                logger.error(f"Error fetching projects: {error_message}")
                st.error(f"Failed to fetch projects: {error_message}")
                return []
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            st.error("Failed to connect to the API")
            return []

    def display_projects(self):
        st.title("Project Management")
        
        # Create new project button
        if st.button("Create New Project"):
            st.session_state.current_page = 'New Project'
            
        # Fetch and display projects
        projects = self.fetch_projects()
        if projects:
            df = pd.DataFrame(projects)
            st.dataframe(
                df[['ProjectID', 'ProjectType', 'ProjectDesc', 'Analyst', 'PM', 'IsActive']],
                use_container_width=True
            )
            
            # Select project for editing
            selected_project = st.selectbox(
                "Select Project to Edit",
                options=[p['ProjectID'] for p in projects]
            )
            
            if selected_project:
                self.edit_project(next(p for p in projects if p['ProjectID'] == selected_project))

    @handle_exceptions
    def edit_project(self, project: Dict):
        logger.info(f"Editing project: {project['ProjectID']}")
        st.subheader(f"Edit Project: {project['ProjectID']}")
        
        with st.form("edit_project"):
            project_desc = st.text_input("Project Description", project['ProjectDesc'])
            project_type = st.selectbox(
                "Project Type",
                options=['A', 'B', 'C'],
                index=['A', 'B', 'C'].index(project['ProjectType'])
            )
            analyst = st.text_input("Analyst", project['Analyst'])
            pm = st.text_input("Project Manager", project['PM'])
            is_active = st.checkbox("Active", project['IsActive'])
            
            if st.form_submit_button("Update Project"):
                logger.info(f"Attempting to update project: {project['ProjectID']}")
                try:
                    response = requests.put(
                        f"{API_URL}/projects/{project['RecordID']}",
                        json={
                            "ProjectDesc": project_desc,
                            "ProjectType": project_type,
                            "Analyst": analyst,
                            "PM": pm,
                            "IsActive": is_active
                        }
                    )
                    UIErrorHandler.api_error_handler(
                        response,
                        f"Project {project['ProjectID']} updated successfully!"
                    )
                except requests.RequestException as e:
                    logger.error(f"Failed to update project: {str(e)}")
                    st.error("Failed to connect to the API")

    @handle_exceptions
    def display_project_details(self, project: Dict):
        logger.info(f"Displaying details for project: {project['ProjectID']}")
        st.subheader(f"Project Details: {project['ProjectID']}")
        
        tabs = st.tabs(["Details", "Status", "Documents"])
        
        with tabs[0]:
            self.edit_project(project)
        
        with tabs[1]:
            try:
                status_tracker = ProjectStatusTracker(API_URL)
                status_tracker.display_status_history(project['ProjectID'])
                status_tracker.update_status(project['ProjectID'])
            except Exception as e:
                logger.error(f"Error displaying status tracker: {str(e)}")
                st.error("Failed to load status information")
        
        with tabs[2]:
            st.info("Document management coming soon...")

    def run(self):
        try:
            logger.info("Starting AxisProgramUI")
            self.sidebar()
            
            if st.session_state.current_page == 'Projects':
                self.display_projects()
            # Add other pages as needed
            
        except Exception as e:
            logger.error(f"Critical error in AxisProgramUI: {str(e)}")
            st.error("An unexpected error occurred. Please contact support.")

if __name__ == "__main__":
    app = AxisProgramUI()
    app.run() 