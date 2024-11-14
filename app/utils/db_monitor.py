"""Database operations monitoring and verification"""
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable
import pandas as pd
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

# Set up logging
logging.basicConfig(
    filename='database_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseMonitor:
    """Monitor and verify database operations"""
    
    def __init__(self):
        self.operation_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
    
    def log_operation(self, operation_type: str, status: str, details: str = None):
        """Log database operations"""
        logging.info(
            f"Operation: {operation_type} | Status: {status} | Details: {details}"
        )
        self.operation_count += 1
    
    def log_error(self, operation_type: str, error: Exception):
        """Log database errors"""
        logging.error(
            f"Operation: {operation_type} | Error: {str(error)} | Type: {type(error)}"
        )
        self.error_count += 1
    
    def get_stats(self) -> dict:
        """Get database operation statistics"""
        return {
            'operations': self.operation_count,
            'errors': self.error_count,
            'uptime': datetime.now() - self.start_time
        }

def monitor_db_operation(operation_type: str) -> Callable:
    """Decorator to monitor database operations"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            monitor = DatabaseMonitor()
            try:
                result = func(*args, **kwargs)
                monitor.log_operation(operation_type, 'SUCCESS')
                return result
            except Exception as e:
                monitor.log_error(operation_type, e)
                raise
        return wrapper
    return decorator

def verify_database_connection(db) -> bool:
    """Verify database connection"""
    try:
        db.execute("SELECT 1")
        return True
    except SQLAlchemyError as e:
        logging.error(f"Database connection error: {str(e)}")
        return False

def verify_table_integrity() -> pd.DataFrame:
    """Verify database table integrity"""
    tables = [
        'CS_EXP_Project_Translation',
        'CS_EXP_ProjectNotes'
    ]
    
    results = []
    for table in tables:
        try:
            query = f"""
            SELECT 
                COUNT(*) as row_count,
                MAX(LastEditDate) as last_update
            FROM {table} WITH (NOLOCK)
            """
            df = pd.read_sql(query, db.bind)
            results.append({
                'table': table,
                'status': 'OK',
                'rows': df['row_count'].iloc[0],
                'last_update': df['last_update'].iloc[0]
            })
        except Exception as e:
            results.append({
                'table': table,
                'status': 'ERROR',
                'error': str(e)
            })
    
    return pd.DataFrame(results)

def display_db_monitor():
    """Display database monitoring information in Streamlit"""
    st.subheader("Database Operations Monitor")
    
    monitor = DatabaseMonitor()
    stats = monitor.get_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Operations", stats['operations'])
    
    with col2:
        st.metric("Errors", stats['errors'])
    
    with col3:
        st.metric("Uptime", f"{stats['uptime'].seconds // 3600}h {(stats['uptime'].seconds // 60) % 60}m")
    
    if st.checkbox("Show Table Integrity Check"):
        integrity_df = verify_table_integrity()
        st.dataframe(integrity_df)
    
    if st.checkbox("Show Recent Errors"):
        with open('database_operations.log', 'r') as f:
            errors = [line for line in f if 'ERROR' in line]
            if errors:
                st.error("\n".join(errors[-5:]))  # Show last 5 errors
            else:
                st.success("No recent errors found") 