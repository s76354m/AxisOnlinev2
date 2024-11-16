"""Test UI functionality"""
import pytest
from unittest.mock import patch
from app.main import display_project_details, display_project_notes

def test_project_details_display(mock_streamlit, mock_db_session):
    """Test project details display"""
    # Arrange
    project_id = "TEST001"
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act
        display_project_details(project_id)
        
        # Assert
        mock_streamlit['expander'].assert_called()
        assert mock_streamlit['error'].call_count == 0

def test_project_notes_display(mock_streamlit, mock_db_session):
    """Test project notes display"""
    # Arrange
    project_id = "TEST001"
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act
        display_project_notes(project_id)
        
        # Assert
        mock_streamlit['form'].assert_called()
        assert mock_streamlit['error'].call_count == 0

def test_project_details_error_handling(mock_streamlit, mock_db_session):
    """Test project details error handling"""
    # Arrange
    project_id = "TEST001"
    mock_db_session.execute.side_effect = Exception("Test error")
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act
        display_project_details(project_id)
        
        # Assert
        mock_streamlit['error'].assert_called()

def test_project_notes_form_submission(mock_streamlit, mock_db_session):
    """Test project notes form submission"""
    # Arrange
    project_id = "TEST001"
    form = mock_streamlit['form'].return_value.__enter__.return_value
    form.form_submit_button.return_value = True
    
    with patch('app.main.get_db', return_value=iter([mock_db_session])):
        # Act
        display_project_notes(project_id)
        
        # Assert
        form.form_submit_button.assert_called()