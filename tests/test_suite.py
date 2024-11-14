import pytest
from sqlalchemy.orm import Session
import requests
import streamlit as st
from app.frontend.main import AxisProgramUI
from app.db.session import get_db
from app.core.logging_config import logger
from unittest.mock import patch, MagicMock

# Database Connection Tests
def test_database_connection(db: Session):
    """Test database connectivity"""
    try:
        result = db.execute("SELECT 1").scalar()
        assert result == 1
        logger.info("Database connection test passed")
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        pytest.fail(f"Database connection failed: {str(e)}")

# API Tests
@pytest.fixture
def mock_api():
    """Mock API responses"""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        yield {
            'get': mock_get,
            'post': mock_post
        }

def test_api_endpoints(mock_api):
    """Test API endpoints"""
    # Test GET request
    response = requests.get('http://localhost:8000/api/v1/projects/')
    assert response.status_code == 200
    
    # Test POST request
    response = requests.post('http://localhost:8000/api/v1/projects/', 
                           json={"name": "Test Project"})
    assert response.status_code == 200

# UI Tests
def test_ui_initialization(mock_streamlit_context):
    """Test UI initialization"""
    try:
        app = AxisProgramUI()
        assert app is not None
        assert st.session_state.current_page == 'Projects'
    except Exception as e:
        pytest.fail(f"UI initialization failed: {str(e)}")

# Integration Tests
def test_project_creation_flow(mock_api, mock_db_session):
    """Test project creation flow"""
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        project_data = {
            "ProjectType": "Translation",
            "ProjectDesc": "Test Project",
            "Status": "New",
            "Analyst": "Test Analyst",
            "PM": "Test PM"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/projects/",
            json=project_data
        )
        assert response.status_code == 200 