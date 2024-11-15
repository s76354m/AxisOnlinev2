"""Y-Line management page"""
import streamlit as st
import pandas as pd
from app.db.session import get_db

def render_page():
    """Render Y-Line management page"""
    st.title("Y-Line Management")
    
    # Add new Y-Line button
    if st.button("+ New Y-Line"):
        st.session_state.current_view = "new_y_line"
        st.rerun()
    
    # Y-Line List/Grid Toggle
    view_type = st.radio("View", ["List", "Grid"], horizontal=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Pre-Award", "Post-Award", "Completed"]
        )
    with col2:
        type_filter = st.selectbox(
            "Type",
            ["All", "Type 1", "Type 2", "Type 3"]
        )
    with col3:
        search = st.text_input("Search", placeholder="Search Y-Lines...")
    
    try:
        db = next(get_db())
        # Query to get Y-Lines
        query = """
        SELECT 
            YLineID,
            YLineName,
            Status,
            Type,
            LastEditDate
        FROM CS_EXP_YLines WITH (NOLOCK)
        WHERE 1=1
        """
        
        params = []
        if status_filter != "All":
            query += " AND Status = ?"
            params.append(status_filter)
        if type_filter != "All":
            query += " AND Type = ?"
            params.append(type_filter)
        if search:
            query += " AND YLineName LIKE ?"
            params.append(f"%{search}%")
            
        query += " ORDER BY LastEditDate DESC"
        
        df = pd.read_sql(query, db.bind, params=params)
        
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "YLineID": "ID",
                    "YLineName": "Name",
                    "Status": "Status",
                    "Type": "Type",
                    "LastEditDate": "Last Updated"
                },
                hide_index=True
            )
        else:
            st.info("No Y-Lines found matching the criteria.")
            
    except Exception as e:
        st.error(f"Error loading Y-Lines: {str(e)}")
    finally:
        db.close() 