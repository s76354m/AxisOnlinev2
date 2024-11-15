"""CSP LOB Management page"""
import streamlit as st
import pandas as pd
from datetime import datetime
from app.db.session import get_db
from app.utils.validators import CSPLOBValidator
from app.services.csp_lob_service import CSPLOBService
import logging

logger = logging.getLogger(__name__)

def render_page():
    """Render CSP LOB management page"""
    st.title("CSP Line of Business Management")

    # Add new mapping button
    if st.button("+ New Mapping"):
        st.session_state.current_view = "new_mapping"
        st.rerun()

    # View type toggle
    view_type = st.radio("View", ["List", "Grid"], horizontal=True)

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Pending", "Terminated"]
        )
    with col2:
        lob_filter = st.selectbox(
            "LOB Type",
            ["All", "Medical", "Pharmacy", "Dental", "Vision"]
        )
    with col3:
        search = st.text_input("Search", placeholder="Search CSP codes...")

    try:
        db = next(get_db())
        # Query to get CSP LOB mappings
        query = """
        SELECT 
            CSPCode,
            LOBType,
            [Description],
            [Status],
            EffectiveDate,
            TerminationDate,
            LastEditDate,
            LastEditMSID
        FROM CS_EXP_CSP_LOB WITH (NOLOCK)
        WHERE 1=1
        """
        
        params = []
        if status_filter != "All":
            query += " AND Status = ?"
            params.append(status_filter)
        if lob_filter != "All":
            query += " AND LOBType = ?"
            params.append(lob_filter)
        if search:
            query += " AND CSPCode LIKE ?"
            params.append(f"%{search}%")
            
        query += " ORDER BY LastEditDate DESC"
        
        df = pd.read_sql(query, db.bind, params=params)
        
        if not df.empty:
            # Format dates for display
            for date_col in ['EffectiveDate', 'TerminationDate', 'LastEditDate']:
                if date_col in df.columns:
                    df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                df,
                column_config={
                    "CSPCode": "CSP Code",
                    "LOBType": "LOB Type",
                    "Description": "Description",
                    "Status": "Status",
                    "EffectiveDate": "Effective Date",
                    "TerminationDate": "Termination Date",
                    "LastEditDate": "Last Updated",
                    "LastEditMSID": "Last Editor"
                },
                hide_index=True
            )
        else:
            st.info("No CSP LOB mappings found matching the criteria.")

        # Bulk Operations
        if not df.empty:
            st.divider()
            st.subheader("Bulk Operations")
            
            col1, col2 = st.columns(2)
            with col1:
                bulk_status = st.selectbox(
                    "Update Status",
                    ["Select Status...", "Active", "Terminated"]
                )
                if st.button("Update Selected"):
                    st.warning("Bulk status update not implemented yet")
            
            with col2:
                uploaded_file = st.file_uploader(
                    "Import Mappings",
                    type=['csv', 'xlsx']
                )
                if uploaded_file is not None:
                    st.warning("File import not implemented yet")

    except Exception as e:
        st.error(f"Error loading CSP LOB mappings: {str(e)}")
    finally:
        db.close()

def create_new_mapping():
    """Create new CSP LOB mapping form"""
    st.subheader("Create New CSP LOB Mapping")
    
    with st.form("new_mapping_form"):
        csp_code = st.text_input(
            "CSP Code *",
            placeholder="Enter CSP code"
        )
        
        lob_type = st.selectbox(
            "LOB Type *",
            ["Medical", "Pharmacy", "Dental", "Vision"]
        )
        
        description = st.text_area(
            "Description",
            placeholder="Enter description"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            effective_date = st.date_input(
                "Effective Date *",
                min_value=datetime.now().date()
            )
        
        with col2:
            termination_date = st.date_input(
                "Termination Date",
                value=None,
                min_value=effective_date if effective_date else None
            )
        
        submitted = st.form_submit_button("Create Mapping")
        
        if submitted:
            if not all([csp_code, lob_type, effective_date]):
                st.error("Please fill in all required fields (*)")
                return
            
            try:
                # Validate CSP code format
                if not CSPLOBValidator.validate_csp_code(csp_code):
                    st.error("Invalid CSP code format")
                    return
                
                # Validate dates
                if termination_date and not CSPLOBValidator.validate_dates(
                    effective_date, termination_date
                ):
                    st.error("Termination date must be after effective date")
                    return
                
                db = next(get_db())
                query = """
                INSERT INTO CS_EXP_CSP_LOB (
                    CSPCode,
                    LOBType,
                    [Description],
                    [Status],
                    EffectiveDate,
                    TerminationDate,
                    LastEditDate,
                    LastEditMSID
                ) VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?)
                """
                
                params = [
                    csp_code,
                    lob_type,
                    description,
                    'Active',
                    effective_date,
                    termination_date,
                    st.session_state.get('user', 'Unknown')
                ]
                
                db.execute(query, params)
                db.commit()
                st.success("CSP LOB mapping created successfully!")
                
                # Return to main view
                st.session_state.current_view = 'list'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error creating CSP LOB mapping: {str(e)}")
                db.rollback()
            finally:
                db.close()

def handle_file_upload():
    """Handle CSP LOB mapping file upload"""
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['csp_code', 'lob_type', 'description', 'status', 'effective_date']
            if not all(col in df.columns for col in required_columns):
                st.error("CSV file must contain all required columns")
                return
            
            # Preview data
            st.write("Preview of data to be imported:")
            st.dataframe(df.head())
            
            # Validate data
            validation_errors = []
            for idx, row in df.iterrows():
                try:
                    CSPLOBValidator.validate_csp_code(row['csp_code'])
                    CSPLOBValidator.validate_dates(
                        row['effective_date'], 
                        row.get('termination_date')
                    )
                except ValueError as e:
                    validation_errors.append(f"Row {idx + 1}: {str(e)}")
            
            if validation_errors:
                st.error("Validation errors found:")
                for error in validation_errors:
                    st.write(error)
                return
            
            # Confirm import
            if st.button("Confirm Import"):
                db = next(get_db())
                service = CSPLOBService(db)
                
                success_count = 0
                error_count = 0
                
                for _, row in df.iterrows():
                    try:
                        mapping_data = {
                            "csp_code": row['csp_code'],
                            "lob_type": row['lob_type'],
                            "description": row['description'],
                            "status": row['status'],
                            "effective_date": row['effective_date'],
                            "termination_date": row.get('termination_date'),
                        }
                        service.create_csp_lob(mapping_data)
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error importing row: {str(e)}")
                
                st.success(f"Import completed: {success_count} successful, {error_count} failed")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            logger.error(f"File upload error: {str(e)}")

def download_template():
    """Provide template download"""
    template_data = pd.DataFrame({
        'csp_code': ['ABC123'],
        'lob_type': ['Medical'],
        'description': ['Sample Description'],
        'status': ['Active'],
        'effective_date': ['2024-01-01'],
        'termination_date': ['2024-12-31']
    })
    
    csv = template_data.to_csv(index=False)
    st.download_button(
        label="Download Template",
        data=csv,
        file_name="csp_lob_template.csv",
        mime="text/csv"
    )