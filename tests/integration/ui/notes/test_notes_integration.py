"""Integration tests for Notes System"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestNotesIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/notes")

    def test_create_note_integration(self):
        """Test note creation with backend integration"""
        # Reference pattern from:
        ```python:tests/integration/ui/service_area/test_service_area_integration.py
        startLine: 24
        endLine: 44
        ```
        
        # Setup mock response
        self.mock_services.notes_service.create_note.return_value = {
            "id": "N1",
            "title": "Test Note",
            "content": "Test content",
            "category": "General",
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        # Create note
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "create-note"))
        )
        create_button.click()
        
        # Fill form
        self.driver.find_element(By.ID, "note-title").send_keys("Test Note")
        self.driver.find_element(By.ID, "note-content").send_keys("Test content")
        self.driver.find_element(By.ID, "note-category").send_keys("General")
        
        # Submit
        self.driver.find_element(By.ID, "submit-note").click()
        
        # Verify backend call
        assert self.mock_services.notes_service.create_note.called
        call_args = self.mock_services.notes_service.create_note.call_args[0][0]
        assert call_args["title"] == "Test Note"
        assert call_args["content"] == "Test content"

    def test_search_integration(self):
        """Test search functionality with backend integration"""
        # Setup mock search results
        self.mock_services.notes_service.search_notes.return_value = {
            "results": [
                {
                    "id": "N1",
                    "title": "Test Note",
                    "content": "Test content",
                    "category": "General"
                }
            ],
            "total": 1
        }
        
        # Perform search
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "search-input"))
        )
        search_input.send_keys("test")
        
        self.driver.find_element(By.ID, "search-button").click()
        
        # Verify backend call
        assert self.mock_services.notes_service.search_notes.called
        assert self.mock_services.notes_service.search_notes.call_args[0][0] == "test"
        
        # Verify results display
        results = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-result"))
        )
        assert len(results) == 1

    def test_attachment_handling(self):
        """Test attachment upload integration"""
        # Setup mock upload response
        self.mock_services.notes_service.upload_attachment.return_value = {
            "file_id": "F1",
            "url": "http://test-url/files/test.pdf"
        }
        
        # Upload file
        file_input = self.driver.find_element(By.ID, "attachment-input")
        file_input.send_keys("/path/to/test.pdf")
        
        # Verify upload call
        assert self.mock_services.notes_service.upload_attachment.called
        
        # Verify attachment display
        attachment_link = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "attachment-link"))
        )
        assert "test.pdf" in attachment_link.text
