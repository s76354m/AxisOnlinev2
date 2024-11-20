import streamlit as st
import pandas as pd
from app.services.service_area_service import ServiceAreaService

def render_page(db_session):
    st.title("Service Area Management")
    
    service_area_service = ServiceAreaService(db_session)
    
    tab1, tab2 = st.tabs(["Service Areas", "Add Service Area"])
    
    with tab1:
        render_service_area_list(service_area_service)
    
    with tab2:
        render_add_service_area_form(service_area_service)

def render_service_area_list(service_area_service):
    st.header("Service Areas")
    
    col1, col2 = st.columns(2)
    with col1:
        state_filter = st.text_input("Filter by State")
    with col2:
        region_filter = st.text_input("Filter by Region")
    
    service_areas = service_area_service.get_service_areas(
        state_filter=state_filter,
        region_filter=region_filter
    )
    
    if service_areas:
        df = pd.DataFrame(service_areas)
        st.dataframe(
            df,
            column_config={
                "ProjectID": "Project ID",
                "Region": "Region",
                "State": "State",
                "County": "County",
                "MaxMileage": "Max Mileage"
            },
            hide_index=True
        )
    else:
        st.info("No service areas found matching the criteria.")

def render_add_service_area_form(service_area_service):
    st.header("Add New Service Area")
    with st.form("add_service_area"):
        region = st.text_input("Region")
        state = st.text_input("State")
        county = st.text_input("County")
        max_mileage = st.number_input("Max Mileage", min_value=0)
        
        if st.form_submit_button("Add Service Area"):
            try:
                service_area_service.create_service_area({
                    'region': region,
                    'state': state,
                    'county': county,
                    'max_mileage': max_mileage
                })
                st.success("Service Area added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding service area: {str(e)}") 