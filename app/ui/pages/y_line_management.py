"""Y-Line management page"""
import streamlit as st
import pandas as pd
from app.services.y_line_service import YLineService
from app.schemas.y_line import YLineCreate

def render_page():
    """Render Y-Line management page"""
    st.title("Y-Line Management")
    y_line_service = YLineService()
    
    # Create New Y-Line Section
    with st.expander("Create New Y-Line", expanded=st.session_state.get('show_new_yline', False)):
        with st.form("new_yline_form"):
            ipa_number = st.text_input("IPA Number*")
            product_code = st.text_input("Product Code*")
            estimated_value = st.number_input("Estimated Value*", min_value=0.0)
            status = st.selectbox(
                "Status*",
                ["Pre-Award", "Post-Award", "Pending", "Completed"]
            )
            project_id = st.text_input("Project ID*")
            
            submitted = st.form_submit_button("Create Y-Line")
            if submitted:
                if not all([ipa_number, product_code, estimated_value, status, project_id]):
                    st.error("Please fill in all required fields")
                else:
                    try:
                        # IPA Validation
                        if not ipa_number.startswith('IPA-'):
                            st.error("IPA Number must start with 'IPA-'")
                            return
                            
                        y_line_data = YLineCreate(
                            ipa_number=ipa_number,
                            product_code=product_code,
                            estimated_value=estimated_value,
                            status=status,
                            project_id=project_id
                        )
                        y_line = y_line_service.create_y_line(y_line_data)
                        st.success(f"Y-Line created successfully: {y_line.ipa_number}")
                        st.session_state.show_new_yline = False
                    except Exception as e:
                        st.error(f"Error creating Y-Line: {str(e)}")
    
    # Y-Line List Section
    st.subheader("Y-Line List")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.multiselect(
            "Status",
            ["Pre-Award", "Post-Award", "Pending", "Completed"],
            default=["Pre-Award", "Post-Award"]
        )
    with col2:
        value_range = st.slider(
            "Value Range",
            min_value=0,
            max_value=1000000,
            value=(0, 1000000)
        )
    with col3:
        project_filter = st.text_input("Project ID Filter")
    
    try:
        y_lines = y_line_service.get_all_y_lines()
        if y_lines:
            # Apply filters
            filtered_y_lines = [
                y for y in y_lines
                if (not status_filter or y.status in status_filter) and
                   (value_range[0] <= y.estimated_value <= value_range[1]) and
                   (not project_filter or project_filter in y.project_id)
            ]
            
            # Convert to DataFrame for display
            df_y_lines = pd.DataFrame([vars(y) for y in filtered_y_lines])
            
            # Bulk Actions
            if len(filtered_y_lines) > 0:
                selected_y_lines = st.multiselect(
                    "Select Y-Lines for Bulk Actions",
                    df_y_lines['ipa_number'].tolist()
                )
                
                if selected_y_lines:
                    action = st.selectbox(
                        "Bulk Action",
                        ["Update Status", "Update Value"]
                    )
                    
                    if st.button("Apply Bulk Action"):
                        try:
                            if action == "Update Status":
                                new_status = st.selectbox(
                                    "New Status",
                                    ["Pre-Award", "Post-Award", "Pending", "Completed"]
                                )
                                for ipa in selected_y_lines:
                                    y_line_service.update_y_line_status(ipa, new_status)
                            elif action == "Update Value":
                                new_value = st.number_input("New Value", min_value=0.0)
                                for ipa in selected_y_lines:
                                    y_line_service.update_y_line_value(ipa, new_value)
                            st.success("Bulk action completed successfully")
                        except Exception as e:
                            st.error(f"Error in bulk operation: {str(e)}")
            
            # Display Y-Lines
            st.dataframe(
                df_y_lines,
                column_config={
                    "ipa_number": "IPA Number",
                    "product_code": "Product Code",
                    "estimated_value": "Est. Value",
                    "status": "Status",
                    "project_id": "Project ID"
                },
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Error loading Y-Lines: {str(e)}")