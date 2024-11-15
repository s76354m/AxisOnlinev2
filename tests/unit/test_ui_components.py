"""Unit tests for UI components"""
import pytest
from unittest.mock import patch
import streamlit as st
from app.ui.pages.csp_lob_management import render_page
from app.ui.pages.project_management import render_page as render_project_page

@pytest.mark.ui
def test_csp_lob_page_render():
    """Test CSP LOB management page rendering"""
    with patch('streamlit.title') as mock_title:
        render_page()
        mock_title.assert_called_once_with("CSP Line of Business Management")

@pytest.mark.ui
def test_project_page_render():
    """Test project management page rendering"""
    with patch('streamlit.title') as mock_title:
        render_project_page()
        mock_title.assert_called_once_with("Project Management")

@pytest.mark.ui
def test_new_mapping_form():
    """Test new CSP LOB mapping form"""
    with patch('streamlit.form') as mock_form:
        with patch('streamlit.text_input') as mock_input:
            render_page()
            mock_form.assert_called_with("new_mapping_form")
            mock_input.assert_called() 