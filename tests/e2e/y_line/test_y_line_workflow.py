"""E2E tests for Y-Line Management"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestYLineAwardManagement:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/y-line/awards")

    def test_pre_post_handling(self):
        """Test pre/post award handling workflow"""
        # Reference pattern from:
        ```python:tests/e2e/service_area/test_service_area_workflow.py
        startLine: 15
        endLine: 39
        ```
        
        # Create pre-award
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "create-award"))
        )
        create_button.click()
        
        # Fill pre-award details
        self.driver.find_element(By.ID, "award-type").send_keys("Pre-Award")
        self.driver.find_element(By.ID, "award-number").send_keys("YL-2024-001")
        self.driver.find_element(By.ID, "award-description").send_keys("Test Award")
        
        # Submit pre-award
        self.driver.find_element(By.ID, "submit-award").click()
        
        # Verify creation
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "Pre-award created successfully" in success_message.text
        
        # Convert to post-award
        convert_button = self.driver.find_element(By.ID, "convert-to-post")
        convert_button.click()
        
        # Fill post-award details
        self.driver.find_element(By.ID, "post-award-details").send_keys("Post Details")
        self.driver.find_element(By.ID, "confirm-conversion").click()
        
        # Verify conversion
        post_status = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "award-status"))
        )
        assert "Post-Award" in post_status.text

    def test_ipa_validation(self):
        """Test IPA validation workflow"""
        # Create award with IPA
        self.driver.find_element(By.ID, "create-award").click()
        
        # Fill invalid IPA details
        self.driver.find_element(By.ID, "ipa-number").send_keys("INVALID")
        self.driver.find_element(By.ID, "submit-award").click()
        
        # Verify validation error
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "validation-error"))
        )
        assert "Invalid IPA format" in error_message.text
        
        # Fill valid IPA
        ipa_input = self.driver.find_element(By.ID, "ipa-number")
        ipa_input.clear()
        ipa_input.send_keys("IPA-2024-001")
        self.driver.find_element(By.ID, "submit-award").click()
        
        # Verify success
        assert "Award created successfully" in self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        ).text

class TestYLineBatchProcessing:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/y-line/batch")

    def test_bulk_updates(self):
        """Test bulk update functionality"""
        # Select multiple awards
        award_checkboxes = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "award-checkbox"))
        )
        for checkbox in award_checkboxes[:3]:
            checkbox.click()
        
        # Open bulk update panel
        self.driver.find_element(By.ID, "bulk-update").click()
        
        # Apply updates
        self.driver.find_element(By.ID, "bulk-status").send_keys("Approved")
        self.driver.find_element(By.ID, "apply-updates").click()
        
        # Verify updates
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "bulk-success"))
        )
        assert "3 awards updated successfully" in success_message.text
