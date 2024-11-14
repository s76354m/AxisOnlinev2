import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from typing import Dict, List, Optional
from app.frontend.components.project_management import ProjectManagement
from app.frontend.components.competitor_management import CompetitorManagement
from app.frontend.components.service_area_management import ServiceAreaManagement
from app.frontend.components.notes_management import NotesManagement

class Dashboard:
    def __init__(self):
        st.set_page_config(
            page_title="Axis Program Management",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize session state
        if 'user' not in st.session_state:
            st.session_state.user = self.get_current_user()
        if 'active_page' not in st.session_state:
            st.session_state.active_page = 'Dashboard'

    @staticmethod
    def get_current_user() -> Dict:
        import getpass
        return {
            'username': getpass.getuser(),
            'role': 'admin'  # This should be fetched from your authentication system
        }

    def sidebar(self):
        with st.sidebar:
            st.title("Axis Program Management")
            st.write(f"Welcome, {st.session_state.user['username']}")
            
            # Navigation
            st.subheader("Navigation")
            pages = [
                "Dashboard",
                "Projects",
                "Competitors",
                "Service Areas",
                "Notes"
            ]
            st.session_state.active_page = st.radio("Go to", pages)
            
            # Quick Actions
            st.subheader("Quick Actions")
            if st.button("➕ New Project"):
                st.session_state.active_page = "New Project"
            
            # User Info
            st.sidebar.markdown("---")
            st.sidebar.info(
                f"Logged in as: {st.session_state.user['username']}\n\n"
                f"Role: {st.session_state.user['role']}"
            )

    def render_dashboard(self):
        st.title("Dashboard")
        
        # Create three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Active Projects",
                value=self.get_active_projects_count(),
                delta="2 from last month"
            )
        
        with col2:
            st.metric(
                label="Pending Reviews",
                value=self.get_pending_reviews_count(),
                delta="-1 from last month"
            )
        
        with col3:
            st.metric(
                label="Completed This Month",
                value=self.get_completed_projects_count(),
                delta="5 from last month"
            )
        
        # Recent Projects
        st.subheader("Recent Projects")
        self.show_recent_projects()
        
        # Project Status Overview
        st.subheader("Project Status Overview")
        self.show_project_status_chart()

    def get_active_projects_count(self) -> int:
        # TODO: Implement API call
        return 15

    def get_pending_reviews_count(self) -> int:
        # TODO: Implement API call
        return 5

    def get_completed_projects_count(self) -> int:
        # TODO: Implement API call
        return 8

    def show_recent_projects(self):
        # TODO: Replace with actual API call
        recent_projects = pd.DataFrame({
            'ProjectID': ['PRJ001', 'PRJ002', 'PRJ003'],
            'Description': ['Project 1', 'Project 2', 'Project 3'],
            'Status': ['Active', 'On Hold', 'Active'],
            'LastUpdated': ['2024-02-20', '2024-02-19', '2024-02-18']
        })
        st.dataframe(recent_projects, use_container_width=True)

    def show_project_status_chart(self):
        # TODO: Replace with actual data
        import plotly.express as px
        
        data = pd.DataFrame({
            'Status': ['Active', 'On Hold', 'Completed', 'Cancelled'],
            'Count': [10, 5, 8, 2]
        })
        
        fig = px.pie(data, values='Count', names='Status', title='Project Status Distribution')
        st.plotly_chart(fig, use_container_width=True)

    def run(self):
        self.sidebar()
        
        # Navigation routing
        if st.session_state.active_page == "Dashboard":
            self.render_dashboard()
        elif st.session_state.active_page == "Projects":
            ProjectManagement().render()
        elif st.session_state.active_page == "New Project":
            ProjectManagement().render_new_project()
        elif st.session_state.active_page == "Competitors":
            st.title("Competitors")
            st.info("Competitor management coming soon...")
        elif st.session_state.active_page == "Service Areas":
            st.title("Service Areas")
            st.info("Service area management coming soon...")
        elif st.session_state.active_page == "Notes":
            st.title("Notes")
            st.info("Notes management coming soon...") 