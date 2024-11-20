"""Unit tests for dashboard components"""
import pytest
from unittest.mock import Mock, patch
from app.ui.pages.dashboard import render_page
import streamlit as st

@pytest.fixture
def mock_streamlit():
    with patch('app.ui.pages.dashboard.st') as mock_st:
        mock_st.columns.return_value = [Mock(), Mock(), Mock(), Mock()]
        yield mock_st

@pytest.fixture
def mock_services():
    with patch('app.services.project_service.ProjectService') as mock_project, \
         patch('app.services.csp_lob_service.CSPLOBService') as mock_csp, \
         patch('app.services.y_line_service.YLineService') as mock_yline:
        yield {
            'project': mock_project,
            'csp_lob': mock_csp,
            'y_line': mock_yline
        }

def test_metrics_display(mock_streamlit, mock_services):
    """Test metrics display components"""
    render_page()
    assert mock_streamlit.metric.call_count == 4

def test_database_status_component(mock_streamlit):
    """Test database status component"""
    render_page()
    mock_streamlit.expander.assert_called_with("Database Status", expanded=True)

def test_activity_feed_component(mock_streamlit, mock_services):
    """Test activity feed component"""
    render_page()
    mock_streamlit.tabs.assert_called_with(["Projects", "CSP LOB", "Y-Lines"])

def test_error_handling(mock_streamlit, mock_services):
    """Test error handling in components"""
    mock_services['project'].side_effect = Exception("Test error")
    render_page()
    mock_streamlit.error.assert_called()
