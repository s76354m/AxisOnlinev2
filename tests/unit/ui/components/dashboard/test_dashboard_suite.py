import pytest
from unittest.mock import Mock, patch
import streamlit as st
from app.ui.pages.dashboard import render_page
from app.utils.session_state_manager import SessionStateManager

@pytest.fixture
def mock_services():
    with patch('app.services.project_service.ProjectService') as mock_project, \
         patch('app.services.csp_lob_service.CSPLOBService') as mock_csp, \
         patch('app.services.y_line_service.YLineService') as mock_yline:
        
        # Configure mock services
        mock_project.get_all_projects.return_value = [Mock(status="Active")] * 3
        mock_csp.get_all_csps.return_value = [Mock()] * 2
        mock_yline.get_all_y_lines.return_value = [Mock()] * 4
        
        yield {
            'project': mock_project,
            'csp': mock_csp,
            'y_line': mock_yline
        }

def test_load_time():
    """Test dashboard load time"""
    import time
    start_time = time.time()
    render_page()
    load_time = time.time() - start_time
    assert load_time < 3, f"Dashboard load time ({load_time}s) exceeds 3s limit"

def test_metrics_accuracy(mock_services):
    """Test metrics display accuracy"""
    render_page()
    
    # Verify metrics match service data
    assert st.session_state.get('total_projects') == 3
    assert st.session_state.get('total_csps') == 2
    assert st.session_state.get('total_y_lines') == 4

def test_chart_rendering():
    """Test chart components render correctly"""
    render_page()
    
    # Verify chart elements
    assert 'chart_data' in st.session_state
    assert st.session_state.get('charts_rendered', 0) > 0

def test_activity_feed_updates(mock_services):
    """Test activity feed real-time updates"""
    render_page()
    
    # Get initial feed state
    initial_feed = st.session_state.get('activity_feed', [])
    
    # Simulate new activity
    mock_services['project'].get_recent_projects.return_value.append(Mock())
    render_page()
    
    # Verify feed updated
    updated_feed = st.session_state.get('activity_feed', [])
    assert len(updated_feed) > len(initial_feed) 