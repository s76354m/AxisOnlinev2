import streamlit as st
from app.frontend.dashboard import Dashboard
from datetime import datetime
import time
from app.db.session import get_db
from app.models import Project, Competitor, ServiceArea, ProjectNote
import getpass

def create_project_in_db(project_data):
    """Create project in database"""
    db = next(get_db())
    try:
        project = Project(
            ProjectID=project_data['project_id'],
            ProjectType=project_data['project_type'],
            ProjectDesc=project_data['description'],
            Analyst=project_data['analyst'],
            PM=project_data['pm'],
            Status='New',
            DataLoadDate=datetime.now(),
            LastEditDate=datetime.now(),
            LastEditMSID=getpass.getuser()
        )
        db.add(project)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def add_competitor_to_db(competitor_data):
    """Add competitor to database"""
    db = next(get_db())
    try:
        competitor = Competitor(
            ProjectID=competitor_data['project_id'],
            StrenuusProductCode=competitor_data['strenuus_code'],
            Payor=competitor_data['payor'],
            Product=competitor_data['product'],
            ProjectStatus='New',
            DataLoadDate=datetime.now(),
            LastEditMSID=getpass.getuser()
        )
        db.add(competitor)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def add_service_area_to_db(service_area_data):
    """Add service area to database"""
    db = next(get_db())
    try:
        service_area = ServiceArea(
            ProjectID=service_area_data['project_id'],
            Region=service_area_data['region'],
            State=service_area_data['state'],
            County=service_area_data['county'],
            MaxMileage=service_area_data['max_mileage'],
            ReportInclude='Y',
            ProjectStatus='New',
            DataLoadDate=datetime.now()
        )
        db.add(service_area)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def add_note_to_db(note_data):
    """Add note to database"""
    db = next(get_db())
    try:
        note = ProjectNote(
            ProjectID=note_data['project_id'],
            Notes=note_data['note'],
            ActionItem='Y' if note_data['action_item'] else 'N',
            ProjectCategory=note_data['category'],
            ProjectStatus='New',
            DataLoadDate=datetime.now(),
            LastEditDate=datetime.now(),
            OrigNoteMSID=getpass.getuser(),
            LastEditMSID=getpass.getuser()
        )
        db.add(note)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def test_project_workflow():
    """Manual test script for project workflow"""
    st.title("Project Management Test Script")
    
    # Initialize session state
    if 'test_stage' not in st.session_state:
        st.session_state.test_stage = 'project'
    if 'project_id' not in st.session_state:
        st.session_state.project_id = None

    # Test 1: Create New Project
    if st.session_state.test_stage == 'project':
        st.header("Test 1: Create New Project")
        with st.form("test_project"):
            project_id = st.text_input("Project ID", value="TEST001")
            project_type = st.selectbox("Project Type", ['A', 'B', 'C'])
            description = st.text_area("Description", value="Test Project Description")
            analyst = st.text_input("Analyst", value="Test Analyst")
            pm = st.text_input("Project Manager", value="Test PM")
            
            submit = st.form_submit_button("Create Project")
            if submit:
                try:
                    # Create project in database
                    create_project_in_db({
                        'project_id': project_id,
                        'project_type': project_type,
                        'description': description,
                        'analyst': analyst,
                        'pm': pm
                    })
                    
                    st.session_state.project_id = project_id
                    st.session_state.test_stage = 'competitor'
                    st.success("Project created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating project: {str(e)}")

    # Test 2: Add Competitor
    elif st.session_state.test_stage == 'competitor':
        st.header("Test 2: Add Competitor")
        with st.form("test_competitor"):
            strenuus_code = st.text_input("Strenuus Code", value="TEST")
            payor = st.text_input("Payor", value="Test Payor")
            product = st.text_input("Product", value="Test Product")
            
            submit_competitor = st.form_submit_button("Add Competitor")
            if submit_competitor:
                try:
                    # Add competitor to database
                    add_competitor_to_db({
                        'project_id': st.session_state.project_id,
                        'strenuus_code': strenuus_code,
                        'payor': payor,
                        'product': product
                    })
                    
                    st.success("Competitor added successfully!")
                    st.session_state.test_stage = 'service_area'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding competitor: {str(e)}")

    # Test 3: Add Service Area
    elif st.session_state.test_stage == 'service_area':
        st.header("Test 3: Add Service Area")
        with st.form("test_service_area"):
            region = st.text_input("Region", value="Test Region")
            state = st.text_input("State", value="TX")
            county = st.text_input("County", value="Test County")
            max_mileage = st.number_input("Max Mileage", value=50)
            
            submit_area = st.form_submit_button("Add Service Area")
            if submit_area:
                try:
                    # Add service area to database
                    add_service_area_to_db({
                        'project_id': st.session_state.project_id,
                        'region': region,
                        'state': state,
                        'county': county,
                        'max_mileage': max_mileage
                    })
                    
                    st.success("Service Area added successfully!")
                    st.session_state.test_stage = 'note'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding service area: {str(e)}")

    # Test 4: Add Note
    elif st.session_state.test_stage == 'note':
        st.header("Test 4: Add Note")
        with st.form("test_note"):
            note = st.text_area("Note", value="Test Note")
            action_item = st.checkbox("Action Item")
            category = st.text_input("Category", value="Test Category")
            
            submit_note = st.form_submit_button("Add Note")
            if submit_note:
                try:
                    # Add note to database
                    add_note_to_db({
                        'project_id': st.session_state.project_id,
                        'note': note,
                        'action_item': action_item,
                        'category': category
                    })
                    
                    st.success("Note added successfully!")
                    st.session_state.test_stage = 'complete'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding note: {str(e)}")

    # Test Complete
    elif st.session_state.test_stage == 'complete':
        st.header("Test Complete")
        st.success("All tests completed successfully!")
        
        if st.button("Reset Tests"):
            st.session_state.test_stage = 'project'
            st.session_state.project_id = None
            st.rerun()

    # Show current test progress
    progress_container = st.sidebar.container()
    with progress_container:
        st.write("Test Progress:")
        stages = ['project', 'competitor', 'service_area', 'note', 'complete']
        current_stage_index = stages.index(st.session_state.test_stage)
        progress = (current_stage_index + 1) / len(stages)
        st.progress(progress)
        
        st.write(f"Current Stage: {st.session_state.test_stage}")
        if st.session_state.project_id:
            st.write(f"Project ID: {st.session_state.project_id}")

if __name__ == "__main__":
    test_project_workflow() 