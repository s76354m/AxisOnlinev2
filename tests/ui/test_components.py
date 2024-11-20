"""UI component tests"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUIComponents:
    def test_navigation(self, driver, base_url):
        """Test navigation components"""
        driver.get(base_url)
        
        # Test sidebar navigation
        sidebar = driver.find_element(By.CLASS_NAME, "sidebar")
        assert sidebar.is_displayed()
        
        # Test project navigation
        project_link = driver.find_element(By.XPATH, "//div[text()='Projects']")
        project_link.click()
        assert "Projects" in driver.title

    def test_project_form(self, driver, base_url):
        """Test project form components"""
        driver.get(f"{base_url}/projects/new")
        
        # Test form fields
        project_type = driver.find_element(By.NAME, "project_type")
        assert project_type.is_displayed()
        
        description = driver.find_element(By.NAME, "description")
        assert description.is_displayed()
        
        # Test validation
        submit = driver.find_element(By.XPATH, "//button[text()='Create Project']")
        submit.click()
        
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
        )
        assert error_message.is_displayed() 