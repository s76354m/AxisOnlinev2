"""Security test suite for data protection"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDataProtection:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        
    def test_data_encryption(self):
        """Test data encryption in transit"""
        self.driver.get("/login")
        
        # Verify HTTPS
        assert self.driver.current_url.startswith("https")
        
        # Verify secure headers
        response_headers = self.driver.execute_script(
            "return window.performance.getEntries()[0].responseHeaders"
        )
        assert "Strict-Transport-Security" in str(response_headers)
        
    def test_data_access_controls(self):
        """Test data access controls"""
        # Login as regular user
        self._login_as_user("regular_user", "password")
        
        # Try accessing admin data
        self.driver.get("/admin/sensitive-data")
        
        # Should be redirected
        assert "/unauthorized" in self.driver.current_url
        
    def _login_as_user(self, username, password):
        """Helper to login as specific user"""
        self.driver.get("/login")
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = self.driver.find_element(By.ID, "password")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        submit = self.driver.find_element(By.ID, "login-submit")
        submit.click()