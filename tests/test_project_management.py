"""Test project management functionality"""
import pytest
from unittest.mock import patch
from app.main import display_project_details, display_project_notes

def test_create_project(mock_streamlit, mock_db_session):
    """Test project creation"""
    # Arrange
    form = mock_streamlit['form'].return_value.__enter__.return_value
    form.form_submit_button.return_value = True
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act & Assert
        try:
            display_project_details(None)  # New project
            assert mock_streamlit['success'].call_count == 1
        except Exception as e:
            pytest.fail(f"Project creation failed: {str(e)}")

def test_display_project_details(mock_streamlit, mock_db_session):
    """Test project details display"""
    # Arrange
    project_id = "TEST001"
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act
        display_project_details(project_id)
        
        # Assert
        mock_streamlit['expander'].assert_called()
        assert mock_streamlit['error'].call_count == 0

def test_display_project_notes(mock_db_session, mock_streamlit):
    """Test project notes display"""
    # Arrange
    project_id = "TEST001"
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act
        display_project_notes(project_id)
        
        # Assert
        mock_streamlit['form'].assert_called()