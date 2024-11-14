import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
import pandas as pd
import streamlit as st
from unittest.mock import MagicMock
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def engine():
    return create_engine("mssql+pyodbc://DESKTOP-PJTAP42\\SQLEXPRESS/ndar?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close() 

@pytest.fixture
def mock_db():
    """Mock database connection"""
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create test tables
    session.execute("""
        CREATE TABLE CS_EXP_Project_Translation (
            ProjectID TEXT PRIMARY KEY,
            ProjectType TEXT,
            ProjectDesc TEXT,
            Status TEXT,
            Analyst TEXT,
            PM TEXT,
            LastEditDate DATETIME
        )
    """)
    
    session.execute("""
        CREATE TABLE CS_EXP_ProjectNotes (
            RecordID INTEGER PRIMARY KEY,
            ProjectID TEXT,
            Notes TEXT,
            ProjectStatus TEXT,
            ActionItem TEXT,
            LastEditMSID TEXT,
            LastEditDate DATETIME,
            DataLoadDate DATETIME
        )
    """)
    
    yield session
    session.close()

@pytest.fixture
def mock_st():
    """Mock Streamlit components"""
    st.session_state = {}
    st.sidebar = MagicMock()
    st.title = MagicMock()
    st.write = MagicMock()
    return st 

@pytest.fixture
def st_client():
    """Provide Streamlit test client"""
    from tests.utils.test_client import StreamlitTestClient
    return StreamlitTestClient()

@pytest.fixture
def mock_db():
    """Provide mock database"""
    from unittest.mock import MagicMock
    db = MagicMock()
    db.execute = MagicMock()
    db.commit = MagicMock()
    return db 

@pytest.fixture
def sample_projects_df():
    """Sample project data for testing"""
    return pd.DataFrame({
        'ProjectID': ['TEST001', 'TEST002'],
        'ProjectType': ['Translation', 'Analysis'],
        'ProjectDesc': ['Test Project 1', 'Test Project 2'],
        'Status': ['Active', 'New'],
        'Analyst': ['Test Analyst', 'Test Analyst 2'],
        'PM': ['Test PM', 'Test PM 2'],
        'LastEditDate': [datetime.now(), datetime.now()]
    })

@pytest.fixture
def mock_db_session():
    """Mock database session without dependency on sample data"""
    session = MagicMock(spec=Session)
    
    # Configure basic mock responses
    mock_result = MagicMock()
    mock_result.fetchone.return_value = {
        'ProjectID': 'TEST001',
        'ProjectType': 'Translation',
        'ProjectDesc': 'Test Project',
        'Status': 'Active'
    }
    mock_result.fetchall.return_value = [
        mock_result.fetchone.return_value,
        {
            'ProjectID': 'TEST002',
            'ProjectType': 'Analysis',
            'ProjectDesc': 'Test Project 2',
            'Status': 'New'
        }
    ]
    session.execute.return_value = mock_result
    
    return session

@pytest.fixture(autouse=True)
def mock_streamlit_context():
    """Mock Streamlit context for all tests"""
    if not hasattr(st, 'session_state'):
        setattr(st, 'session_state', {})
    
    st.session_state.current_page = 'Projects'
    st.session_state.project_id = 'TEST001'
    
    return st

@pytest.fixture
def db():
    """Database session fixture"""
    return mock_db_session()

@pytest.fixture
def mock_streamlit():
    """Mock Streamlit components"""
    mocks = {
        'title': MagicMock(),
        'write': MagicMock(),
        'markdown': MagicMock(),
        'error': MagicMock(),
        'success': MagicMock(),
        'info': MagicMock(),
        'warning': MagicMock(),
        'selectbox': MagicMock(return_value=None),
        'multiselect': MagicMock(return_value=[]),
        'form': MagicMock(),
        'columns': MagicMock(return_value=[MagicMock(), MagicMock()]),
        'expander': MagicMock()
    }
    
    with patch.multiple('streamlit', **mocks):
        yield mocks