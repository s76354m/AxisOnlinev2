import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from app.services.csp_lob_service import CSPLOBService
from app.models.csp_lob import LOBType, CSPStatus

@pytest.mark.nondestructive
class TestCSPLOBAutomated:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.driver = webdriver.Chrome()  # Requires ChromeDriver
        self.wait = WebDriverWait(self.driver, 10)
        self.service = CSPLOBService(db_session)
        self.base_url = "http://localhost:8501"  # Streamlit default port
        yield
        self.driver.quit()

    def test_create_mapping(self):
        """Test creating a new CSP LOB mapping"""
        self.driver.get(f"{self.base_url}")
        
        # Click Create New Mapping in sidebar
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Create New Mapping']"))
        )
        create_button.click()

        # Fill form
        self.driver.find_element(By.XPATH, "//input[@aria-label='Project ID']").send_keys("1")
        self.driver.find_element(By.XPATH, "//input[@aria-label='CSP Code']").send_keys("TEST001")
        
        # Select LOB Type
        lob_select = self.driver.find_element(By.XPATH, "//select[@aria-label='LOB Type']")
        lob_select.click()
        lob_option = self.driver.find_element(By.XPATH, "//option[text()='MEDICAL']")
        lob_option.click()

        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Create Mapping']")
        submit_button.click()

        # Verify success message
        success_message = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'successfully')]"))
        )
        assert success_message.is_displayed()

    def test_validation_rules(self):
        """Test validation rules for CSP LOB creation"""
        self.driver.get(f"{self.base_url}")
        
        # Test invalid CSP code
        self.driver.find_element(By.XPATH, "//input[@aria-label='CSP Code']").send_keys("@#")
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Create Mapping']")
        submit_button.click()
        
        error_message = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'alphanumeric')]"))
        )
        assert error_message.is_displayed()

    def test_filtering(self):
        """Test filtering functionality"""
        self.driver.get(f"{self.base_url}")
        
        # Select MEDICAL from LOB Type filter
        filter_select = self.driver.find_element(By.XPATH, "//select[@aria-label='LOB Type']")
        filter_select.click()
        medical_option = self.driver.find_element(By.XPATH, "//option[text()='MEDICAL']")
        medical_option.click()

        # Verify filtered results
        results = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='dataframe']//td"))
        )
        assert all("MEDICAL" in result.text for result in results) 