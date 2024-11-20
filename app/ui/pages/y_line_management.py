import streamlit as st
import pandas as pd
from app.services.y_line_service import YLineService
from app.models.y_line import YLineStatus
from app.schemas.y_line import YLineCreate

def render_page(db_session):
    st.title("Y-Line Management")
    
    y_line_service = YLineService(db_session)
    
    tab1, tab2 = st.tabs(["Y-Line Items", "Create New"])
    
    with tab1:
        render_y_line_list(y_line_service)
    
    with tab2:
        render_add_y_line_form(y_line_service)

def render_y_line_list(y_line_service):
    st.header("Y-Line List")
    
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All"] + [status.value for status in YLineStatus],
            index=0
        )
    with col2:
        product_filter = st.text_input("Product Code")
    
    y_lines = y_line_service.get_y_lines(
        status=status_filter if status_filter != "All" else None,
        product_code=product_filter
    )
    
    if y_lines:
        df = pd.DataFrame([{
            "IPA Number": y.IPA_Number,
            "Product Code": y.ProductCode,
            "Description": y.Description,
            "Pre-Award Status": y.PreAwardStatus,
            "Post-Award Status": y.PostAwardStatus,
            "Status": y.Status.value,
            "Estimated Value": y.EstimatedValue,
            "Last Updated": y.LastEditDate
        } for y in y_lines])
        
        st.dataframe(df, hide_index=True)
    else:
        st.info("No Y-Line items found matching the criteria.")

def render_add_y_line_form(y_line_service):
    st.header("Add New Y-Line Item")
    with st.form("new_yline_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            ipa_number = st.text_input("IPA Number")
            product_code = st.text_input("Product Code")
            status = st.selectbox(
                "Status",
                [status.value for status in YLineStatus]
            )
        
        with col2:
            pre_award_status = st.text_input("Pre-Award Status")
            post_award_status = st.text_input("Post-Award Status")
            estimated_value = st.number_input("Estimated Value", min_value=0.0)
        
        description = st.text_area("Description")
        
        if st.form_submit_button("Create Y-Line Item"):
            try:
                y_line_service.create_y_line(YLineCreate(
                    ipa_number=ipa_number,
                    product_code=product_code,
                    description=description,
                    pre_award_status=pre_award_status,
                    post_award_status=post_award_status,
                    estimated_value=estimated_value,
                    status=status
                ))
                st.success("Y-Line item created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating Y-Line item: {str(e)}") 