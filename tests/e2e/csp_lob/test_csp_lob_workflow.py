"""E2E tests for csp_lob workflow"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCSPLOBWorkflow:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("/csp-lob")
    
    def test_mapping_creation_workflow(self):
        """Test complete mapping creation workflow"""
        # Reference existing automated test structure from:
        ```python:tests/automated/test_csp_lob_automated.py
        startLine: 21
        endLine: 49
        ```
        
        # Additional validation
        mapping_list = self.driver.find_elements(By.CLASS_NAME, "mapping-item")
        assert len(mapping_list) > 0
        assert "TEST001" in mapping_list[0].text
    
    def test_validation_rules(self):
        """Test mapping validation rules"""
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Create New Mapping']"))
        )
        create_button.click()
        
        # Submit empty form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Create Mapping']")
        submit_button.click()
        
        # Verify validation messages
        error_messages = self.driver.find_elements(By.CLASS_NAME, "error-message")
        required_fields = ["Project ID", "CSP Code", "LOB Type"]
        for field in required_fields:
            assert any(field in msg.text for msg in error_messages)
