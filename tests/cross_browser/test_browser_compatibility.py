"""Cross-browser compatibility test suite"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestBrowserCompatibility:
    @pytest.fixture(params=["chrome", "firefox", "safari", "edge"])
    def browser(self, request):
        if request.param == "chrome":
            driver = webdriver.Chrome()
        elif request.param == "firefox":
            driver = webdriver.Firefox()
        elif request.param == "safari":
            driver = webdriver.Safari()
        else:
            driver = webdriver.Edge()
            
        driver.set_window_size(1920, 1080)
        yield driver
        driver.quit()

    def test_service_area_compatibility(self, browser):
        """Test service area functionality across browsers"""
        # Reference pattern from:
        ```python:tests/e2e/service_area/test_service_area_workflow.py
        startLine: 15
        endLine: 39
        ```
        
        wait = WebDriverWait(browser, 10)
        browser.get("/service-areas")
        
        # Test map rendering
        map_element = wait.until(
            EC.presence_of_element_located((By.ID, "service-area-map"))
        )
        assert map_element.is_displayed()
        
        # Test controls functionality
        controls = browser.find_elements(By.CLASS_NAME, "map-control")
        for control in controls:
            assert control.is_enabled()
            
        # Test responsive layout
        browser.set_window_size(375, 812)  # iPhone X dimensions
        assert "mobile-view" in map_element.get_attribute("class") 