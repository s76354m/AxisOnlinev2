"""E2E tests for Notes System"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestNotesBasicOperations:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/notes")

    def test_create_note(self):
        """Test note creation functionality"""
        # Reference pattern from:
        ```python:tests/e2e/ui/run_functional_tests.py
        startLine: 53
        endLine: 65
        ```
        
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "create-note"))
        )
        create_button.click()
        
        # Fill note form
        self.driver.find_element(By.ID, "note-title").send_keys("Test Note")
        self.driver.find_element(By.ID, "note-category").send_keys("General")
        self.driver.find_element(By.ID, "note-content").send_keys("Test content")
        
        # Add attachment
        file_input = self.driver.find_element(By.ID, "attachment-input")
        file_input.send_keys("/path/to/test.pdf")
        
        # Submit note
        self.driver.find_element(By.ID, "submit-note").click()
        
        # Verify creation
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "Note created successfully" in success_message.text

    def test_edit_note(self):
        """Test note editing functionality"""
        # Create test note first
        self.test_create_note()
        
        # Find and click edit button
        edit_button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "edit-note-btn"))
        )
        edit_button.click()
        
        # Update note content
        content_field = self.driver.find_element(By.ID, "note-content")
        content_field.clear()
        content_field.send_keys("Updated content")
        
        # Save changes
        self.driver.find_element(By.ID, "save-note").click()
        
        # Verify update
        updated_content = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "note-content"))
        )
        assert "Updated content" in updated_content.text

class TestNotesSearch:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/notes/search")

    def test_full_text_search(self):
        """Test notes search functionality"""
        # Setup mock search results
        self.mock_services.notes_service.search.return_value = [
            {"id": "1", "title": "Test Note", "content": "Search content"},
            {"id": "2", "title": "Another Note", "content": "More content"}
        ]
        
        # Perform search
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "search-input"))
        )
        search_input.send_keys("test")
        
        # Click search button
        self.driver.find_element(By.ID, "search-button").click()
        
        # Verify results
        results = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-result"))
        )
        assert len(results) == 2
        assert "Test Note" in results[0].text

    def test_filter_results(self):
        """Test search filter functionality"""
        # Apply category filter
        filter_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.ID, "category-filter"))
        )
        filter_dropdown.click()
        
        # Select category
        self.driver.find_element(By.XPATH, "//option[text()='General']").click()
        
        # Verify filtered results
        filtered_results = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-result"))
        )
        for result in filtered_results:
            assert "General" in result.get_attribute("data-category")
