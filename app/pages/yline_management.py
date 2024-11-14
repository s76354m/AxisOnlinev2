"""Y-Line Management UI"""
import streamlit as st
import pandas as pd
from datetime import datetime
from app.models.yline import YLineItem, YLineManager
from app.utils.db_monitor import monitor_db_operation

@monitor_db_operation("yline_management")
def render_yline_management():
    """Render Y-Line management interface"""
    st.title("Y-Line Management")
    
    tab1, tab2 = st.tabs(["Y-Line Items", "Create New"])
    
    with tab1:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "Active", "Inactive", "Pending"],
                index=0
            )
        
        with col2:
            product_filter = st.text_input("Product Code")
        
        # Display Y-Line items
        manager = YLineManager(next(get_db()))
        items = manager.get_yline_items(
            status_filter=status_filter if status_filter != "All" else None
        )
        
        if not items.empty:
            st.dataframe(
                items,
                column_config={
                    "IPA_Number": st.column_config.TextColumn("IPA Number"),
                    "ProductCode": st.column_config.TextColumn("Product Code"),
                    "Description": st.column_config.TextColumn("Description"),
                    "PreAward": st.column_config.CheckboxColumn("Pre-Award"),
                    "PostAward": st.column_config.CheckboxColumn("Post-Award"),
                    "Status": st.column_config.TextColumn("Status"),
                    "LastEditDate": st.column_config.DatetimeColumn("Last Updated")
                },
                hide_index=True,
                use_container_width=True
            )
    
    with tab2:
        st.subheader("Create New Y-Line Item")
        with st.form("new_yline_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                ipa_number = st.text_input("IPA Number")
                product_code = st.text_input("Product Code")
                status = st.selectbox(
                    "Status",
                    ["Active", "Inactive", "Pending"]
                )
            
            with col2:
                pre_award = st.checkbox("Pre-Award")
                post_award = st.checkbox("Post-Award")
                description = st.text_area("Description")
            
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Create Y-Line Item")
            
            if submitted:
                try:
                    validate_yline_item(YLineItem(
                        ipa_number=ipa_number,
                        product_code=product_code,
                        description=description,
                        pre_award=pre_award,
                        post_award=post_award,
                        status=status,
                        last_updated=datetime.now(),
                        notes=notes
                    ))
                    
                    manager = YLineManager(next(get_db()))
                    manager.create_yline_item(item)
                    st.success("Y-Line item created successfully!")
                    st.experimental_rerun()
                except ValueError as e:
                    st.error(f"Validation error: {str(e)}")
                except Exception as e:
                    st.error(f"Error creating Y-Line item: {str(e)}") 