import streamlit as st
from datetime import datetime
from typing import Optional
from app.services.csp_lob_service import CSPLOBService
from app.models.csp_lob import LOBType, CSPStatus
from app.schemas.csp_lob import CSPLOBCreate, CSPLOBUpdate

def render_csp_lob_page(db_session):
    st.title("CSP Line of Business Management")
    
    # Initialize service
    csp_service = CSPLOBService(db_session)
    
    # Sidebar for filtering and actions
    with st.sidebar:
        st.subheader("Actions")
        action = st.radio(
            "Select Action",
            ["View/Edit Mappings", "Create New Mapping", "Bulk Operations"]
        )
        
        # Filters
        st.subheader("Filters")
        selected_lob = st.selectbox(
            "LOB Type",
            [None] + list(LOBType),
            format_func=lambda x: "All" if x is None else x.value
        )
        
        selected_status = st.selectbox(
            "Status",
            [None] + list(CSPStatus),
            format_func=lambda x: "All" if x is None else x.value
        )

    # Main content area
    if action == "Create New Mapping":
        render_create_form(csp_service)
    elif action == "View/Edit Mappings":
        render_mapping_list(csp_service, selected_lob, selected_status)
    else:
        render_bulk_operations(csp_service)

def render_create_form(csp_service):
    st.subheader("Create New CSP LOB Mapping")
    
    with st.form("create_csp_lob"):
        project_id = st.number_input("Project ID", min_value=1, step=1)
        csp_code = st.text_input("CSP Code")
        lob_type = st.selectbox("LOB Type", list(LOBType))
        description = st.text_area("Description")
        status = st.selectbox("Status", list(CSPStatus))
        
        col1, col2 = st.columns(2)
        with col1:
            effective_date = st.date_input("Effective Date")
        with col2:
            termination_date = st.date_input("Termination Date")
            
        submit = st.form_submit_button("Create Mapping")
        
        if submit:
            try:
                data = CSPLOBCreate(
                    project_id=project_id,
                    csp_code=csp_code,
                    lob_type=lob_type,
                    description=description,
                    status=status,
                    effective_date=datetime.combine(effective_date, datetime.min.time()),
                    termination_date=datetime.combine(termination_date, datetime.min.time())
                )
                csp_service.create_csp_lob(data)
                st.success("CSP LOB Mapping created successfully!")
            except Exception as e:
                st.error(f"Error creating mapping: {str(e)}")

def render_mapping_list(csp_service, lob_type: Optional[LOBType], status: Optional[CSPStatus]):
    st.subheader("CSP LOB Mappings")
    
    # Get mappings with filters
    mappings = csp_service.get_project_csp_lobs(
        project_id=st.session_state.get('current_project_id'),
        lob_type=lob_type,
        status=status
    )
    
    # Display mappings in a dataframe
    if mappings:
        mapping_data = [{
            'ID': m.id,
            'CSP Code': m.csp_code,
            'LOB Type': m.lob_type.value,
            'Status': m.status.value,
            'Effective Date': m.effective_date.date(),
            'Termination Date': m.termination_date.date() if m.termination_date else None
        } for m in mappings]
        
        df = pd.DataFrame(mapping_data)
        st.dataframe(df)
        
        # Edit selected mapping
        if st.button("Edit Selected"):
            selected_rows = df.index[df['Selected']].tolist()
            if selected_rows:
                render_edit_form(csp_service, mappings[selected_rows[0]])
    else:
        st.info("No mappings found with the selected filters.")

def render_bulk_operations(csp_service):
    st.subheader("Bulk Operations")
    
    operation = st.selectbox(
        "Select Operation",
        ["Bulk Status Update", "Bulk Delete", "Bulk Import"]
    )
    
    if operation == "Bulk Status Update":
        new_status = st.selectbox("New Status", list(CSPStatus))
        if st.button("Update Selected"):
            # Implementation for bulk status update
            pass
            
    elif operation == "Bulk Import":
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        if uploaded_file is not None:
            # Implementation for bulk import
            pass 