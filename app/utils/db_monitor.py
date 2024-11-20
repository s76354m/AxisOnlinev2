"""Database operations monitoring and verification"""
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable
import pandas as pd
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import time
import threading
import queue

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
        self.connection_attempts = 0
        self.failed_attempts = 0
        self.last_response_time = 0
        self.connection_pool = queue.Queue(maxsize=10)
        self.status_cache = {'status': True, 'last_check': datetime.now()}
        self.lock = threading.Lock()
        self._init_connection_pool()
    
    def _init_connection_pool(self):
        """Initialize connection pool"""
        try:
            for _ in range(5):  # Create 5 initial connections
                conn = self._create_connection()
                if conn:
                    self.connection_pool.put(conn)
        except Exception as e:
            st.error(f"Error initializing connection pool: {str(e)}")
    
    def _create_connection(self):
        """Create a new database connection"""
        try:
            engine = create_engine(
                st.secrets["db_connection"],
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10
            )
            return engine.connect()
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            conn = self.connection_pool.get(timeout=5)
            return conn
        except queue.Empty:
            new_conn = self._create_connection()
            if new_conn:
                return new_conn
            raise Exception("Unable to establish database connection")
    
    def release_connection(self, conn):
        """Release connection back to pool"""
        try:
            self.connection_pool.put(conn, timeout=5)
        except queue.Full:
            conn.close()
    
    def check_connection(self):
        """Check database connection with caching"""
        now = datetime.now()
        with self.lock:
            if (now - self.status_cache['last_check']) < timedelta(seconds=30):
                return self.status_cache['status']
            
            try:
                conn = self.get_connection()
                start_time = time.time()
                conn.execute(text("SELECT 1"))
                self.last_response_time = (time.time() - start_time) * 1000
                self.release_connection(conn)
                self.status_cache = {'status': True, 'last_check': now}
                return True
            except Exception:
                self.status_cache = {'status': False, 'last_check': now}
                return False
    
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
    
    def get_uptime(self):
        return datetime.now() - self.start_time
    
    def get_error_rate(self):
        if self.connection_attempts == 0:
            return 0
        return (self.failed_attempts / self.connection_attempts) * 100

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

def display_db_status(monitor: DatabaseMonitor):
    """Display database status in Streamlit"""
    status = monitor.check_connection()
    
    if status:
        st.sidebar.success("🟢 Database Connected")
        st.sidebar.metric("Response Time", f"{monitor.last_response_time:.2f}ms")
    else:
        st.sidebar.error("🔴 Database Disconnected")
        if st.sidebar.button("Retry Connection"):
            st.experimental_rerun()
    
    # Show detailed metrics in expander
    with st.sidebar.expander("Database Metrics"):
        st.metric("Uptime", f"{monitor.get_uptime().seconds // 3600}h {(monitor.get_uptime().seconds // 60) % 60}m")
        st.metric("Error Rate", f"{monitor.get_error_rate():.1f}%")
        st.metric("Total Connections", monitor.connection_attempts) 