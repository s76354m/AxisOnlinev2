import pytest
from unittest.mock import Mock, patch
from app.ui.pages.notes import render_page
import streamlit as st

@pytest.fixture
def mock_notes_service():
    with patch('app.services.notes_service.NotesService') as mock_service:
        mock_service.get_all_notes.return_value = [
            Mock(id=1, title="Test Note", category="General"),
            Mock(id=2, title="Project Note", category="Projects")
        ]
        yield mock_service

def test_basic_operations(mock_notes_service):
    """Test basic note operations"""
    with st.form("create_note"):
        # Test note creation
        st.text_input("Title", "Test Note")
        st.selectbox("Category", ["General", "Projects"])
        st.text_area("Content", "Test content")
        
        mock_notes_service.create_note.assert_called_once()
        
        # Test note editing
        st.text_input("Title", "Updated Note")
        mock_notes_service.update_note.assert_called_once()
        
        # Test note deletion
        st.button("Delete")
        mock_notes_service.delete_note.assert_called_once()

def test_search_functionality(mock_notes_service):
    """Test notes search system"""
    # Test full text search
    search_results = mock_notes_service.search_notes("test")
    assert len(search_results) > 0
    
    # Test category filters
    filtered_results = mock_notes_service.filter_notes(category="Projects")
    assert all(note.category == "Projects" for note in filtered_results)
    
    # Test search accuracy
    assert mock_notes_service.search_accuracy_score > 0.8

def test_attachment_handling():
    """Test note attachments"""
    with patch('app.services.storage_service.StorageService') as mock_storage:
        # Test file upload
        uploaded_file = st.file_uploader("Add attachment")
        mock_storage.upload_file.assert_called_once()
        
        # Test file download
        st.download_button("Download")
        mock_storage.download_file.assert_called_once() 