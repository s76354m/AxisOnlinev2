"""Security test suite for authentication and authorization"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestAuthenticationSecurity:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/login")

    def test_brute_force_protection(self):
        """Test brute force attack prevention"""
        # Reference pattern from:
        ```python:tests/security/test_authentication.py
        startLine: 23
        endLine: 46
        ```
        
        # Attempt multiple failed logins
        for _ in range(5):
            username = self.driver.find_element(By.ID, "username")
            password = self.driver.find_element(By.ID, "password")
            
            username.clear()
            password.clear()
            username.send_keys("test_user")
            password.send_keys("wrong_password")
            
            self.driver.find_element(By.ID, "login-button").click()
            time.sleep(1)  # Wait for rate limiting
        
        # Verify account lockout
        lockout_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "account-locked"))
        )
        assert "Account temporarily locked" in lockout_message.text

    def test_session_security(self):
        """Test session handling security"""
        # Login successfully
        self.driver.find_element(By.ID, "username").send_keys("valid_user")
        self.driver.find_element(By.ID, "password").send_keys("valid_password")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Verify session token
        session_cookie = self.driver.get_cookie("session_token")
        assert session_cookie["secure"] == True
        assert session_cookie["httpOnly"] == True
        
        # Test session timeout
        self.driver.execute_script(
            "window.localStorage.setItem('session_expiry', '2000-01-01')"
        )
        self.driver.get("/dashboard")
        
        # Verify redirect to login
        assert "/login" in self.driver.current_url

class TestAuthorizationSecurity:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services

    def test_rbac_enforcement(self):
        """Test Role-Based Access Control"""
        # Login as basic user
        self.driver.get("/login")
        self.driver.find_element(By.ID, "username").send_keys("basic_user")
        self.driver.find_element(By.ID, "password").send_keys("basic_pass")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Try accessing admin routes
        restricted_paths = ["/admin", "/settings/global", "/users/manage"]
        
        for path in restricted_paths:
            self.driver.get(path)
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "access-denied"))
            )
            assert "Unauthorized access" in error_message.text

    def test_api_security(self):
        """Test API security measures"""
        # Test CSRF protection
        self.driver.get("/dashboard")
        csrf_token = self.driver.execute_script(
            "return document.querySelector('meta[name=\"csrf-token\"]').content"
        )
        assert csrf_token is not None
        
        # Test API authorization
        response = self.driver.execute_script("""
            return fetch('/api/sensitive-data', {
                method: 'GET',
                headers: {
                    'Authorization': 'Invalid-Token'
                }
            }).then(r => r.status)
        """)
        assert response == 401