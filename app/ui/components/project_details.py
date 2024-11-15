import streamlit as st
import pandas as pd
from app.db.session import get_db
from datetime import datetime
import getpass

def display_project_info(project_id):
    """Display project information"""
    db = next(get_db())
    try:
        query = """
        SELECT * FROM CS_EXP_Project_Translation 
        WHERE ProjectID = ?
        """
        df = pd.read_sql(query, db.bind, params=[project_id])
        
        if not df.empty:
            project = df.iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Project ID", value=project['ProjectID'], disabled=True)
                st.text_input("Project Type", value=project['ProjectType'], disabled=True)
                st.text_area("Description", value=project['ProjectDesc'])
            
            with col2:
                st.text_input("Analyst", value=project['Analyst'])
                st.text_input("Project Manager", value=project['PM'])
                st.selectbox("Status", 
                    options=['New', 'Active', 'On Hold', 'Completed'],
                    index=['New', 'Active', 'On Hold', 'Completed'].index(project['Status'])
                )
            
            if st.button("Update Project"):
                update_project(project_id, {
                    'ProjectDesc': project['ProjectDesc'],
                    'Analyst': project['Analyst'],
                    'PM': project['PM'],
                    'Status': project['Status'],
                    'LastEditDate': datetime.now(),
                    'LastEditMSID': getpass.getuser()
                })
                st.success("Project updated successfully!")
                
    except Exception as e:
        st.error(f"Error loading project details: {str(e)}")
    finally:
        db.close()

def display_competitors(project_id):
    """Display and manage competitors"""
    st.subheader("Competitors")
    
    # Add new competitor
    with st.expander("Add New Competitor"):
        with st.form("new_competitor"):
            strenuus_code = st.text_input("Strenuus Code")
            payor = st.text_input("Payor")
            product = st.text_input("Product")
            ei = st.checkbox("EI")
            cs = st.checkbox("CS")
            mr = st.checkbox("MR")
            
            if st.form_submit_button("Add Competitor"):
                add_competitor({
                    'project_id': project_id,
                    'strenuus_code': strenuus_code,
                    'payor': payor,
                    'product': product,
                    'ei': ei,
                    'cs': cs,
                    'mr': mr
                })
                st.success("Competitor added successfully!")
                st.rerun()
    
    # Display existing competitors
    competitors = get_competitors(project_id)
    if competitors is not None and not competitors.empty:
        st.dataframe(competitors)

def display_service_areas(project_id):
    """Display and manage service areas"""
    st.subheader("Service Areas")
    
    # Add new service area
    with st.expander("Add New Service Area"):
        with st.form("new_service_area"):
            region = st.text_input("Region")
            state = st.text_input("State")
            county = st.text_input("County")
            max_mileage = st.number_input("Max Mileage", min_value=0)
            
            if st.form_submit_button("Add Service Area"):
                add_service_area({
                    'project_id': project_id,
                    'region': region,
                    'state': state,
                    'county': county,
                    'max_mileage': max_mileage
                })
                st.success("Service Area added successfully!")
                st.rerun()
    
    # Display existing service areas
    service_areas = get_service_areas(project_id)
    if service_areas is not None and not service_areas.empty:
        st.dataframe(service_areas)

def display_notes(project_id):
    """Display and manage project notes"""
    st.subheader("Project Notes")
    
    # Add new note
    with st.expander("Add New Note"):
        with st.form("new_note"):
            note = st.text_area("Note")
            action_item = st.checkbox("Action Item")
            category = st.text_input("Category")
            
            if st.form_submit_button("Add Note"):
                add_note({
                    'project_id': project_id,
                    'note': note,
                    'action_item': action_item,
                    'category': category
                })
                st.success("Note added successfully!")
                st.rerun()
    
    # Display existing notes
    notes = get_notes(project_id)
    if notes is not None and not notes.empty:
        for _, note in notes.iterrows():
            with st.expander(f"Note from {note['OrigNoteMSID']} - {note['DataLoadDate']}"):
                st.write(note['Notes'])
                st.write(f"Category: {note['ProjectCategory']}")
                st.write(f"Action Item: {'Yes' if note['ActionItem'] == 'Y' else 'No'}") 