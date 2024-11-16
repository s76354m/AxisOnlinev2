"""Security test suite for data protection"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import base64
import requests

class TestXSSPrevention:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services
        self.driver.get("/notes")

    def test_xss_input_sanitization(self):
        """Test XSS prevention in input fields"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src='x' onerror='alert(1)'>",
            "<svg/onload=alert('xss')>",
            "'-alert(1)-'",
            "\"><script>alert(1)</script>",
            "<body onload=alert('xss')>",
            "<a href='javascript:alert(1)'>click</a>"
        ]
        
        # Test note creation with XSS payloads
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "create-note"))
        )
        create_button.click()
        
        for payload in xss_payloads:
            # Input XSS payload
            title_input = self.driver.find_element(By.ID, "note-title")
            content_input = self.driver.find_element(By.ID, "note-content")
            
            title_input.clear()
            content_input.clear()
            title_input.send_keys(payload)
            content_input.send_keys(payload)
            
            # Submit form
            self.driver.find_element(By.ID, "submit-note").click()
            
            # Verify sanitized output
            note_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "note-content"))
            )
            sanitized_html = note_element.get_attribute("innerHTML")
            
            assert "<script>" not in sanitized_html.lower()
            assert "javascript:" not in sanitized_html.lower()
            assert "onerror=" not in sanitized_html.lower()
            assert "onload=" not in sanitized_html.lower()
            assert "onclick=" not in sanitized_html.lower()
            assert "alert" not in sanitized_html.lower()

    def test_url_parameter_sanitization(self):
        """Test URL parameter XSS prevention"""
        xss_urls = [
            "/notes?id=<script>alert(1)</script>",
            "/notes?search=javascript:alert(1)",
            "/notes?category=<img src=x onerror=alert(1)>"
        ]
        
        for url in xss_urls:
            self.driver.get(url)
            page_source = self.driver.page_source.lower()
            assert "<script>" not in page_source
            assert "javascript:" not in page_source
            assert "onerror=" not in page_source

    def test_dynamic_content_xss(self):
        """Test XSS prevention in dynamically loaded content"""
        # Login and create test data
        self.driver.get("/login")
        self.driver.find_element(By.ID, "username").send_keys("test_user")
        self.driver.find_element(By.ID, "password").send_keys("test_pass")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Test dynamic content areas
        test_areas = {
            "comments": "/projects/1/comments",
            "notifications": "/notifications",
            "search-results": "/search?q=test"
        }
        
        xss_payloads = [
            "<img src=x onerror=alert(document.cookie)>",
            "<iframe onload=alert(document.domain)>",
            "<svg><script>alert(1)</script></svg>",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>"
        ]
        
        for area, url in test_areas.items():
            self.driver.get(url)
            
            # Inject XSS payload into dynamic content
            script = f"""
                document.querySelector('.{area}-container').innerHTML = '{xss_payloads[0]}';
                return document.querySelector('.{area}-container').innerHTML;
            """
            injected_content = self.driver.execute_script(script)
            
            # Verify content is sanitized
            assert "<script>" not in injected_content.lower()
            assert "onerror=" not in injected_content.lower()
            assert "onload=" not in injected_content.lower()
            assert "javascript:" not in injected_content.lower()

class TestCSRFProtection:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services

    def test_csrf_token_implementation(self):
        """Test CSRF protection implementation"""
        # Login first
        self.driver.get("/login")
        self.driver.find_element(By.ID, "username").send_keys("test_user")
        self.driver.find_element(By.ID, "password").send_keys("test_pass")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Check CSRF token in meta tag
        self.driver.get("/dashboard")
        csrf_meta = self.driver.find_element(By.NAME, "csrf-token")
        csrf_token = csrf_meta.get_attribute("content")
        assert csrf_token is not None
        
        # Verify token in forms
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        for form in forms:
            csrf_input = form.find_element(By.NAME, "_csrf")
            assert csrf_input.get_attribute("value") == csrf_token

    def test_csrf_token_validation(self):
        """Test CSRF token validation"""
        # Try request without token
        response = requests.post(
            f"{self.driver.current_url}/api/notes",
            json={"title": "Test", "content": "Content"}
        )
        assert response.status_code == 403
        
        # Try request with invalid token
        response = requests.post(
            f"{self.driver.current_url}/api/notes",
            json={"title": "Test", "content": "Content"},
            headers={"X-CSRF-Token": "invalid_token"}
        )
        assert response.status_code == 403

    def test_csrf_token_rotation(self):
        """Test CSRF token rotation after authentication"""
        # Reference pattern from:
        ```python:tests/security/test_authentication.py
        startLine: 89
        endLine: 96
        ```
        
        initial_token = self.driver.find_element(By.NAME, "csrf-token").get_attribute("content")
        
        # Logout and login again
        self.driver.get("/logout")
        self.driver.get("/login")
        self.driver.find_element(By.ID, "username").send_keys("test_user")
        self.driver.find_element(By.ID, "password").send_keys("test_pass")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Verify token has changed
        new_token = self.driver.find_element(By.NAME, "csrf-token").get_attribute("content")
        assert initial_token != new_token

class TestEncryptionVerification:
    @pytest.fixture(autouse=True)
    def setup(self, selenium_driver, mock_services):
        self.driver = selenium_driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mock_services = mock_services

    def test_sensitive_data_encryption(self):
        """Test sensitive data encryption"""
        # Login and access sensitive data
        self.driver.get("/login")
        self.driver.find_element(By.ID, "username").send_keys("test_user")
        self.driver.find_element(By.ID, "password").send_keys("test_pass")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Access API endpoint with sensitive data
        response = self.driver.execute_script("""
            return fetch('/api/sensitive-data').then(r => r.text())
        """)
        
        # Verify data is encrypted
        try:
            # Try decoding as base64 (common encoding format)
            base64.b64decode(response)
        except:
            assert False, "Response data is not properly encrypted"
        
        # Verify HTTPS
        assert self.driver.current_url.startswith("https://")
        
        # Verify secure cookies
        for cookie in self.driver.get_cookies():
            if cookie.get("name") in ["session_id", "auth_token"]:
                assert cookie.get("secure") is True
                assert cookie.get("httpOnly") is True

    def test_encryption_headers(self):
        """Test encryption-related security headers"""
        self.driver.get("/dashboard")
        
        # Get response headers using selenium's CDP
        headers = self.driver.execute_script("""
            return fetch(window.location.href).then(r => {
                let headers = {};
                r.headers.forEach((v, k) => headers[k] = v);
                return headers;
            });
        """)
        
        # Verify security headers
        assert headers.get("Strict-Transport-Security") is not None
        assert headers.get("Content-Security-Policy") is not None
        assert "upgrade-insecure-requests" in headers.get("Content-Security-Policy", "").lower()

    def test_data_encryption_in_transit(self):
        """Test data encryption in transit"""
        sensitive_endpoints = [
            "/api/users/profile",
            "/api/payment-info",
            "/api/documents/sensitive"
        ]
        
        for endpoint in sensitive_endpoints:
            # Send request and capture response
            response = self.driver.execute_script(f"""
                return fetch('{endpoint}', {{
                    method: 'GET',
                    headers: {{
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }}
                }}).then(r => {{
                    return {{
                        status: r.status,
                        headers: Object.fromEntries(r.headers.entries()),
                        body: r.text()
                    }};
                }});
            """)
            
            # Verify encryption headers
            assert response['headers'].get('content-security-policy') is not None
            assert response['headers'].get('strict-transport-security') is not None
            
            # Verify response body encryption
            try:
                import json
                decrypted_data = json.loads(response['body'])
                # Verify sensitive fields are encrypted
                for key in ['ssn', 'credit_card', 'password']:
                    if key in decrypted_data:
                        assert not decrypted_data[key].isalnum(), f"{key} should be encrypted"
            except json.JSONDecodeError:
                assert False, "Response should be valid JSON"

    def test_secure_storage(self):
        """Test secure storage of sensitive data"""
        # Test local storage security
        self.driver.execute_script("""
            localStorage.setItem('sensitive_data', 'test123');
            sessionStorage.setItem('temp_data', 'test456');
        """)
        
        # Verify data is not stored in plain text
        local_data = self.driver.execute_script("return localStorage.getItem('sensitive_data')")
        session_data = self.driver.execute_script("return sessionStorage.getItem('temp_data')")
        
        assert 'test123' not in local_data, "Sensitive data should be encrypted in localStorage"
        assert 'test456' not in session_data, "Sensitive data should be encrypted in sessionStorage"