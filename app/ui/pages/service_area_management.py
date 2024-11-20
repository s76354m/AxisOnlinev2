"""Service area management page"""
import streamlit as st
import pandas as pd
from app.db.session import get_db

def render_page():
    """Render service area management page"""
    st.title("Service Area Management")
    
    # Add new service area button
    if st.button("+ New Service Area"):
        st.session_state.current_view = "new_service_area"
        st.rerun()
    
    # Service Area List/Grid Toggle
    view_type = st.radio("View", ["List", "Grid"], horizontal=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"]
        )
    with col2:
        search = st.text_input("Search", placeholder="Search service areas...")
    
    try:
        db = next(get_db())
        # Query to get service areas
        query = """
        SELECT 
            ServiceAreaID,
            ServiceAreaName,
            Status,
            LastEditDate
        FROM CS_EXP_ServiceAreas WITH (NOLOCK)
        WHERE 1=1
        """
        
        params = []
        if status_filter != "All":
            query += " AND Status = ?"
            params.append(status_filter)
        if search:
            query += " AND ServiceAreaName LIKE ?"
            params.append(f"%{search}%")
            
        query += " ORDER BY LastEditDate DESC"
        
        df = pd.read_sql(query, db.bind, params=params)
        
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "ServiceAreaID": "ID",
                    "ServiceAreaName": "Name",
                    "Status": "Status",
                    "LastEditDate": "Last Updated"
                },
                hide_index=True
            )
        else:
            st.info("No service areas found matching the criteria.")
            
    except Exception as e:
        st.error(f"Error loading service areas: {str(e)}")
    finally:
        db.close() 