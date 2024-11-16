import streamlit as st
import pandas as pd
from app.db.session import get_db
from datetime import datetime
import getpass
from sqlalchemy.exc import SQLAlchemyError
from app.utils.db_monitor import DatabaseMonitor

db_monitor = DatabaseMonitor()

def display_project_info(project_id):
    """Display project information"""
    try:
        db = next(get_db())
        try:
            query = """
            SELECT * FROM CS_EXP_Project_Translation 
            WHERE ProjectID = ?
            """
            df = pd.read_sql(query, db.bind, params=[project_id])
            
            if df.empty:
                st.warning(f"No project found with ID: {project_id}")
                return
            
            project = df.iloc[0]
            
            # Display project info in columns
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Project ID", value=project['ProjectID'], disabled=True)
                st.text_input("Project Type", value=project['ProjectType'], disabled=True)
                st.text_area("Description", value=project['ProjectDesc'], key=f"desc_{project_id}")
            
            with col2:
                st.text_input("Analyst", value=project['Analyst'], key=f"analyst_{project_id}")
                st.text_input("Project Manager", value=project['PM'], key=f"pm_{project_id}")
                status_index = ['New', 'Active', 'On Hold', 'Completed'].index(project['Status'])
                st.selectbox("Status", 
                    options=['New', 'Active', 'On Hold', 'Completed'],
                    index=status_index,
                    key=f"status_{project_id}"
                )
            
            if st.button("Update Project", key=f"update_{project_id}"):
                try:
                    update_project(project_id, {
                        'ProjectDesc': st.session_state[f"desc_{project_id}"],
                        'Analyst': st.session_state[f"analyst_{project_id}"],
                        'PM': st.session_state[f"pm_{project_id}"],
                        'Status': st.session_state[f"status_{project_id}"],
                        'LastEditDate': datetime.now(),
                        'LastEditMSID': getpass.getuser()
                    })
                    st.success("Project updated successfully!")
                    db_monitor.log_operation('project_update', 'success', f"Project ID: {project_id}")
                except SQLAlchemyError as e:
                    db_monitor.log_error('project_update', e)
                    st.error(f"Database error while updating project: {str(e)}")
                except Exception as e:
                    st.error(f"Error updating project: {str(e)}")
        
        except SQLAlchemyError as e:
            db_monitor.log_error('project_query', e)
            st.error(f"Database error while loading project: {str(e)}")
            
    except Exception as e:
        st.error(f"Error establishing database connection: {str(e)}")
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