"""Dashboard component"""
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def display_dashboard():
    """Display main dashboard"""
    st.header("Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Projects", "12", "+2")
    with col2:
        st.metric("Pending Reviews", "5", "-1")
    with col3:
        st.metric("Completed This Month", "8", "+3")
    with col4:
        st.metric("On Hold", "3", "0")
    
    # Recent Activity
    st.subheader("Recent Activity")
    st.dataframe({
        "Date": ["2024-01-01", "2024-01-02"],
        "Activity": ["Project Created", "Status Updated"],
        "Project": ["PROJ001", "PROJ002"],
        "User": ["John Doe", "Jane Smith"]
    }) 