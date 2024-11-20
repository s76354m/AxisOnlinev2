"""Competitor management page"""
import streamlit as st
import pandas as pd
from app.db.session import get_db

def render_page():
    """Render competitor management page"""
    st.title("Competitor Management")
    
    # Add new competitor button
    if st.button("+ New Competitor"):
        st.session_state.current_view = "new_competitor"
        st.rerun()
    
    # Competitor List/Grid Toggle
    view_type = st.radio("View", ["List", "Grid"], horizontal=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"]
        )
    with col2:
        search = st.text_input("Search", placeholder="Search competitors...")
    
    try:
        db = next(get_db())
        # Query to get competitors
        query = """
        SELECT 
            CompetitorID,
            CompetitorName,
            Status,
            LastEditDate
        FROM CS_EXP_Competitors WITH (NOLOCK)
        WHERE 1=1
        """
        
        params = []
        if status_filter != "All":
            query += " AND Status = ?"
            params.append(status_filter)
        if search:
            query += " AND CompetitorName LIKE ?"
            params.append(f"%{search}%")
            
        query += " ORDER BY LastEditDate DESC"
        
        df = pd.read_sql(query, db.bind, params=params)
        
        if not df.empty:
            st.dataframe(
                df,
                column_config={
                    "CompetitorID": "ID",
                    "CompetitorName": "Name",
                    "Status": "Status",
                    "LastEditDate": "Last Updated"
                },
                hide_index=True
            )
        else:
            st.info("No competitors found matching the criteria.")
            
    except Exception as e:
        st.error(f"Error loading competitors: {str(e)}")
    finally:
        db.close() 