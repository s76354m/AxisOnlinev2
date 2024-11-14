import streamlit as st
import requests
from datetime import datetime

class ProjectStatusTracker:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def display_status_history(self, project_id: str):
        response = requests.get(f"{self.api_url}/projects/{project_id}/status")
        if response.status_code == 200:
            statuses = response.json()
            st.subheader("Status History")
            
            for status in statuses:
                with st.expander(f"Status: {status['Status']} - {status['StatusDate']}"):
                    st.write(f"Updated by: {status['UpdatedBy']}")
                    st.write(f"Comments: {status['Comments']}")

    def update_status(self, project_id: str):
        with st.form("update_status"):
            status = st.selectbox(
                "New Status",
                options=['In Progress', 'On Hold', 'Completed', 'Cancelled']
            )
            comments = st.text_area("Comments")
            
            if st.form_submit_button("Update Status"):
                response = requests.post(
                    f"{self.api_url}/projects/{project_id}/status",
                    json={
                        "Status": status,
                        "Comments": comments,
                        "UpdatedBy": st.session_state.get('username', 'Unknown')
                    }
                )
                
                if response.status_code == 200:
                    st.success("Status updated successfully!")
                else:
                    st.error("Failed to update status") 