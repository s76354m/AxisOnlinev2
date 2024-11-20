import pytest
from unittest.mock import Mock, patch
from app.ui.pages.dashboard import render_page
from app.services.project_service import ProjectService
from app.services.csp_lob_service import CSPLOBService
from app.services.y_line_service import YLineService

@pytest.fixture
def mock_services():
    return {
        'project_service': Mock(spec=ProjectService),
        'csp_lob_service': Mock(spec=CSPLOBService),
        'y_line_service': Mock(spec=YLineService)
    }

@pytest.fixture
def mock_streamlit():
    with patch('app.ui.pages.dashboard.st') as mock_st:
        # Mock column structure
        mock_st.columns.return_value = [Mock(), Mock(), Mock(), Mock()]
        yield mock_st

def test_dashboard_metrics(mock_streamlit, mock_services):
    """Test dashboard metrics display and calculation"""
    # Arrange
    mock_services['project_service'].get_all_projects.return_value = [
        Mock(Status="Active"), Mock(Status="Active"), Mock(Status="Completed")
    ]
    mock_services['csp_lob_service'].get_all_csp_lobs.return_value = [Mock(), Mock()]
    mock_services['y_line_service'].get_all_y_lines.return_value = [Mock()]
    
    with patch('app.ui.pages.dashboard.ProjectService', return_value=mock_services['project_service']), \
         patch('app.ui.pages.dashboard.CSPLOBService', return_value=mock_services['csp_lob_service']), \
         patch('app.ui.pages.dashboard.YLineService', return_value=mock_services['y_line_service']):
        
        # Act
        render_page()
        
        # Assert
        mock_streamlit.metric.assert_any_call("Total Projects", 3)
        mock_streamlit.metric.assert_any_call("Active Projects", 2)
        mock_streamlit.metric.assert_any_call("LOB Mappings", 2)
        mock_streamlit.metric.assert_any_call("Y-Lines", 1)

def test_dashboard_load_time():
    """Test dashboard load time performance"""
    import time
    
    start_time = time.time()
    with patch('app.ui.pages.dashboard.st'):
        render_page()
    load_time = time.time() - start_time
    
    assert load_time < 3, f"Dashboard load time ({load_time}s) exceeds 3s threshold"

def test_dashboard_database_status(mock_streamlit):
    """Test database status display"""
    with patch('app.ui.pages.dashboard.test_connection') as mock_test:
        # Test successful connection
        mock_test.return_value = (True, "Database connection successful")
        render_page()
        mock_streamlit.success.assert_called_with("Database connection successful")
        
        # Test failed connection
        mock_test.return_value = (False, "Connection error")
        render_page()
        mock_streamlit.error.assert_called_with("Connection error") 