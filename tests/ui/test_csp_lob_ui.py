import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.nondestructive
class TestCSPLOBUI:
    def test_create_new_mapping(self, driver, base_url):
        """Test creating a new CSP LOB mapping"""
        driver.get(f"{base_url}/csp-lob")
        
        # Fill form
        driver.find_element(By.ID, "csp-code").send_keys("TEST001")
        driver.find_element(By.ID, "lob-type").click()
        driver.find_element(By.XPATH, "//option[text()='MEDICAL']").click()
        
        # Submit
        driver.find_element(By.ID, "submit-button").click()
        
        # Verify success
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )
        assert "Successfully created" in success_message.text

    def test_validation_errors(self, driver, base_url):
        """Test form validation errors"""
        driver.get(f"{base_url}/csp-lob")
        
        # Submit empty form
        driver.find_element(By.ID, "submit-button").click()
        
        # Verify error messages
        errors = driver.find_elements(By.CLASS_NAME, "error-message")
        assert len(errors) > 0
        assert "required" in errors[0].text.lower()

    def test_bulk_import(self, driver, base_url):
        """Test bulk import functionality"""
        driver.get(f"{base_url}/csp-lob")
        
        # Upload file
        file_input = driver.find_element(By.ID, "file-upload")
        file_input.send_keys("path/to/test/file.csv")
        
        # Verify processing
        processing_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "processing-status"))
        )
        assert "Processing" in processing_message.text 