import streamlit as st
import pandas as pd
from app.services.csp_lob_service import CSPLOBService

def render_page(db_session):
    st.title("CSP LOB Management")
    
    csp_service = CSPLOBService(db_session)
    
    tab1, tab2 = st.tabs(["CSP LOB List", "Add CSP LOB"])
    
    with tab1:
        render_csp_list(csp_service)
    
    with tab2:
        render_add_csp_form(csp_service)

def render_csp_list(csp_service):
    st.header("CSP LOB List")
    
    csps = csp_service.get_all_csps()
    
    if csps:
        df = pd.DataFrame(csps)
        st.dataframe(
            df,
            column_config={
                "CSPCode": "CSP Code",
                "LOBCode": "LOB Code",
                "Description": "Description",
                "Status": "Status"
            },
            hide_index=True
        )
    else:
        st.info("No CSP LOBs found.")

def render_add_csp_form(csp_service):
    st.header("Add New CSP LOB")
    with st.form("add_csp"):
        csp_code = st.text_input("CSP Code")
        lob_code = st.text_input("LOB Code")
        description = st.text_area("Description")
        status = st.selectbox("Status", ["Active", "Inactive"])
        
        if st.form_submit_button("Add CSP LOB"):
            try:
                csp_service.create_csp({
                    'csp_code': csp_code,
                    'lob_code': lob_code,
                    'description': description,
                    'status': status
                })
                st.success("CSP LOB added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding CSP LOB: {str(e)}") 