import streamlit as st
from app.db.session import get_db
from app.core.config import Settings
from sqlalchemy import text
from app.utils.model_verification import verify_all_models

def verify_startup_requirements():
    """Verify all requirements before app startup"""
    settings = Settings()
    checks = []
    
    # Verify database connection
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        checks.append(("Database Connection", True, "Connected"))
        
        # Add model verification
        model_results = verify_all_models()
        model_issues = [
            r for r in model_results 
            if r.get('missing_columns') or r.get('extra_columns') or r.get('error')
        ]
        
        if not model_issues:
            checks.append(("Model Verification", True, "All models match schema"))
        else:
            issues = [f"{r['table_name']}: {r.get('error', 'Schema mismatch')}" 
                     for r in model_issues]
            checks.append(("Model Verification", False, "; ".join(issues)))
            
    except Exception as e:
        checks.append(("Database Connection", False, str(e)))
    
    return checks

def display_startup_status():
    """Display startup verification results"""
    st.sidebar.expander("System Status", expanded=False)
    checks = verify_startup_requirements()
    
    for check_name, status, message in checks:
        if status:
            st.sidebar.success(f"✓ {check_name}")
        else:
            st.sidebar.error(f"✗ {check_name}: {message}") 