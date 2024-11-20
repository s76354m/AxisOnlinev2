"""CSP LOB Management page"""
import streamlit as st
import pandas as pd
from app.services.csp_lob_service import CSPLOBService
from app.schemas.csp_lob import CSPLOBCreate
import io

def render_page():
    st.title("CSP Line of Business Management")
    csp_lob_service = CSPLOBService()
    
    # Create New Mapping Section
    with st.expander("Create New CSP LOB Mapping", expanded=st.session_state.get('show_new_mapping', False)):
        with st.form("new_mapping_form"):
            csp_code = st.text_input("CSP Code*")
            lob_type = st.selectbox(
                "LOB Type*",
                ["Medical", "Dental", "Vision", "Pharmacy", "Other"]
            )
            description = st.text_area("Description*")
            status = st.selectbox("Status*", ["Active", "Inactive", "Pending"])
            project_id = st.text_input("Project ID*")
            
            submitted = st.form_submit_button("Create Mapping")
            if submitted:
                if not all([csp_code, lob_type, description, status, project_id]):
                    st.error("Please fill in all required fields")
                else:
                    try:
                        mapping_data = CSPLOBCreate(
                            csp_code=csp_code,
                            lob_type=lob_type,
                            description=description,
                            status=status,
                            project_id=project_id
                        )
                        mapping = csp_lob_service.create_csp_lob(mapping_data)
                        st.success(f"Mapping created successfully: {mapping.csp_code}")
                        st.session_state.show_new_mapping = False
                    except Exception as e:
                        st.error(f"Error creating mapping: {str(e)}")
    
    # Import/Export Section
    st.subheader("Data Operations")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Import CSP LOB Mappings (CSV)", type=['csv'])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                for _, row in df.iterrows():
                    mapping_data = CSPLOBCreate(**row.to_dict())
                    csp_lob_service.create_csp_lob(mapping_data)
                st.success("Import completed successfully")
            except Exception as e:
                st.error(f"Import error: {str(e)}")
    
    with col2:
        if st.button("Export Mappings"):
            try:
                mappings = csp_lob_service.get_all_csp_lobs()
                if mappings:
                    df = pd.DataFrame([vars(m) for m in mappings])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        "csp_lob_mappings.csv",
                        "text/csv"
                    )
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    # Mapping List Section
    st.subheader("CSP LOB Mappings")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Active", "Inactive", "Pending"],
            default=["Active"]
        )
    with col2:
        lob_filter = st.multiselect(
            "LOB Type",
            ["Medical", "Dental", "Vision", "Pharmacy", "Other"]
        )
    
    try:
        mappings = csp_lob_service.get_all_csp_lobs()
        if mappings:
            # Apply filters
            filtered_mappings = [
                m for m in mappings
                if (not status_filter or m.status in status_filter) and
                   (not lob_filter or m.lob_type in lob_filter)
            ]
            
            # Convert to DataFrame for display
            df_mappings = pd.DataFrame([vars(m) for m in filtered_mappings])
            
            # Bulk Actions
            if len(filtered_mappings) > 0:
                selected_mappings = st.multiselect(
                    "Select Mappings for Bulk Actions",
                    df_mappings['csp_code'].tolist()
                )
                
                if selected_mappings:
                    action = st.selectbox(
                        "Bulk Action",
                        ["Update Status", "Delete"]
                    )
                    
                    if st.button("Apply Bulk Action"):
                        try:
                            if action == "Update Status":
                                new_status = st.selectbox(
                                    "New Status",
                                    ["Active", "Inactive", "Pending"]
                                )
                                for code in selected_mappings:
                                    csp_lob_service.update_csp_lob_status(code, new_status)
                            elif action == "Delete":
                                for code in selected_mappings:
                                    csp_lob_service.delete_csp_lob(code)
                            st.success("Bulk action completed successfully")
                        except Exception as e:
                            st.error(f"Error in bulk operation: {str(e)}")
            
            # Display mappings
            st.dataframe(
                df_mappings,
                column_config={
                    "csp_code": "CSP Code",
                    "lob_type": "LOB Type",
                    "description": "Description",
                    "status": "Status",
                    "project_id": "Project ID"
                },
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Error loading mappings: {str(e)}")