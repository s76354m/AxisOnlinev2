import streamlit as st
import pandas as pd
from app.services.competitor_service import CompetitorService

def render_page(db_session):
    st.title("Competitor Management")
    
    competitor_service = CompetitorService(db_session)
    
    tab1, tab2 = st.tabs(["Competitor List", "Add Competitor"])
    
    with tab1:
        render_competitor_list(competitor_service)
    
    with tab2:
        render_add_competitor_form(competitor_service)

def render_competitor_list(competitor_service):
    st.header("Competitor List")
    
    col1, col2 = st.columns(2)
    with col1:
        payor_filter = st.text_input("Filter by Payor")
    with col2:
        product_filter = st.text_input("Filter by Product")
    
    competitors = competitor_service.get_competitors(
        payor_filter=payor_filter,
        product_filter=product_filter
    )
    
    if competitors:
        df = pd.DataFrame(competitors)
        st.dataframe(
            df,
            column_config={
                "ProjectID": "Project ID",
                "StrenuusProductCode": "Strenuus Code",
                "Payor": "Payor",
                "Product": "Product",
                "EI": "EI",
                "CS": "CS",
                "MR": "MR"
            },
            hide_index=True
        )
    else:
        st.info("No competitors found matching the criteria.")

def render_add_competitor_form(competitor_service):
    st.header("Add New Competitor")
    with st.form("add_competitor"):
        strenuus_code = st.text_input("Strenuus Code")
        payor = st.text_input("Payor")
        product = st.text_input("Product")
        ei = st.checkbox("EI")
        cs = st.checkbox("CS")
        mr = st.checkbox("MR")
        
        if st.form_submit_button("Add Competitor"):
            try:
                competitor_service.create_competitor({
                    'strenuus_code': strenuus_code,
                    'payor': payor,
                    'product': product,
                    'ei': ei,
                    'cs': cs,
                    'mr': mr
                })
                st.success("Competitor added successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding competitor: {str(e)}") 